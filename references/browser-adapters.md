# Direct-Browser Source Adapters

Read this only for `WMF Scout go` collection or when activating a source. It
records working browser paths, not a claim of exhaustive historical coverage.

## Shared page contract

For every page save: source ID, query, canonical search URL, page number,
next-page URL when present, collection time, every canonical lot URL, visible
title/card text and primary image URL. Deduplicate first by `source_id` plus
lot ID, then by canonical URL.

Extract result cards with a DOM-scoped selector (`article` where available) and
derive the lot ID from its canonical URL. Do not treat image alt text, price
text, or a source claim as a full authentication. Before detail-page work, run
the deterministic triage and open only the shortlist.

When pagination is visible, follow the direct next-page URL until it ends or a
previous page hash repeats. Save each page before continuing. When a source
uses a load-more/infinite list, record its current state and page ambiguity;
do not simulate an unbounded scroll loop.

## Enabled discovery adapters

| Source | Direct search path | Lot identity and price treatment | Resume / current limitation |
|---|---|---|---|
| Auctionet | `https://auctionet.com/de/search?q=<encoded query>` | `/de/<numeric-id>-…`; a search-card figure is current bid, estimate or unknown according to its visible label. | Follow a visible source-native page link only after saving the page. |
| Interencheres | `https://www.interencheres.com/recherche/lots?search=<encoded query>` | `/…/lot-<numeric-id>.html`; search-card estimate is never a result. | The first direct results page and individual lots are verified; confirm the live page control before a multi-page continuation. |
| Lot-tissimo | Start at `https://www.lot-tissimo.com/de-de`, use its visible `main-search-term` field. Result URL: `/de-de/search-results?searchTerm=<query>`. | `/de-de/auction-catalogues/…/lot-<UUID>`; cards visibly separate current bid, start price and estimate. | Verified: `?page=2` is the next page; 60 results/page was displayed for the WMF test. |
| Drouot | Start at `https://drouot.com/en`, use its visible search field. Result URL: `/en/s?query=<query>`. | `/en/l/<numeric-id>-…`; cards detail starting price or estimate separately. | First result page and lot URLs are verified. Confirm load-more/page behavior in the current UI before continuation. |
| Auktionshaus Wendl | Read the current catalogue ID from `https://auktionen.auktionshauswendl.de/de/auctions`; search path is `/listsearch?filter=<query>&id=<catalogue-id>`. | `/de/lot/lot-details/<numeric-id>/…`; detail pages can show maker/model statement, material, dimensions, condition, `Zuschlag` and `Aufgeld` separately. | Current-catalog and archive traversal must be saved as separate query/page scopes. |
| Hebergs Auktioner | `https://hebergsauktioner.se/auktion/sök?searchQuery=<encoded>&searchType=text&frmSearch=true`. | `/auktion/objekt/<slug>/<numeric-id>`; detail pages expose end time, `Högsta bud`, condition text, images and a separately calculated fee total. | A zero-result WMF page is an explicit saved end-of-results scope. Do not interpret the total-with-fee figure as the hammer/current bid. |
| Olséns Auktioner | `https://www.olsensauktioner.se/sv-SE/lots?search=<encoded>`. | `/sv-SE/inventories/<slug>_<numeric-id>`; cards/details distinguish `Aktuellt bud`, `Startbud` and `Värdering`; details include condition, dimensions, end time, premium and images. | The current page either exposes a native continuation or an explicit end. Save the active/closed mode separately. |
| Snapphane Auktioner | `https://www.snapphaneauktioner.se/sv-SE/lots?orderBy=enddate+asc&search=<encoded>&auctionCompany=`. | `/sv-SE/inventories/<numeric-id>`; cards/details separate `Aktuellt bud` and `Startbud`, with end time, condition and images. | The current page either exposes a native continuation or an explicit end. Save the active/closed mode separately. |
| Tradera | `https://www.tradera.com/search?q=<encoded>&categoryId=20&sortBy=MostBids`. | `/item/<category-id>/<numeric-id>/<slug>`; detail pages show object number, end time, description, condition and images. | `&paging=2` was visibly linked on the WMF result. Preserve `Ledande bud`, `Utropspris` and `Köp nu` as distinct price types; Buy-now is an offer, never a realised reference. |
| Bukowskis | `https://www.bukowskis.com/en/lots?query=<encoded>`. | `/en/lots/<numeric-id>-<slug>`; details contain material, mark statement, condition, images, bid/estimate and minimum-price status. | Native `/en/lots/page/2` controls were visible. A result only becomes a price reference after its original detail page establishes a completed-sale basis. |
| Bruun Rasmussen | Start at `https://bruun-rasmussen.dk/m/auctions`, then use only a current source-native catalogue and its stated relevant category/page. | `/m/lots/<hex-id>`; details include description, condition, images, auction end, `Next bid`/current bid and purchase-cost notice. | Catalogue pages use visible `?page=2` links. This is catalogue-bounded discovery, not a guessed global query route; only record an outcome once the closed lot page gives its basis. |
| Blocket | `https://www.blocket.se/recommerce/forsale/search?q=<encoded>`. | `/recommerce/forsale/item/<numeric-id>`; the original page's JSON-LD exposes SKU, title, description, image, condition/status and offer price in SEK. | Native `page=2` is visible. Treat every number as `asking_price`; do not store seller personal data. |
| DBA | `https://www.dba.dk/recommerce/forsale/search?q=<encoded>`. | `/recommerce/forsale/item/<numeric-id>`; the original page's JSON-LD exposes SKU, title, description, image, used/new condition and offer price in DKK. | Native `page=2` is visible. Treat every number as `asking_price`; do not store seller personal data. |
| Tori.fi | `https://www.tori.fi/recommerce/forsale/search?q=<encoded>`. | `/recommerce/forsale/item/<numeric-id>`; the original page's JSON-LD exposes SKU, title, description, image, condition/status and offer price in EUR. | Native `page=2` is visible. Treat every number as `asking_price`; do not store seller personal data. |
| Kleinanzeigen | Use the visible site search; the canonical result path is `/s-<normalized-query>/k0` and continuation is `/s-seite:2/<normalized-query>/k0`. | `/s-anzeige/<slug>/<numeric-ad-id>-<category>-<region>`; details expose asking/VB price, description, condition statements, dimensions and original images. Deduplicate on the first numeric ad ID. | Native page 2 was verified on a 486-result WMF-Jugendstil search. Treat every price as `asking_price`; do not store seller name, location or profile data. |
| Leboncoin | `https://www.leboncoin.fr/recherche?text=<encoded>`. | `/ad/<category>/<numeric-id>`; detail pages expose fixed asking price, condition, material/brand fields, description and a full photo gallery. | Native `page=2` continuation is visible; preserve the exact source-generated next URL because it may include a transient `ref_id`. No seller personal data; every price is an offer. |
| Ricardo | `https://www.ricardo.ch/de/s/<encoded-query>/`. | `/de/a/<slug>-<numeric-id>/`; detail pages expose CHF start/current/fixed price context, bid count, end time, description, condition, delivery and images. | Use the native numbered buttons (`page 2` / `Go to next page`) and save the selected-page state; the UI may update client-side without changing the canonical URL. Active bids and Buy-now amounts are not realised references. |
| Lauritz.com | `https://www.lauritz.com/da/auctions/search/<encoded-query>`. | `/da/auction/<slug>/<numeric-id>`; original lots expose description/condition, dimensions/marks when catalogued, images, end time, estimate and next/current bid. | Verified: 60 items/page and `skip=60&take=60` after native `Next page`. A zero-result query is a terminal saved scope. `Vurdering` and `Næste bud` are not sold prices. |
| Blomqvist | `https://www.blomqvist.no/sok/<encoded-query>`, then follow every active `Auksjoner / Kategori` link returned by the search. | `/auksjoner/<category-path>/<numeric-id>`; lots expose object number, description, note/condition, images, estimate, next bid and end time. | Category/list pages use native `Neste` and `?page=2`. Do not confuse the separate `Tilslagsliste` section with active discovery; only an original ended lot can provide a realised result. |
| Hagelstam | `https://www.hagelstam.fi/en/search?search=<encoded-query>` via the visible `Site search` field. | `/en/items/<category>/<slug>-<numeric-id>`; detail pages expose title/attribution, material, dimensions, original full-size images, start/status and, for ended lots, explicit hammer price. | Search-result pagination is source-native; the all-items archive independently shows 40/page and a `Seuraava sivu` control. Exclude expert contact details. Only explicit `Hammer price` on an ended original lot is `sold_hammer`. |

## Detail enrichment

For a shortlisted lot, record its own visible description and condition text,
mark/model statement, dimensions, auction house and every original image URL.
The importer accepts these in `record.detail`. Classify a stated mark as a
seller/auction-house claim unless it is visibly read; `not_shown` remains valid
and does not override a user decision.

For Wendl only, `Zuschlag <amount>` plus `Verkauft` on the individual lot page
can be stored as `sold_hammer`; the separately displayed buyer premium is not
folded into it. Other sources require their individual closed-lot page to make
that distinction.

## Activation gate for next sources

The registered next-source queue is Willhaben, Marktplaats, FINN.no, Tutti,
Anibis, Allegro, Allegro Lokalnie, OLX Polska, Subito, Wallapop, CustoJusto,
Aukro and Bazoš. Facebook Marketplace is excluded. Some have prototype search
evidence, but none becomes recurring/live merely because a result page loaded.

For each new regional house, first prove all five fields in the Codex browser:

1. direct public search or catalogue route;
2. canonical stable lot identifier;
3. card/listing price label and currency;
4. detail description, image and condition fields; and
5. explicit next-page, load-more or end-of-results behavior.

Only then add its parser and mark it `enabled`. If any field is missing, keep
the source in `research` or `verification`; do not silently route it through
another website or a search engine.
