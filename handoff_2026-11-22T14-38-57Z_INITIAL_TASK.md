# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T14:41:38Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation
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

## Current State

- All experiments (E001–E043) completed
- Verification suite operational
- Golden artifacts in `experiments/*.json` are canonical baselines
- Data cached in `data/` (gitignored except pinned vintages)
- No active verification runs in progress

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Review any open items in the ledger (E041 optimizer drift, E029/E030 pinned data)
4. Consider running verification suite to confirm reproducibility

## Important Notes

- **Never leave a verification run half-finished** — it overwrites golden artifacts and must restore them
- Use `SEED=42` for all runs (walk-forward + placebo RNG)
- If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`
- Do not commit verification output — restore goldens before committing