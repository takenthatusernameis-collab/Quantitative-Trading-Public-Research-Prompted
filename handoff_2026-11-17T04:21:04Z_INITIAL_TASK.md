# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T05:14:21Z
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

## Key Notes for Next Session

- **Golden artifacts**: `experiments/*.json` are canonical. Verification suite backs them up to `.verify_snapshot/` and restores after.
- **If interrupted**: Run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Never commit verification output** - restore goldens before committing
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` - must be created manually via GitHub UI
- **Optimizer determinism**: Known issue with SLSQP status 8 (ledger E049) - tangency QP is ill-conditioned
- **Dependencies**: `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Current Ledger Entries of Note

- E045: E029 offline-reproducible (fundamentals pinned)
- E048: E030 cache coverage enforced, panel committed
- E049: Optimizer determinism fixed (validator now checks constraints, not solver status); E041 still drifts numerically (133 diffs, 1-ulp ill-conditioned QP)

---
*This handoff was created automatically at session start.*