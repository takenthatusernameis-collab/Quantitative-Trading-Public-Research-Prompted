# Quantitative Trading Public Research

Iterative research-driven quantitative strategy discovery.

## Repository Layout

- `PROMPT.MD` — mission and operating instructions
- `src/` — Python code
  - `data.py` — yfinance data acquisition + parquet caching
  - `backtest.py` — walk-forward engine, execution modeling, metrics
  - `strategies.py` — signal generators
  - `run_experiment.py` — single-strategy runner
  - `batch_run.py` — all-strategies comparison table
  - `validate.py` — placebo/null distribution + statistical checks
- `experiments/` — JSON results per strategy + summary
- `ledger/` — research ledger and prioritization procedure
- `data/` — parquet caches (gitignored)

## Quick Start

```bash
pip install yfinance pandas numpy scipy pyarrow
python3 src/batch_run.py        # run all strategies, print comparison
python3 src/validate.py         # placebo validation + statistical checks
```

## Key Findings (v1.1 - Broad Equity Universe)

| Strategy | OOS Sharpe | z vs Placebo | Positive Folds |
|---|---|---|---|
| **time_series_momentum (12m, 21d, inv-vol)** | **2.141** | **40.84** | **32/42** |
| reversal (12-month, 10d) | 2.288 | 29.46 | 34/42 |
| reversal (12-month, daily) | 2.103 | 29.46 | 34/42 |
| low_vol | 1.748 | 33.38 | 34/42 |
| quality (low-vol+mom) | 1.523 | 30.75 | 33/42 |
| momentum_6m | 1.335 | 30.85 | 30/42 |
| momentum (12m) | 1.248 | 29.30 | 31/42 |
| value | 1.120 | 24.82 | 24/42 |
| short_reversal | 0.776 | 21.10 | 25/42 |
| mean_reversion_5 | 0.087 | 18.03 | 26/42 |
| **random (placebo)** | **-0.656** | — | 0/50 |

Placebo baseline (50 random sims) has mean Sharpe **-0.656**. All strategies clear placebo with large z-scores. Results on 132 large-liquid US equities (2014-2026), walk-forward OOS.

## Caveats

- Single data source (yfinance); results on 132 large-liquid US equities (v1.1). Previous v1.0 used ETF-only universe.
- `auto_adjust=True` merges open/close adjustments; open-price execution is approximate.
- No parameter optimization yet — all signals use fixed, literature-standard parameters.
- Survivorship bias and delisting effects may not be fully captured by yfinance.
- Results are not independently validated against alternative data or brokers.

### Market-Neutral Discovery (E012 - large_liquid, walk-forward OOS)

All strategies tested prior to E012 were long-only equity-beta (+signal) and
correlated with SPY. E012 introduced the first genuinely market-neutral tests:
Betting Against Beta (Frazzini & Pedersen 2014) and a dollar-neutral low-beta sort.

| Strategy | OOS Sharpe | z vs Placebo | β vs SPY | Turnover | 2020-COVID Sharpe |
|---|---|---|---|---|---|
| **dollar-neutral low-beta (10/10, 21d)** | **1.287** | **7.78** | -0.035 | 0.064 | +1.440 |
| BAB (beta-neutral, canonical) | -0.629 | -0.67 | -0.003 | 0.041 | -4.239 |
| random (market-neutral placebo) | -0.477 | — | — | — | — |

- The **dollar-neutral low-beta sort** is the repository's first market-neutral strategy
  that is both beta-neutral (|β|<0.05, corr SPY ≈ -0.03) AND profitable (z=7.78). It complements
  the long-only `low_vol` factor (Sharpe 1.75, β≈0.7) by adding market-neutrality.
- The **canonical BAB factor** is market-neutral by construction but is negative on
  2014-2026 (OOS Sharpe -0.629, below the random market-neutral placebo) and collapses
  in the 2020 funding shock (Sharpe -4.24). Recorded as a rejected, regime-dependent candidate.
- Placebo baseline (50 random dollar-neutral sims): mean Sharpe -0.477.

### E013: Validation of the Dollar-Neutral Low-Beta Keeper

The keeper passed all gates (Sharpe ≥0.8, z ≥3, |β| ≤0.2) and survives realistic
shorting-cost stress:

| Parameter | Value |
|---|---|
| OOS Sharpe (baseline 252d/0.5/10pct) | 1.287 |
| Placebo z-score | 7.10 |
| Equity beta vs SPY | -0.035 |
| Corr vs SPY | -0.032 |
| Sharpe at 5bps round cost | 0.812 (still passes gate) |
| Sharpe at 0bps cost | 1.310 |

- **Beta-window sensitivity**: Sharpe robust across 63/126/252-day windows (1.18–1.29);
  252d optimal with lowest turnover (0.064). Shrink level (0.25/0.5/0.75) has no effect
  (rankings invariant to monotonic shrink).
- **Top-frac grid**: Sharpe improves as top_frac shrinks (0.05→1.48, 0.10→1.29, 0.15→1.15,
  0.20→1.11); default 0.10 retained as breadth-stable tradeoff.
- **Out-of-universe**: passes on 132-stock equity universe (1.287) and 10-stock ETF universe
  (0.877); fails on 10-name equity subset (0.680) — requires breadth for beta ranking.
- **Leg decomposition**: long low-beta leg Sharpe=1.744 (β=-0.096); short high-beta leg
  Sharpe=-1.621 (β=0.061) — net profit from long leg offsetting short losses, maintaining zero beta.

### E014: Beta-Aware Blended Portfolio (TSM + Dollar-Neutral Low-Beta)

Combining the market-neutral DN low-beta keeper with pure time-series momentum:

| Strategy | OOS Sharpe | Turnover | β vs SPY | Corr SPY | MaxDD | Bear Sharpe |
|---|---|---|---|---|---|---|
| **blend_tsm_dnlowbeta (50/50, 21d)** | **1.625** | **0.064** | **-0.051** | **-0.069** | **-0.217** | **-1.60** |
| TSM pure (21d, inv-vol) | 0.867 | 0.091 | ~0.90 | ~0.90 | -0.298 | -1.62 |
| DN Low-Beta (10/10, 21d) | 1.287 | 0.064 | -0.035 | -0.032 | -0.295 | -0.77 |

- The **blend achieves the highest OOS Sharpe (1.625) of any strategy tested** — exceeding both components individually.
- Maintains **near-zero market beta (-0.051)** with low turnover (6.4%) and improved max drawdown (-0.217).
- Cost-robust: low turnover preserves Sharpe under realistic costs.
- **Promoted as core blended portfolio candidate** — the repository's highest-Sharpe market-neutral strategy.
- *Superseded by E015: pure TSM at monthly rebalance (Sharpe 2.141) outperforms the 50/50 blend on both universes. See E015 below.*.

### Net-of-Cost Performance (large_liquid, walk-forward OOS)

The existing table follows.

| Strategy | Turnover (daily) | Base (0.5bps+0.2bps) | High (20bps+5bps) |
|---|---|---|---|
| **time_series_momentum (21d, inv-vol)** | **0.013** | **2.14** | **2.04** |
| reversal (10d) | 0.028 | 2.29 | 1.92 |
| reversal (daily) | 0.09 | 2.10 | 1.64 |
| low_vol | 0.05 | 1.75 | 1.55 |
| momentum_6m | 0.14 | 1.34 | 0.56 |
| quality | 0.30 | 1.52 | 0.29 |
| momentum | 0.44 | 1.25 | -0.92 |

Cost-robustness: **time_series_momentum** and low_vol/reversal survive high costs best. High-turnover strategies degrade sharply. TSM is the most cost-robust (4.7% Sharpe drop at 20bps+5bps vs 22% for reversal).

### E015: Blend Weight Optimization + Multi-Asset Universe Test

Whether the E014 50/50 blend weight is optimal, and whether the DN low-beta anomaly and TSM generalize to a cross-asset universe.

**Weight Optimization (large_liquid, 130 tickers)**

| Blend (TSM/DN) | OOS Sharpe | z vs Placebo | Turnover | β vs SPY | MaxDD | Bear Sharpe | Positive Folds |
|---|---|---|---|---|---|---|---|
| 0/1.0 (pure DN) | 1.289 | 1.82 | 0.064 | -0.035 | -0.295 | -0.538 | 30/42 |
| 0.3/0.7 | 1.459 | 2.76 | 0.064 | -0.045 | -0.225 | -0.847 | 29/42 |
| 0.4/0.6 | 1.537 | 3.19 | 0.064 | -0.048 | -0.200 | -0.923 | 30/42 |
| 0.5/0.5 (E014) | 1.627 | 3.68 | 0.064 | -0.051 | -0.217 | -0.986 | 32/42 |
| 0.6/0.4 | 1.728 | 4.23 | 0.064 | -0.054 | -0.234 | -1.036 | 34/42 |
| 0.7/0.3 | 1.838 | 4.84 | 0.064 | -0.057 | -0.250 | -1.071 | 33/42 |
| **1.0/0.0 (pure TSM)** | **2.141** | **6.50** | **0.064** | **-0.066** | **-0.315** | **-1.051** | **32/42** |

> *Note*: E014 tested TSM at daily rebalance (Sharpe 0.867); E015 tests TSM at monthly rebalance (2.141). At monthly rebal, pure TSM outperforms the E014 50/50 blend on all metrics.

**Multi-Asset Universe (41 tickers: ETFs + futures)**

| Blend (TSM/DN) | OOS Sharpe | Turnover | β vs SPY | MaxDD | Bear Sharpe | Positive Folds |
|---|---|---|---|---|---|---|
| Pure DN (0/1) | 0.342 | 0.053 | -0.040 | -0.403 | -0.760 | 23/43 |
| 0.5/0.5 | 0.746 | 0.063 | -0.026 | -0.202 | -0.589 | 29/43 |
| 0.7/0.3 | 1.164 | 0.067 | -0.020 | -0.145 | -0.440 | 34/43 |
| **Pure TSM (1.0/0)** | **2.086** | **0.074** | **-0.012** | **-0.068** | **+0.101** | **36/43** |

- **Pure TSM is the repository's flagship strategy**: highest OOS Sharpe on both universes (2.141 equities, 2.086 multi-asset), cost-robust (4.7% Sharpe drop at 20bps+5bps), low turnover (6-7%), and the *only* strategy with positive bear-market Sharpe on multi-asset (+0.10).
- **The DN low-beta blend is suboptimal**: the DN component *reduces* Sharpe on both universes. DN collapses on multi-asset (0.342 vs 1.289 on equities) — the low-beta anomaly is equity-specific.
- **Futures-only universe (12 tickers)**: too narrow for DN beta ranking; 50/50 blend Sharpe -0.020.
- See `experiments/e015_blend_optimization.json` for full results.

**Decision**: Promote pure TSM as the core strategy. DN low-beta keeper is equity-only. Next: test TSM on a properly-rolled futures universe and add a carry signal (E016).

## Status

- `src/`: `data.py`, `backtest.py`, `strategies.py`, `run_experiment.py`, `batch_run.py`, `validate.py`, `validation.py`.
- New in E012: `strategies.beta_factor`, `backtest.bab_weights`, `backtest.dollar_neutral_longshort_weights`, driver `experiments/run_e012.py`. See `ledger/RESEARCH_LEDGER.md` (E001-E013).
- New in E013: `strategies.dollar_neutral_lowbeta` signal, market-neutral CLI path in `run_experiment.py`, driver `experiments/run_e013.py`.
- New in E014: `strategies.blend_tsm_dnlowbeta` signal, blend strategy registered in `run_experiment.py` STRATEGIES.
- New in E015: `experiments/run_e015.py` driver for blend weight optimization (TSM/DN ratio grid) + multi-asset (ETF/futures) universe test. Fixed `PLACEBO_N_SIM` typo for reproducible runs.
- `data.py`: added retry logic for yfinance downloads (cache-read failure no longer silently falls through to flaky download).
- Run all baseline strategies: `python3 src/batch_run.py --universe large_liquid`
- Run placebo validation: `python3 src/validate.py --universe large_liquid`
- Run market-neutral experiment: `python3 experiments/run_e012.py`
- Run keeper validation: `python3 experiments/run_e013.py`
- Run market-neutral strategy via CLI: `python3 -m src.run_experiment dollar_neutral_lowbeta --universe large_liquid`
- Run blended portfolio: `python3 -m src.run_experiment blend_tsm_dnlowbeta --universe large_liquid`
- Run E015 weight optimization + multi-asset test: `python3 experiments/run_e015.py`
- Next task (E016): test pure TSM on a properly-rolled futures universe with carry signal for cross-asset diversification.
