# Handoff - Next Agentic Work Session

**Timestamp:** 2026-11-25T14:36:58Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Notes for Next Session

- **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during runs and restores them afterwards. Never leave a verification run half-finished.
- **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden Baseline**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
- **Data Coverage**: `scripts/check_data_coverage.py` enforces cache coverage invariant. All data inputs must be pinned.
- **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.

## Recent Ledger Entries

- E049: Optimizer determinism fix (SLSQP status gating removed)
- E050: Exact KKT active-set enumeration for tangency solver (bit-reproducible)
- E048: Data coverage enforcement, E029/E030 fundamentals/ETF panels pinned
- E045: E029 offline-reproducible since 2026-10-20

## Next Steps Available

1. Run verification suite (`make verify-quick` / `verify-extended` / `verify-full`)
2. Review ledger for surviving strategies
3. Investigate any convention robustness issues
4. Explore new experiment ideas (pre-registration required)