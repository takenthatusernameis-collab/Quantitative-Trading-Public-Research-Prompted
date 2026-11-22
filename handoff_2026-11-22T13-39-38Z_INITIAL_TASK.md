# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T13:40:58Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Notes for Next Session
- Baseline integrity: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them while re-running drivers and restores them afterwards.
- Golden files are backed up to `.verify_snapshot/` with `ACTIVE.json` marker. If a run is interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` to recover.
- Cache coverage is enforced: all data inputs must be pinned in `ledger/data_baseline.json` and tracked in git.
- Reproducibility seed: Always use `SEED=42`.
- The CI gate workflow cannot be created by automated agents; a maintainer must create it via GitHub UI using the template at `.github/workflow-templates/verification-gate.yml`.

## Current State
No active verification run detected. Repository is at a clean state ready for next task.