# Handoff - Next Agentic Work Session

**Timestamp**: 2026-11-25T17:17:18Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 committed drivers vs goldens)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages); offline mode `QUANT_RESEARCH_OFFLINE=1` enforced during verification
- **Baseline integrity**: Run `scripts/check.sh` before committing to verify golden files match HEAD and match `ledger/golden_baseline.json`
- **No separate linter**: run `python3 -m py_compile` on changed Python files

## Current Status
Working tree is clean on `main`. No active verification snapshot (`.verify_snapshot/` absent). Repository is at a clean state ready for next task. Recent commits are `chore(kilo): checkpoint agent session`.

## Next Task
Run `SEED=42 bash scripts/check.sh` and confirm the convention-robustness gate passes with no golden drift. If it passes, report completion. Do not commit verification output or re-pin golden files.

(End of file)
