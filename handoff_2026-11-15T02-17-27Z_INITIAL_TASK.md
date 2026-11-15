# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T02:21:26Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Notes for Next Session

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them while re-running and restores them afterwards. A verification run must never be left half-finished.

2. **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG).

3. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.

4. **Golden Files**: `experiments/*.json` are committed artifacts. `run_all_verification.py` backs them up before re-running and restores them afterward — the baseline is never modified by verification.

5. **Do not commit verification output**: If a run is interrupted, the working tree holds driver output instead of the goldens. Restore before committing (`run_all_verification.py --restore-only`).

## Current Status

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification suite operational with quick/extended/full modes
- CI gate template available at `.github/workflow-templates/verification-gate.yml`

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Determine if any new experiments need to be run or if verification is needed
4. Review any open items in the ledger (E041 optimizer determinism, E042 min-var confirmatory)

---

*This handoff was created automatically at session initialization.*