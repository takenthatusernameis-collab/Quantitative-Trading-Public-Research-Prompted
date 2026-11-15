# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T16:19:34Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
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

## Important Notes

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them while re-running and restores afterward. Never leave a verification run half-finished.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Golden Files**: Committed artifacts in `experiments/` must match `ledger/golden_baseline.json` SHA-256 fingerprints. Do not re-pin as side effect of verification.

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced invariant - all inputs must be pinned.

5. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

## Current Status

- Research phase: COMPLETE (E001–E043)
- Verification suite: Ready to run
- No active verification runs in progress
- Working tree clean relative to HEAD

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Choose verification level based on need:
   - `make verify` for convention robustness only
   - `make verify-quick` for 8-driver quick verification
   - `make verify-extended` for 26-driver extended verification
   - `make verify-full` for full verification with sensitivity grid
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
4. Review any open items in ledger (E045, E049 - optimizer determinism)

---
*This handoff was created automatically at session initialization.*