# Data dictionary

All CSVs use UTF-8, comma delimiters, LF newlines and one header row. No missing values occur in the exported measurement fields. Original blank accuracy regions and untested QR conditions were not imputed. A recorded zero is retained as zero.

## Training series

| Column | Type / unit | Meaning |
| --- | --- | --- |
| `step` | Integer, recorded step units | Original `Step`. Starts at 50,000; increments by 50,000. The exact counter convention is not recorded in the CSV. |
| `value` | Decimal, reward scale provisionally assigned | Original scalar string. The author recalls cumulative reward; the raw tag and summary aggregation are unverified. Negative values are retained. Not a percentage or success rate. |
| `elapsed_wall_time_s` | Decimal, seconds | Original `Wall time` minus its series' first exported timestamp, using exact decimal arithmetic. First sample is zero, not the start of training. |

Absolute clock origins are omitted; cross-run calendar alignment is not available. Elapsed wall time can include pauses and does not establish comparable training speed. No smoothing or interpolation was applied.

## Human study: common fields and conditions

| Field | Meaning |
| --- | --- |
| `condition` | Source condition label, preserved verbatim |
| `record_index` | Ordinal 1–10 within a condition and source block; not a global person identifier or verified cross-table key |
| Fields ending in `_source_cell` | Original worksheet and cell address, without a filesystem path; source workbook is listed in the file manifest |

| Condition | Manuscript interpretation |
| --- | --- |
| `2D Drawings` | Manual assembly guided by drawings |
| `MR Interface` | MR guidance with manual component manipulation |
| `MR-Controlled Cable Robot` | MR guidance and manually controlled cable robot |
| `MR-Controlled Cable Robot with ML Agents` | MMCR: MR guidance with learning-based cable-robot automation |

The manuscript describes four groups of ten participants. Workbook ordinals do not independently verify unique identity or participant linkage across tables.

### `task_performance.csv`

| Column | Type / unit | Meaning |
| --- | --- | --- |
| `completion_time_min` | Decimal, minutes | Recorded total assembly-task completion time; decimal minutes, not `minutes.seconds` notation |
| `assistance_requests` | Integer-valued numeric string, count | Recorded requests for help; values such as `6.0` retain the workbook's stored numeric representation |
| `completion_time_source_cell`, `assistance_source_cell` | Cell references | Trace each observed value to the original workbook |

### `human_placement_accuracy.csv`

| Column | Type / unit | Meaning |
| --- | --- | --- |
| `incorrect_placements` | Integer-valued numeric string, count | Observed count from selected source block H58:Q61 |
| `total_components` | Integer, count | 49, supported by workbook formulas and manuscript methods |
| `correct_placements` | Integer, count; derived | `49 - incorrect_placements` |
| `accuracy_proportion` | Decimal, proportion; derived | `(49 - incorrect_placements) / 49`, rounded to 12 decimal places; multiply by 100 for percent |
| `incorrect_placements_source_cell` | Cell reference | Original measured error-count cell |
| `accuracy_formula_source_cell` | Cell reference | Corresponding original accuracy formula cell |

Keep observed counts distinct from derived accuracy. The competing error-count table is excluded based on formula/chart lineage and manuscript ranges, not because of more favorable outcomes. The selected source is not adjusted to force agreement with inconsistent prose means.

## QR trials

Both `recognition_trials_block_1.csv` and `recognition_trials_block_2.csv` have:

| Column | Type / unit | Meaning |
| --- | --- | --- |
| `source_block` | Text | `block_1` or `block_2`; preserves workbook block identity |
| `qr_side_length_cm` | Decimal, cm | Side length of a square QR code. Source header says cm², but the manuscript explicitly gives square side dimensions. Numeric values are unchanged. |
| `trial_index` | Integer, local ordinal | 1–10 for a QR size within a source block; no cross-size/session linkage asserted |
| `recognition_time_s` | Decimal, seconds | Recorded recognition time |
| `detection_distance_m` | Decimal, metres | Recorded paired detection distance; do not replace it with the separate range-table maximum |
| `time_source_cell`, `distance_source_cell` | Cell references | Original paired cells in the QR workbook |

Block 1 corresponds to **indoor** measurements: eight sizes from 2.5 to 20 cm, supported by all eight Figure A3 peak annotations. Block 2 corresponds to **outdoor** measurements: 12.5, 15, 17.5 and 20 cm, supported by Appendix C's protocol and Figure A5 distributions. The paired worksheet headers themselves do not label the environments.

Detection efficiency, if computed, is `detection_distance_m / recognition_time_s` in m/s. It is a detection-performance ratio, not physical movement speed. Means and medians must be named separately; the original workbook uses some `MEDIAN` formulas under a `mean` heading.

## QR distance ranges

`detection_ranges.csv` has `qr_side_length_cm`, `environment` (`indoor`/`outdoor`), `min_detectable_distance_m`, `max_detectable_distance_m` and source-cell references. Each row is a source range summary for one size/environment, not an individual timed trial. Unlike the paired blocks, its environment labels are explicit.

Four indoor paired distances exceed maxima in this separate table. They remain in the released data; see [known differences](KNOWN_DIFFERENCES.md). The range table must not be used to clip the trial observations.

## Metadata tables

`file_manifest.csv`: one row per data CSV; `columns` and `source_files` use semicolons within fields. `rows` excludes the header. `published_sha256` hashes the exact public file.

`training_manifest.csv`: original and published SHA-256 hashes, row/step/value ranges, source grouping and filename-derived algorithm labels. `metric_status` records author recollection and unverified tags. Numbered filenames are not known seed values.

`duplicate_aliases.csv`: three original byte-identical copies mapped to retained training IDs; these are not extra runs.

`source_workbooks.csv`: original basenames and hashes, selected blocks and transformation summaries. Source files remain local.

`paper_correspondence.csv`: manuscript locations, source-derived values, stated manuscript values and match status. Locations refer to the supplied 27-page manuscript, not an independently checked publisher PDF.
