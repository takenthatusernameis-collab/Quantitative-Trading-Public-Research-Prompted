# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T07:08:24Z
**Session ID**: Initial handoff for next session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Critical Notes

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them while re-running and restores them afterwards. A verification run must never be left half-finished.

2. **Reproducibility**: Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention. Data is cached in `data/` (gitignored except pinned vintages).

3. **Golden Files**: Committed artifacts in `experiments/*.json` must be restored before committing if verification is interrupted (`run_all_verification.py --restore-only`).

4. **Cache Coverage**: Enforced invariant - all `data.download()` call sites must have corresponding cache files that exist, are git-tracked, and match SHA-256 in `ledger/data_baseline.json`.

## Next Steps for New Session

- Run `SEED=42 bash scripts/check.sh` to verify environment integrity
- Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
- Review any open items in the ledger (E041 optimizer drift, E049 tangency QP ill-conditioning)
- Consider running verification suite to confirm reproducibility