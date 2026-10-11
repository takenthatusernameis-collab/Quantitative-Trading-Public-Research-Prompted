# E025 Task Specification: Cointegration-Based Statistical Arbitrage

## Repository State Summary (Post-E024)

**Completed Experiments**: 24 (E001–E024) with rigorous pre-registered gates, placebo validation, and honest negative recording.

**Validated Strategies** (survived all gates):
- **Equity flagship**: TSM pure (12m lookback, 1m skip, inverse-vol, long-only, monthly) — OOS Sharpe 2.141 (overnight) / 1.724 (c2c)
- **Equity market-neutral**: Dollar-neutral low-beta sort (252d beta vs SPY, 10/10 percentile, monthly) — OOS Sharpe 1.289 (overnight) / 1.053 (c2c)
- **Futures cross-asset**: TSM 18m on de-seamed panel — OOS Sharpe 0.841 (c2c); Carry (realized roll yield, 252d) — OOS Sharpe 0.472 (c2c)
- **Macro diversifier**: Macro momentum (E022) — OOS Sharpe 0.428 (overnight) / 0.006 (c2c), strong bear-market profile (+0.792)

**E024 Convention Audit Results** (completed 2026-10-11):
- FE1 (adjusted-open integrity): **PASSED** — no artifact found on ex-dividend dates
- FE2 (flagship overnight share ≥ 40%): **PASSED** — TSM flagship overnight share = 71%
- FE3 (no intraday-only Sharpe exceeds c2c by > 0.3): **PASSED**
- All equity strategies are overnight-concentrated (overnight share 42–95%)
- Futures TSM/carry have balanced intraday/overnight splits
- Convention policy recorded in `ledger/PRIORITIZATION.md` v1.2.3: primary = close-to-close, mixed-convention portfolios prohibited

**Prioritization**: v1.2.3 active (added data-integrity 0.06, execution-convention concentration screen, mandatory convention-robustness column)

---

## Why Cointegration-Based Stat-Arb is the Next Candidate

1. **E021 Distance-Method Rejection** (Gatev et al. 2006): OOS Sharpe 0.315, placebo z=0.77, 3/5 gates — honest negative on 2014-2026 large_liquid universe.

2. **v1.2.2 Lesson**: The canonical distance method failed *on this universe/sample* despite strong academic evidence (replicated in other markets/eras). The procedure now discounts evidence that is "replicated in other markets/eras only" and requires a **within-sample falsification expectation** before committing compute.

3. **E016 Search Order**: Pairs/stat-arb is the #3 candidate after cross-asset trend (E016–E019, partial) and Betting Against Beta (E012–E013, equity-only keeper). Cointegration-based methods (Engle-Granger, Johansen) are the pre-registered untested variant from the E021 handoff.

4. **Complementarity**: A genuine cointegration-based market-neutral equity strategy would be uncorrelated to TSM (trend), reversal (mean-reversion), and DN low-beta (beta anomaly) — all current equity strategies.

5. **Data Availability**: Uses existing large_liquid cached data (130 tickers, 12+ years, 42 OOS folds).

6. **Prioritization v1.2.3 Scores** (estimated):
   - Economic plausibility: 0.20 (cointegration = long-run equilibrium)
   - Evidence quality: 0.15 (academic replications exist but US 2014-2026 is untested)
   - Data availability: 0.12 (existing data)
   - Cost robustness: 0.12 (monthly rebalance, low turnover)
   - Turnover/Capacity: 0.08 (pair capacity constraints)
   - Data integrity: 0.06 (same validated equity data)
   - Complementarity: 0.05 (uncorrelated to current set)
   - **Total: ~0.78** — competitive with macro momentum (E022 scored under v1.2.2)

---

## E025 Pre-Registered Specification

### Source
- Engle, R.F. & Granger, C.W.J. (1987) "Co-integration and Error Correction: Representation, Estimation, and Testing", *Econometrica* 55(2):251-276.
- Gatev, Goetzmann & Rouwenhorst (2006) pairs framework; cointegration variant per Vidyamurthy (2004) "Pairs Trading: Quantitative Methods and Analysis".
- Quantpedia "Statistical Arbitrage" / "Cointegration Pairs Trading" entries.

### Hypothesis
Cointegration-based pair selection (Engle-Granger two-step or Johansen) identifies pairs with a stable long-run equilibrium, producing a mean-reverting spread that generates positive risk-adjusted returns after costs on the 2014-2026 large_liquid universe, with a within-sample edge detectable vs a pair-level placebo.

### Data
- Universe: large_liquid (130 tickers, 2014-01-02 to 2026-10-09, daily adjusted closes)
- Walk-forward: 504-day formation / 63-day trading / 63-day step (42 OOS folds)
- Base costs: tc=0.5bps + slippage=0.2bps
- Execution: close-to-close (primary convention per v1.2.3 policy)

### Pre-Registered Primary Configuration
- **Formation window**: 252 trading days (12 months) of log prices
- **Testing method**: Engle-Granger two-step (OLS hedge ratio + ADF test on residuals)
  - Step 1: OLS regression `log(P_a) = α + β·log(P_b) + ε` on formation window
  - Step 2: ADF test on residuals ε; select pairs with p-value < 0.05 (or top-K by ADF stat)
- **Pair selection**: Top-K=20 pairs by most negative ADF test statistic (strongest mean-reversion evidence)
- **Trading signal**: z-score of spread `s_t = log(P_a,t) - β·log(P_b,t) - α`
  - Entry: |z| ≥ 2.0
  - Exit: |z| ≤ 0.5 (or 0.0)
  - Stateful positions (hold between rebalances)
- **Weighting**: Dollar-neutral per pair (0.5 long / 0.5 short leg); inverse-vol weighted across active pairs (63-day vol window)
- **Rebalancing**: Monthly (21 days), weights executed next-day close (c2c convention)

### Pre-Registered Falsification Expectation (v1.2.2 requirement)
**FE1 (within-sample mechanism)**: On the formation window, the mean ADF test statistic across selected pairs must be significantly negative (more negative than -2.5, the 5% critical value for typical sample sizes) AND ≥ 60% of selected pairs must have ADF p-value < 0.10. If this fails, the pair-selection mechanism has no within-sample mean-reversion evidence.

**FE2 (predictive content)**: Mean per-pair |Spearman(spread z-score at formation end, next-trading-period return)| ≥ 0.03 AND ≥ 10/20 pairs show negative correlation (mean-reversion direction).

### Pre-Registered Promotion Gates
| Gate | Threshold | Notes |
|------|-----------|-------|
| G1: OOS Sharpe (c2c) | ≥ 0.8 | Market-neutral equity stat-arb target |
| G2: Placebo z (pair-level) | ≥ 3.0 | Random pair matching within universe, same stateful rule |
| G3: |β vs SPY| | ≤ 0.1 | Market-neutrality |
| G4: Bear-market Sharpe | > 0 | Crisis alpha test (regime split) |
| G5: Turnover (daily) | ≤ 0.15 | Capacity check |

### Sensitivity Grid (reported, not gated)
- Formation window: {126, 252, 378} days
- ADF threshold: p-value {0.05, 0.10, top-20 by stat}
- Top-K pairs: {10, 20, 30}
- Entry z: {1.5, 2.0, 2.5}
- Exit z: {0.0, 0.5, 1.0}
- Method: Engle-Granger vs Johansen (trace test, r=1)

---

## Implementation Requirements

### New Module: `src/cointegration.py`
```python
def find_cointegrated_pairs(
    close: pd.DataFrame,
    formation_window: int = 252,
    max_pairs: int = 20,
    method: str = "engle_granger",  # or "johansen"
    adf_threshold: float = 0.05,
    min_half_life: int = 1,
    max_half_life: int = 252,
) -> List[Tuple[str, str, float, float, float]]:
    """
    Returns list of (stock_a, stock_b, hedge_ratio, intercept, half_life)
    for pairs selected at each rebalance date.
    """
    pass

def cointegration_weights(
    close: pd.DataFrame,
    pairs: List[Tuple[str, str, float, float, float]],
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    vol_window: int = 63,
) -> pd.DataFrame:
    """
    Computes daily dollar-neutral weights for cointegrated pairs
    using z-score of spread with stateful entry/exit logic.
    """
    pass

def cointegration_placebo_weights(
    close: pd.DataFrame,
    n_pairs: int,
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    vol_window: int = 63,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Pair-level placebo: random pair matching within universe,
    identical stateful trading rule.
    """
    pass
```

### Driver: `experiments/run_e025.py`
Follow the repo pattern:
- Pre-registered gates and falsification expectations in docstring + JSON `pre_registered` block
- Walk-forward 504/63/63 with `src/backtest.py` engine
- Placebo: 50 simulations of random pair matching (pair-level null)
- Regime analysis: bull/bear/sideways by SPY fold return
- Cost sweep: {0, base, 10bps+5bps, 20bps+5bps}
- Per-pair decomposition: OOS Sharpe per selected pair
- SEED=42 for reproducibility

### Registration
- Add to `src/strategies.py` STRATEGIES dict
- Add to `src/run_experiment.py` if CLI support desired

---

## Concrete Completion Criteria

1. **Implementation**: `src/cointegration.py` with `find_cointegrated_pairs`, `cointegration_weights`, `cointegration_placebo_weights`
2. **Driver**: `experiments/run_e025.py` with pre-registered gates, falsification expectations, placebo, cost sweep, sensitivity grid
3. **Pre-registration**: Record gates, FE1, FE2 in driver docstring and JSON before running
4. **Execution**: Run on large_liquid universe (cached data), 42 OOS folds, c2c convention
5. **Results Table**: Report OOS Sharpe, placebo z, β, bear Sharpe, turnover, positive folds for primary config + sensitivity grid
6. **Falsification Report**: Report FE1 (ADF stats) and FE2 (predictive content) results
7. **Decision**: Record keep/reject against pre-registered gates in ledger (E025 entry)
8. **Artifacts**: `experiments/e025_cointegration_stat_arb.json`, `experiments/run_e025.py`, `src/cointegration.py`
9. **If validated**: Register in STRATEGIES dict, update README

---

## Blockers / Risks

| Risk | Mitigation |
|------|------------|
| Pair formation instability (cointegration sensitive to window) | Pre-register primary 252d; report full sensitivity grid |
| Delisting/survivorship breaking pairs | Drop pair if either leg missing data; log dropped pairs |
| Multiple testing across method/params | Pre-register primary; sensitivity only; no post-hoc selection |
| Shorting/borrow costs on hard-to-borrow names | Stress-test with +5bps/day short premium (measurement) |
| Capacity (top-K pairs limits diversification) | Test K={10,20,30}; report active pair count per fold |
| ADF test power on 252d window | Report half-life distribution; filter implausible (>252d) |
| Look-ahead in formation (using future data) | Strict walk-forward: formation window ends at rebalance date - 1 |

---

## Next Steps After E025

Per E024 handoff search order (if E025 fails):
1. **Equity carry / dividend-yield factor** (Koijen et al. 2018 equity-carry sleeve) — feasibility check: verify yfinance dividend history first
2. **Idiosyncratic-volatility anomaly** (Ang et al. 2006) — residual vol vs SPY; pre-register within-sample falsification (v1.2.2)
3. **Crypto cross-asset signals** (BTC-USD/ETH-USD via yfinance) — data-integrity screen first

---

## Command to Execute
```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
python3 experiments/run_e025.py
```

Expected runtime: ~2-5 minutes (pair formation + 50-sim placebo on 130 tickers × 42 folds)

---

## Handoff for Next Agent

Inspect the actual repository state before proceeding:
1. Verify `src/cointegration.py` and `experiments/run_e025.py` exist
2. Verify `ledger/PRIORITIZATION.md` is at v1.2.3+ (convention policy recorded)
3. Verify `data/` has large_liquid cached parquet
4. Verify `experiments/e024_part_a.json` and `e024_convention_audit.json` exist (audit complete)
5. Read this task spec and the E021 rejection entry to understand context
6. Execute E025 with pre-registered gates — **do not move goalposts**

The mission continues: maximize the rate of independently reproducible evidence about potentially profitable, automatable trading strategies.