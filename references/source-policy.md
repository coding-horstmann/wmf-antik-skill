# Source Policy

## Hard Boundaries

- Never browser-scrape eBay.
- Never bypass a CAPTCHA, login, technical access control, robots restriction,
  terms-of-use boundary, or rate limit.
- Do not use an aggregator's thumbnail or derivative data as the sole listing
  evidence. Preserve the original lot or marketplace URL.
- Use Railway first for recurring direct retrieval when a source contract has
  passed that execution gate. Do not start unrestricted cross-source collection
  from a browser. Codex in-app Browser fallbacks remain user-started, bounded
  and auditable.
- Do not purchase, bid, message a seller, or expose seller personal data.

## Per-Source Entry Gate

Before any source is included in a dry run, document all of the following:

1. original, non-eBay source and canonical URL pattern;
2. source terms, robots/technical limits, and permitted access method;
3. stable external ID and source-level deduplication key;
4. accessible item images and sufficient listing facts;
5. parseable original price, currency, and price type;
6. auction end time and status, where applicable;
7. expected query volume, rate cap, and raw-result cap;
8. availability of an audit trail without unnecessary personal data.

A source with unknown access status may be researched manually but cannot be
enabled for recurring collection. A failed or blocked source is an
implementation gap, not evidence that WMF supply is absent.

## Proposed Deal-Source Tiers

| Tier | Candidates | Use |
|---|---|---|
| Active direct discovery | Auctionet, Interencheres, Lot-tissimo, Drouot, Wendl, Hebergs, Olséns, Snapphane, Tradera, Bukowskis, catalogue-bounded Bruun Rasmussen, Blocket, DBA, Tori.fi, Kleinanzeigen, Leboncoin, Ricardo, Lauritz.com, Blomqvist, Hagelstam, Willhaben, Marktplaats, Subito, Wallapop, FINN.no, Aukro, Bazoš | Page-by-page bounded jobs; document source query/catalogue, rate and continuation. Marketplace numbers are offers, not realised prices. FINN.no is limited to 2 requests/minute; do not persist seller identity, contact data or precise location from private marketplaces. Hagelstam archives may contribute only explicit original-lot hammer prices. Marktplaats sponsor mirrors are rejected before import. |
| Durable realised-reference backfill | Auctionet ended archive, Quittenbaum sold archive, Van Ham, Koller, Lempertz | Railway-first native pagination with original-lot URLs. Lempertz uses bounded native maker/place/series/designer terms and only explicit premium-inclusive results. A source-specific failed response becomes a durable Codex in-app Browser fallback job; it never becomes a false zero. Koller, Quittenbaum and Lempertz condition may remain nullable when the house does not publish it. |
| Reference-only | Mehlis | Original completed lots only |
| Validated but non-live candidates | Dorotheum | Maintain source-specific proof gaps; do not include in a `go` discovery run yet. |
| Expansion candidates | Tutti, Anibis, Allegro, Allegro Lokalnie, OLX Polska, CustoJusto plus the disabled French/Benelux, UK and Nordic houses in `source-plan-manifest.mjs` | Registered but disabled until each passes the same source gate; Facebook Marketplace excluded |

The list is a research queue, not a claim that any source currently permits or
technically supports WMF collection.

## Reference Sources

Prefer original auction-house results and preserve the stated price basis.
Potential additional sources include Dorotheum, Lempertz, Bonhams,
Christie's, Sotheby's, Auctionet, Bukowskis, Bruun Rasmussen, Drouot, and
Interencheres. Use museum records and historical WMF catalogues for
attribution, not numerical valuation.

Invaluable, LiveAuctioneers, MutualArt, Barnebys, Artnet, dealer sites, and
marketplace offers are discovery or context sources. A number may enter a
valuation only when a traceable original lot confirms a completed sale and its
price basis.

## Collection Limits

A deliberately small pilot should normally cap each source at 20 explicit WMF
results plus 5–10 broad, unbranded discovery records. A user-started
`WMF Scout go` uses the larger source-specific safety segments in the verified
source-specific plan instead; each segment remains bounded and auditable, while
native pagination is continued until its explicit end or a frozen blocker.
Record query, timestamp, page/category scope and continuation. Stop an
individual collector when its source gate fails or its rate/technical boundary
becomes ambiguous, then continue the other enabled sources.
