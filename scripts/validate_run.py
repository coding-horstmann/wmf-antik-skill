#!/usr/bin/env python3
"""Validate a local WMF dry-run artifact bundle without network access."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BASE_METALS = {"silver", "nickel_silver_alpacca", "britannia_pewter", "brass_copper", "other_alloy", "glass", "unknown"}
SURFACES = {"solid_or_uncoated", "silver_plated", "gilded", "patinated", "unknown"}
MATERIAL_LABELS = {"solid_silver_supported", "silver_plated", "nickel_silver_alpacca", "britannia_pewter", "other_alloy_or_unknown", "glass_exception_track"}
SOLD_PRICE_TYPES = {"sold_hammer", "sold_with_premium", "realised_price"}


def load_records(path: Path, key: str) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    records = payload.get(key) if isinstance(payload, dict) else payload
    if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
        raise ValueError(f"{path} must contain an array or an object with {key}.")
    return records


def exists_number(value: Any) -> bool:
    if value is None or value == "":
        return False
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def validate_material(candidate: dict[str, Any], errors: list[str]) -> None:
    material = candidate.get("material")
    candidate_id = candidate.get("candidate_id", "<missing candidate_id>")
    if not isinstance(material, dict):
        errors.append(f"{candidate_id}: material must be an object.")
        return
    base, surface, label = material.get("base_metal"), material.get("surface"), material.get("label")
    if base not in BASE_METALS:
        errors.append(f"{candidate_id}: unsupported base_metal {base!r}.")
    if surface not in SURFACES:
        errors.append(f"{candidate_id}: unsupported surface {surface!r}.")
    if label not in MATERIAL_LABELS:
        errors.append(f"{candidate_id}: unsupported material label {label!r}.")
    if label == "solid_silver_supported":
        if base != "silver" or surface != "solid_or_uncoated" or not material.get("evidence"):
            errors.append(f"{candidate_id}: solid_silver_supported needs silver base, solid surface, and explicit evidence.")
    if label == "silver_plated" and "massivsilber" in json.dumps(candidate, ensure_ascii=False).lower():
        errors.append(f"{candidate_id}: silver_plated candidate contains the prohibited Massivsilber claim.")


def validate_candidate(
    candidate: dict[str, Any],
    listing_ids: set[str],
    references: dict[str, dict[str, Any]],
    errors: list[str],
    warnings: list[str],
) -> None:
    candidate_id = candidate.get("candidate_id", "<missing candidate_id>")
    level = candidate.get("candidate_level")
    if not candidate.get("candidate_id"):
        errors.append("Candidate missing candidate_id.")
    if candidate.get("listing_id") not in listing_ids:
        errors.append(f"{candidate_id}: listing_id does not exist in raw batch.")
    if level not in {"A", "B", "watch", "user_confirmed"}:
        errors.append(f"{candidate_id}: candidate_level must be A, B, watch, or user_confirmed.")
    if candidate.get("wmf_attribution_status") not in {"documented", "plausible", "claimed_only", "unknown", "contradicted"}:
        errors.append(f"{candidate_id}: invalid or missing wmf_attribution_status.")
    if not candidate.get("object_class"):
        errors.append(f"{candidate_id}: missing object_class.")
    if not candidate.get("inspected_image_paths"):
        errors.append(f"{candidate_id}: needs at least one inspected image path.")
    if not isinstance(candidate.get("uncertainties"), list):
        errors.append(f"{candidate_id}: uncertainties must be an array, including an empty array when none are known.")
    validate_material(candidate, errors)

    reference_ids = candidate.get("reference_ids", [])
    if not isinstance(reference_ids, list):
        errors.append(f"{candidate_id}: reference_ids must be an array.")
        reference_ids = []
    compatibility = candidate.get("reference_compatibility", {})
    if not isinstance(compatibility, dict):
        errors.append(f"{candidate_id}: reference_compatibility must be an object.")
        compatibility = {}
    for reference_id in reference_ids:
        reference = references.get(reference_id)
        if reference is None:
            errors.append(f"{candidate_id}: unknown reference_id {reference_id!r}.")
            continue
        if reference.get("price_type") not in SOLD_PRICE_TYPES:
            errors.append(f"{candidate_id}: reference {reference_id} is not a completed-sale price.")
        if reference.get("material_label") != candidate.get("material", {}).get("label"):
            errors.append(f"{candidate_id}: reference {reference_id} has incompatible material_label.")
        if not compatibility.get(reference_id):
            errors.append(f"{candidate_id}: reference {reference_id} lacks a compatibility explanation.")

    if level == "watch":
        forbidden_value_fields = ("conservative_value_eur", "median_value_eur", "directional_spread_eur")
        for field in forbidden_value_fields:
            if candidate.get(field) not in (None, ""):
                errors.append(f"{candidate_id}: watch records must not state {field}.")
        return

    if level == "user_confirmed":
        decision = candidate.get("human_decision")
        if not isinstance(decision, dict):
            errors.append(f"{candidate_id}: user_confirmed needs a human_decision object.")
        elif decision.get("decision_owner") != "user" or decision.get("decision") != "deal" or not decision.get("basis"):
            errors.append(f"{candidate_id}: user_confirmed needs user ownership, a deal decision, and a recorded basis.")
        if not reference_ids:
            errors.append(f"{candidate_id}: user_confirmed needs at least one completed-sale reference.")
        for field in ("conservative_value_eur", "median_value_eur", "directional_spread_eur"):
            if candidate.get(field) not in (None, ""):
                errors.append(f"{candidate_id}: user_confirmed must not state AI-derived {field}.")
        return

    required_count = 3 if level == "A" else 2
    if len(set(reference_ids)) < required_count:
        errors.append(f"{candidate_id}: {level} needs at least {required_count} unique sold references.")
    if level == "A" and candidate.get("wmf_attribution_status") != "documented":
        errors.append(f"{candidate_id}: A requires documented WMF attribution.")
    if level == "A" and candidate.get("mark_visibility") != "clear":
        errors.append(f"{candidate_id}: A requires a clear mark photo.")
    if candidate.get("material", {}).get("label") == "other_alloy_or_unknown":
        errors.append(f"{candidate_id}: A/B cannot use an unknown material class.")
    if not any(exists_number(candidate.get(field)) for field in ("deal_price_eur", "max_hammer_eur")):
        errors.append(f"{candidate_id}: A/B needs deal_price_eur or max_hammer_eur.")
    for field in ("conservative_value_eur", "median_value_eur", "directional_spread_eur"):
        if not exists_number(candidate.get(field)):
            errors.append(f"{candidate_id}: A/B requires numeric {field}.")
    if candidate.get("wmf_attribution_status") == "plausible":
        warnings.append(f"{candidate_id}: A/B attribution remains plausible rather than documented.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--candidates", required=True, type=Path)
    parser.add_argument("--references", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    raw_listings = load_records(args.raw, "listings")
    candidates = load_records(args.candidates, "candidates")
    reference_records = load_records(args.references, "references") if args.references else []
    listing_ids = {record.get("listing_id") for record in raw_listings if record.get("listing_id")}
    references = {record.get("reference_id"): record for record in reference_records if record.get("reference_id")}
    errors: list[str] = []
    warnings: list[str] = []
    candidate_ids: set[str] = set()
    for candidate in candidates:
        candidate_id = candidate.get("candidate_id")
        if candidate_id in candidate_ids:
            errors.append(f"Duplicate candidate_id {candidate_id!r}.")
        if candidate_id:
            candidate_ids.add(candidate_id)
        validate_candidate(candidate, listing_ids, references, errors, warnings)

    report = {
        "schema_version": "wmf-validation-1",
        "valid": not errors,
        "network_access": "none",
        "stats": {
            "raw_listing_count": len(raw_listings),
            "candidate_count": len(candidates),
            "reference_count": len(reference_records),
            "error_count": len(errors),
            "warning_count": len(warnings),
        },
        "errors": errors,
        "warnings": warnings,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validation {'passed' if not errors else 'failed'}: {len(errors)} errors, {len(warnings)} warnings")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
