# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T03:09:19Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

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

1. **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores afterward — the baseline is never modified by verification.

2. **Baseline integrity**: If `scripts/check.sh` reports a golden mismatch, fix it **before** committing. A checkpoint commit that captures verification output silently replaces the canonical baseline.

3. **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG).

4. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). E029's fundamentals are separately pinned in `data/fundamentals/`.

5. **Do not commit verification output**: If a run is interrupted, restore before committing (`run_all_verification.py --restore-only`).

## Current State

- Research phase: Complete (E001–E043)
- Ledger: `ledger/RESEARCH_LEDGER.md` contains surviving validated strategies
- Verification: Ready to run with `SEED=42` prefix

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
4. Any new experiments must follow pre-registration protocol

---

*This handoff was created automatically at session start. Update as needed during work.*