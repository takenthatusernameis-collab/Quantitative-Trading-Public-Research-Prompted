# Agentic Work Session Handoff

**Timestamp:** 2026-11-24T22:11:36Z
**Session:** Initial task message for next agentic work session

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Notes for Next Session
- Always use `SEED=42` for reproducibility
- Golden files in `experiments/*.json` are canonical artifacts - verification overwrites and restores them
- Data cached in `data/` (gitignored except pinned vintages)
- Convention: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Baseline Integrity Reminders
- `scripts/check_goldens_clean.py` compares working tree with HEAD
- `scripts/check_golden_baseline.py` compares with SHA-256 in `ledger/golden_baseline.json`
- Never commit verification output; restore with `run_all_verification.py --restore-only` if interrupted
- Re-pinning requires explicit `--update` flag and ledger entry

## Next Steps Available
- Run verification suite (`make verify-quick`, `make verify-extended`, `make verify-full`)
- Explore specific experiment drivers in `experiments/`
- Review surviving strategies in `ledger/RESEARCH_LEDGER.md`
- Check data coverage with `scripts/check_data_coverage.py`