# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T00:40:34Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043)**. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Critical Integrity Notes

1. **Golden files**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them while re-running drivers and restores them afterwards. **Never leave a verification run half-finished.**

2. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are first-class steps in `scripts/check.sh`. Run `make check` before committing.

3. **Recovery**: If a verification run is interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

4. **Data cache**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant via `scripts/check_data_coverage.py`.

5. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.

## Current State

- Research phase complete (E001–E043)
- All experiment drivers in `experiments/` directory
- Verification suite in `run_all_verification.py`
- Ledger of surviving strategies in `ledger/RESEARCH_LEDGER.md`

## Next Steps for New Session

1. Run `SEED=42 make check` to verify baseline integrity
2. Run `SEED=42 make verify-quick` for quick full verification
3. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Any new experiments must follow pre-registration discipline with falsification expectations

---
*This handoff was created automatically at session start. Update as work progresses.*