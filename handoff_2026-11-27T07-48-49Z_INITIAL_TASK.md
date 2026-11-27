# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T08:45:43Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward.
- **Do not commit verification output**: If a run is interrupted, restore before committing (`run_all_verification.py --restore-only`).
- **Baseline integrity**: See AGENTS.md for details on `.verify_snapshot/` recovery and golden baseline pinning.

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment and baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current research status
3. Review any open tasks or experiments that need attention