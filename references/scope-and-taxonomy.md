# Scope And Taxonomy

## Target

Prioritize antique WMF Jugendstil/Art Nouveau and Art Deco objects, normally
from 1890–1940. Treat 1880–1950 as an edge range that needs a documented form,
model, catalogue, or designer link. The normal output is an online plausibility
assessment, not a physical expert opinion.

## Priority Tiers

| Tier | Include |
|---|---|
| P1 | Jardinières, centrepieces/epergnes, large candelabra or girandoles, large pitchers and decanters, bowls or punch vessels, documented designs |
| P2 | Rare large trays and bowls, complete tea or coffee services, figural objects, unusual Ikora metal, exceptional Myra or Ikora glass objects |
| P3 | Desk objects, smaller candlesticks, boxes, and utility ware only with a documented rare form, model, or designer |
| Exclude by default | Modern stainless/Cromargan goods, ordinary cutlery, single everyday cups or beakers, replacement parts, reproductions, and "WMF style" listings |

Ikora/Myra glass is an exceptional parallel track. Do not compare its sold
prices with metal objects merely because both are WMF.

## Evidence Statuses

Use these labels rather than forcing certainty:

- `documented`: a clear image or an attributable catalogue/auction reference
  supports the claim.
- `plausible`: multiple non-conflicting signals support it, but decisive proof
  is missing.
- `claimed_only`: seller text says it; local evidence does not support it.
- `unknown`: no usable evidence either way.
- `contradicted`: a visible mark, object form, or record conflicts with it.

`documented` means documented from the available online evidence. It is never
a guarantee of physical authenticity.

## Material Taxonomy

Record both axes below. Do not collapse them just because a listing says
"silver".

| Field | Allowed values |
|---|---|
| `base_metal` | `silver`, `nickel_silver_alpacca`, `britannia_pewter`, `brass_copper`, `other_alloy`, `glass`, `unknown` |
| `surface` | `solid_or_uncoated`, `silver_plated`, `gilded`, `patinated`, `unknown` |

Use only these public labels:

- `solid_silver_supported`: base is `silver`, surface is `solid_or_uncoated`,
  and online evidence supports a fineness/purity claim.
- `silver_plated`: surface is `silver_plated`; state the base when known, for
  example `silver_plated on nickel_silver_alpacca`.
- `nickel_silver_alpacca`: unplated or surface unknown.
- `britannia_pewter`.
- `other_alloy_or_unknown`.
- `glass_exception_track` for Myra/Ikora glass.

Never use `Massivsilber` for `silver_plated`, even when the base is Alpacca or
the seller uses an ambiguous foreign-language silver term.

## Exclusions And Exceptions

- An explicit foreign maker mark, modern production mark, reproduction claim,
  or clear primary-form contradiction is an exclusion.
- A complete rare flatware service can be reviewed only when its form/model and
  market exception are documented. Individual ordinary flatware stays out.
- Incomplete rare P1/P2 objects may become `watch`, not A or B, until missing
  components and restoration impact are known.
- An unmarked or badly photographed item may stay `watch` only if a distinctive
  form justifies follow-up. It cannot become a high-confidence candidate.
