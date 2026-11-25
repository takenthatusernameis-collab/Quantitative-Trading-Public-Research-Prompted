# Agentic Work Session Handoff

**Timestamp:** 2026-11-25T16:26:08Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is a quantitative trading research repository focused on reproducible strategy research on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Reproducibility Requirements

- Always use `SEED=42` (walk-forward + placebo RNG)
- Data cached in `data/` (gitignored except pinned vintages)
- Cache coverage is enforced invariant - all inputs must be pinned
- Golden files in `experiments/*.json` are canonical artifacts

## Next Session Priorities

1. Run verification suite to confirm reproducibility
2. Check for any baseline integrity issues with `scripts/check_goldens_clean.py`
3. Review ledger for any pending strategy promotions
4. Consider extending sensitivity grids for surviving strategies

## Important Notes

- Verification suite overwrites `experiments/*.json` temporarily and restores them
- Never leave a verification run half-finished (breaks baseline integrity)
- If interrupted, recover with: `SEED=42 python3 run_all_verification.py --restore-only`
- CI gate cannot be created by automated agents (maintainer must create via GitHub UI)