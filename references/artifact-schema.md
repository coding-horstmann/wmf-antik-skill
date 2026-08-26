# Frozen Artifacts And Candidate Schema

## Required Run Files

- `raw-listings.json`: normalized, deduplicated, hash-bearing batch.
- `review-queue.json`: included, deferred, and excluded records with reasons.
- `reference-corpus.json`: only selected sold references.
- `manual-review.json`: visual, mark, material, and condition evidence.
- `candidate-bundle.json`: final watch/A/B candidates.
- `validation-report.json`: validator results.

## Object-Centred Corpus

Every corpus object has exactly one role: `gold_sold_reference`,
`silver_offer_context`, `live_candidate`, or `negative_example`. Attach
multiple `corpus_images` rows with roles such as `hero`, `object`, `mark`,
`detail`, or `condition`; never collapse different views into separate objects.
Price observations remain typed and linked to the object. Offer observations
cannot enter a sold corridor.

Benchmark pairs have two independent labels: `visual_label` for model/family
identity and `valuation_label` for numerical comparability. `queued` means only
machine-prefiltered. It becomes `complete` only after both images/objects were
inspected in two passes.

## Raw Listing

```json
{
  "listing_id": "auctionet:12345",
  "source": "auctionet",
  "external_id": "12345",
  "title": "...",
  "url": "https://...",
  "image_urls": ["https://..."],
  "price_value": "120.00",
  "currency": "EUR",
  "price_type": "current_bid",
  "sale_mode": "auction",
  "auction_end": "2026-09-01T18:00:00Z",
  "discovery_queries": ["WMF jardiniere"],
  "collected_at": "2026-08-23T12:00:00Z"
}
```

## Reference Record

```json
{
  "reference_id": "quittenbaum:987",
  "source": "quittenbaum",
  "url": "https://...",
  "sale_date": "2024-10-21",
  "price_value": "650.00",
  "currency": "EUR",
  "price_type": "sold_hammer",
  "object_class": "jardiniere",
  "material_label": "silver_plated",
  "form_or_model": "...",
  "condition": ["minor wear"],
  "evidence": ["catalogue photo", "lot description"]
}
```

## Per-Candidate Reference Check

Use this after inspecting the original detail and completed-sale pages for one
shortlist candidate. `completed` with no references is valid only with a
specific outcome note; it must never be used for an unstarted search.

```json
{
  "listingId": "auctionet:12345",
  "status": "completed",
  "rawResultCount": 3,
  "note": "One exact, material-compatible realised lot; two generic category lots rejected.",
  "searches": [
    {"sourceId": "mehlis", "query": "WMF Jardiniere versilbert", "status": "completed", "resultCount": 1}
  ],
  "references": [
    {
      "sourceId": "mehlis",
      "externalId": "123:456",
      "url": "https://...",
      "title": "...",
      "objectClass": "Jardinière / große Schale",
      "materialClass": "silver_plated",
      "priceAmount": 450,
      "currency": "EUR",
      "priceType": "sold_hammer",
      "compatibility": "near",
      "explanation": "Same material and form family; dimensions differ."
    }
  ]
}
```

## Candidate Record

```json
{
  "candidate_id": "W001",
  "listing_id": "auctionet:12345",
  "candidate_level": "watch",
  "object_class": "jardiniere",
  "wmf_attribution_status": "plausible",
  "period_status": "plausible",
  "material": {
    "base_metal": "nickel_silver_alpacca",
    "surface": "silver_plated",
    "label": "silver_plated",
    "evidence": ["clear underside mark photo"]
  },
  "mark_visibility": "clear",
  "mark_transcription": "WMF ...",
  "model_number_status": "unclear",
  "condition_flags": ["liner not shown"],
  "inspected_image_paths": ["C:/absolute/path/listing-1.jpg"],
  "reference_ids": [],
  "uncertainties": ["material base inferred from mark context"],
  "manual_review_required": true
}
```

## User-Confirmed Record

Use this when the user—not the scout—has expressly made the commercial deal
decision. It is deliberately distinct from A/B scoring:

```json
{
  "candidate_level": "user_confirmed",
  "wmf_attribution_status": "plausible",
  "material": {
    "base_metal": "britannia_pewter",
    "surface": "silver_plated",
    "label": "silver_plated",
    "evidence_mode": "matched_model_inference",
    "evidence": ["same-form documented realised lot"]
  },
  "reference_ids": ["auction-house:lot"],
  "human_decision": {
    "decision_owner": "user",
    "decision": "deal",
    "basis": ["listing attribution", "form comparison", "realised lot"]
  }
}
```

`user_confirmed` records must not be represented as documented physical
authentication, a solid-silver claim, or an AI-derived numerical valuation.

A and B additionally require `deal_price_eur` or `max_hammer_eur`,
`conservative_value_eur`, `median_value_eur`, `directional_spread_eur`,
`reference_ids`, and one compatibility explanation per reference.

## Invariants

- IDs are stable and source-scoped.
- Every candidate listing ID exists in the frozen raw batch.
- Every candidate reference ID exists in the frozen reference corpus.
- A/B references have a completed-sale price type and compatible material.
- `solid_silver_supported` includes explicit material evidence.
- `silver_plated` never appears with a `Massivsilber` label or claim.
- Watch records do not invent a numerical value corridor.
- A missing source image is labelled `source_thumbnail_only` or `unavailable`;
  it is never silently represented as a completed original-image review.
- A saved but externally blocked image is distinct from no saved image; the
  dashboard must attempt all frozen image URLs before reporting it unrenderable.
- A completed candidate reference check includes an outcome note and is not
  interchangeable with `queued`, `collecting`, `failed`, or `skipped`.
- `user_confirmed` records preserve a user decision and at least one completed
  reference, while keeping uncertain attribution/material evidence explicit.
