# Correspondence with the supplied manuscript

The reference examined was the author-supplied `MMCR.pdf`, a 27-page preprint manuscript. Figure/page numbering below follows that file. The publisher version of record was not supplied for this comparison. Each claim is limited to the evidence stated below.

## Human-study measurements

The methods on pp. 13–14 define four groups with ten participants each, task duration, assistance requests and incorrect placements among 49 components. Figure 13 on p. 15 defines the four conditions.

The actual axes in Figure 14 are **(a) completion time, (b) accuracy, (c) question frequency**. Its caption reverses (b) and (c) and refers to five techniques, although four are shown. This release follows the plotted axes and the four-condition methods.

### Selecting the accuracy source

Two candidate sets were present in `tester.xlsx`:

| Source block | Evidence | Release decision |
| --- | --- | --- |
| H58:Q61 | Feeds the 49-component accuracy formulas; an active workbook chart references this block; derived traditional and MR-controlled-robot ranges match the manuscript | Include its 40 observed counts and derive accuracy explicitly |
| C52:E91, repeated as G52:P55 | Different values at 33 of 40 corresponding positions; does not match the stated accuracy ranges | Exclude from public data; retain in the local audit |

Selected traditional-group accuracy spans **83.673469%–91.836735%**, matching the text's **83.67%–91.84%** after rounding. Selected MR-controlled-robot accuracy spans **89.795918%–97.959184%**, matching **89.8%–97.96%**. Figure 14(b)'s visible ranges are consistent with the selected block. These are stronger selection criteria than choosing the nearest mean.

The source chart also references a group mean beyond the ten measurement columns. That summary cell is not exported as an eleventh observation. Formula caches were independently recalculated; the discrepancies between tables are not explained by stale caches.

The selected block's sample-variance pattern also matches the Figure 14(b) bars when the plotted accuracy variances are scaled by 1,000. The alternate block produces a different pattern, especially for the two middle conditions. The undocumented plot scaling is recorded in [known differences](KNOWN_DIFFERENCES.md).

### Summary reconciliation

All source means below are recomputed from the selected records, without changing any measurement:

| Condition | Time, min | Help requests | Accuracy, % |
| --- | ---: | ---: | ---: |
| 2D drawings | 15.19 | 6.8 | 87.755102 |
| MR interface | 7.32 | 2.1 | 95.510204 |
| MR-controlled cable robot | 8.96 | 5.7 | 93.877551 |
| MMCR | 5.00 | 0.6 | 99.387755 |

Appendix D p. 27 explicitly matches MR time **7.32**, MR-controlled-robot time **8.96**, and assistance means **2.1** and **5.7**. Timing and assistance distributions are consistent with the Figure 14 panels and active workbook chart references. Main-text means differ in several places; the full value-by-value comparison is in [paper_correspondence.csv](../metadata/paper_correspondence.csv). Agreement with a figure or appendix must not be described as agreement with every sentence in the paper.

## QR measurements

Appendix C, pp. 22–24, defines square QR code side lengths, HoloLens 2 detection, timing in seconds, distance in metres and efficiency as distance/time.

### Figure A3: indoor paired measurements

For block 1, all eight annotated peak coordinates match the exported observations after rounding to two decimals:

| QR side, cm | Distance, m | Distance/time, m/s |
| ---: | ---: | ---: |
| 2.5 | 0.23 | 0.33 |
| 5 | 0.54 | 0.78 |
| 7.5 | 0.72 | 1.41 |
| 10 | 1.04 | 1.76 |
| 12.5 | 1.27 | 2.05 |
| 15 | 1.57 | 3.14 |
| 17.5 | 2.00 | 4.00 |
| 20 | 2.16 | 3.13 |

This numerical agreement supports block 1's indoor assignment. The 2.5-cm observation at distance 0.82 m, which conflicts with the separate range table, is also visible in Figure A3 and is retained.

### Figures A4 and A5

The source indoor/outdoor range table corresponds to Figure A4. Block 2's four sizes correspond to the outdoor protocol and Figure A5 distributions. The source paired blocks do not explicitly name environments, so their source block IDs remain in the CSVs.

In Figure A5 the indoor red-X positions agree with source **medians**, although the legend says "Mean". The workbook also places `MEDIAN` formulas beneath a `mean` heading. The outdoor red-X positions agree with arithmetic means of the paired efficiencies. This release provides measured time/distance pairs and names any recomputed statistic correctly; it does not treat the original mislabeled summaries as new observations.

## Training exports

Figure 10 (p. 12) presents algorithm comparisons with an *Average Reward* axis, including an initial PPO/POCA/SAC comparison, an extended POCA comparison and a final PPO/POCA comparison. These are consistent with the source filename groups and observed training horizons. Figure 12(b) (p. 14) explicitly plots *Cumulative Reward*. Appendix B gives a 50,000-step summary frequency, consistent with all exported step intervals.

The author's recollection identifies these CSVs as cumulative-reward exports. This is recorded as author-supplied metadata, not an independently recovered TensorBoard tag. No exact panel-to-file mapping, smoothing window, seed identity or full training reproduction is claimed.
