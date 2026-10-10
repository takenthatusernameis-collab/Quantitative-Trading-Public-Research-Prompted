# Research Prioritization Procedure

Version 1.0 (initial bootstrap). Records the explicit ranking criteria used to select
public research for testing. Each experiment entry in the ledger cites the ranking
rationale that motivated it.

## Ranking Criteria (weighted, transparent, not empirically calibrated)

| Criterion | Weight | What it means |
|---|---|---|
| Economic plausibility | 0.20 | Clear mechanism; why would an inefficiency persist? |
| Evidence quality | 0.20 | Independent replication, out-of-sample, no obvious bias |
| Data availability | 0.15 | Free/low-cost data, no survivorship, sufficient history |
| Implementation ease | 0.10 | Direct translation to executable rules |
| Cost robustness | 0.10 | Edge survives realistic transaction costs and slippage |
| Novelty vs existing | 0.10 | Not duplicating experiments already in the ledger |
| Statistical rigor | 0.05 | Multiple-testing awareness, uncertainty quantified |
| Complementarity | 0.05 | Adds diversification to existing strategy set |
| Validation potential | 0.05 | Can be independently verified / walk-forward tested |

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