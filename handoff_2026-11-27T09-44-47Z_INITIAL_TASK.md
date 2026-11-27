# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T09:49:55Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. Never leave a verification run half-finished.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Golden Baseline**: Compare artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json` using `scripts/check_golden_baseline.py`

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced invariant.

5. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

## Current State

- Research phase complete (E001–E043)
- Ledger documents surviving validated strategies
- Verification suite operational
- No active experiment running

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Consider running `verify-quick` if baseline verification needed
4. Review any open issues or planned experiments

---

*This handoff was created automatically at session initialization.*