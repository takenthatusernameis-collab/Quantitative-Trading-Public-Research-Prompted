# Agent Handoff — 2026-11-20T14:13:43Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min, 8 drivers + batch + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min, +18 drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# Restore goldens after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Integrity Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. Use `--restore-only` if interrupted.
- **Golden baseline** pinned in `ledger/golden_baseline.json` (SHA-256). Do not re-pin without ledger entry.
- **Data cache** pinned in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029). Coverage enforced by `scripts/check_data_coverage.py`.
- **Optimizer determinacy**: `src/portfolio_opt.py` validates on constraints, not solver status (ledger E049). E041/E042 grid artifacts drift ~1e-5 — do not re-pin.

## Current State
- No active verification run (checked: no `.verify_snapshot/ACTIVE.json`)
- All experiment drivers committed. `experiments/*.json` match HEAD.
- Ledger documents E045 (E029 offline-reproducible), E048 (cache coverage), E049 (optimizer fix).

## Next Steps (if continuing)
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Choose verification tier: `verify-quick` / `verify-extended` / `verify-full`
3. Review any drift reports in `.verify_reports/` (gitignored)
4. Update ledger if new findings

---
*Generated automatically for session continuity*