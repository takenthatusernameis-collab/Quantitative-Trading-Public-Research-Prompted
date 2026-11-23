# Handoff - 2026-11-23T15:28:12Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast check (convention robustness + template validation)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full

# Restore golden artifacts after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Data cache coverage enforced via `scripts/check_data_coverage.py` (ledger E048)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Optimizer determinism fixed via exact KKT active-set (ledger E050, commit 72dc947)

## Current State
- All 8 quick drivers + 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)
- No tolerance violations remaining — do not re-pin artifacts
- CI gate template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI)

## Initial Task (next session)
- No pending task specified. Start from a clean verification check: `SEED=42 bash scripts/check.sh`.
