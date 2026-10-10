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

### Net-of-Cost Performance (large_liquid, walk-forward OOS)

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
