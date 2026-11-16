# Agentic Work Session Handoff

**Timestamp:** 2026-11-16T22:03:06Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

## Important Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up before re-running and restores afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Never commit verification output** — if a run is interrupted, restore with `run_all_verification.py --restore-only`

## Current State

No active verification run in progress. The working tree is clean and ready for the next session.

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment and conventions
2. Check `ledger/RESEARCH_LEDGER.md` for current experiment statuses
3. Review any open items in the ledger (e.g., E041/E042 optimizer determinism)
4. Proceed with desired verification level or individual experiment runs

---
*Generated automatically for session handoff*
