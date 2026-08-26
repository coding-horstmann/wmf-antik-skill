# WMF Antik Scout

A reusable Codex skill for sourcing and assessing potentially undervalued
antique WMF Jugendstil and Art Deco metal objects. It is designed for an
auditable shortlist, rather than a high-volume listing feed.

## Install

Clone or copy this folder into your Codex skills directory as
`scout-wmf-antiques`. The skill is invoked explicitly with `WMF Scout go` and
can also be selected automatically for WMF mark, material, comparable-price or
candidate-review tasks.

The repository contains the reusable skill instructions, reference files and
small local validation helpers. A private dashboard, database credentials,
source-capture batches and deployment configuration intentionally stay outside
this repository.

## What `WMF Scout go` does

The command starts or resumes one shared sourcing run, triggers Railway-first
collection for compatible pages, completes every Codex in-app Browser
fallback, freezes page-level evidence, deduplicates and triages candidates,
then performs detailed multi-image/mark/reference work only for the diversified
shortlist. A run does not claim completion while planned
source scopes, native pagination, selected original-image/detail checks or
candidate-level realised-price checks remain open. Documented source blockers
remain visible in the result.

The current source contract contains 24 enabled discovery sources and 234
bounded initial query scopes. Railway handles source-compatible HTTP work;
Willhaben, Marktplaats, Subito, Wallapop and other dynamic fallbacks are worked
only in the Codex in-app Browser. Shortlist images are copied to durable object
storage so the dashboard is not dependent on expiring marketplace URLs.

The current source contract contains 24 enabled discovery sources and 234
bounded initial query scopes. Railway handles source-compatible HTTP work;
Willhaben, Marktplaats, Subito, Wallapop and other dynamic fallbacks are worked
only in the Codex in-app Browser. Shortlist images are copied to durable object
storage so the dashboard is not dependent on expiring marketplace URLs.

The skill never browser-scrapes eBay, bypasses access controls, bids, buys or
asserts physical authenticity. Visible mark photos are valuable evidence but
are not a mandatory admission condition; unresolved attribution and material
remain clearly labelled.

## Data and valuation rules

- Solid silver, silver plate, nickel silver/Alpacca, Britannia metal/pewter,
  tin and other alloys remain separate material classes.
- Asking prices, current bids and estimates are not realised-price references.
- Only material- and object-compatible original sold lots may support a market
  corridor.
- Modern stainless WMF, routine cutlery, ordinary cups, spares, reproductions
  and “WMF-style” listings are excluded or sharply down-ranked.

Read `SKILL.md` for the operational workflow and load the relevant files in
`references/` only when their subject is needed.
