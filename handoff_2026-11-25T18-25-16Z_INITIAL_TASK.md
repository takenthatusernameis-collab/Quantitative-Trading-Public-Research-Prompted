# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T00:41:15Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

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

- **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites and restores them. Never leave a verification run half-finished.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden Baseline**: `ledger/golden_baseline.json` pins SHA-256 fingerprints. Never re-pin as side effect of verification.
- **Data Coverage**: Cache coverage is enforced invariant. `scripts/check_data_coverage.py` validates all download call sites.
- **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.

## Current Git State

Check with: `git status`, `git log --oneline -5`

## Next Steps (if any)

[Add specific next steps here based on current work]