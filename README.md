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

## Key Findings (v1.0)

| Strategy | OOS Sharpe | z vs Placebo | Positive Folds |
|---|---|---|---|
| reversal (12-month) | 1.337 | 16.97 | 32/42 |
| low_vol | 1.245 | 16.18 | 27/42 |
| momentum_6m | 1.123 | 15.15 | 28/42 |
| value | 1.090 | 14.87 | 21/42 |
| short_reversal | 0.972 | 13.86 | 29/42 |
| momentum (12m) | 0.848 | 12.81 | 30/42 |
| quality (low-vol+mom) | 0.387 (IS) | — | — |
| mean_reversion_5 | 0.489 | 9.75 | 24/42 |
| **random (placebo)** | **-0.656** | — | 0/50 |

Placebo baseline (50 random sims) has mean Sharpe **-0.656** — costs destroy noise.
All real strategies clear the placebo with large z-scores, suggesting genuine signal.

## Caveats

- Single data source (yfinance), ETF universe only — not a representative cross-section.
- `auto_adjust=True` merges open/close adjustments; open-price execution is approximate.
- No parameter optimization yet — all signals use fixed, literature-standard parameters.
- Results are not independently validated against alternative data or brokers.