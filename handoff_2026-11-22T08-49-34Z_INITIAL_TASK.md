# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T08:49:59Z
**Session**: Initial handoff for next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current State**: Ready for verification/reproduction tasks

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Notes

1. **Always use `SEED=42`** for reproducibility
2. **Golden files**: `experiments/*.json` are canonical artifacts - verification backs them up and restores after
3. **Never commit verification output** - if interrupted, run `run_all_verification.py --restore-only` or `git checkout -- experiments/`
4. **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`
5. **Dependencies**: `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Important Conventions

- Pre-registration: Every experiment has falsification expectations and gates defined before execution
- Multiple-testing discipline: Sensitivity grids are "reported, not gated"
- Negative results recorded honestly (REJECTED / PARTIAL)
- Convention: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification suite as needed (`make verify-quick` recommended for first run)
4. Review any open items in ledger (E041 optimizer drift, E049 tangency QP ill-conditioning)