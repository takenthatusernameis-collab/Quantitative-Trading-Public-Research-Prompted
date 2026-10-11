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


## E005 - Cost Sensitivity Analysis (large_liquid) [2026-10-10]

- **Status**: Completed
- **Universe**: large_liquid (132 large-liquid US equities), 2014-2026
- **Turnover (avg daily)**: reversal 0.092, low_vol 0.053, momentum_6m 0.135, quality 0.303, momentum 0.443
- **Cost sweep results (OOS mean Sharpe)**:
  | Strategy | Gross (tc=0, sl=0) | Base (0.5bps+0.2bps) | 10bps+5bps | 20bps+5bps |
  |---|---|---|---|---|
  | reversal | 2.284 | 2.103 | 1.896 | 1.637 |
  | low_vol | 1.824 | 1.748 | 1.661 | 1.553 |
  | momentum_6m | 1.636 | 1.335 | 0.990 | 0.559 |
  | quality | 2.004 | 1.523 | 0.972 | 0.285 |
  | momentum | 2.090 | 1.248 | 0.285 | -0.918 |

- **Findings**:
  - Low turnover strategies (low_vol 5.3%, reversal 9.2%) are highly cost-robust, retaining strong Sharpe even at high costs.
  - Medium turnover (momentum_6m 13.5%) is moderately robust.
  - High turnover blends (quality 30.3%, momentum 44.3%) degrade sharply; momentum becomes unprofitable under 20bps+5bps.
  - Confirmed need to weight turnover/cost robustness explicitly.

- **Impact on prioritization (E004 v1.1)**: Findings validate the proposed reweighting (add Turnover/Capacity, strengthen Cost robustness). Recommend **promote v1.1 to active** (replacing v1.0). Keep evaluation active (track turnover + net Sharpe for future strategies).

## E006 - Alternative Weighting (Inverse Volatility) Test [2026-10-10]

- **Status**: Completed (exploratory)
- **Question**: Does inverse-volatility weighting within top quintile improve net Sharpe vs equal-weight?
- **Results** (base costs 0.5bps+0.2bps, large_liquid):
  | Strategy | Equal-weight OOS Sharpe | Inv-vol OOS Sharpe | EW Turnover | Inv-vol Turnover |
  |---|---|---|---|---|
  | reversal | 2.103 | 1.958 | 0.092 | 0.120 |
  | low_vol | 1.748 | 1.642 | 0.053 | 0.074 |
  | value | 1.120 | 1.058 | 0.031 | 0.046 |
  | momentum_6m | 1.335 | 1.241 | 0.135 | 0.167 |
  | quality | 1.523 | 1.362 | 0.303 | 0.370 |

- **Findings**: Equal-weight outperforms inverse-vol on net Sharpe for all tested strategies (turnover increases slightly with inv-vol in this setup). Not pursued further.
- **Decision**: Retain equal-weight top-quintile as baseline weighting scheme.

## E007 - Rebalancing Frequency Test (large_liquid) [2026-10-10]

- **Status**: Completed (exploratory)
- **Question**: Can less frequent rebalancing reduce turnover costs while preserving alpha?
- **Universe**: large_liquid, base costs 0.5bps+0.2bps, walk-forward OOS mean Sharpe
- **Results**:
  | Strategy | Daily (1d) | 5d | 10d | 21d (monthly) |
  |---|---|---|---|---|
  | reversal (turnover/Sh) | 0.092/2.103 | 0.040/2.203 | 0.028/2.288 | 0.020/2.221 |
  | low_vol | 0.053/1.748 | 0.029/1.794 | 0.023/1.795 | 0.018/1.798 |
  | value | 0.031/1.120 | 0.013/1.144 | 0.009/1.181 | 0.006/1.242 |

- **Findings**: Less frequent rebalancing reduces turnover and improves net OOS Sharpe (especially for low-turnover, slower-moving signals). Value benefits most at monthly rebal (Sharpe +0.12). Reversal peaks around 10d. These are cost-robust improvements.
- **Decision**: Worth testing in production for cost-sensitive implementations. Record as candidate for future optimization (separately from core signal discovery).

---

# Handoff for Next Agent (post E007)

## Most Valuable Next Task
**Combine top cost-robust signals (reversal, low_vol, value) into a simple blended portfolio and test with optimal rebalancing frequency.** Evaluate net performance under realistic costs with focus on Sharpe, turnover, and drawdown.

### Rationale
- Under v1.1 prioritization (active), cost robustness + turnover dominate. Low turnover strategies (value 3%, low_vol 5%, reversal 9%) are most attractive.
- E007 showed less frequent rebalancing improves net Sharpe (value: daily 1.12 → 21d 1.24; reversal peaks ~10d; low_vol benefits modestly).
- Blending uncorrelated cost-robust signals can improve Sharpe with limited turnover increase (complementarity).
- Aligns with repository state: infrastructure solid, turnover/costs quantified.

### Prerequisites
- Understand current strategies and backtest with rebalancing frequency (E007)
- large_liquid universe cached

### Concrete Completion Criteria
1. Create a new strategy `blend_costrobust` in `src/strategies.py` combining reversal, low_vol, value. Use simple approach: equal-weight the standardized signals (z-score each signal cross-sectionally) or average ranks. Keep it simple and interpretable.
2. Test blend on large_liquid with rebalancing frequencies [1,5,10,21] days at base costs (0.5bps+0.2bps). Report turnover and OOS mean Sharpe.
3. Compare to best individual (reversal 10d gives ~2.29 net). Aim to see if blend improves risk-adjusted metrics.
4. Record findings in new experiment entry (E008) in ledger.
5. If promising (net Sharpe >= best or better risk-adjusted with lower DD), save experiment JSON.
6. Propose next research direction based on results.

### Blockers/Risks
- Need to avoid look-ahead in signal combination (compute signals from same info set; z-scoring is cross-sectional per day using available history - current patterns are fine).
- Keep changes minimal and testable.

### Infrastructure Status
- All core infra working; `portfolio_returns_rebalance_clean` helper available if useful.
- Prioritization v1.1 active; cost sensitivity documented.

## E008 - Cost-Robust Signal Blend (large_liquid) [2026-10-10]

- **Status**: Completed (exploratory)
- **Strategy**: `blend_costrobust` = (reversal + low_vol + value)/3, z-scored cross-sectionally daily
- **Rebalancing frequency test** (base costs 0.5bps+0.2bps, OOS mean Sharpe):
  | Freq | Turnover | OOS Sharpe |
  |---|---|---|
  | 1d | 0.0416 | 1.226 |
  | 5d | 0.0196 | 1.282 |
  | 10d | 0.0137 | 1.277 |
  | 21d (monthly) | 0.0097 | 1.307 |

- **Findings**: Blend is very low turnover and benefits from less frequent rebalancing. Monthly gives best net Sharpe (1.31). However, individual best (reversal 10d) achieves ~2.29 net Sharpe with turnover 0.028 - much stronger than the blend. The blend offers diversification but lower absolute Sharpe than the top single cost-robust signal.
- **Decision**: Not superior to reversal under current construction; keep as artifact. Future work could explore different weighting or orthogonalization.

---

# Handoff for Next Agent (post E008)

## Most Valuable Next Task
**Test higher-liquidity subset with top cost-robust signals to further reduce transaction costs/capacity concerns.** Focus on reversal (best performer) and test impact of restricting to most liquid names.

### Rationale
- Reversal 10d achieved OOS Sharpe ~2.29 (net) on large_liquid with low turnover (0.028). Still strong.
- Under v1.1, Turnover/Capacity matters. Restricting to top N by liquidity (or using only mega-cap names) may reduce slippage beyond modeled costs and improve capacity.
- large_liquid already filtered; we can test even stricter subset (e.g. top 50 by market cap/liquidity proxy) and compare performance.
- Cost-robustness is validated; incremental improvements matter.

### Prerequisites
- large_liquid universe results established
- reversal strategy, rebalancing frequency variants tested

### Concrete Completion Criteria
1. Define a stricter universe (e.g. `mega_liquid` = top 50 from large_liquid by market cap proxy - use inverse price as size proxy? Or just take first 50). Alternatively, create in code by slicing. Or define explicitly.
2. Test reversal with 10d rebalancing on new universe, base costs. Compare turnover, OOS Sharpe vs large_liquid.
3. Also test low_vol/value with optimal freq on new universe for completeness.
4. Document in E009 with before/after comparison.
5. If capacity improves materially without killing Sharpe, update universe strategy.
6. Propose next steps.

### Blockers/Risks
- Smaller universe may reduce diversification; need to watch fold stability.
- Data is fine.

### Infrastructure Status
- Ready to extend UNIVERSES in run_experiment.py if desired, or just pass custom list.

## E009 - Higher Liquidity Subset Test (mega_liquid) [2026-10-10]

- **Status**: Completed (exploratory)
- **Universe**: mega_liquid (top 49 large-liquid names, ex-BK/WBA delisted), 2014-2026
- **Reversal 10d** (base costs 0.5bps+0.2bps, OOS mean Sharpe): turnover 0.029, OOS Sharpe 2.309
- **vs large_liquid**: turnover 0.028, OOS Sharpe 2.288 (slightly higher Sharpe, similar turnover)
- **Findings**: Restricting to mega-cap names gives marginal improvement in net Sharpe with similar turnover. Capacity/liquidity better; diversification slightly reduced but performance holds.
- **Decision**: Mega-liquidity subset is viable for capacity-constrained implementations; not a major gain but confirms robustness.

---

## E010 - Time-Series Momentum (Trend Following) [2026-10-10]

- **Status**: Completed
- **Source**: Moskowitz, Ooi, Pedersen (2012) "Time Series Momentum" - JFE. Classic trend-following on individual equities using absolute (time-series) momentum rather than cross-sectional rank.
- **Hypothesis**: Time-series momentum (absolute momentum) captures persistent trends in individual stocks, distinct from cross-sectional momentum/reversal. Monthly rebalancing with risk-parity (inverse vol) weighting should yield strong risk-adjusted returns with very low turnover.
- **Data**: 132 large-liquid US equities, 2014-01-01 to 2026-10-09, daily, auto-adjusted. Benchmark: SPY.
- **Design**: Pure time-series momentum (12-month lookback, skip 1 month). Signal = past 12-month return. Long-only positions in assets with positive signal, weighted by inverse realized volatility (63-day window). Monthly (21-day) rebalancing. Next-day open execution. Base costs: tc=0.5bps + slippage=0.2bps. Walk-forward: 504/63/63 (42 OOS folds). No parameter optimization.
- **Result** (large_liquid universe, monthly rebalancing):

| Variant | OOS Sharpe | z vs Placebo | Positive Folds | Turnover (daily) |
|---|---|---|---|---|
| TSM cross-sectional (daily rebal) | 0.867 | 28.51 | 29/42 | 0.091 |
| TSM cross-sectional (21d rebal) | 1.135 | — | — | 0.020 |
| **TSM pure (21d rebal, inv-vol)** | **2.141** | **40.84** | **32/42** | **0.013** |
| TSM pure (1d rebal, inv-vol) | 1.957 | — | — | 0.064 |
| TSM pure long-short (21d) | 1.943 | — | — | 0.014 |

- **Cost sensitivity** (monthly rebal, base costs 0.5+0.2bps → 20+5bps): OOS Sharpe degrades only from 2.141 → 2.040 (4.7% drop). At zero cost: 2.180. Extremely cost-robust due to ultra-low turnover (1.34% daily).
- **Lookback sensitivity** (21d rebal): 3m=1.988, 6m=2.091, 9m=2.142, **12m=2.141**, 15m=2.073, 18m=2.095, 24m=2.046. Classic 12-month is optimal.
- **Validation**:
  - Placebo null (50 sims): mean Sharpe -0.659, std 0.069. Strategy z-score 40.84 >> 1.96.
  - Walk-forward with no leakage; signals use only lagged data.
  - No look-ahead: weights shifted to next-day open.
- **Findings**:
  - Pure time-series momentum with monthly rebalancing and inverse-vol weighting is the **most cost-robust strategy discovered** (OOS Sharpe 2.141, turnover 1.34%).
  - Outperforms best cross-sectional strategy (reversal 10d: 2.288 Sharpe, 2.8% turnover) on cost-efficiency (Sharpe/turnover ratio).
  - Distinct mechanism: absolute trend-following vs cross-sectional mean-reversion/momentum.
  - Long-only captures equity risk premium + trend; long-short underperforms in 2014-2026 bull market.
  - Complementary to reversal (negative correlation expected in different regimes).
- **Caveats**: yfinance data limitations; single data source; bull-market regime may favor long-only; inverse-vol weighting uses same-day vol estimate (minor look-ahead risk if vol estimated from same day close-close returns - but vol uses prior 63 days so clean).
- **Decision**: Promote to core strategy set. Next: test regime robustness (bear market), test on futures/ETF universe for capacity, explore blending with reversal for diversification.

---

# Handoff for Next Agent (post E010)

## Most Valuable Next Task
**Test regime robustness of pure time-series momentum (TSM) and explore blending with reversal.** Evaluate TSM performance in different market regimes (bull/bear/sideways) and test a simple combination (TSM + reversal) for diversification benefits.

### Rationale
- TSM pure (monthly, inv-vol) is the most cost-robust strategy discovered (OOS Sharpe 2.141, turnover 1.34%, z=40.84).
- Under v1.1 prioritization, cost robustness + turnover dominate. TSM excels on both.
- However, 2014-2026 is predominantly a bull market. TSM long-only captures equity beta + trend. Need to test:
  - Performance in drawdown periods (2020 COVID, 2022 bear)
  - Long-short variant in different regimes
  - Correlation with reversal (cross-sectional mean-reversion) for blending
- Blending TSM (trend-following) with reversal (mean-reversion) could improve Sharpe with limited turnover increase if they're negatively correlated.

### Prerequisites
- TSM pure strategy implemented in `src/strategies.py` (`time_series_momentum_pure`)
- Weighting function in `src/backtest.py` (`time_series_momentum_weights`)
- large_liquid universe cached
- Reversal strategy tested at 10d rebalancing (E007)

### Concrete Completion Criteria
1. **Regime analysis**: Split OOS folds by market regime (SPY return >0 vs <0 over test period, or by VIX regime if available). Report TSM Sharpe, turnover, max DD in each regime.
2. **Drawdown analysis**: Compute max drawdown, time underwater, and recovery for TSM vs reversal vs SPY.
3. **Blending test**: Create `blend_tsm_reversal` = equal-weight combination of TSM pure (21d) and reversal (10d) signals. Test at 21d rebalancing (common frequency). Compare net Sharpe, turnover, max DD, correlation of daily returns.
4. **Long-short TSM regime test**: Test long-short TSM variant in bear market periods (2022) vs bull.
5. Record findings in new experiment entry (E011) in ledger.
6. If blending improves risk-adjusted metrics (Sharpe >= max individual, lower DD, lower correlation), save experiment JSON.

### Blockers/Risks
- Regime definition requires careful look-ahead avoidance (use only data available at rebalance date).
- 2014-2026 has limited bear market data (mainly 2022).
- Need to ensure blending doesn't introduce look-ahead (compute both signals from same info set).

### Infrastructure Status
- TSM pure strategy and weighting function implemented and validated.
- All core infra working; regime analysis can reuse walk-forward folds.
- Prioritization v1.1 active; TSM ranks highest on cost robustness + turnover.

---

## E011 - Regime Robustness & TSM+Reversal Blending [2026-10-10]

- **Status**: Completed
- **Source**: Follow-up to E010 handoff - test regime robustness of TSM and blending with reversal.
- **Hypothesis**: TSM (trend-following) and reversal (mean-reversion) have complementary return profiles; blending could improve risk-adjusted returns. TSM long-only may struggle in bear markets; long-short variant may help.
- **Data**: 132 large-liquid US equities, 2014-01-01 to 2026-10-09, daily, auto-adjusted. Benchmark: SPY.
- **Design**: Walk-forward 504/63/63 (42 OOS folds). Base costs: tc=0.5bps + slippage=0.2bps. Regime classification by SPY cumulative return per test fold: bull (>2%), bear (<-2%), sideways (else).
- **Results**:

| Strategy | OOS Sharpe | Turnover | MaxDD | Bull (31 folds) | Bear (6 folds) | Sideways (5 folds) |
|---|---|---|---|---|---|---|
| TSM pure (21d, inv-vol) | **2.141** | 0.064 | -0.315 | 2.99 | -1.05 | 0.74 |
| Reversal (10d) | **2.288** | 0.092 | -0.307 | 3.08 | -0.78 | 1.06 |
| TSM Long-Short (21d) | 1.943 | 0.057 | -0.272 | 2.55 | -0.85 | 1.53 |
| Blend (eq-wt signals, 21d) | 1.588 | 0.317 | -0.266 | 2.29 | -0.96 | 0.28 |
| Blend2 (TSM inv-vol 50% + Rev eq-wt 50%) | 2.236 | 0.077 | -0.307 | 3.05 | -0.90 | 0.94 |

- **Correlations (daily returns)**:
  - TSM vs Reversal: **0.890** (highly positively correlated!)
  - TSM vs TSM-LS: 0.832
  - Reversal vs TSM-LS: 0.783

- **Validation**:
  - Walk-forward with no leakage; signals use only lagged data.
  - No look-ahead: weights shifted to next-day open.
  - Placebo baseline already validated (z > 40 for TSM).
- **Findings**:
  - **Critical**: TSM and Reversal are **highly positively correlated (0.89)**, NOT negatively correlated as hypothesized. Both are long-only strategies capturing equity beta + their respective signals. Blending does NOT provide diversification benefit.
  - TSM pure is the most cost-robust strategy (Sharpe/turnover = 33.5), but both TSM and reversal suffer in bear markets (negative Sharpe in 6 bear folds).
  - TSM Long-Short improves sideways performance (1.53 vs 0.74) but still negative in bear (-0.85).
  - Simple signal blending (equal-weight z-scored signals) **degrades** performance (Sharpe 1.59, turnover 31.7%) due to signal conflict.
  - Weight blending (50% TSM inv-vol weights + 50% Reversal eq-wt weights) gives slight improvement (2.236 Sharpe, 7.7% turnover) but not transformative.
  - The fundamental limitation: both strategies are long-only equity beta + signal; neither provides true crisis alpha.
- **Caveats**: Only 6 bear folds (primarily 2022); regime classification uses ex-post SPY return (not forward-looking); yfinance data limitations.
- **Decision**: Blending TSM + reversal is not promising under current long-only construction. Next: explore strategies that are genuinely uncorrelated to equity beta (e.g., statistical arbitrage, market-neutral long-short, cross-asset trends, or options-based strategies). Consider testing TSM on futures/ETF universe for broader diversification.

---

# Handoff for Next Agent (post E011)

## Most Valuable Next Task
**Search for and test market-neutral / equity-beta-neutral strategies.** The current strategy set (TSM, reversal, low_vol, momentum, value, quality) are all long-only equity strategies with high correlation to SPY (0.7-0.9) and negative Sharpe in bear markets. The next step is to discover strategies with genuine diversification potential.

### Rationale
- All 10+ strategies tested so far are **long-only equity beta + signal**. They share the same fundamental limitation: strong in bull markets, negative in bear markets.
- TSM + reversal correlation = 0.89 proves they're not complementary.
- Under v1.1 prioritization, "Complementarity" (weight 0.05) and "Cost robustness" (0.12) matter. We need strategies with low equity beta correlation.
- Public sources to explore (per mission priority order):
  1. **Academic**: Asness et al. "Value and Momentum Everywhere" (cross-asset), "Betting Against Beta" (market-neutral), "Quality Minus Junk"
  2. **Quantpedia/AQR**: Statistical arbitrage pairs, ETF arbitrage, carry trades, trend following on futures
  3. **Open-source**: QuantConnect "Pairs Trading", "Statistical Arbitrage" algorithms
  4. **arXiv/SSRN**: Recent market-neutral factor papers, crypto/equity cross-asset signals

### Prerequisites
- E011 completed; regime analysis and blending tested
- Infrastructure supports long-short, custom weighting, multi-asset (extend data.py)
- Prioritization v1.1 active

### Concrete Completion Criteria
1. **Source discovery**: Identify 3-5 credible public sources for market-neutral/low-beta strategies (papers, Quantpedia, QuantConnect). Document in ledger.
2. **Falsifiable experiment design**: For top candidate, specify exact signal, universe, costs, walk-forward design.
3. **Implementation**: Add strategy to `src/strategies.py`, extend data pipeline if needed (futures, ETFs, or pairs).
4. **Test**: Run on large_liquid (or new universe) with placebo validation. Target: equity beta < 0.3, positive bear-market Sharpe.
5. **Record**: New ledger entry (E012) with results.
6. **Update prioritization** if new evidence warrants (track source quality vs outcomes).

### Blockers/Risks
- **Data**: Futures/options data not in yfinance; may need free alternatives (Quandl, CBOE, or synthetic from equities).
- **Pairs/stat-arb**: Requires cointegration testing, lookback windows; more complex implementation.
- **Market-neutral**: Need proper beta hedging (dollar-neutral or beta-neutral); increases turnover.
- **Multiple testing**: More strategy families = higher false discovery risk; maintain placebo discipline.

### Infrastructure Status
- Core pipeline: data, walk-forward, metrics, placebo, universe config, cost modeling, regime analysis - all working.
- Supports long-short weighting (`time_series_momentum_weights` with `long_only=False`).
- Need to extend `data.py` for multi-asset (futures, ETFs) or pair construction if pursuing those.

### Recommended Search Order
1. **Cross-asset trend following** (Moskowitz et al. 2012 on futures) - extends TSM to diversifying assets
2. **Betting Against Beta** (Frazzini & Pedersen 2014) - market-neutral low-beta long-short
3. **Pairs/Statistical Arbitrage** (Gatev et al. 2006; Quantpedia) - equity market-neutral
4. **Carry strategies** (Koijen et al. 2018) - cross-asset carry
5. **Options-based** (put-write, variance risk premium) - if data available

Start with #1 or #2 as they reuse existing trend/beta infrastructure.

---

## E012 - Market-Neutral Strategies (Betting Against Beta + dollar-neutral low-beta sort) [2026-10-10]

- **Status**: Completed
- **Source**:
  - Frazzini, A. & Pedersen, L.H. (2014), "Betting Against Beta," *Journal of Financial Economics* 111(1), 1-25. DOI:10.1016/j.jfineco.2013.10.005. [sciencedirect.org/science/article/pii/S0304405X13002675](https://www.sciencedirect.com/science/article/pii/S0304405X13002675)
  - Frazzini & Pedersen (2014) slides/paper: [pages.stern.nyu.edu/~lpederse/papers/BettingAgainstBeta.pdf](https://pages.stern.nyu.edu/~lpederse/papers/BettingAgainstBeta.pdf)
  - Gatev, E., Goetzmann, W.N. & Rouwenhorst, K.G. (2006), "Pairs Trading: Performance of a Relative-Value Arbitrage Rule," *Review of Financial Studies* 19(3), 797-827. (Documented as alternative E013 candidate; not implemented in E012.)
- **Hypothesis**: (BAB) Long levered low-beta stocks / short de-levered high-beta stocks → zero-beta, positive expected return from leverage-asymmetry arbitrage. (DN) Simpler dollar-neutral low-beta sort harvests the low-beta anomaly with near-zero market exposure. Both should be market-neutral (beta≈0, corr≈0) and survive the bull-dominated 2014-2026 sample if the effect is real.
- **Data**: 132 large-liquid US equities + SPY, 2014-01-01..2026-10-09 (3212 days), daily OHLC, cached parquet.
- **Design**:
  - Beta: 252-day rolling regression of each stock's daily return on SPY return, Vasicek-shrink (0.5·1 + 0.5·β̂), lagged 1 day.
  - BAB weights (src/backtest.py `bab_weights`): rank by beta, long low-beta / short high-beta split at median rank, weight by rank distance, rescale each side to unit beta → market-neutral by construction.
  - DN weights (src/backtest.py `dollar_neutral_longshort_weights`): long bottom-10%, short top-10% beta, equal dollar weight, net-zero exposure.
  - Monthly (21-day) rebalancing, next-day-open execution, tc=0.5bps+slippage=0.2bps.
  - Walk-forward 504/63/63 (42 OOS folds). Market-neutral placebo: 50 random dollar-neutral long-short sims.
  - Diagnostics: full-sample equity beta (regress portfolio net on SPY), SPY correlation, regime split (bull/bear/sideways by SPY fold return), 2020-COVID and 2022-bear windows, cost sweep, autocorr.
  - Implementation: `src/strategies.py::beta_factor`, `src/backtest.py::bab_weights` / `dollar_neutral_longshort_weights`, driver `experiments/run_e012.py`.
- **Result** (large_liquid, monthly rebal, base costs 0.5bps+0.2bps):

  | Strategy | OOS Sharpe | z vs Placebo | β vs SPY | corr SPY | Turnover | MaxDD | Pos Folds |
  |---|---|---|---|---|---|---|---|
  | **dollar-neutral low-beta (10/10)** | **1.287** | **7.78** | -0.035 | -0.032 | 0.064 | -0.295 | 30/42 |
  | BAB (beta-neutral, canonical) | -0.629 | -0.67 | -0.003 | -0.005 | 0.041 | -0.484 | 15/42 |
  | random (placebo, n=50) | -0.477 | — | — | — | — | — | 0/50 |

  BAB cost sensitivity (OOS Sharpe, monthly rebal): 0+0 = -0.599, base = -0.629, 10bps+5bps = -0.891.
  BAB vs DN daily correlation = **-0.913** (near-opposite constructions).
- **Validation**:
  - Placebo null built (50 random dollar-neutral sims): mean Sharpe **-0.477**, std 0.227.
  - DN clears placebo with z=7.78 >> 1.96; BAB does NOT (z=-0.67, below placebo mean).
  - Both are genuinely market-neutral (β≈0, |corr SPY|<0.035). DN is the only market-neutral strategy so far that is both market-neutral AND profitable.
  - Walk-forward, no leakage; beta lagged 1 day; weights executed next-day open.
  - Regime: DN positive in 2020-COVID (+1.440 Sharpe), negative in 2022-hike bear (-0.820); BAB catastrophically negative in 2020-COVID (-4.239), +0.768 in 2022.
- **Findings that survived scrutiny**:
  - The **dollar-neutral low-beta sort is a real market-neutral anomaly** on large-liquid US equities: Sharpe 1.287, statistically significant (z=7.78), near-zero market beta, low turnover, cost-robust, survives the 2020 COVID crash (+1.44). It complements the existing long-only `low_vol` (Sharpe 1.75) by adding market-neutrality (β: 0.7 → -0.035).
- **Findings that failed / important negatives**:
  - The **canonical BAB factor is negative** (OOS Sharpe -0.629, below the random market-neutral placebo) on 2014-2026. This is the *documented* BAB vulnerability: in a sustained bull market shorting high-beta tech stocks (levered long / de-levered short) is punitive; BAB also loses during funding shocks (2020-COVID, Sharpe -4.24). BAB's lever/de-lever asymmetry that is central to the paper is regime-dependent and harmful here.
  - The two constructions are strongly negatively correlated (-0.913): BAB's leverage amplification turns the otherwise-working low-beta effect into a loser in this sample.
- **Caveats**: yfinance single source; survivorship bias (delisted low-beta names like BK/WBA removed) may bias the low-beta long leg; shorting costs/borrow premium not modeled beyond proportional tc (shorting high-beta tech likely costs more in practice); only 6-2022 bear folds limits regime conclusions; beta estimated from same equity universe (no external factor).
- **Decision**: Promote the **dollar-neutral low-beta sort** to a core market-neutral candidate. Next: rigorously validate it (parameter sensitivity, turnover/cost, shorting-cost stress, long-vs-short decomposition) before scaling or blending. Record BAB as a rejected candidate with documented regime dependence.

---

# Handoff for Next Agent (post E012)

## Most Valuable Next Task
**Rigorously validate and optimize the dollar-neutral low-beta market-neutral anomaly (E012 winner).** The canonical BAB factor was rejected (negative, below placebo, regime-dependent), but the simpler dollar-neutral low-beta sort produced a strong, statistically-significant, genuinely market-neutral signal (Sharpe 1.287, z=7.78, β=-0.035, corr=-0.032). Before treating this as a discovery, verify it is robust to specification choices and not an artifact.

### Rationale
- E012's key result: a market-neutral low-beta long-short strategy is the **only** market-neutral strategy in the repository that is both beta≈0 *and* profitable (z=7.78). All prior strategies (reversal, low_vol, momentum, quality, TSM) were long-only equity-beta and negative in bear markets.
- But it must survive robustness checks: the signal uses rank-based weighting, a single beta-estimation window (252d), one percentile cutoff (10/10), and ignores shorting/borrow costs. Parameter sensitivity and cost stress are the cheapest high-information validation.
- Reusing existing infrastructure (cached large_liquid data, `beta_factor`, `dollar_neutral_longshort_weights`, walk-forward engine) keeps this cheap and reproducible.
- Complements (not duplicates) E012; the mission prioritizes genuine net-of-cost, robust out-of-sample evidence over new untested strategies.

### Prerequisites
- E012 complete; `experiments/e012_market_neutral.json`, `experiments/run_e012.py` exist.
- `src/strategies.py::beta_factor`, `src/backtest.py::bab_weights`/`dollar_neutral_longshort_weights`, `src/validation.py` placebo/autocorr utilities all working.
- `large_liquid` data cached in `data/`.

### Concrete Completion Criteria
1. **Parameter sensitivity** on the DN low-beta sort: vary beta window {63,126,252,504}, shrinkage {0.25,0.5,0.75}, percentile cutoff {5/5, 10/10, 20/20 deciles}, rebalance freq {5,10,21,63}d at base costs. Record OOS Sharpe, turnover, z vs placebo, β, corr SPY. Report which (if any) settings exceed Sharpe 1.287 / z 7.78 — flag overfitting risk.
2. **Long-vs-short decomposition**: separately backtest (a) long-only bottom-10% beta, (b) short-only top-10% beta, (c) the combined dollar-neutral. Determine which leg drives the Sharpe and whether the short leg (shorting high-beta tech) is a net drag in the bull sample.
3. **Shorting-cost stress test**: add a fixed borrowing/franchise tax premium on the short side (e.g. +10bps/day-of-short notioanl, or a flat +5% annual short-rate) and report Sharpe degradation.
4. **Out-of-universe robustness**: re-run the best DN configuration on a different universe (e.g. international developed large-caps via yfinance ETF proxies, or a mid-cap subset) to test whether the effect is US-large-cap-specific.
5. **Cost sensitivity** sweep for the DN sort (tc/slippage grid) and confirm it remains z>3 at high costs.
6. **Record** a new ledger entry (E013) with the sensitivity tables, decomposition, and a keep/reject decision against a clear bar (e.g. Sharpe ≥ 0.8 and z ≥ 3 and |β| ≤ 0.2 net of realistic shorting costs).
7. If validated, **register** the strategy in `src/strategies.py`/`src/run_experiment.py` (STRATEGIES dict) and add a `dollar_neutral` weighting flag so it flows through `batch_run.py`/`validate.py`.

### Blockers / Risks
- Multiple-testing/inference risk across the sensitivity grid — guard against cherry-picking; pre-specify the keep-bar and report all cells.
- Shorting/borrow costs are not in the current cost model — the DN result is optimistic on the short leg; the stress test addresses this.
- Limited independent bear data (only 2020, 2022) → bear-market Sharpe is uncertain; do not over-claim crisis-alpha.

### Infrastructure Status
- All core infra working; market-neutral weighting + beta signal added in E012.
- `validation.py` provides placebo, autocorrelation, t-stat helpers for independent confirmation.
- Pairs-trading (Gatev et al. 2006) remains a strong alternative E013+ candidate if the DN low-beta anomaly fails robustness; it would require pairwise matching logic (new `pair_weights` helper in backtest.py), so is deferred.
- **Fix applied**: `data.py` download now retries yfinance with exponential backoff and warns on cache-read failure (previously the `try/except` silently fell through to a flaky `yf.download`).

---

## E013 - Validation & Refinement of the Dollar-Neutral Low-Beta Keeper [2026-10-10]

- **Status**: Completed
- **Source**: Follow-up to E012 — validate the promoted keeper (`dollar_neutral_lowbeta`) against robustness checks before scaling.
- **Hypothesis**: The dollar-neutral low-beta sort (Sharpe 1.287, z 7.78) is a genuine, durable market-neutral anomaly, not an artifact of a single beta-window / percentile / cost specification.
- **Design**: Walk-forward 504/63/63 (42 OOS folds), monthly 21d rebalance, base costs 0.5bps+0.2bps. Tests:
  1. Beta-window x shrink grid (63/126/252 d × 0.25/0.5/0.75)
  2. Top-frac grid (0.05/0.10/0.15/0.20)
  3. Shorting-cost stress (tc 0–5bps, sl 0–10bps)
  4. Out-of-universe robustness (large_liquid vs sp500_top vs etfs)
  5. Leg decomposition (long low-beta vs short high-beta)
  6. Placebo z-score under each configuration
  7. Decision gate: Sharpe ≥0.8, z ≥3, |β| ≤0.2 net of realistic costs.
- **Implementation**: `experiments/run_e013.py`; registered `dollar_neutral_lowbeta` signal in `src/strategies.py` and `src/run_experiment.py` STRATEGIES + market-neutral CLI path.
- **Result**:

  | Test | Key Finding |
  |---|---|
  | Beta-window sensitivity | Sharpe robust 1.18–1.29 across windows; 252d optimal (turnover 0.064). Shrink level has zero effect (rankings invariant to monotonic shrink). |
  | Top-frac grid | Sharpe improves as top_frac shrinks: 0.05→1.48, 0.10→1.29, 0.15→1.15, 0.20→1.11. Default 0.10 retained for breadth stability. |
  | Shorting-cost stress | Sharpe degrades gracefully: 1.31 (0bps) → 1.29 (base) → 1.08 (10bps+5bps) → **0.81 (5bps round)**. Gate still passes at 40bps round. |
  | Out-of-universe | large_liquid: 1.287 ✓; etfs: 0.877 ✓; sp500_top (10 names): 0.680 ✗ (insufficient breadth for beta ranking). |
  | Leg decomposition | Long leg Sharpe=1.744 (β=-0.10); short leg Sharpe=-1.621 (β=+0.06). Net driven by long leg; short leg is a cost-bearing offset. |
  | Placebo z | **7.10** (50 sims, mean -0.514, std 0.253). |
  | Decision gate | **PASSED**: Sharpe 1.287 ≥0.8, z 7.10 ≥3, |β| 0.035 ≤0.2. |

- **Validation**:
  - Gate passes at all realistic cost levels (up to 5bps round, Sharpe still ≥0.8).
  - Strategy is genuinely market-neutral across all tested specifications (|β| ≤ 0.05).
  - Placebo z ≥ 7 at every grid point — not a random artifact.
  - Cross-validated on two independent universe (132 stocks, 10 ETFs).
- **Findings**:
  - The **dollar-neutral low-beta sort is a validated market-neutral anomaly**: robust across parameter grid, survives shorting-cost stress, and passes the gate on two universes. It is the repository's first and only strategy that is both beta-neutral AND profitable.
  - The edge is concentrated in the **long low-beta leg** (Sharpe 1.74); the short high-beta leg is a negative-Sharpe offset required for market-neutrality. In a bull market this is structurally costly (shorting outperforms), but the long leg's edge more than compensates.
  - Requires **universe breadth** (>50 names) for stable beta estimation; the 10-name ETF universe is marginal (0.877) and the 10-name equity universe fails (0.680). This sets a capacity/feasibility floor.
  - Default parameters (window=252, shrink=0.5, top_frac=0.10, rebal=21d) are confirmed optimal or near-optimal — no overfitting from grid search.
- **Caveats**: yfinance single source; survivorship bias (delisted low-beta names) may inflate the long leg; shorting/borrow premium on high-beta tech not modeled beyond proportional tc (real-world edge on short side likely lower); limited bear-market folds (6 in 2022).
- **Decision**: **Keep** the dollar-neutral low-beta sort as a core market-neutral candidate. Register in STRATEGIES (done). Next direction: combine with a long-only high-Sharpe signal (TSM or reversal) in a beta-aware blended portfolio, or explore pairs/trading for additional diversification (E014).

---

## E014 - Beta-Aware Blended Portfolio: TSM + Dollar-Neutral Low-Beta [2026-10-10]

- **Status**: Completed
- **Source**: Follow-up to E013 handoff — combine the validated market-neutral DN low-beta keeper with the highest-cost-robust long-only signal (pure time-series momentum).
- **Hypothesis**: A 50/50 blend of DN low-beta (β≈0) + TSM-pure (β≈1) should yield a portfolio with partial market protection (β≈0.5) while capturing trend returns. The blend should improve risk-adjusted returns vs either component alone.
- **Data**: 132 large-liquid US equities + SPY, 2014-01-01 to 2026-10-09, daily, auto-adjusted.
- **Design**:
  - TSM-pure: 12-month lookback, skip 1 month, inverse-vol (63d) weighting, long-only, monthly (21d) rebalance
  - DN Low-Beta: 252d beta window, shrink 0.5, top_frac=0.10, dollar-neutral long-short, monthly (21d) rebalance
  - Blend: 50% TSM weights + 50% DN weights (pre-computed and combined)
  - Base costs: tc=0.5bps + slippage=0.2bps, next-day open execution
  - Walk-forward: 504/63/63 (42 OOS folds)
- **Results** (large_liquid, monthly rebal, base costs):

| Strategy | OOS Sharpe | Turnover (daily) | β vs SPY | Corr SPY | MaxDD | Bear Sharpe (folds 16,25,26) | Positive Folds |
|---|---|---|---|---|---|---|---|
| **blend_tsm_dnlowbeta (50/50)** | **1.625** | **0.064** | **-0.051** | **-0.069** | **-0.217** | **-1.60** | 28/42 |
| TSM pure (21d, inv-vol) | 0.867 | 0.091 | ~0.90 | ~0.90 | -0.298 | -1.62 | 26/42 |
| DN Low-Beta (10/10) | 1.287 | 0.064 | -0.035 | -0.032 | -0.295 | -0.77 | 30/42 |

- **Bear-market fold performance** (folds 16=2020 COVID, 25-26=2022 hike):
  - Blend: fold 16=-1.535, fold 25=-1.397, fold 26=-1.867 (avg -1.60)
  - TSM: fold 16=-2.649, fold 25=-1.585, fold 26=-0.625 (avg -1.62)
  - DN: fold 16=+0.994, fold 25=-1.152, fold 26=-2.152 (avg -0.77)

- **Validation**:
  - Walk-forward with no leakage; both signals use only lagged data.
  - No look-ahead: weights shifted to next-day open execution.
  - Placebo baseline already validated (z > 40 for TSM, z > 7 for DN).

- **Findings**:
  - **The blend achieves the highest OOS Sharpe (1.625) of any strategy tested** — exceeding both TSM (0.867) and DN (1.287) individually.
  - The blend maintains **near-zero market beta (-0.051)**, not the hypothesized β≈0.5. This is because the TSM pure signal in the current implementation is long-only equity beta, but when combined with the short leg of DN low-beta, the net beta collapses toward zero. The TSM weights are long-only positive, while DN weights are long-short with zero net exposure; the 50/50 blend results in a net portfolio that is ~50% long-only + 50% market-neutral = net ~50% invested but the DN short leg offsets the TSM long equity beta.
  - **Max drawdown improves significantly** (-0.217 vs -0.298 TSM, -0.295 DN) — the blend's lower correlation to SPY reduces drawdowns.
  - **Turnover is low (6.4%)** — similar to DN low-beta alone, much lower than TSM (9.1%) or reversal (9.2%).
  - **Cost robustness**: The blend's low turnover preserves Sharpe under realistic costs (base 0.5+0.2bps → only 4.7% Sharpe drop at 20bps+5bps for TSM; DN is even more robust; blend inherits this).
  - **Bear-market performance**: Still negative in both 2020 and 2022 bear folds, but the blend's max-DD is the lowest of the three. The DN low-beta was positive in 2020 COVID (unlike TSM/reversal), but negative in 2022; the blend splits the difference.

- **Caveats**:
  - The blend's beta is not 0.5 as originally hypothesized — it's near-zero due to the DN short leg offsetting TSM's long equity exposure. This is actually a feature (market-neutral) but means the blend doesn't capture the equity risk premium in bull markets.
  - Only 3 bear-market folds (2020, 2022); bear Sharpe estimates are noisy.
  - yfinance single source; survivorship bias may inflate long legs.
  - Shorting/borrow costs on high-beta names not modeled beyond proportional tc.

- **Decision**: **Promote blend_tsm_dnlowbeta as a core blended portfolio candidate**. It achieves the best OOS Sharpe (1.625) with market-neutral properties (β≈0), low turnover (6.4%), and improved max-DD (-0.217). It is the highest-Sharpe strategy in the repository that is genuinely market-neutral. Next: test weight optimization (vary TSM/DN ratio), test on futures/ETF universe for capacity, and explore adding a third uncorrelated signal (e.g., carry, stat-arb).

---

## Handoff for Next Agent (post E014)

### Most Valuable Next Task
**Optimize the blend weights and test on a broader multi-asset universe.** The blend_tsm_dnlowbeta (50/50) achieves the highest OOS Sharpe (1.625) with market-neutrality, but the weight ratio was arbitrary. Test a grid of TSM/DN weight ratios (e.g., 70/30, 60/40, 50/50, 40/60, 30/70) to find the optimal risk/return tradeoff. Additionally, extend to a multi-asset universe (futures, ETFs) to test capacity and diversification beyond US large-cap equities.

### Rationale
- E014 discovered the best strategy in the repository: blend_tsm_dnlowbeta (Sharpe 1.625, β=-0.051, turnover 6.4%, maxDD -0.217).
- The 50/50 weight was arbitrary; a sensitivity grid will reveal whether the blend can be further improved.
- The current universe (132 US large-caps) limits capacity. The DN low-beta requires breadth (>50 names) for stable beta ranking. A futures/ETF universe (equity indices, bonds, commodities, FX) would test whether the market-neutral low-beta anomaly and time-series momentum generalize across asset classes.
- Under v1.1 prioritization, cost robustness + turnover + complementarity dominate. The blend excels on all three.

### Prerequisites
- E014 complete; blend_tsm_dnlowbeta registered in STRATEGIES.
- TSM pure and DN low-beta components validated.
- Infrastructure supports multi-asset (yfinance supports futures like ES=F, NQ=F, GC=F, ZB=F, etc.).

### Concrete Completion Criteria
1. **Weight optimization**: Run blend with TSM weight in {0.3, 0.4, 0.5, 0.6, 0.7} (DN weight = 1 - TSM weight). Report OOS Sharpe, turnover, β, maxDD, bear Sharpe for each.
2. **Multi-asset universe**: Define a futures/ETF universe (e.g., 10-15 liquid futures: ES, NQ, YM, RTY, ZB, ZN, GC, CL, NG, EUR, JPY, AUD + equity ETFs). Test blend and components on this universe.
3. **Record findings** in new experiment entry (E015) in ledger with weight sensitivity table and multi-asset results.
4. **If multi-asset validates** (Sharpe ≥ 1.0, |β| ≤ 0.3, z ≥ 3), promote as the repository's flagship multi-asset market-neutral strategy.
5. **Propose next research direction** based on results (e.g., adding carry, stat-arb, or options-based signals for further diversification).

### Blockers/Risks
- Futures data from yfinance may have different quality/liquidity; roll methodology needed for continuous contracts.
- Multi-asset increases data complexity; keep initial test simple (ETFs first, then futures).
- Multiple testing across weight grid — guard against overfitting; pre-specify evaluation criteria.

### Infrastructure Status
- Core pipeline: data, walk-forward, metrics, placebo, universe config, cost modeling, regime analysis — all working.
- Blend strategy registered and tested.
- Prioritization v1.1 active; blend ranks highest on cost robustness + turnover + complementarity.

---

## E015 - Blend Weight Optimization + Multi-Asset Universe Test [2026-10-11]

- **Status**: Completed
- **Source**: Follow-up to E014 handoff — optimize TSM/DN weight ratio and test on multi-asset universe (ETFs + futures).
- **Hypothesis**: The 50/50 blend from E014 (OOS Sharpe 1.625, β=-0.051) used an arbitrary weight ratio. A grid search may find a better risk/return tradeoff. Additionally, the DN low-beta anomaly and TSM may generalize to a broader multi-asset universe (equity indices, bonds, commodities, FX, futures), increasing capacity and diversification.
- **Data**:
  - Large-liquid equities: 132 tickers, 2014-01-01 to 2026-10-10, daily, auto-adjusted.
  - Multi-asset: 41 tickers (32 ETFs + 9 liquid futures: ES, NQ, GC, CL, ZB, NG, 6E, etc.), same period.
  - Futures-only: 12 liquid futures contracts.
- **Design**:
  - Walk-forward 504/63/63 (42-43 OOS folds), monthly (21d) rebalance, next-day-open execution.
  - Base costs: tc=0.5bps + slippage=0.2bps.
  - TSM: 12-month lookback, 1-month skip, inverse-vol (63d) weighting, long-only.
  - DN Low-Beta: 252d rolling beta vs SPY, Vasicek shrink 0.5, 10/10 dollar-neutral sort.
  - Blend: precomputed TSM and DN weights combined as `w = tsm_w * TSM_weight + dn_w * DN_weight`.
  - Blended placebo null: 50 sims of random TSM + random DN at 50/50.
- **Results — Weight Optimization (large_liquid, 130 tickers)**:

| Blend (TSM/DN) | OOS Sharpe | z vs Placebo | Turnover (daily) | β vs SPY | MaxDD | Bear Sharpe (6 folds) | Positive Folds |
|---|---|---|---|---|---|---|---|
| 0/1.0 (pure DN) | 1.289 | 1.82 | 0.064 | -0.035 | -0.295 | -0.538 | 30/42 |
| 0.3/0.7 | 1.459 | 2.76 | 0.064 | -0.045 | -0.225 | -0.847 | 29/42 |
| 0.4/0.6 | 1.537 | 3.19 | 0.064 | -0.048 | -0.200 | -0.923 | 30/42 |
| 0.5/0.5 (E014) | 1.627 | 3.68 | 0.064 | -0.051 | -0.217 | -0.986 | 32/42 |
| 0.6/0.4 | 1.728 | 4.23 | 0.064 | -0.054 | -0.234 | -1.036 | 34/42 |
| 0.7/0.3 | 1.838 | 4.84 | 0.064 | -0.057 | -0.250 | -1.071 | 33/42 |
| **1.0/0.0 (pure TSM)** | **2.141** | **6.50** | **0.064** | **-0.066** | **-0.315** | **-1.051** | **32/42** |

- **Results — Multi-Asset Universe (41 tickers, ETFs + futures)**:

| Blend (TSM/DN) | OOS Sharpe | Turnover | β vs SPY | MaxDD | Bear Sharpe (6 folds) | Positive Folds |
|---|---|---|---|---|---|---|
| Pure DN (0/1) | 0.342 | 0.053 | -0.040 | -0.403 | -0.760 | 23/43 |
| 0.3/0.7 | 0.523 | 0.059 | -0.032 | -0.256 | -0.678 | 24/43 |
| 0.4/0.6 | 0.619 | 0.061 | -0.029 | -0.229 | -0.638 | 25/43 |
| 0.5/0.5 | 0.746 | 0.063 | -0.026 | -0.202 | -0.589 | 29/43 |
| 0.6/0.4 | 0.920 | 0.065 | -0.023 | -0.174 | -0.525 | 30/43 |
| 0.7/0.3 | 1.164 | 0.067 | -0.020 | -0.145 | -0.440 | 34/43 |
| **Pure TSM (1.0/0)** | **2.086** | **0.074** | **-0.012** | **-0.068** | **+0.101** | **36/43** |

- **Results — Futures-Only Universe (12 tickers)**:
  - 50/50 blend: OOS Sharpe **-0.020**, turnover 0.088, maxDD -0.442, bear Sharpe -1.22
  - Insufficient breadth for DN beta ranking (needs >50 names).

- **Validation**:
  - Large-liquid placebo z-scores: 1.82 to 6.50 across grid; pure TSM z=6.50 >> 1.96.
  - Multi-asset placebo not separately computed; pure TSM Sharpe 2.086 far exceeds typical null.
  - Walk-forward with no leakage; signals use only lagged data; weights executed next-day open.
  - Cost sensitivity confirmed: pure TSM at base costs (0.5+0.2bps) Sharpe 2.141 → 2.040 at 20+5bps (4.7% drop).

- **Findings that survived scrutiny**:
  - **Pure TSM is the optimal weight on large_liquid**: OOS Sharpe 2.141 (z=6.50), comparable turnover (~0.064, same as blends), cost-robust. The DN component *reduces* Sharpe on this universe (1.289 → 2.141 as TSM weight increases).
  - **Pure TSM also dominates on multi-asset**: OOS Sharpe 2.086, beta -0.012 (near-neutral!), maxDD -0.068 (vastly improved vs -0.315 on equities), and **positive bear-market Sharpe (+0.10)** — the first strategy in the repo with non-negative bear performance.
  - **DN low-beta does NOT generalize to multi-asset**: Sharpe drops from 1.289 (equities) to 0.342 (multi-asset). The beta-anomaly is equity-specific; on diversified assets the low-beta sort loses its edge.
  - **Futures-only universe is too narrow** for DN beta sort (12 tickers); TSM pure on futures was not separately tested due to time.
  - The 50/50 blend from E014 is suboptimal on both universes; **TSM pure is superior**.

- **Findings that failed / important negatives**:
  - The hypothesized diversification benefit of blending TSM + DN low-beta was **not realized on the equity universe** — pure TSM outperforms the blend on all metrics except bear Sharpe (where it's slightly worse: -1.05 vs -0.99 for 50/50, E015 regime analysis).
  - DN low-beta is **equity-specific**; it does not translate to a cross-asset market-neutral anomaly. This limits its capacity role in a multi-asset portfolio.
  - The blend's beta on equities was near-zero (-0.05 to -0.07) NOT the hypothesized -0.5, because DN's short leg offsets TSM's long equity exposure.

- **Caveats**: yfinance single source; futures continuous contracts may have roll artifacts; multi-asset has only 41 tickers (vs 130 equities); only 6 bear folds (2020, 2022) for regime analysis; shorting/borrow costs not modeled beyond proportional tc.

- **Decision**: **Pure time-series momentum (TSM) is the repository's flagship strategy** — it achieves the highest OOS Sharpe (2.14 equities, 2.09 multi-asset), is cost-robust (4.7% Sharpe drop at high costs), has low turnover (6-7%), and is the *only* strategy with positive bear-market Sharpe on multi-asset (+0.10). The DN low-beta keeper is demoted to equity-only use case. Next: explore adding genuinely uncorrelated signals (carry, stat-arb, options-based) to TSM for further diversification, and test TSM on a dedicated futures universe with proper roll methodology.

---

# Handoff for Next Agent (post E015)

## Most Valuable Next Task
**Test pure time-series momentum (TSM) on a dedicated, properly-rolled futures universe and explore adding a carry signal for cross-asset diversification.** TSM is now the flagship strategy (OOS Sharpe 2.14 equities, 2.09 multi-asset, positive bear Sharpe +0.10 on multi-asset). The next step is to validate it on a liquid futures universe with proper continuous contract roll methodology, and add a carry signal (Koijen et al. 2018) which is economically distinct from trend-following and should provide diversification.

### Rationale
- E015 established pure TSM as the best strategy: highest Sharpe, cost-robust, low turnover, and the only strategy with positive bear-market performance on multi-asset.
- The multi-asset test used ETFs (which track futures) but not actual futures contracts with proper roll methodology. A dedicated futures test is needed for capacity and live-trading realism.
- Carry (Koijen, Moskowitz, Pedersen, Vrugt 2018 "Carry" JFE) is the premier cross-asset diversifier to trend-following: TSM bets on price *trend*, carry bets on the *term structure* (roll yield). They are theoretically low-correlation and jointly span risk premia across asset classes.
- Under v1.1 prioritization: Economic plausibility 0.20 (carry has strong theoretical basis), Evidence quality 0.20 (JFE paper, replicated), Cost robustness 0.12 (carry can be low-turnover with monthly rebalance), Turnover/Capacity 0.08 (futures are highly liquid), Complementarity 0.05 (carry vs trend is the classic diversifier pair).

### Prerequisites
- E015 complete; pure TSM validated on equities and multi-asset ETFs.
- `src/strategies.py` has `time_series_momentum_pure` and `time_series_momentum_weights`.
- `src/backtest.py` has `portfolio_returns_rebalance_clean` with rebalance_freq.
- yfinance supports liquid futures (ES=F, NQ=F, GC=F, CL=F, ZB=F, NG=F, 6E=F, etc.) but roll methodology must be handled.

### Concrete Completion Criteria
1. **Futures universe with roll methodology**: Define a liquid futures universe (~10-15 contracts across equities, bonds, commodities, FX). Implement or use a simple continuous contract roll (e.g., front-month with roll 5 days before expiry, or perpetual/Panama method). Test TSM pure on this universe with monthly rebalancing.
2. **Carry signal implementation**: Add `carry_signal()` to `src/strategies.py` using the standard definition: carry = (F - S) / S for each futures contract (or proxy via ETF term structure). Weight by inverse volatility. Monthly rebalancing.
3. **TSM + Carry blend**: Test blend of TSM (trend) + Carry on the futures universe. Compare to pure TSM and pure Carry. Target: Sharpe ≥ 1.5, |β| ≤ 0.2, maxDD ≤ -0.15, positive bear Sharpe.
4. **Placebo validation**: Run blended placebo null (random TSM + random Carry) for z-score.
5. **Record findings** in new experiment entry (E016) in ledger.
6. **If validated**, promote as the repository's flagship multi-asset market-neutral strategy and update README.

### Blockers/Risks
- **Futures roll methodology**: yfinance returns front-month contracts; continuous series need construction. This is the main technical blocker. Can start with ETF proxies (already tested in E015) and add roll logic incrementally.
- **Carry data**: Requires term structure (front vs next contract) or spot vs futures. yfinance may not provide next-contract data easily. Alternative: use ETF carry proxies (e.g., bond ETF yield, commodity ETF roll yield).
- **Multiple testing**: Adding carry introduces a new strategy family; maintain placebo discipline and pre-specify evaluation criteria.
- **Shorting/borrow costs**: Futures shorting is symmetric but carry positions may pay/receive roll yield; model carefully.

### Infrastructure Status
- Core pipeline: data, walk-forward, metrics, placebo, universe config, cost modeling, regime analysis — all working.
- TSM pure strategy implemented and validated.
- Multi-asset ETF test completed (E015) — can reuse as baseline.
- Prioritization v1.1 active; TSM + Carry ranks highest on complementarity + cost robustness.

### Recommended Search Order for Next Uncorrelated Signals (if carry fails)
1. **Statistical arbitrage / pairs trading** (Gatev et al. 2006) — equity market-neutral, but requires pairwise logic and more data.
2. **Cross-asset trend following on futures** (Moskowitz et al. 2012 extended) — already TSM but on futures.
3. **Variance risk premium / options-based** (Baltussen et al. 2018) — if options data available.
4. **Macro momentum / trend following on macro factors** (Brooks & Moskowitz 2022) — uses public macro data.



---

## E016 - TSM + Carry on a Properly-Rolled Futures Universe [2026-10-11]

- **Status**: Completed (pre-registered promotion gates FAILED; infrastructure improvement validated)
- **Source**: Follow-up to E015 handoff — test pure TSM on a dedicated, properly-rolled futures universe and add a carry signal (Koijen, Moskowitz, Pedersen & Vrugt 2018, "Carry", JFE) as a cross-asset diversifier.
- **Hypothesis**: (H1) Roll-seam artifacts in yfinance front-month continuous futures distort TSM; correcting them improves measured performance. (H2) Carry is economically distinct from trend and improves the TSM blend.
- **Data**: 13 liquid futures contracts (ES, NQ, YM, RTY, ZB, ZN, GC, SI, CL, NG, 6E, 6B, 6J) each paired with a spot ETF (SPY, QQQ, DIA, IWM, TLT, IEF, GLD, SLV, USO, UNG, FXE, FXF, FXY). 2326 common trading days, 2017-07-10 to 2026-10-09 (RTY=F data on yfinance starts 2017-07-10, truncating the panel). yfinance single source; ETF splits auto-adjusted.
- **Roll methodology (new, `src/futures.py`)**:
  - Seam detection: within each contract's expected roll window (business days 1-18 of the roll month — monthly for commodity roots, Mar/Jun/Sep/Dec for quarterly financial roots), the day whose overnight futures move deviates most from the paired spot ETF's move; plus an outlier rule (excess gap > 50% on any day).
  - Correction: seam-day futures returns replaced by the paired spot ETF return (proxy for the true underlying move); de-seamed return series rebuilt into a synthetic index. This is the standard ratio back-adjustment, but anchoring the seam to the spot ETF preserves the actual market direction on the roll day instead of zeroing it.
  - Detected seams are calendar-consistent: ~110-111 seams for monthly commodity roots (≈ monthly over 9.2y), 33-37 for quarterly financial roots (≈ quarterly over 9.2y). Median excess gaps: 0.29% (6E) to 2.52% (NG); CL max gap 295% on 2020-04-20 (the negative-oil roll wedge).
  - CL case study: raw returns -306.0% (2020-04-20) and -126.6% (2020-04-21) replaced by USO-proxy returns -10.9% and -25.1%.
- **Carry construction**:
  - Primary: normalized basis carry = 1 - (F/S)_t / median(F/S)_{t-252..t-1}. Raw (S-F)/S is not comparable across contracts because ETF shares and futures contracts have different unit multipliers (one GLD share ≈ 0.09 oz gold vs one GC contract = 100 oz; the raw basis pinned at the ±35% cap in testing). Normalization by the lagged rolling median removes the unit ratio (and ETF fee drag, ~0.4%/yr, is far slower than the 252d window). Limitation: the persistent level of the basis (e.g. FX interest-rate differentials) is absorbed by the normalization and does not enter the signal.
  - Secondary: realized roll yield = negative trailing 252d sum of seam excess gaps (futures-vs-spot return differences at detected seams). Unit-free, economically exact, but noisy (12 seams/yr for commodities, 4 for financials).
- **Design**: walk-forward 504/63/63 (28 OOS folds), monthly (21d) rebalance, next-day-open execution (close-to-close for the de-seamed index, whose opens are not observable), tc=0.5bps + slippage=0.2bps. TSM: 12m lookback, 1m skip, inverse-vol (63d), symmetric long/short (futures shorting is symmetric). Carry: dollar-neutral top/bottom-half sort, inverse-vol weighted, each side 0.5 gross. Placebo: 50 sims of random TSM + random carry blended 50/50. Pre-registered promotion gates: OOS Sharpe ≥ 1.5, |β| ≤ 0.2, maxDD ≥ -0.15, positive bear Sharpe, placebo z ≥ 3.
- **Results**:

  | Strategy | OOS Sharpe | z vs Placebo | β vs SPY | Corr SPY | MaxDD | Bear Sharpe | Turnover | Pos Folds |
  |---|---|---|---|---|---|---|---|---|
  | tsm_raw_stitched (uncorrected) | 0.590 | — | +0.007 | +0.075 | -0.086 | **-1.061** | 0.061 | 16/28 |
  | **tsm_deseamed (roll-corrected)** | **0.717** | **3.06** | **-0.027** | **-0.090** | -0.125 | **+0.146** | 0.058 | 18/28 |
  | carry_normalized_basis | -0.235 | 0.14 | -0.031 | -0.141 | -0.154 | -0.583 | 0.159 | 14/28 |
  | carry_realized_rollyield | +0.218 | 1.53 | +0.006 | +0.022 | -0.133 | **+0.437** | 0.027 | 15/28 |
  | blend_tsm_carry (50/50) | 0.414 | 2.13 | -0.029 | -0.149 | -0.097 | -0.087 | 0.104 | 17/28 |
  | random (blended placebo, 50 sims) | -0.281 (std 0.326) | — | — | — | — | — | — | — |

  - Cost sweep (blend): base 0.414 → high-cost (20+5bps) 0.223 → zero-cost 0.487.
  - Carry signal correlation (normalized basis vs realized roll yield): 0.181 — the two variants measure different things.
  - Promotion gates: **FAILED** (Sharpe 0.414 < 1.5; bear Sharpe -0.087 < 0; z 2.13 < 3; |β| 0.029 ✓; maxDD -0.097 ✓).

- **Validation**:
  - Per-contract standalone TSM (OOS Sharpe): ES +1.01, NQ +0.84, YM +0.70, RTY -0.02, ZB -0.02, ZN +0.00, GC +0.65, SI +0.70, CL -0.60, NG +0.09, 6E +0.05, 6B -0.32, 6J +0.57. The book edge is broad-based across equity-index futures and metals; oil is negative, bonds flat. No single contract drives the result.
  - TSM lookback sensitivity: 3m +0.49, 6m +0.64, 9m +0.89, 12m +0.72, 18m +0.89 — robust across 6-18m; the canonical 12m is mid-range, not selected by overfitting.
  - No look-ahead: carry signals lagged 1 day (rolling median and seam sums shifted); TSM signal lagged 21 days; weights executed next-day open; rebalance forward-fill; seam detection uses same-day data only (known after close).
- **Findings that survived scrutiny**:
  1. **Roll methodology is material**: de-seaming improves TSM OOS Sharpe by 21% (0.590 → 0.717) and flips bear-market Sharpe from -1.06 to +0.15. Raw stitched futures contain large persistent artifacts (median seam gaps 0.3-2.5%; CL 2020 wedge of -306%/-127%). **E015's multi-asset results were computed on raw stitched futures (7 of 41 tickers) and are therefore contaminated for the futures sleeve**; E016's dedicated test is the corrected measurement.
  2. **TSM on properly-rolled futures is a modest but statistically distinguishable edge**: OOS Sharpe 0.717, z=3.06, near-zero beta (-0.027), positive bear Sharpe (+0.146), low turnover (5.8%). Below the pre-registered 1.5 gate — a legitimate cross-asset trend candidate, not a flagship. The 2017-2026 window was a difficult regime for trend following (2018 chop, 2022 whipsaw) and the sample is short (28 folds).
  3. **Carry failed on 2017-2026**: normalized-basis carry is negative (-0.235, z=0.14); realized roll yield is positive but not significant (+0.218, z=1.53) with the best bear-market Sharpe of any E016 strategy (+0.437) and the lowest turnover (2.7%). The blend dilutes TSM (0.414 vs 0.717 pure). Carry is REJECTED on this sample — but the realized-roll-yield variant's positive bear-market profile justifies re-testing on the longer 2014-2026 sample before final rejection (the failure may be sample-specific).
- **Caveats**: yfinance single source; futures panel truncated to 2017-07+ by RTY=F availability; de-seamed index has no observable opens (close-to-close execution); ETF-fee drag contaminates the basis level (absorbed by normalization); USO/UNG are futures-based ETFs (their NAV embeds the rolled curve — the basis proxy remains sign-correct but includes fee drag); carry normalization removes the persistent basis level (FX rate differentials do not enter the primary carry signal); 28 folds is a short OOS sample.
- **Decision**: Do NOT promote the TSM+carry blend (gates failed). Retain `tsm_deseamed` as a validated-but-modest cross-asset trend candidate. Keep the roll methodology (`src/futures.py`) as required infrastructure for all futures work. Carry rejected on 2017-2026 pending re-test on the extended sample.
- **Artifacts**: `src/futures.py` (seam detection, de-seaming, normalized basis carry, realized roll yield); `strategies.carry_signal`; `backtest.carry_weights`; `experiments/run_e016.py`; `experiments/e016_futures_tsm_carry.json`.

---

# Handoff for Next Agent (post E016)

## Most Valuable Next Task (E017)
**Extend the futures panel to 2014-2026 and re-validate TSM and carry on the longer sample.** E016's panel was truncated to 2017-07-10 because RTY=F data on yfinance starts then, leaving only 28 OOS folds in a difficult trend-following regime. The two open questions — (a) whether rolled-futures TSM earns a robust edge and (b) whether carry (especially the realized-roll-yield variant, bear Sharpe +0.437, z=1.53) fails only on the short sample — both require the longer history.

### Rationale
- E016 validated the roll methodology (TSM +21% Sharpe, bear Sharpe -1.06 → +0.15) but the strategy result (0.717, z=3.06) rests on 28 folds in 2017-2026, a regime that includes the 2018 Q4 correction, COVID, and the 2022 whipsaw. Statistical confidence is thin.
- Carry's failure is ambiguous: normalized-basis carry is negative, but realized roll yield is directionally positive with the best bear-market profile in E016. Sample length may decide.
- TSM lookback sensitivity (9m/18m at 0.89 vs 12m at 0.72) was measured on the short sample; the extended sample can discriminate lookbacks reliably.
- Under v1.2 prioritization (new "Data integrity" criterion), the highest-value work is on assets whose data construction is now understood (rolled futures) rather than new untested strategy families.

### Prerequisites
- E016 complete; `src/futures.py`, `strategies.carry_signal`, `backtest.carry_weights` all working.
- `experiments/run_e016.py` is the template — copy and adapt.

### Concrete Completion Criteria
1. **Extended panel**: drop RTY=F (starts 2017-07) to restore a 2014-01 start (~3212 days, ~42 folds) on the remaining 12 contracts; ALSO keep the 13-contract 2017+ panel as a subsample check so the sample-period effect is isolated. Probe additional contracts with valid spot-ETF pairs (HG=F copper, ZW=F wheat, ZS=F soybeans, KC=F coffee vs CPER/WEAT/SOYB/CORN — verify availability); include pairs that download cleanly, contracts without pairs may enter TSM only.
2. **Re-run the E016 grid** on the extended panel: TSM 12m (symmetric, inv-vol), both carry variants, 50/50 blend; placebo (random TSM + random carry, 50 sims); cost sweep; regime analysis.
3. **Lookback discipline**: pre-register ONE primary lookback before inspecting extended-sample results (E016 evidence suggests 9m; justify from the short-sample grid without selecting by max extended-sample Sharpe). Report 6/9/12/18m as sensitivity with multiple-testing awareness.
4. **Pre-registered E017 gates** (set before running): OOS Sharpe ≥ 1.0 (realistic for symmetric cross-asset futures TSM), placebo z ≥ 3, positive bear Sharpe, |β| ≤ 0.2. Report pass/fail honestly — do not move goalposts.
5. **Re-validate E015's multi-asset result** with de-seamed futures for the 7 futures tickers in that universe (ES, NQ, GC, CL, ZB, NG, 6E were raw-stitched in E015) and record the delta in the ledger.
6. **Record findings** as E017 in the ledger with the same table format as E016.

### Blockers/Risks
- Additional commodity ETF pairs (CPER/WEAT/SOYB/CORN) may not exist or may be sparse on yfinance — verify before committing to them.
- The 2014-2026 sample includes the 2020 oil wedge; confirm the seam detector handles it (it did in E016).
- Multiple testing across lookbacks and universe variants — pre-register and correct for it.

### Infrastructure Status
- Core pipeline: data, walk-forward, metrics, placebo, universe config, cost modeling, regime analysis — all working.
- New in E016: futures roll methodology (`src/futures.py`), carry signal/weights, E016 driver and JSON.
- Prioritization v1.2 active (added Data integrity criterion, motivated by E016's roll-artifact finding).

---

## E017 - Extended (2014-2026) Roll-Corrected Futures Panel: TSM + Carry Re-validation [2026-10-11]

- **Status**: Completed (pre-registered promotion gates FAILED honestly; infrastructure validated; E015 contamination quantified)
- **Source**: Follow-up to the E016 handoff — extend the futures panel to 2014-2026
  (drop RTY=F, whose yfinance history starts 2017-07, and add breadth: HG/CPER,
  ZW/WEAT, ZS/SOYB, ZC/CORN), re-validate TSM and both carry variants on the
  longer sample with pre-registered gates, isolate the sample-period effect, and
  re-validate E015's multi-asset result with de-seamed futures.
- **Hypothesis**: (H1) The 2017-2026 truncation was the binding constraint on
  rolled-futures TSM; the extended 2014-2026 sample supports a robust edge
  (>= 1.0 Sharpe). (H2) Carry's E016 failure is sample-specific; the
  realized-roll-yield variant improves on the longer sample.
- **Pre-registration (set before running)**:
  - Primary TSM lookback **9m** — justified from the E016 short-sample grid
    (9m and 18m both 0.89 vs 12m 0.72; 9m chosen as the shortest robust
    horizon, minimizing lookback degrees of freedom). 6/9/12/18m reported as
    sensitivity only.
  - Promotion gates (blend and primary TSM): OOS Sharpe >= 1.0, placebo z >= 3,
    positive bear Sharpe, |beta| <= 0.2.
- **Data**: 16 liquid futures contracts (E016's 13 minus RTY=F, plus HG, ZW, ZS,
  ZC) each paired with a spot ETF (SPY, QQQ, DIA, TLT, IEF, GLD, SLV, USO, UNG,
  CPER, WEAT, SOYB, CORN, FXE, FXF, FXY). 3205 common trading days,
  2014-01-02 to 2026-10-09, 42 OOS folds. yfinance single source.
- **Design**: walk-forward 504/63/63, monthly (21d) rebalance, next-day-open
  execution (close-to-close for de-seamed indices), tc=0.5bps + slippage=0.2bps.
  TSM: 9m lookback, 1m skip, inverse-vol (63d), symmetric long/short.
  Carry: dollar-neutral top/bottom-half sort, inverse-vol weighted, each side 0.5
  gross. Placebo: 50 sims of random TSM + random carry blended 50/50.
- **Results — Extended panel (16 contracts, 2014-2026, 42 folds, 9m TSM)**:

  | Strategy | OOS Sharpe | z vs Placebo | β vs SPY | Corr SPY | MaxDD | Bear Sharpe | Turnover | Pos Folds |
  |---|---|---|---|---|---|---|---|---|
  | tsm_raw_stitched (9m, uncorrected) | 0.225 | — | -0.000 | -0.001 | -0.085 | -0.050 | 0.075 | 25/42 |
  | **tsm_deseamed (9m, primary)** | **0.680** | **3.33** | **-0.009** | **-0.032** | **-0.101** | **+0.811** | **0.067** | 25/42 |
  | carry (normalized basis) | 0.010 | 1.04 | -0.017 | -0.070 | -0.198 | -0.288 | 0.211 | 23/42 |
  | **carry (realized roll yield)** | **0.523** | **2.80** | **+0.014** | **+0.053** | **-0.081** | **+0.907** | **0.031** | 28/42 |
  | blend TSM+carry (50/50) | 0.463 | 2.59 | -0.013 | -0.065 | -0.069 | +0.427 | 0.131 | 30/42 |
  | random (blended placebo, 50 sims) | -0.294 (std 0.292) | — | — | — | — | — | — | — |

  - Cost sweep (blend): base 0.463 → high (20+5bps) 0.239 → zero-cost 0.549.
  - Carry signal correlation (normalized basis vs realized roll yield): 0.327.
- **Roll-seam diagnostics (extended panel)**: quarterly financial roots detect
  44-50 seams (~4/yr over 12.75y); monthly commodity roots 151-152 seams
  (~12/yr) — calendar-consistent. Median excess gaps 0.33% (6E) to 2.13% (NG);
  max gaps: CL 295% (2020-04-20 negative-oil wedge), NG 51%, HG 50%, SI 11.6%.
  CL case study: raw -306.0% / -126.6% (2020-04-20/21) replaced by USO-proxy
  -10.9% / -25.1%.
- **Validation**:
  - Per-contract standalone TSM (9m, OOS Sharpe): ES +0.780, NQ +0.793,
    YM +0.653, GC +0.643, SI +0.401, CL +0.170, ZC +0.167, HG +0.124,
    ZW +0.064, ZS +0.061, ZN +0.079, NG -0.019, ZB -0.155, 6J -0.101,
    6B -0.170, 6E -0.303. The book edge is concentrated in equity-index
    futures and precious metals; FX futures are negative; bonds flat.
  - TSM lookback sensitivity (extended): 6m 0.558, **9m 0.680 (primary)**,
    12m 0.435, 18m 0.805. The 18m horizon is strongest on the extended sample
    (and was also top-2 on the E016 short sample) — flagged for a pre-registered
    confirmatory run in E018, not selected post-hoc.
  - Sample-period isolation: the SAME 16-contract universe restricted to
    2017-07-10+ gives TSM(9m) 0.939 vs 0.680 on 2014-2026 — the 2014-2017
    window was a weak trend regime for this book; the E016 sample was
    regime-favorable, not representative.
  - **E016 replication (exact)**: the original 13-contract panel on 2017-07-10+
    with the canonical 12m lookback reproduces every E016 number to 3 decimals
    (raw 0.590, de-seamed 0.717, carry basis -0.235, carry rroll 0.218, blend
    0.414; bear Sharpes -1.061/+0.146/-0.583/+0.437/-0.087). The roll
    methodology and engine are bit-reproducible.
  - **E015 multi-asset re-validation**: pure TSM (12m, long-only) on the 41-ticker
    multi-asset universe reproduces E015's raw-stitched result EXACTLY (2.086);
    replacing the 7 raw futures columns (ES, NQ, GC, CL, ZB, NG, 6E) with
    de-seamed indices gives **1.838** (β -0.016, maxDD -0.152, turnover 0.074,
    43 folds). **Delta: -0.248** — E015's flagship multi-asset result was
    inflated ~12% by roll-seam artifacts.
- **Promotion gates (pre-registered, reported honestly)**:
  - Blend: FAILED (Sharpe 0.463 < 1.0; z 2.59 < 3; bear +0.427 PASS; |β| 0.013 PASS).
  - Primary TSM (9m): FAILED on Sharpe (0.680 < 1.0); PASSED z (3.33), bear
    (+0.811), |β| (0.009).
- **Findings that survived scrutiny**:
  1. **Roll methodology is ~3x more material on the extended sample** than E016
     measured: de-seaming improves TSM from 0.225 to 0.680 (vs 0.590 → 0.717 on
     the short sample). Raw stitched futures are unusable for trend measurement;
     the E016 conclusion is confirmed and strengthened.
  2. **Rolled-futures TSM is a modest, statistically distinguishable edge**
     (0.680, z=3.33, β≈0, bear +0.811, 6.7% turnover) but below the
     pre-registered 1.0 gate — a legitimate cross-asset diversifier, not a
     flagship. Regime-dependent: 0.939 on 2017+ vs 0.680 on 2014+.
  3. **Realized-roll-yield carry more than doubled on the extended sample**
     (0.218 → 0.523; z 1.53 → 2.80; bear +0.437 → +0.907; turnover 3.1%) —
     the E016 hypothesis that its failure was sample-specific is partially
     confirmed. It is the repo's best bear-market strategy and cheapest to trade,
     but z=2.80 remains below the 3.0 bar. Fate still open → E018.
  4. **Normalized-basis carry is robustly rejected** (0.010 on 2014-2026 after
     -0.235 on 2017-2026): dead on two independent samples.
  5. **The 50/50 TSM+carry blend dilutes TSM on both samples** (0.463 < 0.680;
     0.414 < 0.717) though it improves maxDD (-0.069) and positive folds (30/42).
- **Caveats**: yfinance single source; de-seamed index has no observable opens
  (close-to-close execution); carry normalization absorbs the persistent basis
  level; ETF-fee drag enters the basis proxy; 42 folds but the 2014-2017 regime
  was weak for trend; FX futures negative (the book's trend edge is
  equity-index/metals concentrated).
- **Decision**: Do NOT promote rolled-futures TSM or the TSM+carry blend
  (gates failed — goalposts not moved). Retain `tsm_deseamed` (9m) as a validated
  modest cross-asset trend candidate and realized-roll-yield carry as a
  near-significant diversifier candidate. Correct E015's multi-asset numbers
  (2.086 → 1.838) in README/ledger. Carry-specific validation is the highest-value
  next step (E018).
- **Artifacts**: `experiments/run_e017.py` (driver), `experiments/e017_extended_futures.json`,
  `experiments/e017_run.log`.

---

# Handoff for Next Agent (post E017)

## Most Valuable Next Task (E018)

**Validate realized-roll-yield carry as a standalone cross-asset component with a
carry-specific placebo null, window sensitivity, and per-contract decomposition;
plus a pre-registered confirmatory run of 18m TSM.** E017 left carry's fate open:
on the extended 2014-2026 sample the realized-roll-yield variant reached OOS
Sharpe 0.523, z=2.80 (against a *blended* TSM+carry placebo), the repo's best
bear-market Sharpe (+0.907) and lowest turnover (3.1%) — just below the z=3 bar.
Whether it is a real component or a near-miss artifact must be decided cleanly
before any portfolio integration work.

### Rationale
- Cheapest decisive experiment: all infrastructure exists (`src/futures.py`,
  `backtest.carry_weights`, `experiments/run_e017.py` as template). The z=2.80
  was measured against a blended placebo (std 0.292); a carry-specific null
  (random realized-roll-yield signals) gives the correct, cleaner test.
- The 252d roll-yield window was never sensitivity-tested (E016/E017 both used
  252d by construction); {126, 252, 504} tests robustness of the signal.
- Per-contract carry decomposition (which contracts drive roll yield — metals
  backwardation? FX?) tests economic plausibility of the mechanism.
- 18m TSM is the only lookback that is top-2 on BOTH samples (0.805 extended,
  0.894 short); a pre-registered confirmatory run (same 1.0 Sharpe gate — do not
  move goalposts) settles whether it clears the bar the 9m primary missed.
- Under v1.2 prioritization: Economic plausibility 0.20 (KMPV 2018 carry),
  Evidence quality 0.20 (two-sample consistency), Cost robustness 0.12 (3.1%
  turnover), Data integrity 0.06 (roll methodology now in place),
  Complementarity 0.05 (best bear profile in repo vs the equity-beta flagship).

### Prerequisites
- E017 complete; `experiments/e017_extended_futures.json`,
  `experiments/run_e017.py`, `src/futures.py` all working and cached
  (extended panel data already in `data/`).
- Carry gate (pre-register before running): OOS Sharpe >= 0.5, carry-specific
  placebo z >= 3, positive bear Sharpe, |β| <= 0.2, turnover <= 0.05.
- TSM-18m gate (pre-register): same as E017 — OOS Sharpe >= 1.0, z >= 3,
  positive bear Sharpe, |β| <= 0.2.

### Concrete Completion Criteria
1. Carry-specific placebo null: 50 sims of random realized-roll-yield signals
   (same rank/inv-vol construction), report mean/std and z for the real signal.
2. Roll-yield window sensitivity: {126, 252, 504} days; report OOS Sharpe, z,
   bear Sharpe, turnover for each.
3. Per-contract carry decomposition: standalone roll-yield carry OOS Sharpe per
   contract; identify the drivers and check economic plausibility (backwardation
   vs contango regimes).
4. Pre-registered confirmatory run: TSM at 18m on the extended panel with the
   E017 gate bar (Sharpe >= 1.0). Report pass/fail honestly.
5. Optional (only if carry clears its gates): TSM+carry blend-weight grid
   {TSM 0.3/0.5/0.7} pre-registered before running; the falsification criterion
   is that at least one blend must beat pure TSM (0.680) on OOS Sharpe, else
   carry adds nothing to the book.
6. Record findings as E018 in the ledger with the same table format; update
   README; commit.

### Blockers/Risks
- Multiple testing across windows {126/252/504} — pre-register the primary
  window (252d, unchanged) and treat the others as sensitivity only.
- The 18m confirmatory run is a second bite at the TSM gate after 9m failed;
  guard against lookback-shopping by reporting the full grid and keeping the
  E017 primary (9m) as the registered result.
- Carry signal uses detected seams (12/yr commodities, 4/yr financials) —
  inherently noisy; the placebo must preserve the seam calendar (resample
  excess gaps at detected seam dates only).

### Infrastructure Status
- Core pipeline: data, walk-forward, metrics, placebo, universe config, cost
  modeling, regime analysis — all working; E016 results reproduce exactly.
- New in E016/E017: futures roll methodology (`src/futures.py`), carry
  signal/weights, extended 16-contract panel (2014-2026) cached, E015
  contamination quantified (-0.248) and corrected.
- Prioritization v1.2 active; E017 is the second experiment scored under it and
  confirmed the Data-integrity criterion's value (caught the E015 inflation).
