# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T23:08:06Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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
- Always use `SEED=42` for reproducibility
- Golden files in `experiments/*.json` are canonical artifacts - verification suite backs them up and restores them
- If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` to recover
- Data cached in `data/` (gitignored except pinned vintages)
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- cvxpy/cvxopt optional; optimizer falls back to scipy.optimize

## Baseline Integrity Reminders
- `scripts/check_goldens_clean.py` compares working tree with HEAD
- `scripts/check_golden_baseline.py` compares artifacts with SHA-256 in `ledger/golden_baseline.json`
- Never re-pin as side effect of verification - only deliberate code changes recorded in ledger
- Cache coverage enforced via `scripts/check_data_coverage.py`

## Recent Status (from ledger)
- Research phase complete (E001–E043)
- E050 fix landed (exact KKT active-set enumeration) - resolved E041/E042 optimizer drift
- E029, E030 now offline-reproducible with pinned data
- All 18 extended drivers reproduce with 0 differences (2026-11-23T05:17Z measurement)