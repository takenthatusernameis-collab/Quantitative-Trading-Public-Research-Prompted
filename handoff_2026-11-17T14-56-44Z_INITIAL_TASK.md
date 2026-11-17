# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T14:57:35Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Individual experiments
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Key Integrity Notes

- **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up before re-running and restores after.
- **Never commit verification output** - if interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json` for offline reproducibility
- **Seed**: Always use `SEED=42` for walk-forward + placebo RNG

## Current State

No active verification run in progress. Working tree is clean relative to HEAD.