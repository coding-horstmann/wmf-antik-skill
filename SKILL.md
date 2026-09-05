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
   It seeds all registered contracts, starts or resumes the single unfinished
   `skill_go` run, creates durable jobs and triggers the Railway collector when
   configured. Do not create a competing run.
2. Report the enabled set honestly. Currently 27 discovery sources are live:
   **Auctionet, Interencheres, Lot-tissimo, Drouot, Wendl, Hebergs, Olséns,
   Snapphane, Tradera, Bukowskis, catalogue-bounded Bruun Rasmussen, Blocket,
   DBA, Tori.fi, Kleinanzeigen, Leboncoin, Ricardo, Lauritz.com, Blomqvist and
   Hagelstam, Willhaben, Marktplaats, Subito, Wallapop, FINN.no, Aukro and
   Bazoš**. **Mehlis** is
   reference-only. The durable sold-reference backfill has live Railway
   adapters for **Auctionet, Quittenbaum, Van Ham, Koller and Lempertz**; a
   source-specific failure becomes bounded Codex in-app Browser work.
3. The registry contains 74 discovery, reference and research contracts. Its
   disabled expansion queue includes Dorotheum, Tutti, Anibis, Allegro,
   Allegro Lokalnie, OLX Polska, CustoJusto and additional French/Benelux, UK
   and Nordic auction houses documented
   in `source-plan-manifest.mjs`. Do not count any as searched merely because it
   is registered. Facebook Marketplace is excluded.
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
   hard maximum of 75. Display the complete selected shortlist in the dashboard;
   missing detail, image, price or material evidence stays visible as `?` and
   never causes a selected candidate to disappear. Review the highest-priority
   20–30 original detail pages before final matching. Import
   description, condition, dimensions, model/mark text and every original
   detail image. A card thumbnail is `source_thumbnail_only`, not a completed
   image review. Archive shortlist images in the configured Railway object
   bucket with `archive-shortlist-images.mjs`; if the server receives a blocked
   HTML response instead of image bytes, bundle the original gallery through
   the Codex in-app Browser and import it with
   `import-browser-image-bundle.mjs`. Never call an archived-but-uninspected
   file an image review.
7. Start or resume `start-or-resume-reference-backfill.mjs`; ordinary `npm run
   go` already does this. Railway must work every native historical page of
   Auctionet's ended archive and Quittenbaum's sold archive, plus the bounded
   Van Ham, Koller and Lempertz collectors. Lempertz uses its proven native
   `tx_kesearch_pi1[sword]` route with a small maker/place/series/designer seed
   set and stores only explicit `Ergebnis … (inkl. Aufgeld)` records. Monitor with
   `inspect-reference-backfill.mjs`. A failed server response becomes a
   durable `browser_fallback` job and is completed only in the Codex in-app
   Browser through `browser-reference-receiver.mjs`, including explicit
   terminal evidence for a genuine zero-result page. Never substitute a local
   or Chrome scrape. Registered research houses and context aggregators are
   not described as searched until a source-specific original-lot, price,
   image and pagination gate is live. Refresh official ECB reference rates on
   Railway with `refresh-reference-fx.mjs`. For newly harvested Auctionet lots,
   queue 400–600 high-priority detail enrichments with
   `select-reference-enrichment.mjs`; let Railway run
   `reference-detail-enrichment-worker.mjs` to completion and freeze the hero
   image with `archive-reference-images.mjs`. Run
   `analyze-reference-gaps.mjs` on the reviewed shortlist, rebuild the
   controlled model/form registry with `build-model-registry.mjs`, then run
   `backfill-object-corpus.mjs` and the v2 `match-known-reference-corpus.mjs` so
   compatible, already frozen sold lots
   can be linked without browser cost. For every selected candidate, complete
   its remaining original-house reference plan.
   Use `scripts/record-reference-checks.mjs`. A no-result outcome is valid only
   with terminal evidence for every planned source. An exact/near reference
   requires the original sold-lot URL, price basis, material, form/model and an
   explanation. Keep estimates, active bids and offers out of realised values.
8. Run `scripts/reconcile-reference-matches.mjs`. A numerical EUR corridor
   requires at least three compatible realised results of one explicit price
   type and reports Q1, median and Q3. Never mix hammer prices with
   premium-inclusive prices. Foreign currencies enter only through stored ECB
   observations applicable to the sale date. One or two results are `sparse`:
   show them with links but create no corridor. `directional_spread_eur` means
   conservative Q1 minus acquisition price, never the upper reference value or
   range width.
9. Run `scripts/backfill-object-corpus.mjs`. Preserve several views per object
   and the separate roles `gold_sold_reference`, `sold_context`,
   `dealer_context`, `estimate_context`, `identity_context`,
   `silver_offer_context`, `live_candidate`, and `negative_example`. Never mix
   offers, estimates or identity context into the valuation-grade sold corpus.
10. Maintain a balanced 300–500 pair benchmark with
    `scripts/build-quality-benchmark-pairs.mjs`, `materialize-benchmark-review.mjs`,
    `import-benchmark-labels.mjs` and `export-benchmark-review.mjs`.
    Visual/model similarity and valuation comparability are separate labels.
    Codex inspects both objects in two passes. A metadata-prefiltered `queued`
    pair is not an AI-reviewed visual label. Codex completes the 300–500 labels
    by viewing the generated contact sheets and recording both passes; run
    `inspect-quality-sprint.mjs` before declaring the benchmark complete;
    the user remains the final authority and receives only disagreements or an
    optional small audit sample, never a mandatory manual labeling burden.
11. Preserve explicit user decisions as `user_confirmed` without upgrading
    maker, material or physical authenticity. Run `advance-scout-go` until it
    closes the run. It must refuse completion while planned pages, pagination,
    selected image/detail reviews, reference pages or historical backfill jobs
    remain open, unless every blocker has frozen evidence.
12. The database-backed dashboard updates without redeployment after ordinary
   runs. Deploy only code changes. The landing page is the latest completed run;
   `/references` is the filterable combined reference library and `/ebay`
   redirects to the eBay offer-context filter. There is no watchlist workflow.
   The run summary separates all reviewed shortlist candidates from active
   evidence-qualified A/B deals. Candidate cards show only valuation-eligible
   exact/near realised-price links; context matches and asking prices remain in
   the reference library and never masquerade as deal evidence.
   Report source coverage, Railway/browser routing, raw/unique counts,
   shortlist, all linked comparable results, corridor status,
   corpus/benchmark counts and unresolved risks.

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
- `archive-shortlist-images.mjs`, `railway-image-store.mjs` and
  `import-browser-image-bundle.mjs` preserve shortlist images independently of
  expiring source URLs.
- `backfill-object-corpus.mjs`, `match-known-reference-corpus.mjs`,
  `start-or-resume-reference-backfill.mjs`, `reference-backfill-worker.mjs`,
  `inspect-reference-backfill.mjs`, `analyze-reference-gaps.mjs`,
  `build-model-registry.mjs`, `verify-matcher-v2.mjs`, `refresh-reference-fx.mjs`,
  `refresh-auction-reference-sources.mjs`, `browser-reference-receiver.mjs`,
  `build-benchmark-pairs.mjs`, `materialize-benchmark-review.mjs`,
  `import-benchmark-labels.mjs` and `export-benchmark-review.mjs` maintain the
  object/reference corpus and two-axis benchmark without treating queued work
  as reviewed evidence.
