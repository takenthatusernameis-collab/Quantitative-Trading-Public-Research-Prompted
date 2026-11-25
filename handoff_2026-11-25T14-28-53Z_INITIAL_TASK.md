# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T14:30:17Z
**Session ID**: Initial handoff created for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is a quantitative trading research repository covering 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Critical Notes for Next Session

1. **Golden files**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during runs and restores afterward. Never leave a verification run half-finished.

2. **Baseline integrity**: If `scripts/check.sh` reports a golden mismatch, fix it BEFORE committing. A checkpoint commit that captures verification output silently replaces the canonical baseline.

3. **Data caching**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals are separately pinned in `data/fundamentals/`. Cache coverage is an enforced invariant.

4. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

5. **CI/Automation**: The intended CI gate cannot be created by automated agents. A maintainer must create the workflow via GitHub UI using the template at `.github/workflow-templates/verification-gate.yml`.

## Current State

- Research phase: COMPLETE (E001–E043)
- Verification suite: Ready to run
- Golden artifacts: At HEAD
- No active verification runs in progress

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment health
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Check for any pending tasks or issues in the ledger

---
*This handoff was created automatically at session initialization.*