# Agent Handoff — 2026-11-21T04:03:34Z

## Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast check (convention robustness + template validation)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites then restores them.
- **Never leave verification half-finished** — use `--restore-only` to recover if interrupted.
- **Seed**: Always `SEED=42` for reproducibility.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Offline mode enforced via `QUANT_RESEARCH_OFFLINE=1`.
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` — must be created manually via GitHub UI.

## Current State
No active verification run. Repository is at a clean baseline ready for next task.