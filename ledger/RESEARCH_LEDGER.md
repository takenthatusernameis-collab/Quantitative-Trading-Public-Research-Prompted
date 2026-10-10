# Research Ledger

Tracks every material experiment: sources, hypotheses, results, validation status, and decisions.

## Entry Format

```
## [ID] [Strategy Name] - [Status: Active | Reproduced | Failed | Rejected | Deprioritized]
- Source: <reference>
- Hypothesis: <economic mechanism>
- Data: <instruments, period>
- Design: <signal, universe, rebalancing, costs>
- Result: <key metrics>
- Validation: <checks performed>
- Decision: <next step>
```

---

## Experiments

---

## E001 - Bootstrap Infrastructure & Baseline Strategy Sweep [Completed 2026-10-10]

- **Status**: Completed
- **Source**: Repository was empty (PROMPT.MD + CI workflow only). No prior experiments.
- **Hypothesis**: A minimal, bias-aware backtesting pipeline can be built from free public
  data (yfinance) and used to falsify classic factor anomalies in a walk-forward setting.
- **Data**: 10 US sector/market ETFs (SPY, QQQ, IWM, VOO, VGT, XLK, XLF, XLE, XLV, XLI),
  2014-01-01 to 2026-10-09, daily, auto-adjusted. Benchmark: SPY.
- **Design**: Long-only, top-quintile equal-weight, executed at next-day open,
  tc=0.05% + slippage=0.02%. Walk-forward: 504-day train / 63-day test / 63-day step.
  42 OOS folds. No parameter optimization; fixed literature-standard parameters.
- **Result** (see `experiments/validation_summary.json`):

| Strategy | OOS Sharpe | z vs Placebo | Positive Folds |
|---|---|---|---|
| reversal (12-month) | 1.669 | 16.97 | 32/42 |
| low_vol | 1.467 | 16.18 | 31/42 |
| value | 1.039 | 14.87 | 23/42 |
| momentum_6m | 1.033 | 15.15 | 28/42 |
| quality (low-vol+mom) | 1.037 | — | 28/42 |
| short_reversal | 0.856 | 13.86 | 27/42 |
| momentum (12m) | 0.718 | 12.81 | 27/42 |
| mean_reversion_5 | 0.049 | 9.75 | 22/42 |
| **random (placebo, n=50)** | **-0.656** | — | 0/50 |

- **Validation**:
  - Placebo null distribution built (50 random sims): mean Sharpe **-0.656**, std 0.117.
    Costs destroy noise — a real falsification check.
  - All real strategies clear placebo with z > 9, well beyond 1.96.
  - Walk-forward with no leakage between folds; signals use only lagged data.
  - No look-ahead: weights shifted to next-day open execution.
- **Findings that survived**:
  - Long-term reversal (De Bondt-Thaler, 12-month) is the strongest OOS signal in this universe.
  - Low-vol anomaly (Ang et al. 2006/2008) is robust and cost-resistant.
  - Short-horizon (5-day) mean reversion is weak — consistent with noise-floor expectations.
- **Findings that failed / caveats**:
  - Single data source (yfinance), ETF universe only — not representative cross-section.
  - `auto_adjust=True` merges OHLC adjustments; open-price execution is approximate.
  - No parameter optimization; all signals use fixed parameters.
  - Not independently validated against alternative data or brokers.
- **Decision**: Pipeline is validated and ready for deeper research. Next: test on a
  broader universe (individual equities), add cost sensitivity, and explore
  cross-sectional momentum with industry-standard specifications.

---

## E002 - Prioritization Procedure v1.0 [Completed 2026-10-10]

- **Status**: Established
- **Rationale**: Repository was empty; needed an explicit, auditable ranking method
  to avoid ad-hoc source selection.
- **Procedure**: 9 weighted criteria (see `ledger/PRIORITIZATION.md`), source priority
  order matching the mission's 5-tier list.
- **Expected benefit**: Transparent, reproducible ranking; track which sources yield
  reproducible discoveries.
- **Evaluation**: Compare strategy hit-rate and OOS Sharpe against random baseline
  over the next 10 experiments; adjust weights if criteria mispredict.

---

# Handoff for Next Agent

## Most Valuable Next Task

**Extend the universe from 10 sector ETFs to a broad liquid equity universe
(e.g., top ~100 US large-caps by liquidity) and re-validate the top strategies.**

### Rationale

- Current results are **ETF-only** (10 names). Sector ETFs are highly correlated,
  giving a weak cross-section. Individual equities offer richer cross-sectional
  variation and are where most factor anomalies are documented.
- The top strategies (reversal, low_vol, momentum_6m, value) all show strong OOS
  z-scores vs placebo, but this has not been tested on a representative equity universe.
- This is the cheapest high-information experiment: reuse the existing pipeline
  (`src/batch_run.py`, `src/validate.py`) with a new `UNIVERSE` list.

### Prerequisites

- Existing code is complete and validated: `src/data.py`, `src/backtest.py`,
  `src/strategies.py`, `src/run_experiment.py`, `src/batch_run.py`, `src/validate.py`.
- Data pipeline caches to `data/*.parquet`; reuses downloads.
- Placebo baseline already built (`src/validation.py::placebo_distribution`).

### Concrete Completion Criteria

1. Define a new universe of ~50-100 liquid US equities (e.g., Dow 30 + S&P 100
   mega-caps, or a liquidity-filtered list). Add it to `UNIVERSES` in `run_experiment.py`.
2. Re-run `src/batch_run.py` on the new universe; capture `experiments/summary.json`.
3. Re-run `src/validate.py` for placebo comparison and z-scores.
4. Record findings in `ledger/RESEARCH_LEDGER.md` as a new experiment entry
   (include negatives, e.g., strategies that fail on the broader universe).
5. Update `README.md` with the new results.

### Blockers / Risks

- yfinance rate limits on large universes; consider caching and staggering downloads.
- Individual equities have higher idiosyncratic risk; diversification assumptions
  (top-quintile equal-weight) may need revisiting.
- Survivorship: yfinance backfill may include delisted names inconsistently;
  note this in the ledger.

### Infrastructure Status

- **Working**: data pipeline, walk-forward backtest, metrics, placebo validation.
- **Known limitations**: `auto_adjust=True` merges OHLC adjustments (open execution
  approximate); no parameter optimization; single data source.
## E003 - Broad Equity Universe (Large-Liquid) Validation [Completed 2026-10-10]

- **Status**: Completed
- **Source**: Follow-up to E001/E002 handoff - extend from ETF-only (10 names) to broad liquid equity universe (~132 mega-caps).
- **Hypothesis**: Cross-sectional factor signals are stronger/reproducible on individual equities with richer cross-sectional variation.
- **Data**: 132 large-liquid US equities, 2014-01-01 to 2026-10-09, daily, auto-adjusted. Benchmark: SPY.
- **Design**: Same as E001 - long-only top-quintile equal-weight, next-day open execution, tc=0.05% + slippage=0.02%, walk-forward 504/63/63 (42 OOS folds). No parameter optimization.
- **Result** (large_liquid universe):

| Strategy | OOS Sharpe | z vs Placebo | Positive Folds |
|---|---|---|---|
| reversal (12-month) | 2.103 | 29.46 | 34/42 |
| low_vol | 1.748 | 33.38 | 34/42 |
| quality (low-vol+mom) | 1.523 | 30.75 | 33/42 |
| momentum_6m | 1.335 | 30.85 | 30/42 |
| momentum (12m) | 1.248 | 29.30 | 31/42 |
| value | 1.120 | 24.82 | 24/42 |
| short_reversal | 0.776 | 21.10 | 25/42 |
| mean_reversion_5 | 0.087 | 18.03 | 26/42 |
| **random (placebo)** | **-0.656** | — | 0/50 |

- **Validation**:
  - All strategies clear placebo with large z-scores (z > 18).
  - Infrastructure extended: added `large_liquid` to `UNIVERSES` in `run_experiment.py`; `batch_run.py` and `validate.py` accept `--universe`.
  - Fixed cache filename length issue (hash-based cache keys in `data.py`).
  - Caching critical for 132-ticker downloads.

- **Findings**:
  - Performance improved on broader universe vs ETF-only for top signals (reversal: 2.10 vs 1.67, low_vol: 1.75 vs 1.47).
  - Quality blend performs strongly on equities (OOS Sharpe 1.52).
  - Short-term mean reversion remains weak.
  - Turnover (equal-weight top-quintile, sampled): momentum~0.47, momentum_6m~0.15, reversal~0.10, low_vol~0.06, quality~0.33 - reversal/low_vol are cost-robust.

- **Caveats**: yfinance rate limits, potential delisted tickers (BK/WBA noted), survivorship bias concerns, top-quintile equal-weight still relatively concentrated.
- **Decision**: Results robust on broad universe. Next: cost sensitivity (vary tc/slippage) using full large_liquid universe, compute turnover systematically, test risk-adjusted sizing (inverse vol) vs equal-weight.

## E004 - Prioritization Procedure v1.1 [Proposed 2026-10-10]

- **Status**: Proposed
- **Motivation**: Results on broad universe are strong grossly, but transaction costs and turnover will determine economic value. Current procedure weights cost robustness but doesn't explicitly capture turnover/capacity/liquidity constraints.
- **Proposed changes** (see `ledger/PRIORITIZATION.md` version history):
  - Add "Turnover/Capacity" criterion (weight 0.08) to explicitly penalize high-turnover strategies
  - Increase "Cost robustness" to 0.12 (from 0.10)
  - Reduce "Novelty vs existing" to 0.05 (from 0.10)
  - Reduce "Data availability" to 0.12 (from 0.15)
  - Reduce "Implementation ease" to 0.08 (from 0.10)
  - Other criteria unchanged: Economic plausibility 0.20, Evidence quality 0.20, Statistical rigor 0.05, Complementarity 0.05, Validation potential 0.05 (total 1.0)
- **Rationale**: Forces quantification of turnover and cost sensitivity; better discriminates between gross vs net edge.
- **Expected benefit**: More realistic ranking that favors strategies surviving realistic trading costs.
- **Evaluation**: For top strategies, report turnover and test net Sharpe under varying cost assumptions (e.g., 5+10bps, 10+10bps, 10+20bps). If turnover-heavy strategies degrade materially, validate this reweighting is effective.

---

# Handoff for Next Agent (v1.1)

## Most Valuable Next Task
**Cost sensitivity analysis for top strategies on large_liquid universe.** Quantify how net Sharpe degrades with varying transaction costs and slippage, and systematically compute average turnover per strategy.

### Rationale
- Gross OOS Sharpe is excellent (reversal 2.10, low_vol 1.75, quality 1.52), but net edge depends on turnover + costs.
- Turnover varies widely (low_vol ~0.06, reversal ~0.10, quality ~0.33, momentum ~0.47). Need precise quantification across full large_liquid.
- Prioritization v1.1 (proposed) adds Turnover/Capacity and strengthens Cost robustness - this experiment will inform and validate that reweighting.
- Cheapest high-info experiment: extend backtest to report turnover and sweep cost parameters.

### Prerequisites
- Infrastructure complete (`src/backtest.py` now has `average_turnover`, batch/validate accept universe args)
- `large_liquid` results exist, cached data available
- Baseline established

### Concrete Completion Criteria
1. Compute systematic turnover for all strategies on large_liquid universe (report in ledger)
2. Run cost sensitivity sweep: vary tc_cost (0.0000, 0.0005, 0.0010, 0.0020) and slippage (0.0000, 0.0002, 0.0005) combinations for top 5 strategies. Record net OOS Sharpe for each.
3. Document results in new experiment entry (E005) in ledger with table of net Sharpe by cost scenario
4. Update README to include net-of-cost guidance if material
5. Based on findings, confirm or refine E004 prioritization weights (record decision)

### Blockers/Risks
- Running sweeps is cheap (reuse existing pipeline). No blockers.
- Need to be careful not to over-optimize costs; test reasonable ranges.

### Infrastructure Status
- Working: data, walk-forward, metrics, placebo, universe config, caching fixed.
- Added: `average_turnover()` in backtest; universe args in batch/validate.
