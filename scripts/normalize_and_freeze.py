#!/usr/bin/env python3
"""Normalize a supplied local listing batch into an immutable WMF review input.

This utility never fetches URLs. It accepts a JSON array or an object containing
``listings`` or ``records``, removes exact source/external-ID duplicates, and
writes a hash-bearing normalized artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def iso_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [item for item in (string(item) for item in value) if item]
    return [str(value).strip()]


def source_key(value: Any) -> str | None:
    text = string(value)
    if not text:
        return None
    return "_".join(text.lower().split())


def input_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = payload.get("listings", payload.get("records"))
    else:
        raise ValueError("Input must be a JSON array or an object with listings/records.")
    if not isinstance(records, list):
        raise ValueError("Input listings/records must be a JSON array.")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every input listing must be a JSON object.")
    return records


def normalized_price(record: dict[str, Any]) -> tuple[str | None, str | None]:
    value = record.get("price_value", record.get("price"))
    currency = record.get("currency")
    if isinstance(value, dict):
        currency = currency or value.get("currency")
        value = value.get("value", value.get("amount"))
    return string(value), string(currency)


def normalize_one(record: dict[str, Any], index: int, collected_at: str) -> dict[str, Any]:
    source = source_key(record.get("source"))
    external_id = string(record.get("external_id", record.get("id")))
    title = string(record.get("title"))
    url = string(record.get("url", record.get("canonical_url")))
    missing = [
        label
        for label, value in (("source", source), ("external_id", external_id), ("title", title), ("url", url))
        if not value
    ]
    if missing:
        raise ValueError(f"Record {index} is missing required fields: {', '.join(missing)}")

    price_value, currency = normalized_price(record)
    listing = {
        "listing_id": f"{source}:{external_id}",
        "source": source,
        "external_id": external_id,
        "title": title,
        "url": url,
        "image_urls": string_list(record.get("image_urls", record.get("images"))),
        "price_value": price_value,
        "currency": currency,
        "price_type": string(record.get("price_type")),
        "sale_mode": string(record.get("sale_mode")),
        "auction_end": string(record.get("auction_end")),
        "availability": string(record.get("availability")),
        "description": string(record.get("description")),
        "discovery_queries": string_list(record.get("discovery_queries", record.get("query"))),
        "discovery_scope": string(record.get("discovery_scope")),
        "collected_at": string(record.get("collected_at")) or collected_at,
        "raw_record_sha256": sha256_bytes(canonical_json(record)),
    }
    return {key: value for key, value in listing.items() if value is not None}


def completeness(listing: dict[str, Any]) -> int:
    return sum(
        bool(listing.get(field))
        for field in ("image_urls", "price_value", "currency", "price_type", "sale_mode", "auction_end", "description")
    )


def deduplicate(listings: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    winners: dict[str, dict[str, Any]] = {}
    duplicates: list[dict[str, Any]] = []
    for listing in listings:
        key = listing["listing_id"]
        current = winners.get(key)
        if current is None:
            winners[key] = listing
            continue
        keep, drop = (listing, current) if completeness(listing) > completeness(current) else (current, listing)
        winners[key] = keep
        duplicates.append(
            {
                "listing_id": key,
                "kept_raw_record_sha256": keep["raw_record_sha256"],
                "dropped_raw_record_sha256": drop["raw_record_sha256"],
                "reason": "exact source:external_id duplicate; retained record with more populated fields",
            }
        )
    return sorted(winners.values(), key=lambda record: record["listing_id"]), duplicates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Local source JSON; no network access is performed.")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--collected-at", default=None, help="ISO timestamp for records that lack one.")
    args = parser.parse_args()

    input_bytes = args.input.read_bytes()
    payload = json.loads(input_bytes.decode("utf-8-sig"))
    collected_at = args.collected_at or iso_now()
    normalized = [normalize_one(record, index, collected_at) for index, record in enumerate(input_records(payload), start=1)]
    listings, duplicates = deduplicate(normalized)
    sources = dict(sorted(Counter(record["source"] for record in listings).items()))
    run_id = args.run_id or f"wmf-dry-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"

    result: dict[str, Any] = {
        "schema_version": "wmf-raw-1",
        "run": {
            "run_id": run_id,
            "normalized_at": iso_now(),
            "input_sha256": sha256_bytes(input_bytes),
            "input_record_count": len(normalized),
            "unique_listing_count": len(listings),
            "source_counts": sources,
            "network_access": "none",
        },
        "listings": listings,
        "exact_duplicates": duplicates,
    }
    result["content_sha256"] = sha256_bytes(canonical_json(result))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(listings)} frozen listings to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
