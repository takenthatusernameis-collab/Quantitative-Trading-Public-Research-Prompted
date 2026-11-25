# Handoff - Next Agentic Work Session

**Timestamp**: 2026-11-25T08:21:52Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 drivers in the 5a block)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Restore golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42` for reproducibility (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages); `QUANT_RESEARCH_OFFLINE=1` enforced during verification
- **Baseline integrity**: Run `scripts/check.sh` before committing to verify golden files match HEAD (`check_goldens_clean.py` + `check_golden_baseline.py`)
- **Optimizer determinism**: `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on solver exit status (pins scipy-build-independent tangency results)

## Current Status
No active verification run. Repository is at a clean state ready for the next task. No pending code change or experiment driver in progress.

## Next Steps (suggested)
1. Run `SEED=42 bash scripts/check.sh` to confirm convention/baseline integrity.
2. If starting new work, define the pre-registered experiment (gates, falsification expectations, sensitivity grid) before executing any driver.
3. If resuming interrupted verification, run `--restore-only` first, then never leave a run half-finished.
