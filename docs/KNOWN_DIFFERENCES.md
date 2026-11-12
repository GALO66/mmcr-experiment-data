# Known differences and interpretation limits

These differences were found during source-to-manuscript reconciliation. Measurements were not changed to force agreement.

## Human-study prose and figures

| Metric | Main text: 2D / MR / MR+CR / MMCR | Selected source means, same order |
| --- | --- | --- |
| Completion time, min | 14 / 6.5 / 9.5 / 5 | 15.19 / 7.32 / 8.96 / 5 |
| Assistance requests | 7.2 / 2.1 / 4.3 / 0.8 | 6.8 / 2.1 / 5.7 / 0.6 |
| Accuracy, % | 87.6 / 95.4 / 93.3 / 99.6 | 87.755102 / 95.510204 / 93.877551 / 99.387755 |

Several time and assistance means agree exactly with Appendix D instead. Selected accuracy ranges match the manuscript's reported ranges for the traditional and MR-controlled-robot conditions. Figure 14's caption swaps the accuracy and question-frequency panels. Follow actual axis labels, as detailed in [PAPER_CORRESPONDENCE.md](PAPER_CORRESPONDENCE.md).

The accuracy variance bars in Figure 14(b) visually match sample variances of the accuracy proportions multiplied by 1,000 (approximately 0.555324, 0.351705, 0.740432 and 0.097182). The axis does not state this scaling. Recomputed variance should retain its true squared-proportion units, or explicitly state any display scaling. These plot-bar heights are not raw variance observations.

The unused placement-count block differs in 33/40 entries and is not part of the public dataset. A separate 40-cell accuracy region was blank except for an isolated summary value elsewhere; those blanks were not converted to zeros or reconstructed from the isolated summary.

## QR source labels and records

- The workbook labels QR size as cm²; the manuscript explicitly describes square side dimensions in cm. Public `qr_side_length_cm` corrects the label without altering numeric values.
- Some source columns headed `mean` contain `MEDIAN` formulas. In Figure A5 indoor red-X markers correspond to medians, despite the legend's "Mean" label. Means and medians must be recomputed and labeled distinctly.
- Paired trial `Sheet1!I12` records **0.82 m** for a 2.5-cm code, while the indoor range table records a maximum of **0.32 m**. The 0.82-m point is visible in Figure A3. It is preserved, not replaced with 0.28 or clipped.
- Paired trials `J16`, `K16`, `L16` record **1.55, 1.56, 1.55 m** for a 12.5-cm code; the separate indoor range maximum is **1.53 m**. The trial and range tables remain separate source records.
- The 10-cm outdoor range-table maximum is **1.10 m**. The supplied manuscript prose says less than 1.0 m and gives a reduction percentage that does not exactly follow the tabulated 1.35-m indoor / 1.10-m outdoor maxima. The measured source values are preserved.
- Outdoor paired timing records exist only for sizes 12.5 cm and above. The separate range table covers all eight sizes. Missing outdoor paired conditions are not zero-duration or zero-distance observations.

## Remaining scope limits

Record ordinals do not establish cross-table participant identity or independent random seeds. Training tags, sampling/aggregation settings, seeds and exact plotted-file associations remain unverified. Unequal training horizons are retained, including the 5-million-step SAC export versus 10-million-step POCA/PPO exports in the initial group.

The release is not a complete reproduction environment and contains no trained models, Unity scenes, event logs, original plotting code, robot tension records or trajectories. The supplied manuscript was checked; the publisher's final PDF was not independently compared.
