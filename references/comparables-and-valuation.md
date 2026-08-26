# Comparables And Valuation

## Comparable Gate

Use numerical references only after WMF attribution and material class are
reviewed. A usable comparable matches the same object family and does not have
a known conflict in material, form/model, period, dimensions, piece count,
condition, completeness, or documented designer.

Examples of prohibited shortcuts:

- a plated tray versus solid silver;
- an Ikora glass vase versus a metal bowl;
- a single candleholder versus a pair or candelabrum;
- a damaged item versus an intact one without an explicit condition adjustment;
- a generic Jugendstil object versus a documented WMF model.

## Price Evidence

- Use realised results only for numerical bands.
- Preserve `hammer`, `sold_with_premium`, and `realised_price` separately. Do
  not silently blend them.
- Preserve estimates, limits, starting bids, current bids, and dealer offers
  as context only.
- Convert currencies using one dated FX snapshot, while retaining original
  price, currency, basis, sale date, and source URL.

## Conservative Corridor

For three or more compatible sold results, report count, Q1, median, Q3,
and a conservative lower value. Start with the lower quartile where the sample
supports it; retain visible condition and completeness adjustments rather than
hiding them in a model score. Remove only clear non-comparable outliers and
record why.

With one or two compatible sales, label the evidence `sparse`, link the sales,
and do not emit a numerical corridor. A sparse group may support `watch`, never
A or B.

`directional_spread_eur` is the conservative Q1 value minus the displayed
acquisition price. It is not Q3, the full range, or expected profit.

## Explicit User Deal Decision

The user may explicitly decide that a candidate is commercially attractive even
when the online evidence falls short of the ordinary A/B evidence threshold.
Record this separately as `user_confirmed`, not as an AI-authentication claim
and not as an automatic-buy instruction.

- Preserve the stated basis: listing claim, visual form/model comparison,
  condition evidence, and the matching realised sale(s).
- A maker's mark need not be visible to use this route. A non-visible mark
  keeps attribution `plausible` or `claimed_only`; it must never be upgraded to
  `documented` merely because the user decided to pursue the object.
- A material class inferred from an unusually close documented model match must
  be labelled `matched_model_inference`, not direct material proof. It cannot
  support a solid-silver claim.
- A `user_confirmed` record may cite one strong same-model completed result as
  proof of market relevance, but must not invent a statistical value corridor.
- The user's deal decision does not authorize a bid, purchase, seller contact,
  or publication. The user sets any maximum hammer/all-in budget.

## Acquisition Calculation

For a fixed-price listing, state the displayed price and separately add only
known buyer protection, shipping, tax, or platform costs. For auctions, keep
the current bid separate from the maximum admissible hammer price:

```text
max_hammer = (target_ratio * conservative_value - known_fixed_costs)
             / (1 + known_premium_and_tax_rate)
```

An unknown premium, shipping cost, or condition issue remains an uncertainty;
do not substitute an invented number.

## Candidate Classes

| Class | Requirements |
|---|---|
| A | Documented WMF and material evidence, sufficient condition photos, at least 3 compatible sold results, acquisition cost at most 35% of conservative value, and at least EUR 500 directional spread |
| B | Plausible or documented WMF/material evidence, at least 2 strong or 3 near-compatible sold results, acquisition cost at most 50% of conservative value, and at least EUR 250 directional spread |
| Watch | Interesting form but mark, material, condition, final price, or reference evidence remains sparse or uncertain; no unsupported market-value claim |
| User-confirmed | User expressly calls the object a deal after reviewing the evidence. Preserve the decision and its basis, but retain the evidence labels and do not create an AI-derived value corridor or bid ceiling. |
| Reject/Deferred | Out of scope, contradictory maker/material evidence, reproduction, inadequate evidence, or no commercial case |

Directional spread is a review signal, not profit. It excludes unverified
restoration, storage, holding time, resale fees, and final resale risk.
