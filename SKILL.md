---
name: scout-wmf-antiques
description: Find and assess potentially undervalued antique WMF Jugendstil and Art Deco objects through complete Railway-first, Codex-Browser-fallback, dashboard-backed European sourcing runs. Use for “WMF Scout go”, material/mark review, sold-price comparison, or candidate validation; exclude routine modern WMF goods.
---

# WMF Antik Scout

Run broad European retrieval followed by precision-first review. The output is
an auditable shortlist of potentially underpriced antique WMF objects, not an
authenticity guarantee or automatic purchase instruction.

## Modes

- **`WMF Scout go` / `Skill go` in WMF context:** start or resume one complete
  sourcing job. Continue through collection, browser fallbacks, pagination,
  triage, multi-image review, realised-reference search, valuation, corpus
  update and dashboard update without asking the user to say `weiter`.
- **Review / validation:** assess user-supplied or frozen listings without fresh
  collection.
- **Skill maintenance:** change source contracts, collectors, model, corpus or
  dashboard. Do not imply that a registered but disabled source was searched.

## Hard Boundaries

- A skill-maintenance request alone does not authorize a fresh run. `WMF Scout
  go` authorizes collection only from individually enabled source contracts.
- Never buy, bid, contact sellers, expose seller personal data, publish leads,
  or assert physical authenticity.
- Never browser-scrape eBay. User-supplied local eBay data is asking-price and
  identity context only.
- Railway is the first collection surface when a source supports safe direct
  retrieval. The Codex in-app Browser is the only browser fallback. Never use
  Chrome, a browser extension, Google results, or search-engine caches.
- Never bypass a CAPTCHA, login, access control, robots restriction, or rate
  limit. A blocked source remains visibly blocked.
- Freeze canonical URL, source ID, external ID, query/page, price and price
  type, currency, status/end time, image URLs, collection time and hashes.
- Do not force candidate counts. Zero candidates can be a correct result.
- A visible mark photo is useful but not mandatory. `not_shown` limits
  attribution confidence; it is not an automatic rejection.

## Load References On Demand

- Read [references/scope-and-taxonomy.md](references/scope-and-taxonomy.md)
  before classification.
- Read [references/marks-and-materials.md](references/marks-and-materials.md)
  for maker/material/model/condition/restoration review.
- Read [references/objects-and-search-terms.md](references/objects-and-search-terms.md)
  for query planning or title triage.
- Read [references/source-policy.md](references/source-policy.md) before a run,
  source activation or source evaluation.
- Read [references/comparables-and-valuation.md](references/comparables-and-valuation.md)
  before reference selection, corridors or deal classes.
- Read [references/artifact-schema.md](references/artifact-schema.md) for frozen
  artifacts, object corpus, pair labels or validators.
- Read [references/dashboard-runbook.md](references/dashboard-runbook.md) for a
  complete run, Railway/Vercel persistence or deployment.
- Read [references/browser-adapters.md](references/browser-adapters.md) before
  browser collection, pagination, activation or a full run.

## Required Separation

Keep these judgments independent:

1. WMF attribution;
2. material class;
3. object/form/model and period;
4. condition, completeness and restoration;
5. visual/model similarity;
6. valuation comparability and realised-price evidence; and
7. acquisition-price attractiveness.

Never call silver-plated metal `Massivsilber`. Never compare plated metal with
solid silver numerically. Unknown evidence remains unknown. Image similarity is
retrieval evidence, never authentication or automatic price comparability.

## Full `WMF Scout go` Workflow

1. Read the run references above. From the dashboard project run `npm run go`.
   It seeds all 36 registered contracts, starts or resumes the single unfinished
   `skill_go` run, creates durable jobs and triggers the Railway collector when
   configured. Do not create a competing run.
2. Report the enabled set honestly. Currently 20 discovery sources are live:
   **Auctionet, Interencheres, Lot-tissimo, Drouot, Wendl, Hebergs, Olséns,
   Snapphane, Tradera, Bukowskis, catalogue-bounded Bruun Rasmussen, Blocket,
   DBA, Tori.fi, Kleinanzeigen, Leboncoin, Ricardo, Lauritz.com, Blomqvist and
   Hagelstam**. **Mehlis** is reference-only.
3. The registry additionally contains **Dorotheum, Koller, Willhaben,
   Marktplaats, FINN.no, Tutti, Anibis, Allegro, Allegro Lokalnie, OLX Polska,
   Subito, Wallapop, CustoJusto, Aukro and Bazoš**. Do not count any of them as
   searched until its own public-access, stable-ID, price, image and pagination
   gate passes. Facebook Marketplace is excluded.
4. Monitor `scripts/inspect-collection-jobs.mjs <run-id>`. Railway completes
   only source-compatible direct pages. A blocked, dynamic or ambiguous server
   response becomes `browser_fallback`; work every such job in the Codex
   in-app Browser and persist it with the shared `scoutRunId`. Store each
   query/page separately. Never convert a failed parse into a false zero-result
   claim.
5. Continue every enabled scope until the native end, a repeated page hash, or
   a frozen source-specific blocker. Import browser pages with
   `scripts/import-browser-batch.mjs`. Run `scripts/inspect-go-progress.mjs`
   after source waves. One slow or blocked source does not end the other work.
6. Run `scripts/advance-scout-go.mjs <run-id>`. It performs deterministic
   exclusions, conservative cross-source deduplication and a diversified
   shortlist. The default is 50 records, at most eight per object class and a
   hard maximum of 75. Open only shortlisted original details. Import
   description, condition, dimensions, model/mark text and every original
   detail image. A card thumbnail is `source_thumbnail_only`, not a completed
   image review.
7. For every selected candidate complete its original-house reference plan.
   Use `scripts/record-reference-checks.mjs`. A no-result outcome is valid only
   with terminal evidence for every planned source. An exact/near reference
   requires the original sold-lot URL, price basis, material, form/model and an
   explanation. Keep estimates, active bids and offers out of realised values.
8. Run `scripts/reconcile-reference-matches.mjs`. A numerical EUR corridor
   requires at least three compatible realised results and reports Q1, median
   and Q3. One or two results are `sparse`: show them with links but create no
   corridor. `directional_spread_eur` means conservative Q1 minus acquisition
   price, never the upper reference value or range width.
9. Run `scripts/backfill-object-corpus.mjs`. Preserve several views per object
   and the separate roles `gold_sold_reference`, `silver_offer_context`,
   `live_candidate`, and `negative_example`. Never mix offer prices into the
   sold corpus.
10. Maintain a balanced 300–500 pair benchmark with
    `scripts/build-benchmark-pairs.mjs` and `export-benchmark-review.mjs`.
    Visual/model similarity and valuation comparability are separate labels.
    Codex inspects both objects in two passes. A metadata-prefiltered `queued`
    pair is not an AI-reviewed visual label. Send only disagreements and a
    small 20–30-pair audit sample to the user.
11. Preserve explicit user decisions as `user_confirmed` without upgrading
    maker, material or physical authenticity. Run `advance-scout-go` until it
    closes the run. It must refuse completion while planned pages, pagination,
    selected image/detail reviews or reference work remain open, unless every
    blocker has frozen evidence.
12. The database-backed dashboard updates without redeployment after ordinary
    runs. Deploy only code changes. Report source coverage, Railway/browser
    routing, raw/unique counts, shortlist, all linked comparable results,
    corridor status, corpus/benchmark counts and unresolved risks.

## Candidate And Review Rules

- Prioritize Jardinières, centrepieces/epergnes, candelabra, large pitchers and
  decanters, punch vessels, rare trays/bowls, figural objects, exceptional
  Ikora/Myra and documented designs.
- Exclude or sharply down-rank modern stainless/Cromargan, routine cutlery,
  ordinary single cups/beakers, spares, reproductions and “WMF style”.
- Inspect object photos before accepting seller language. Record exact visible
  mark/model text without silently correcting it.
- Match object family, model/form, material, period, dimensions, piece count,
  completeness, condition and documented designer. Reject generic category
  matches.
- For auctions, current bid and maximum admissible hammer remain separate. A
  low current bid alone is not a deal.

## Script Roles

- Skill scripts `normalize_and_freeze.py`, `build_review_queue.py` and
  `validate_run.py` support bounded supplied batches.
- Dashboard scripts `source-plan-manifest.mjs`, `run-wmf-scout-go.mjs`,
  `enqueue-collection-jobs.mjs`, `railway-collector-server.mjs`,
  `import-browser-batch.mjs`, `triage-browser-run.mjs`,
  `prepare-shortlist-review.mjs`, `record-reference-checks.mjs`,
  `reconcile-reference-matches.mjs` and `complete-scout-run.mjs` implement the
  durable full-run ledger.
- `backfill-object-corpus.mjs`, `build-benchmark-pairs.mjs` and
  `export-benchmark-review.mjs` maintain the multi-image identity corpus and
  two-axis benchmark without treating queued work as reviewed evidence.
