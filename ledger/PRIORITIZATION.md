# Research Prioritization Procedure

Version 1.0 (initial bootstrap). Records the explicit ranking criteria used to select
public research for testing. Each experiment entry in the ledger cites the ranking
rationale that motivated it.

## Ranking Criteria (weighted, transparent, not empirically calibrated)

| Criterion | Weight | What it means |
|---|---|---|
| Economic plausibility | 0.20 | Clear mechanism; why would an inefficiency persist? |
| Evidence quality | 0.20 | Independent replication, out-of-sample, no obvious bias |
| Data availability | 0.12 | Free/low-cost data, no survivorship, sufficient history |
| Implementation ease | 0.05 | Direct translation to executable rules |
| Cost robustness | 0.12 | Edge survives realistic transaction costs and slippage |
| Turnover/Capacity | 0.08 | Turnover, liquidity, capacity constraints for implementability |
| Novelty vs existing | 0.03 | Not duplicating experiments already in the ledger |
| Statistical rigor | 0.05 | Multiple-testing awareness, uncertainty quantified |
| Complementarity | 0.05 | Adds diversification to existing strategy set |
| Validation potential | 0.04 | Can be independently verified / walk-forward tested |
| Data integrity | 0.06 | Signal/return series free of stitching, split, survivorship, roll artifacts; data construction understood |

## Source Priority Order

1. Original academic papers / working papers with reproducible empirical studies
2. Quantpedia / AQR research libraries
3. Open-source implementations (QuantConnect, Freqtrade, etc.)
4. arXiv / SSRN / NBER recent research
5. Other publicly accessible specialist sources

## Procedure

1. Inspect repository state (ledger, experiments, data, code).
2. Search public sources for candidate strategies.
3. Score each candidate on the criteria above.
4. Pick the highest-scoring untested candidate.
5. Design the cheapest falsifiable experiment.
6. Run, validate for biases, record in ledger (including negatives).
7. Re-rank remaining candidates; repeat.

## Version History

### v1.0 (2026-10-10)
- Initial bootstrap procedure.
- Motivation: repository was empty; needed a baseline ranking method.
- Expected benefit: explicit, auditable criteria to avoid ad-hoc selection.
- Evaluation: compare strategy hit-rate and OOS Sharpe against random baseline over next 10 experiments.
### v1.1 (2026-10-10) - Active
- Motivation: With strong gross results on broad universe, need to explicitly account for turnover/capacity and strengthen cost robustness.
- Changes:
  - Cost robustness: 0.12 (was 0.10)
  - Turnover/Capacity: 0.08 (new) - penalize high turnover, liquidity/capacity constraints
  - Novelty vs existing: 0.05 (was 0.10)
  - Data availability: 0.12 (was 0.15)
  - Implementation ease: 0.08 (was 0.10)
  - Economic plausibility: 0.20, Evidence quality: 0.20, Statistical rigor: 0.05, Complementarity: 0.05, Validation potential: 0.05
- Expected benefit: Better discrimination between gross vs net edge; forces turnover quantification.
### v1.2 (2026-10-11) - Active
- Motivation: E016 found that raw stitched futures (yfinance `=F` continuous contracts) contain large roll-seam artifacts (median gaps 0.3-2.5%; CL 2020 wedge of -306%/-127% overnight) that moved TSM OOS Sharpe by 21% (0.590 raw vs 0.717 de-seamed) and flipped its bear-market Sharpe (-1.06 to +0.15). E015's multi-asset results were computed on contaminated futures data. A candidate's data-construction risk must be screened before backtesting, not discovered after.
- Changes:
  - Data integrity: 0.06 (new) - is the signal/return series free of stitching, roll, split and survivorship artifacts; is the data construction understood?
  - Implementation ease: 0.05 (was 0.08)
  - Novelty vs existing: 0.03 (was 0.05)
  - Validation potential: 0.04 (was 0.05)
- Expected benefit: Catches artifact-dominated candidates early (e.g. futures on stitched series, split-unadjusted equities); redirects effort to strategies whose data pipeline is validated.
- Evaluation: Track whether top-ranked candidates require data-correction passes before backtesting; E016/E017 are the first scored under v1.2.
- Evaluation: Track turnover and net Sharpe under varying cost assumptions for top strategies.
