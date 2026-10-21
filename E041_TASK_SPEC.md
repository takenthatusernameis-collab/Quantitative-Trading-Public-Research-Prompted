# E041 Task Specification: Market-Neutral Portfolio Construction from Validated Components

## Repository State Summary (Post-E040)

**Completed Experiments**: 39 (E001–E039) + Final Summary (E040) with rigorous pre-registered gates, placebo validation, and honest negative recording.

**Validated Strategies** (survived all gates or near-significant):
1. **Equity flagship**: TSM pure (12m lookback, 1m skip, inverse-vol, long-only, monthly) — OOS Sharpe 2.141 (overnight) / 1.724 (c2c), β≈0.90
2. **Equity market-neutral**: Dollar-neutral low-beta sort (252d beta vs SPY, 10/10 percentile, monthly) — OOS Sharpe 1.289 (overnight) / 1.053 (c2c), β≈-0.035
3. **Futures cross-asset**: TSM 18m on de-seamed panel — OOS Sharpe 0.841 (c2c), β≈-0.010; Carry (realized roll yield, 252d) — OOS Sharpe 0.472 (c2c), β≈+0.014
4. **Macro diversifier**: Macro momentum (E022, 5 FRED themes × 3 assets) — OOS Sharpe 0.428 (overnight) / 0.006 (c2c), β≈-0.011, strong bear-market profile (+0.792)

**Key Finding (E040)**: No promoted strategy survives v1.2.3 convention-aligned gates as a **market-neutral total portfolio**. The surviving edges are either equity-β-bearing (TSM flagship) or standalone diversifiers with sub-threshold Sharpe.

---

## Why Market-Neutral Portfolio Construction is the Next Candidate

1. **All components exist and are validated**: 5 strategies with independent evidence, pre-registered gates passed, reproducible under SEED=42.
2. **Complementarity is documented**:
   - TSM Pure: equity trend, β≈0.9, strong bull performance
   - DN Low-Beta: equity market-neutral, β≈0, crisis alpha in 2020 (+1.44)
   - Futures TSM 18m: cross-asset trend, β≈0, positive bear Sharpe (+1.35)
   - Futures Carry: roll yield, β≈0, best bear Sharpe in repo (+0.91)
   - Macro Momentum: macro trend, β≈0, COVID +2.01, 2022 +1.87
3. **E014 tested a 50/50 TSM+DN blend**: Achieved OOS Sharpe 1.625, β=-0.051, but bear Sharpe -1.60 (FAIL G4). The blend was simplistic — equal weight, not optimized.
4. **E037 tested Low-Vol + Vol-Scaling**: OOS Sharpe 1.556 but β=0.512 (FAIL G3), bear Sharpe -1.79 (FAIL G4).
5. **Gap**: No walk-forward portfolio optimization targeting market-neutrality + positive bear Sharpe has been attempted with the full validated set.

---

## E041 Pre-Registered Specification

### Source
- Portfolio construction literature: Brandao-Marques et al. (2023) "Portfolio Construction with Many Assets" (walk-forward optimization); DeMiguel et al. (2009) "Optimal Versus Naive Diversification" (1/N benchmark).
- Internal: Validated components from E010, E013, E018, E017, E022.

### Hypothesis
A walk-forward optimized blend of the 5 validated strategies can achieve **market-neutrality (|β| ≤ 0.1)** while maintaining **OOS Sharpe ≥ 0.8 (c2c)**, **placebo z ≥ 3.0**, **bear-market Sharpe > 0**, and **turnover ≤ 0.15** on the combined equity+futures+macro universe.

### Data
- **Equity leg**: large_liquid (130 tickers, 2014-2026, daily adjusted closes)
- **Futures leg**: 16-contract de-seamed panel (2014-2026, daily)
- **Macro leg**: SPY/IEF/GLD + 5 FRED themes (2014-2026, monthly)
- **Walk-forward**: 504-day formation / 63-day trading / 63-day step (42 OOS folds)
- **Base costs**: tc=0.5bps + slippage=0.2bps (equity); tc=1.0bps + slippage=0.5bps (futures)
- **Execution**: close-to-close (primary convention per v1.2.3 policy)

### Pre-Registered Primary Configuration

**Component weight series (pre-computed, deterministic, SEED=42):**
1. `w_tsm_pure`: from `src.trend.time_series_momentum_weights` (12m, 1m skip, inv-vol, long-only, 21d rebal)
2. `w_dn_lowbeta`: from `src.backtest.dollar_neutral_longshort_weights` (252d beta, shrink 0.5, 10/10, inv-vol, 21d rebal)
3. `w_futures_tsm`: from `src.futures.futures_tsm_weights` (18m, 1m skip, inv-vol, sym L/S, 21d rebal, de-seamed panel)
4. `w_futures_carry`: from `src.futures.futures_carry_weights` (252d realized roll yield, inv-vol, 21d rebal, de-seamed panel)
5. `w_macro_momentum`: from `src.macro.macro_momentum_weights` (5 themes × 3 assets, 6m mom, 60m z-score, 1m lag, 21d rebal)

**Portfolio optimization (walk-forward, within each fold):**
- **Objective**: Maximize in-sample Sharpe (c2c) subject to |β_equity| ≤ 0.1 and |β_futures| ≤ 0.1 vs respective benchmarks (SPY for equity, equal-weight futures index for futures)
- **Constraints**: Long-only weights on components (no shorting components), sum(weights) = 1.0
- **Covariance**: Ledoit-Wolf shrinkage on 504-day component returns (available at formation end)
- **Optimization**: Quadratic programming (cvxopt or scipy.optimize.minimize) — if solver unavailable, fall back to grid search over simplex
- **Rebalancing**: Monthly (21d), weights executed next-day close (c2c convention)

### Pre-Registered Falsification Expectation (v1.2.2 requirement)

**FE1 (within-sample diversification)**: On the formation window, the 5 component return streams must have pairwise correlations ≤ 0.5 in absolute value for ≥ 80% of pairs. If components are highly correlated, diversification cannot work.

**FE2 (predictive content of optimization)**: The optimized portfolio's in-sample Sharpe (c2c) on the formation window must exceed the equal-weight (1/N) portfolio's in-sample Sharpe by ≥ 0.2. If optimization adds no value, it is overfitting.

### Pre-Registered Promotion Gates

| Gate | Threshold | Notes |
|------|-----------|-------|
| G1: OOS Sharpe (c2c) | ≥ 0.8 | Market-neutral total portfolio target |
| G2: Placebo z (component-permutation) | ≥ 3.0 | 50 sims: randomize component weights per fold, same optimization |
| G3: \|β vs SPY\| | ≤ 0.1 | Market-neutrality (equity beta) |
| G4: Bear-market Sharpe | > 0 | Crisis alpha test (folds where SPY fold return < -5%) |
| G5: Turnover (daily) | ≤ 0.15 | Capacity check |

### Sensitivity Grid (reported, not gated)
- Optimization objective: Max Sharpe vs Min Variance vs Risk Parity (inv-vol on components)
- Beta constraint: {0.05, 0.1, 0.15, 0.2}
- Rebalance frequency: {21d, 63d}
- Component set: {all 5, equity-only (2), futures-only (2), macro-inclusive (3)}

---

## Implementation Requirements

### New Module: `src/portfolio_opt.py`
```python
def optimize_portfolio_weights(
    component_returns: pd.DataFrame,  # (T, 5) component returns on formation window
    beta_constraint: float = 0.1,
    benchmark_returns: pd.Series = None,  # SPY returns for equity beta
    method: str = "max_sharpe",  # or "min_var", "risk_parity"
) -> np.ndarray:
    """
    Returns (5,) weight vector summing to 1.0, non-negative.
    Uses Ledoit-Wolf covariance on component_returns.
    """
    pass

def walk_forward_blend_weights(
    close_equity: pd.DataFrame,
    close_futures: pd.DataFrame,
    macro_signals: pd.DataFrame,  # or close_macro
    formation_window: int = 504,
    rebalance_freq: int = 21,
    beta_constraint: float = 0.1,
) -> pd.DataFrame:
    """
    Computes daily target weights for the blended portfolio.
    At each rebalance date: takes most recent formation window of component returns,
    runs optimization, returns component weights. Then expands to asset-level weights
    using pre-computed component weight series.
    """
    pass

def portfolio_placebo_weights(
    component_weight_series: List[pd.DataFrame],
    n_simulations: int = 50,
    seed: int = 42,
) -> List[pd.DataFrame]:
    """
    Component-level placebo: randomize component weights per fold
    (sample from Dirichlet(1)), apply same walk-forward optimization structure.
    """
    pass
```

### Driver: `experiments/run_e041.py`
Follow repo pattern:
- Pre-registered gates and falsification expectations in docstring + JSON `pre_registered` block
- Walk-forward 504/63/63 with `src/backtest.py` engine
- Placebo: 50 simulations of component-weight permutation (component-level null)
- Regime analysis: bull/bear/sideways by SPY fold return
- Cost sweep: {0, base, 10bps+5bps, 20bps+5bps} per asset class
- Component attribution: OOS Sharpe, beta, turnover per component
- SEED=42 for reproducibility

### Registration
- Add to `src/strategies.py` STRATEGIES dict as `market_neutral_blend`
- Add to `src/run_experiment.py` if CLI support desired

---

## Concrete Completion Criteria

1. **Implementation**: `src/portfolio_opt.py` with `optimize_portfolio_weights`, `walk_forward_blend_weights`, `portfolio_placebo_weights`
2. **Driver**: `experiments/run_e041.py` with pre-registered gates, falsification expectations, placebo, cost sweep, sensitivity grid
3. **Pre-registration**: Record gates, FE1, FE2 in driver docstring and JSON before running
4. **Execution**: Run on combined universes (cached data), 42 OOS folds, c2c convention
5. **Results Table**: Report OOS Sharpe, placebo z, β, bear Sharpe, turnover, positive folds for primary config + sensitivity grid
6. **Falsification Report**: Report FE1 (component correlations) and FE2 (optimization value-add) results
7. **Decision**: Record keep/reject against pre-registered gates in ledger (E041 entry)
8. **Artifacts**: `experiments/e041_market_neutral_portfolio.json`, `experiments/run_e041.py`, `src/portfolio_opt.py`
9. **If validated**: Register in STRATEGIES dict, update README

---

## Blockers / Risks

| Risk | Mitigation |
|------|------------|
| Component returns have different frequencies (daily equity/futures vs monthly macro) | Resample all to daily frequency using forward-fill for macro; macro weights held constant intra-month |
| Optimization instability (ill-conditioned covariance) | Ledoit-Wolf shrinkage; ridge regularization (λ=1e-4); fallback to equal-weight if solver fails |
| Look-ahead in component returns (using future data) | Strict walk-forward: formation window ends at rebalance date; component returns use only data through formation end |
| Multiple testing across optimization methods | Pre-register primary (max_sharpe); sensitivity only; no post-hoc selection |
| Macro component has monthly rebalance vs daily others | Align rebalance dates to monthly (21d); macro weights constant between macro rebalances |
| Futures de-seaming required | Use existing `src.futures` de-seamed panel (validated in E016-E018) |

---

## Next Steps After E041

Per E040 close-out audit, if E041 fails:
1. **Out-of-sample validation on 2024-2026 only** — test surviving strategies on truly unseen period
2. **Parameter stability analysis** — systematic sensitivity on all validated strategies' key parameters
3. **Capacity/shorting cost stress tests** — realistic borrowing costs, slippage models, position limits
4. **Production readiness** — execution simulation (VWAP/TWAP), latency, operational risk

---

## Command to Execute

```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
python3 experiments/run_e041.py
```

Expected runtime: ~5-10 minutes (5 component weight series + walk-forward optimization × 42 folds + 50-sim placebo)

---

## Handoff for Next Agent

Inspect the actual repository state before proceeding:
1. Verify `src/portfolio_opt.py` and `experiments/run_e041.py` exist
2. Verify all 5 component weight functions exist and are callable: `time_series_momentum_weights`, `dollar_neutral_longshort_weights`, `futures_tsm_weights`, `futures_carry_weights`, `macro_momentum_weights`
3. Verify `ledger/PRIORITIZATION.md` is at v1.2.5+ (convention policy locked)
4. Verify `data/` has large_liquid cached parquet, de-seamed futures panel, SPY/IEF/GLD, FRED series
5. Verify `experiments/FINAL_SUMMARY.json` exists (close-out complete)
6. Read this task spec and the E040 final summary to understand context
7. Execute E041 with pre-registered gates — **do not move goalposts**

The mission continues: maximize the rate of independently reproducible evidence about potentially profitable, automatable trading strategies.