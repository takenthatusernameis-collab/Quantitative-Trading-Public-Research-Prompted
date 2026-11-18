# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T00:37:53Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043)**. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

1. **Golden artifacts**: `experiments/*.json` are canonical research artifacts. The verification suite backs them up before re-running and restores them afterward.
2. **Never commit verification output**: If a run is interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Seed**: Always use `SEED=42` for reproducibility
4. **Data cache**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.
5. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Current State

- Research phase: **COMPLETE** (E001–E043)
- Ledger: `ledger/RESEARCH_LEDGER.md` documents surviving validated strategies
- Verification suite: Ready to run with `SEED=42`

## Next Steps (if needed)

- Run verification suite to confirm reproducibility
- Review ledger for strategy dispositions
- Check `scripts/check.sh` for any convention robustness issues