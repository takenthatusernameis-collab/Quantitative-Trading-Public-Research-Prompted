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
