#!/usr/bin/env python3
"""Create a bounded, source-balanced WMF review queue from a frozen batch.

The script uses title/description metadata only. It does not open images,
authenticate an object, calculate value, or make network requests.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any


HARD_EXCLUSIONS = (
    "cromargan",
    "edelstahl",
    "stainless",
    "reproduktion",
    "reproduction",
    "wmf style",
    "im stil von",
    "ersatzteil",
    "replacement part",
)
LOW_VALUE_TERMS = (
    "besteck",
    "cutlery",
    "einzelbecher",
    "eierbecher",
    "serviettenring",
    "single cup",
)
WMF_SIGNALS = ("wmf", "w.m.f", "wurttembergische metallwarenfabrik", "geislingen")
STYLE_SIGNALS = ("jugendstil", "art nouveau", "art deco", "art deco", "secession", "skonvirke", "secesja", "secese", "stile liberty", "modernista")
MATERIAL_SIGNALS = ("versilbert", "silver plate", "silverplate", "alpacca", "alpaka", "nysilver", "nysolv", "solvplet", "forsolvet", "forsilvrad", "nikkelzilver", "maillechort", "britannia", "pewter", "zinn", "etain", "peltro")
P1_TERMS = ("jardiniere", "jardinjar", "bloembak", "tafelaufsatz", "epergne", "centerpiece", "centre de table", "bordsuppsats", "bordopsats", "nástolec", "nastolec", "kandelaber", "candelabra", "candelabre", "kandelabr", "girandole", "punsch", "punch", "bowle", "boolimalja", "ponchera")
P2_TERMS = ("tablett", "plateau", "tray", "dienblad", "bricka", "bakke", "tarjotin", "taca", "vassoio", "bandeja", "schale", "schaal", "skal", "kulho", "misa", "coupe", "karaffe", "karaf", "carafe", "karahvi", "decanter", "figur", "figural", "figurka", "ikora", "myra")
P3_TERMS = ("leuchter", "candlestick", "kandelaar", "lysestage", "svicen", "dose", "box", "schreibzeug", "desk")


def fold(value: Any) -> str:
    text = str(value or "").lower().translate(
        str.maketrans({"ø": "o", "æ": "ae", "œ": "oe", "ß": "ss", "ł": "l", "đ": "d", "ð": "d"})
    )
    return "".join(char for char in unicodedata.normalize("NFKD", text) if not unicodedata.combining(char))


def matches(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if term in text]


def listing_text(listing: dict[str, Any]) -> str:
    return fold(f"{listing.get('title', '')} {listing.get('description', '')}")


def triage(listing: dict[str, Any], include_unbranded: bool) -> tuple[str, int, str | None, list[str]]:
    text = listing_text(listing)
    exclusion_hits = matches(text, HARD_EXCLUSIONS)
    if exclusion_hits:
        return "excluded", 0, "explicit excluded term: " + ", ".join(exclusion_hits), exclusion_hits

    wmf_hits = matches(text, WMF_SIGNALS)
    p1_hits = matches(text, P1_TERMS)
    p2_hits = matches(text, P2_TERMS)
    p3_hits = matches(text, P3_TERMS)
    low_hits = matches(text, LOW_VALUE_TERMS)
    if low_hits and not (p1_hits or p2_hits):
        return "deferred", 0, "ordinary low-value object signal: " + ", ".join(low_hits), low_hits
    if not wmf_hits and not include_unbranded:
        return "deferred", 0, "no explicit WMF/Geislingen title signal", []
    if not (p1_hits or p2_hits or p3_hits):
        return "deferred", 0, "no prioritized object-class signal", wmf_hits

    signals = wmf_hits + matches(text, STYLE_SIGNALS) + matches(text, MATERIAL_SIGNALS)
    if p1_hits:
        tier, score = "P1", 40
    elif p2_hits:
        tier, score = "P2", 25
    else:
        tier, score = "P3", 10
    score += 35 if wmf_hits else 0
    score += min(10, 5 * len(matches(text, STYLE_SIGNALS)))
    score += min(5, 2 * len(matches(text, MATERIAL_SIGNALS)))
    score += 3 if listing.get("image_urls") else 0
    score += 2 if listing.get("price_value") else 0
    return "included", score, tier, signals + p1_hits + p2_hits + p3_hits


def load_listings(path: Path) -> tuple[list[dict[str, Any]], str | None]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(payload, dict):
        records = payload.get("listings")
        content_hash = payload.get("content_sha256")
    else:
        records, content_hash = payload, None
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        raise ValueError("Expected a raw artifact or JSON array of listing objects.")
    return records, content_hash


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-total", type=int, default=30)
    parser.add_argument("--max-per-source", type=int, default=10)
    parser.add_argument("--include-unbranded", action="store_true")
    args = parser.parse_args()
    if args.max_total < 1 or args.max_per_source < 1:
        raise SystemExit("Queue limits must be positive.")

    listings, raw_hash = load_listings(args.raw)
    included: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for listing in listings:
        status, score, tier, signals = triage(listing, args.include_unbranded)
        entry = {"listing_id": listing.get("listing_id"), "source": listing.get("source"), "reason": tier if status == "included" else tier, "signals": signals}
        if status == "included":
            entry.update({"queue_score": score, "priority_tier": tier, "listing": listing})
            included.append(entry)
        elif status == "deferred":
            deferred.append(entry)
        else:
            excluded.append(entry)

    included.sort(key=lambda item: (-item["queue_score"], item["listing_id"] or ""))
    source_counts: Counter[str] = Counter()
    queue: list[dict[str, Any]] = []
    overflow: list[dict[str, Any]] = []
    for entry in included:
        source = entry["source"] or "unknown"
        if len(queue) >= args.max_total or source_counts[source] >= args.max_per_source:
            entry["reason"] = "queue cap reached"
            overflow.append(entry)
            continue
        source_counts[source] += 1
        queue.append(entry)

    output = {
        "schema_version": "wmf-review-queue-1",
        "raw_content_sha256": raw_hash,
        "configuration": {
            "max_total": args.max_total,
            "max_per_source": args.max_per_source,
            "include_unbranded": args.include_unbranded,
            "network_access": "none",
        },
        "queue": queue,
        "deferred": deferred + overflow,
        "excluded": excluded,
        "summary": {
            "queue_count": len(queue),
            "queue_source_counts": dict(sorted(source_counts.items())),
            "deferred_count": len(deferred) + len(overflow),
            "excluded_count": len(excluded),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(queue)} review-queue records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
