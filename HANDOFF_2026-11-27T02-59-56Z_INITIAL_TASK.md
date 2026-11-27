# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T04:57:01Z
**Session ID**: Initial handoff for next session
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete.

**Key surviving validated strategies** are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Critical Integrity Notes

- **Never leave verification half-finished**: The suite backs up `experiments/*.json` to `.verify_snapshot/` and restores after. If killed, recover with:
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  # or
  git checkout -- experiments/
  ```

- **Golden baseline protection**: `scripts/check_golden_baseline.py` compares tracked artifacts against SHA-256 fingerprints in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.

- **Data cache coverage**: All `data.download()` call sites must have committed, SHA-256-pinned cache files per `ledger/data_baseline.json`.

## Recent Key Findings (from ledger)

- **E050 fix** (commit `72dc947`): Exact KKT active-set enumeration as primary tangency solver → bit-reproducible E041/E042 artifacts
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`)
- **E030**: Offline-reproducible since 2026-10-20 (16-ETF panel committed)
- **Optimizer determinism**: `src/portfolio_opt.py` validates on constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`)

## Next Session Suggestions

1. Run `make check` to verify current state
2. Consider running `make verify-quick` for full regression
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Any new experiments require pre-registration with falsification expectations

## Environment

- Python 3, dependencies in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- cvxpy/cvxopt optional (fallback to scipy.optimize)
- SEED=42 for all reproducibility
- Cache in `data/` (gitignored except pinned vintages)