# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T21:56:36Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Key Notes for Next Session
- Baseline integrity: `experiments/*.json` are canonical artifacts; verification overwrites and restores them
- Seed: Always use `SEED=42` for reproducibility
- Data: Cached parquet in `data/` (gitignored except pinned vintages)
- Convention: Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Verification Suite Status
- `verify-quick`: Re-executes 8 drivers in 5a block
- `verify-extended`: Adds 18 more committed drivers with structural match
- `verify-full`: E042 n_sim=50 + 96-config sensitivity grid
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

## Last Known State
- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies
- Verification suite operational with convention robustness checks