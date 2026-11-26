# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T20:18:09Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
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

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts — verification suite backs up and restores them
- **Never leave a verification run half-finished** — use `--restore-only` to recover if interrupted
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Cache coverage enforced via `scripts/check_data_coverage.py` — all data inputs must be pinned
- Reproducibility seed: **SEED=42** (walk-forward + placebo RNG)

## Current State
- No active verification run detected
- All golden artifacts should be at HEAD
- Ready for next task session