# Provenance and transformations

Version 1.1.0 expands the earlier training-only preparation using two additional author-supplied workbooks. It was prepared on 2026-11-12. All original source files remain unchanged.

## Source inventory

- Fifteen training CSVs: twelve distinct byte sequences and three duplicate aliases.
- `tester.xlsx`: one visible worksheet containing human-task records, alternate placement blocks, formulas and charts.
- `QR test record.xlsx`: one visible worksheet containing paired recognition measurements, distance ranges, duplicate layouts and formulas.
- Four TensorBoard desktop screenshots: inspected for context and excluded.
- `MMCR.pdf`: read only for correspondence; not redistributed.

Source digests and public digests are recorded in the metadata. Local paths, correspondence and internal review artifacts remain outside the public package.

## Training preparation

Original headers were `Wall time,Step,Value`. `Step` and `Value` numeric strings were retained exactly and in order as `step` and `value`. Absolute `Wall time` was replaced by `Decimal(Wall time) - Decimal(first Wall time)` in seconds. Files were renamed with normalized group labels and written as UTF-8 with LF newlines. All 3,190 observations in distinct series remain. No smoothing, clipping, interpolation or statistical selection was applied.

Algorithm names come from source filenames or byte-identical aliases. Metric meaning is attributed to the author's recollection and qualified by the missing raw tag. File suffixes do not establish seeds or independence.

## Workbook preparation

Workbook ZIP/XML contents were inspected without executing macros or external links. Both had one visible sheet and no hidden rows/columns, external links, defined names, embedded media, macros, direct personal identifiers in cells or author properties. Empty person registries carried no comment records. Original workbook containers are not redistributed.

Flat CSVs use one row per observation, single-level headers, explicit units, local record ordinals and source-cell references. Source measured numeric strings are preserved, including integer-valued strings such as `6.0`. Summary cells, duplicated transposed tables and blank measurement blocks are excluded from observation counts.

For human accuracy, block H58:Q61 was selected through formula/chart lineage and matching manuscript ranges. The alternate C52:E91/G52:P55 block was excluded; the decision and differences are recorded in [paper correspondence](PAPER_CORRESPONDENCE.md). Correct count and accuracy are explicitly derived from 49 components; proportions are rounded to twelve decimal places. No measured error count is changed.

For QR data, paired time/distance records are retained separately from source minimum/maximum range summaries. The source cm² size label is normalized to side length in cm using the manuscript's stated square dimensions, without changing numbers. Repeated image-size timing layouts and computed ratio/statistic cells are not added as extra trials. Ratios can be recomputed from the exported measured pairs.

All 360 workbook formula caches inspected were independently recalculated and agreed within 5e-10. This verifies arithmetic consistency of those formula blocks; it does not resolve differences between separate source blocks or inconsistent manuscript prose.

## Checks

- Compare every exported measured cell with its selected source cell and verify derived accuracy.
- Recompute SHA-256 for all original sources before and after preparation.
- Check CSV schemas, finite values, unique local record keys, row counts and relevant ranges.
- Check all training step/value strings and decimal elapsed times against the original exports.
- Inspect numeric versus text fields for formula-injection payloads and scan public text for common credentials, email addresses and absolute local paths.
- Package only an explicit file allowlist, check local documentation links and verify archive bytes against the public directory.

No individual names or contact details are released. Condition labels and local ordinals are retained for interpretation, without asserting globally unique participants or cross-table linkage. Removal of direct identifiers is not independent proof of consent, anonymity or scientific reproducibility.
