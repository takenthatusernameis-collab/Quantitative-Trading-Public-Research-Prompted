# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T15:24:56Z
**Session ID**: Initial handoff created for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task

No specific task assigned. Next session should begin by verifying environment health and reviewing the research ledger for any pending follow-ups.

## Project Context

This is a quantitative trading research repository covering 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Critical Notes for Next Session

1. **Golden files**: `experiments/*.json` are canonical. Never leave a verification run half-finished.
2. **Baseline integrity**: Fix golden mismatches before committing. If `scripts/check.sh` reports a mismatch, fix before committing.
3. **Data caching**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/`.
4. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
5. **CI/Automation**: CI gate must be created by maintainer via GitHub UI.
6. **Recovery**: Interrupted runs recover via `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

## Current State

- Research phase: COMPLETE (E001–E043)
- Verification suite: Ready to run
- Golden artifacts: At HEAD
- No active verification runs in progress
- `handoff_CURRENT` symlink points to this file

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment health
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Check for any pending tasks or issues in the ledger

---
*This handoff was created automatically at session initialization.*
