# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T06:01:38Z
**Session ID**: Initial handoff for next session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

## Critical Notes for Next Session

1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up before re-running and restores them afterward.
2. **Never commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Seed**: Always use `SEED=42` for reproducibility
4. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced invariant.
5. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Current State

- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies
- Verification suite is the primary gate for any changes
- No active work in progress

---

*This handoff was created automatically at session start.*