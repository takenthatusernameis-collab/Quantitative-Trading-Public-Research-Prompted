# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T11:06:42Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043)**. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Critical Notes

1. **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
2. **Golden files**: `experiments/*.json` are canonical research artifacts - never commit verification output
3. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.
4. **Verification**: `run_all_verification.py` backs up goldens before re-running and restores them afterward
5. **If interrupted**: Run `SEED=42 python3 run_all_verification.py --restore-only` to recover golden artifacts

## Current State

- Research phase complete (E001–E043)
- Verification suite operational
- Ledger documents surviving validated strategies
- No active verification run in progress

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification if needed: `SEED=42 python3 run_all_verification.py`
4. Any new experiments must follow pre-registration protocol with falsification expectations