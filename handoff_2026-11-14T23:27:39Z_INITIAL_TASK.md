# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T23:29:17Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

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

## Key Integrity Notes

- **Golden files**: `experiments/*.json` are canonical research artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Never commit verification output**: If a run is interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement
- **Cache coverage**: Enforced invariant — all data inputs must be pinned in `ledger/data_baseline.json`

## Current State

- Research phase complete (E001–E043)
- Validation suite operational
- No active experiment running
- Ready for next task

## Next Steps (Suggested)

1. Run `make check` to verify environment integrity
2. Run `make verify-quick` for quick validation
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Consider any new experiment ideas or validation tasks

---
*This handoff was created automatically at session start. Update with actual work performed before ending session.*