# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T01:28:36Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

3. **Golden Baseline**: `ledger/golden_baseline.json` pins SHA-256 fingerprints. Never re-pin as side effect of verification.

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.

5. **Reproducibility**: Always use `SEED=42`. Convention: close-to-close is v1.2.3 primary.

## Next Steps for New Session

- Run `SEED=42 bash scripts/check.sh` to verify environment
- Check `ledger/RESEARCH_LEDGER.md` for current strategy status
- Review any open issues or TODOs in the codebase