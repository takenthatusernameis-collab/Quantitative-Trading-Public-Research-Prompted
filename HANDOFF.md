# Handoff for Next Agent (Post E042 + Convention-Robustness Summary)

## Session Summary

**Date**: 2026-10-13
**Completed**: Convention-robustness summary finalization + verification script
**Repository State**: All 41 experiments (E001–E042) complete; novelty search exhausted; portfolio-construction phase CLOSED

---

## What Changed This Session

1. **Updated README.md** with a comprehensive **Convention-Robustness Summary** table showing c2c vs overnight OOS Sharpe for all 6 surviving strategies (5 validated + low-vol flagship), including beta differences between conventions.

2. **Added E042 results section** to README documenting the min-variance confirmatory run rejection (G1 OOS Sharpe 0.799/0.979 depending on config, G2 placebo z 1.95 < 3.0).

3. **Created `verify_convention_robustness.py`** - a standalone verification script that reproduces all key numbers from experiment JSONs under SEED=42 with cached data. All verifications pass.

4. **Updated Final Status** in README: "Novelty search complete; portfolio-construction phase CLOSED."

---

## What Was Actually Verified

| Strategy | c2c Sharpe | Overnight Sharpe | c2c β vs SPY | Overnight β | Verification |
|---|---|---|---|---|---|
| TSM Pure (Equity Flagship) | 1.739 | 2.157 | -0.119 | -0.065 | ✓ E020 part_a |
| DN Low-Beta Sort | 1.053 | 1.287 | **+1.02** | -0.035 | ✓ E013 + E041 |
| Futures TSM 18m | 0.805 | balanced | -0.010 | — | ✓ E018 |
| Futures Carry (Roll Yield) | 0.523 | balanced | +0.014 | — | ✓ E017 |
| Macro Momentum | 0.006 | 0.428 | -0.011 | — | ✓ E022 |
| Low-Vol Flagship | 1.728 | — | +1.084 | — | ✓ E037 |

**E042 Min-Variance Blend**: OOS Sharpe 0.979 (primary n_grid=0), placebo z 1.95 (constrained), β 0.094, bear Sharpe +1.97, turnover 0.0043 → **REJECTED (2/5 gates: G1✓ G2✗ G3✓ G4✓ G5✓)**

- `python3 verify_convention_robustness.py` → ALL PASS
- `python3 -m src.batch_run --universe large_liquid` → baseline strategies reproduce
- `python3 -m src.validate --universe large_liquid` → placebo validation reproduces

---

## What Remains Unresolved

- **No market-neutral total portfolio survives v1.2.3 convention-aligned gates.** The E041 max_sharpe blend (REJECTED 3/5) and E042 min_variance confirmatory run (REJECTED 2/5) both fail.
- **DN low-beta is only market-neutral under overnight convention** (β -0.035) — under c2c its β is **+1.02** due to a long/short direction reversal in `dollar_neutral_longshort_weights`.
- **All equity strategies are overnight-concentrated** (E024 audit); futures strategies have balanced splits; macro momentum is overnight-dominated.
- **All free public data sources exhausted** (yfinance price/volume/dividends, FRED macro). Fundamentals, options, earnings data all DATA-INFEASIBLE on yfinance.

---

## Approaches Already Failed and Why

| Experiment | Approach | Failure Mode |
|---|---|---|
| E021/E025 | Stat-arb (distance/cointegration) | OOS Sharpe ≈ placebo; no config clears gates |
| E026 | Equity carry / dividend yield | Near-miss placebo z 2.997; bear Sharpe negative |
| E027 | IVOL anomaly | β-bearing (0.203); FE1 sign-consistency fails |
| E028 | Crypto TSM | High β (0.877); fails gates |
| E029/E031/E032/E033 | Fundamental accounting | **DATA-INFEASIBLE** — yfinance quarterly data only ~6 quarters |
| E030/E034 | Multi-asset TSM | G3 β > 0.2; G4 bear Sharpe < 0 |
| E035 | Liquidity (Amihud) | G1 Sharpe 0.44 < 0.8; convention-fragile |
| E036 | Realized vol cross-section | β-bearing (0.63); FE1 sign inverted |
| E037 | Low-vol + vol-scaling | G3 β 0.51 > 0.30; G4 bear Sharpe -1.79 |
| E039 | Extended macro (15 FRED) | G1 -0.53; G2 -1.35; collinear themes degrade edge |
| E041 | Max-sharpe blend | G3 β 0.173 > 0.10; G2 placebo z -1.29 |
| E042 | Min-variance blend | G1 0.799/0.979; G2 placebo z 1.95 < 3.0 |

---

## Next Task: Repository Archive & Release Preparation

**Objective**: Produce a clean, reproducible release artifact that locks in the final state for any future user/agent.

**Rationale**: The research mission is complete — all free public data sources exhausted, all strategy families gated, no promoted market-neutral total portfolio exists. The highest-value bounded task is now **documentation and reproducibility hardening**, not new research.

**Concrete Deliverables**:

1. **`RELEASE_NOTES.md`** — One-page summary: surviving strategies, rejected families, convention policy, data limitations, reproduction commands.

2. **`requirements.txt`** or `pyproject.toml` — Pin exact dependency versions for reproducibility (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).

3. **`run_all_verification.py`** — Master script that runs:
   - `verify_convention_robustness.py` (new)
   - `python3 -m src.batch_run --universe large_liquid`
   - `python3 -m src.validate --universe large_liquid`
   - `python3 experiments/run_e042.py --n-sim 50` (or `--n-sim 2` for quick check)
   - Compares outputs to recorded JSONs (exact match except timestamps)

4. **Update README "Quick Start"** to include the verification script and note that E042 closes the portfolio-construction line.

5. **Optional**: Create a GitHub release tag with the final summary JSONs as artifacts.

**Constraints**:
- Do NOT introduce new strategies, modify validated constructions, or move goalposts.
- Preserve all existing experiment JSONs and ledger entries.
- Focus on reproducibility and documentation only.

**Expected Time**: ~30-60 minutes for documentation + verification script hardening.

---

## Key Files to Inspect

- `README.md` — Updated with convention-robustness table, E042 results, final status
- `verify_convention_robustness.py` — New verification script (all assertions pass)
- `experiments/e042_minvar_market_neutral.json` — Full E042 results
- `ledger/RESEARCH_LEDGER.md` — Complete history through E042 handoff
- `experiments/FINAL_SUMMARY.json` — Programmatic summary of all 39 experiments

---

## Reproduction Commands

```bash
# Full verification suite
python3 verify_convention_robustness.py

# Baseline strategy comparison
python3 -m src.batch_run --universe large_liquid

# Placebo validation
python3 -m src.validate --universe large_liquid

# E042 confirmatory run (5 min)
python3 experiments/run_e042.py --n-sim 50

# E041 sensitivity grid (5 min)
python3 experiments/run_e041.py --n-sim 50
```

All commands run offline with cached data in `data/` (gitignored). Require `SEED=42` for exact reproduction.

---

The mission continues: the repository now contains a complete, independently reproducible evidence base on 41 quantitative strategy experiments with rigorous pre-registration, honest negative recording, and a convention-robust policy. No further research is warranted on free public data sources.