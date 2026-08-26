# Marks, Materials, Condition, And Model Evidence

## Review Sequence

1. Inspect all supplied object photos before interpreting the title.
2. Locate any maker mark, assay/fineness mark, model/form number, glass mark,
   patent text, or repair mark. Record image path and exact visible text.
3. Record material evidence separately from maker evidence.
4. Check the object class, dimensions, count, liners/inserts, electrical
   conversions, and any replacements before looking at prices.
5. Compare marks and model numbers only with a cited catalogue, museum, or
   relevant same-object auction reference.

## Mark Reporting

For every shortlisted record, report:

- `wmf_attribution_status` using the scope evidence labels;
- `mark_visibility`: `clear`, `partial`, `blurred`, `not_shown`, or
  `conflicting`;
- exact transcribed mark text, without silently correcting it;
- mark-photo path or source-image URL;
- `model_number_status`: `legible`, `reported_not_seen`, `not_found`, or
  `unclear`;
- the reference used to interpret a mark or model, if any.

WMF, W.M.F., I/O, OX, G, Geislingen, and similar marks are discovery or
attribution signals. They do not by themselves prove a material, a precise
date, a model, or physical authenticity. Never interpret a partial mark from
memory alone.

## Solid Silver Gate

Use `solid_silver_supported` only when the available evidence includes a
clear, compatible fineness/purity hallmark or a traceable high-quality auction
record that explicitly identifies solid silver and shows compatible marks. A
seller claim, colour, weight claim, or the word "silver" is insufficient.

If the fineness mark is unreadable, classify the material as `unknown` or as
the supported non-silver class. Do not value that object against solid-silver
references.

## Condition And Completeness Flags

Record rather than infer:

- plate wear, base-metal exposure, corrosion, pitting, deep polish, or lacquer;
- dents, splits, warping, cracks, solder, later joins, drilled holes, or
  altered electrification;
- replaced or missing glass/crystal liners, lids, handles, feet, burners, and
  candle cups;
- monograms, engraving removal, bent elements, and unstable construction;
- dimensions, weight, piece count, and whether those facts came from the
  seller or image measurement.

State `not visible` when an important area is not photographed. Do not convert
the absence of a described defect into evidence of good condition.
