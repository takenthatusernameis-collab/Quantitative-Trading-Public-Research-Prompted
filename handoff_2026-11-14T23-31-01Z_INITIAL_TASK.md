# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T23:31:51Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

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

## Key Notes for Next Session

- **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite overwrites them during runs and restores afterward — never leave a verification run half-finished.
- **Recovery**: If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Seed**: Always use `SEED=42` for reproducibility
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced invariant.
- **CI**: Cannot be created by automated agents — maintainer must create via GitHub UI using template at `.github/workflow-templates/verification-gate.yml`

## Active Items from Ledger

- E041 drift (133 numeric differences) — optimizer QP ill-conditioned, do not re-pin
- E042 grid artifacts still drift by 29-133 differences — open item
- Convention: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside

---
*This handoff was created automatically at session start.*