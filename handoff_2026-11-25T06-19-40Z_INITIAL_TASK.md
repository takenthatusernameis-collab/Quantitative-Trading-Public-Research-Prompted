# Handoff - Next Agentic Work Session

**Timestamp**: 2026-11-25T06:19:40Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD**: 04794f1e (working tree clean, no stashes)

## Initial Task
No specific task assigned for the next agentic work session. Repository is at a clean, verified state (HEAD `04794f1e`, `git status` clean, no stashes) ready for the next instruction.

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42` for reproducibility (walk-forward + placebo RNG).
- **Golden files**: `experiments/*.json` are committed artifacts - never commit verification output. A verification run must never be left half-finished.
- **Baseline integrity**: Run `scripts/check.sh` before committing to verify golden files match HEAD and `ledger/golden_baseline.json`.
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages; E029 fundamentals pinned in `data/fundamentals/`).
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification; cache coverage is an enforced invariant.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout <commit> -- experiments/<file>` where `<commit>` matches `ledger/golden_baseline.json`).

## Current Status
No active verification run. Repository is at a clean state (HEAD `04794f1e`) ready for next task.