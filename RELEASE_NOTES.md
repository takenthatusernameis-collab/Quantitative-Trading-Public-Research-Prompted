# Release Notes — Quantitative Trading Public Research

**Release**: v1.2.3 (stable repository archive)
**Date**: 2026-10-13
**Status**: Novelty search complete; portfolio-construction phase CLOSED.
**Data vintage**: large_liquid equity (130 tickers) + 16 continuous futures + SPY/IEF/GLD + 15 FRED macro series, all cached to `data/*.parquet` (gitignored) and downloaded via `yfinance`/`FRED CSV` under `start=2014-01-01`, end pinned to the committed vintage (`data/vintages.json`, `default_end_date: 2026-10-12`) whenever `SEED` is set — so the same cache keys are used regardless of the calendar date at run time.

Reproducible with `SEED=42`. Every committed artifact below was re-verified in this
session: `verify_convention_robustness.py` passes, `batch_run --universe large_liquid`,
`validate --universe large_liquid`, and `run_e042 --n-sim 50` reproduce their golden
JSONs **exactly** (modulo timestamps). See `run_all_verification.py` for the one-command
verification driver.

---

## Mission Result

Systematic, pre-registered search over the free-public-data surface
(price/dividend/volume, continuous futures, FRED macro) for walk-forward
close-to-close (c2c) anomalies on a 130-ticker large-liquid US equity universe.
**No market-neutral total portfolio survives the v1.2.3 convention-aligned gates.**
The surviving edges are standalone component strategies (table below).

---

## Surviving Strategies (Validated / Significant)

| Strategy | Experiment | OOS Sharpe (c2c) | OOS Sharpe (overnight) | β vs SPY (c2c) | β vs SPY (overnight) | Market-Neutral (c2c) | Status |
|---|---|---|---|---|---|---|---|
| **TSM Pure (Equity Flagship)** | E010/E015/E020 | **1.739** | **2.157** | -0.119 | -0.065 | No (β-bearing / overnight-concentrated) | Validated |
| **Dollar-Neutral Low-Beta Sort** | E012/E013/E041 | **1.053** | **1.287** | **+1.02** | -0.035 | **No (c2c)** / Yes (overnight) | Validated |
| **Futures TSM 18m (de-seamed)** | E017/E018 | **0.805** | balanced | -0.010 | — | Yes | Validated |
| **Futures Carry (Realized Roll Yield)** | E017/E018 | **0.523** | balanced | +0.014 | — | Yes | Near-significant (4/5) |
| **Macro Momentum (Brooks 2017)** | E022/E023 | 0.006 | **0.428** | -0.011 | — | Yes | Diversifier (3/5) |
| **Low-Vol Flagship (unlevered)** | E003/E004/E037 | **1.728** | — | +1.084 | — | No (β-bearing) | Validated edge |

**Convention policy (v1.2.3).** Primary = close-to-close; mixed-convention
portfolios prohibited; overnight (open→open) decomposition mandatory for every
new experiment. Equity strategies are overnight-concentrated (E024 audit);
DN low-beta is market-neutral only under the overnight convention (β −0.035 vs
+1.02 c2c — see the `dollar_neutral_longshort_weights` direction finding in
`experiments/run_e042.py`). Futures strategies are balanced intraday/overnight.

---

## Market-Neutral Total Portfolio: CLOSED (E042)

E042 pre-registered a walk-forward **min_variance** blend of all 5 validated
components (β cap 0.05 vs SPY and vs the equal-weight de-seamed futures index,
504/21/63, c2c, base costs, SEED=42). The committed result
(`experiments/e042_minvar_market_neutral.json`) is:

| Gate | Bar | Result | Pass |
|---|---|---|---|
| G1 OOS Sharpe (c2c) | ≥ 0.8 | **0.979** (28/38 folds) | PASS |
| G2 placebo z (β-constrained) | ≥ 3.0 | **1.95** (mean 0.750, 50 sims) | FAIL |
| G3 \|β vs SPY\| | ≤ 0.1 | **+0.094** full / **+0.068** OOS | PASS |
| G4 bear Sharpe (SPY fold < -5%) | > 0 | **+1.967** (5 bear folds) | PASS |
| G5 daily turnover | ≤ 0.15 | **0.0043** | PASS |

**Decision: PARTIAL (4/5).** Defining gates (G1 Sharpe ≥ 0.8, G3 market-neutral)
both pass, but the significance gate G2 (β-constrained placebo z 1.95 < 3.0)
fails → **not promoted**. The market-neutral-total-portfolio line is **CLOSED**:
no blend of the 5 components meets all five gates with a valid placebo.
FE1 (diversification 10/10 pairs |ρ| ≤ 0.5) and FE2 (OOS variance reduction vs
1/N, ratio 0.188 < 0.90) both pass. The E041 max-Sharpe blend was REJECTED (3/5:
G3 β 0.173 > 0.10, G2 placebo z −1.29).

> **Note on a stale README/ledger table**: an earlier transcription recorded the
> E042 *diagnostic* Dirichlet-grid overlay (n_grid=2000) numbers as the primary
> (0.799 / +1.36 / 0.0109 / β +0.114). The committed JSON (n_grid=0 primary,
> 0.979 / +1.967 / 0.0043 / β +0.094) is authoritative and reproduced exactly;
> an erratum is recorded in `ledger/RESEARCH_LEDGER.md`.

---

## Rejected Families (no surviving edge on free public data)

| Family | Representative | Reason |
|---|---|---|
| Stat-arb / pairs / cointegration | E021, E025 | OOS Sharpe ≈ placebo (z ≤ 0.8) |
| Equity carry / dividend yield | E026 | placebo z 2.997 (< 3); bear Sharpe negative |
| Idiosyncratic volatility (IVOL) | E027 | β-bearing; FE1 sign-consistency fails |
| Crypto momentum | E028 | β-bearing (0.878); fails gates |
| Fundamental factors (QMJ, accruals, PEAD, SUE) | E029, E031, E032, E033 | **DATA-INFEASIBLE** — yfinance `t.quarterly_*` returns only the trailing ~6 quarters vs ~50 required |
| Multi-asset TSM | E030, E034 | G3 β > 0.2; G4 bear Sharpe < 0 |
| Liquidity (Amihud) | E035 | G1 Sharp 0.44 < 0.8; convention-fragile |
| Realized-vol cross-section | E036 | β-bearing; FE1 sign inverted |
| Portfolio integration (low-vol + vol-scaling) | E037 | G3 β 0.51 > 0.30; G4 bear −1.79 |
| Extended macro (15 FRED) | E039 | G1 −0.53; G2 −1.35; collinear themes |
| Max-Sharpe blend (5 components) | E041 | G3 β 0.173 > 0.10; G2 placebo z −1.29; FE2 falsified |
| Min-Variance blend (confirmatory) | E042 | G2 placebo z 1.95 < 3.0 (4/5) — not promoted |

Free data sources are **exhausted**: yfinance (price/volume/dividends), FRED
(macro). Historical options, earnings-consensus, and global/international
fundamentals are not available without a paid feed.

---

## Reproduction

```bash
pip install -r requirements.txt
export SEED=42

# Fast: convention table + recorded numbers (reads JSONs only)
python3 verify_convention_robustness.py

# Baseline + placebo (offline, cached data; ~6 min)
python3 src/batch_run.py --universe large_liquid
python3 src/validate.py --universe large_liquid

# E042 confirmatory (offline; ~1 min quick / ~10 min full)
python3 experiments/run_e042.py --n-sim 2 --no-sensitivity
SEED=42 python3 experiments/run_e042.py --n-sim 50

# One-command full verification (backs up & restores golden JSONs):
python3 run_all_verification.py        # quick E042 (n_sim=2)
python3 run_all_verification.py --full # full E042 (n_sim=50) + 96-config sensitivity grid
```

`run_all_verification.py` snapshots all `experiments/*.json` to a temp dir,
runs every command, deep-compares fresh outputs to the golden commits
(excluding `timestamp` and seed/count of stochastic placebo sims), and **always
restores** the golden files — the committed baseline is left untouched.

**Reproducibility scope note:** `batch_run`/`validate`/`run_e042` derive their
`end` date from the run date via `src/data.py`. Full offline reproduction
requires the cached `data/*.parquet` vintage dated to the current UTC date
(present in this archive). Re-running on a later date will attempt a fresh
yfinance/FRED download and may shift the last few samples; pin the data vintage
or run on the archive's data date for byte-exact reproduction.

---

## Artifact Inventory

- `README.md` — full results, convention-robustness summary, E042 gate table, final status.
- `ledger/RESEARCH_LEDGER.md` — complete history E001–E042 with erratum.
- `ledger/PRIORITIZATION.md` — v1.0–v1.2.6 procedure; v1.2.6 = portfolio-construction phase.
- `E025/E041/E042_TASK_SPEC.md` — task specifications.
- `experiments/*.json` — per-experiment results (E001–E042) + `FINAL_SUMMARY.json`. Note:
  `FINAL_SUMMARY.json` is a point-in-time snapshot dated 2026-10-12 covering
  E001–E039 (39 experiments); it predates E040–E042 and is retained as a
  historical artifact. The authoritative final summary (E001–E042) is
  `README.md` (Surviving Strategies / Convention-Robustness Summary / E042 gate table),
  asserted by `verify_convention_robustness.py`.
- `experiments/run_e041.py`, `experiments/run_e042.py` — walk-forward portfolio drivers.
- `src/` — `data.py`, `backtest.py`, `strategies.py`, `portfolio_opt.py`, `batch_run.py`, `validate.py`, `validation.py`, per-asset modules.
- `verify_convention_robustness.py` — asserts every number in the convention table.
- `run_all_verification.py` — master reproduction-verification driver.
- `requirements.txt` — pinned dependencies (Python 3.12.3).

## Release follow-ups (completed this release)

- **Tag**: the final commit is tagged `v1.2.3` (this release); the
  `experiments/*.json` golden set is versioned in-repo alongside the code.
- **Data-vintage freeze**: implemented in `src/data.py` (`_resolve_end_date`,
  priority: explicit `end` > `END_DATE` env > `data/vintages.json` > `utcnow`)
  and verified — with `SEED=42` the end date resolves to `2026-10-12` from
  `data/vintages.json`, making reproduction calendar-independent.
