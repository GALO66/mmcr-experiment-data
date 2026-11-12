# MMCR experimental data

Version **1.1.0**, prepared 2026-11-12. This release contains training exports, human assembly-task measurements and QR-detection measurements associated with *Mixed reality and machine learning-guided cable robot framework (MMCR) for real-time prefabricated construction automation*. [Associated article](https://doi.org/10.1016/j.aei.2026.104580).

The tables were checked against the author-supplied **27-page `MMCR.pdf` manuscript**. That local manuscript contains internal differences between figures, main text and appendices. This release preserves source measurements and records the differences; it does not claim exact reproduction of every published summary or verification against the publisher's final PDF.

## Data

| Directory / table | Contents | Rows |
| --- | --- | ---: |
| `data/training/` | Twelve distinct training scalar series; three duplicate source copies consolidated | 3,190 |
| `data/human_study/task_performance.csv` | Completion time and assistance requests; four conditions with ten records each | 40 |
| `data/human_study/human_placement_accuracy.csv` | Selected placement-error counts, component count and explicitly derived accuracy | 40 |
| `data/qr_detection/recognition_trials_block_1.csv` | Eight QR sizes, ten paired time/distance observations each; indoor correspondence | 80 |
| `data/qr_detection/recognition_trials_block_2.csv` | Four QR sizes, ten paired observations each; outdoor correspondence | 40 |
| `data/qr_detection/detection_ranges.csv` | Minimum/maximum distance for eight sizes in each environment | 16 |

There are **17 data CSVs**. The 40 human-study rows in each table do not represent 80 participants; the tables contain different measurements. Record ordinals are local to their source blocks and are not verified cross-table participant identifiers. Training points are not independent trials. Range-summary rows are not additional QR trials.

All tables are UTF-8 CSV with one header row, one observation per row, explicit units and no merged cells, formulas, hidden sheets or embedded workbook metadata. Measured numeric strings are preserved. Original workbooks and screenshots are not included.

## How the tables match the manuscript

- **Human performance:** the selected timing and assistance blocks are linked to active source-workbook charts. MR-only time **7.32 min**, MR-controlled robot time **8.96 min**, and corresponding assistance means **2.1** and **5.7** match Appendix D. Some main-text values differ.
- **Placement accuracy:** the source block `H58:Q61` was selected because it feeds the accuracy formulas and an active workbook chart, and its 49-component accuracy ranges match the manuscript's traditional and MR-controlled-robot groups. The conflicting `C52:E91` / `G52:P55` block is excluded. All ten measured counts per condition are kept; mean-summary cells are not counted as trials.
- **QR trials:** all eight annotated peak coordinates in Figure A3 match block 1's distance/time ratios after rounding to two decimals. Block 2's four size groups and efficiency distributions correspond to the outdoor series in Figure A5. Source block IDs remain explicit because the paired-data headers omit environment labels.
- **QR range data:** the eight-size indoor/outdoor table corresponds to Figure A4. Four paired-trial distances exceed the separate range-table maxima; both records are retained with a documented flag.
- **Training:** the author recalls the exported metric as cumulative reward. Figure 10 labels its plotted quantity *Average Reward*, and Figure 12(b) labels *Cumulative Reward*. CSV metric tags, averaging settings and exact per-file panel mappings are not preserved. Algorithm labels remain filename-derived.

Read [paper correspondence](docs/PAPER_CORRESPONDENCE.md) and [known differences](docs/KNOWN_DIFFERENCES.md) before reproducing reported summaries. The machine-readable comparison is [metadata/paper_correspondence.csv](metadata/paper_correspondence.csv).

## Reading and checking the data

Use [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for definitions, missingness and units; [PROVENANCE.md](docs/PROVENANCE.md) explains selection and transformations.

```python
import csv
from pathlib import Path

path = Path('data/human_study/task_performance.csv')
with path.open(encoding='utf-8', newline='') as stream:
    records = list(csv.DictReader(stream))
```

Run `python tools/verify_release.py` from the repository root (`py tools/verify_release.py` on Windows). Python 3.9+ and its standard library are sufficient. The utility checks SHA-256, complete file membership, table schemas, numeric values, row counts and accuracy arithmetic without accessing the network or original sources. Checksums establish content consistency, not scientific validity.

## Metadata and scope

`metadata/file_manifest.csv` inventories every data table. `training_manifest.csv` describes the twelve training series and their hashes; `duplicate_aliases.csv` identifies three duplicate source exports. `source_workbooks.csv` records source-workbook digests without local paths. `dataset.json` describes the release.

This remains a partial study-data release: robot tension/trajectory logs, trained models, Unity environments, original event files and plotting code are not included. Source discrepancies and incomplete metadata are described explicitly. No claim is made that absent materials are unavailable elsewhere.

The preparation omitted direct personal identifiers, local paths, absolute training clock origins, email correspondence and original workbook containers. Human records contain condition labels, local ordinals and task outcomes only. These steps do not independently establish consent or guarantee that linkage with other information is impossible.

## License and citation

Data and documentation are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), with full terms in [LICENSE](LICENSE). Attribute the associated MMCR authors and this dataset title, link to the repository and license, and indicate changes. The verification utility uses the [MIT license](tools/LICENSE). The article and excluded materials are not relicensed by this package.

Qi Wang, Maowei Jiang, Tingtao Yu, Yusong Hu, Zhiyong Dong, Hongfei Ai, Yifan Wang and Peter Búš (2026). *Mixed reality and machine learning-guided cable robot framework (MMCR) for real-time prefabricated construction automation*. *Advanced Engineering Informatics*, 74, 104580. [DOI](https://doi.org/10.1016/j.aei.2026.104580). See [CITATION.bib](CITATION.bib).

Cite **MMCR experimental data, version 1.1.0**, the actual repository/release URL and commit or release used, together with the associated article. The article DOI is not a dataset DOI. No dataset DOI has been assigned here.
