# Dashboard-Backed Sourcing Run

Use this runbook only for `WMF Scout go` after the user has asked for a fresh
scan. It is intentionally a small operational reference so the main skill
stays token-light.

## Deployment Contract

- Dashboard project: `<workspace>/wmf-scout-dashboard`
- Frozen live batches: `<workspace>/reports/wmf-antik-live`
- Dashboard deployment: configure the private Vercel dashboard outside source
  control; its URL, password and environment variables are never skill data.
- Storage: use a configured database. Pull any production environment to the
  ignored file `.env.migrate.local`; never print or commit it.

## Source Contracts

| Source | Role | Status |
|---|---|---|
| Auctionet, Interencheres, Lot-tissimo, Drouot, Auktionshaus Wendl | Direct European auction discovery through Codex in-app browser | Enabled; each page/query is frozen and price labels stay distinct |
| Hebergs, Olséns, Snapphane | Direct Swedish regional-auction discovery | Enabled; native search, stable lot IDs, details and end behavior were proven |
| Tradera | Swedish auction/Buy-now marketplace discovery | Enabled; current bid, starting bid and asking price use different price types |
| Bukowskis | Nordic auction discovery and future original-lot reference evidence | Enabled; public search, stable lots, details and native pagination were proven |
| Bruun Rasmussen | Catalogue-bounded Danish auction discovery and future original-lot reference evidence | Enabled; scan only explicit current house catalogues and their visible pages |
| Blocket, DBA, Tori.fi | Swedish, Danish and Finnish marketplace discovery | Enabled; source-native search, stable ad IDs, detail JSON-LD and native page-2 links were proven. Asking prices are only offer context. |
| Kleinanzeigen, Leboncoin, Ricardo | German, French and Swiss marketplace discovery | Enabled; direct search, stable ad/offer IDs, detail evidence and native continuation were proven. Asking prices and active bids are never realised references. |
| Lauritz.com, Blomqvist, Hagelstam | Danish, Norwegian and Finnish regional-auction discovery | Enabled; direct search/catalogue path, stable lot IDs, detail evidence and native page/end behavior were proven. Blomqvist expands search categories before pagination; Hagelstam separates active lots from explicit archived hammer prices. |
| Auktionshaus Mehlis | Original completed-sale reference | Reference-only |
| Dorotheum, Koller | Staged research sources | Not included in a `go` run until their remaining individual browser gate is complete |

The collector does not imply pagination exhaustion. Continue only on a proven
source-native page control and save every page scope. The dashboard is not a
reason to fetch from an unimplemented source.

## Operational Sequence

1. From the dashboard project, refresh only the local ignored credentials,
   then run the single orchestration command. It seeds contracts, starts or
   resumes the shared run, enqueues Railway/direct-browser work and triggers
   the Railway collector when configured.

   ```powershell
   npx --yes vercel@latest env pull .env.migrate.local --environment=production --yes
   npm run go
   ```

   Retain the returned `runId`. The current plan has 197 bounded
   source/query scopes across 20 enabled discovery sources. It is a declared
   breadth target, not a claim that every result page has already been read.
2. Monitor `scripts/inspect-collection-jobs.mjs <run-id>`. Railway processes
   compatible direct pages. In the Codex in-app browser, work every explicit
   `browser_fallback` and browser-only scope directly from the original site.
   Extract only the original lot/ad URL, title or
   search-card text, visible price context, image URL and query/page context.
   Save every page as its own batch under `reports/wmf-antik-live`; do not
   replace older evidence. Continue only on a visible source-native next-page
   control. Never use Google or browser-scrape eBay.
3. Import each frozen page with the shared run ID. The importer refuses a
   batch without that ID, so a detail page cannot silently become a second
   dashboard run:

   ```powershell
   node --env-file=.env.migrate.local scripts/import-browser-batch.mjs <absolute-or-relative-batch-path>
   ```

   An inaccessible, semantically ambiguous, or exhausted source page must be
   recorded as the scope's `scopeStatus: "failed"` or `"skipped"` with an
   `errorSummary`; it is never silently counted as searched.
4. Inspect progress after each source wave:

   ```powershell
   npm run go:progress -- <run-id>
   ```

   Do not stop the job merely because one source is slow or empty. Continue
   all remaining planned scopes, then resolve source-native pagination.
5. When all planned source pages are completed or have frozen blockers, call
   the phase coordinator:

   ```powershell
   npm run go:advance -- <scout-run-id>
   ```

   It runs triage, conservatively removes documented cross-source mirrors, and
   chooses a diversified shortlist (default 50, maximum eight per class). For every selected
   original lot, import description, condition, dimensions, mark/model text
   and `detail.imageUrls`. A small search-card image remains
   `source_thumbnail_only`; only URLs captured on the original detail page
   count as an inspected image set.
6. For every selected candidate, inspect its original-lot reference query plan
   in the Codex browser. Freeze the source outcomes and import them with
   `scripts/record-reference-checks.mjs`. It records a genuine no-result search
   separately from an unstarted search, requires a terminal result for every
   planned reference source before a candidate check can be complete, and accepts only original realised-price
   records. Run `go:advance` again; it reconciles exact/near references and
   finishes only when all selected checks are resolved. A `skill_go` run cannot
   be closed while a planned initial scope, a native next page, an in-progress
   scope, or selected review work remains. Only allow a closure with blockers
   when each blocker has frozen evidence.

   ```powershell
   node --env-file=.env.migrate.local scripts/inspect-run.mjs <scout-run-id>
   npm run go:advance -- <scout-run-id>
   npm run lint
   npm run build
   ```

   Production reads from the database dynamically, so normal completed runs
   do not require a redeploy. Deploy only when dashboard code changed.
7. After review, run `scripts/backfill-object-corpus.mjs`; build/extend the
   balanced pair queue with `scripts/build-benchmark-pairs.mjs 500`. Do not
   count queued pairs as visual labels.

## Price Handling

- Current bid: store as `current_bid`.
- Explicit estimate: store as `estimate` and never use it as a comparable.
- Search-card number for an ended listing: store as `unknown` price basis,
  even when its wording suggests an auction result.
- `sold_hammer` or `sold_with_premium` requires direct original-lot evidence.
- A user-supplied local eBay archive may be imported with
  `scripts/import-offer-context.mjs` only when its manifest explicitly labels
  all numbers as active offers. It stays in `offer_context_*` tables and is
  excluded from `references_sold`, candidate valuation and deal scoring.

## First-Pass Exclusions

Reject or sharply down-rank modern stainless/Cromargan, ordinary cutlery,
single cups or beakers, replacement parts, reproductions and “WMF style”.
Prioritize designer candlesticks, jardinières, epergnes, large serving pieces,
figural work, documented Ikora/Myra and complete high-value groups.
