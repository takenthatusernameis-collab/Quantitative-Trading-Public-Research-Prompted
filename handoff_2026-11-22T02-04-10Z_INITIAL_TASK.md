# Agent Handoff — 2026-11-22T02:05:39Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min + 50 sims)
SEED=42 python3 run_all_verification.py --full
```

## Critical Integrity Notes
- `experiments/*.json` are canonical golden artifacts — verification overwrites then restores them
- **Never leave a verification run half-finished** — use `--restore-only` to recover if interrupted
- Golden baseline pinned in `ledger/golden_baseline.json` (SHA-256 fingerprints)
- Data cache coverage enforced via `scripts/check_data_coverage.py` — all inputs must be pinned

## Open Items (from Ledger)
- E041: 133 numeric diffs remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- E042: Grid artifacts drift 29-133 diffs — do not re-pin
- CI workflow template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI)

## Reproducibility
- Seed: `SEED=42` (walk-forward + placebo RNG)
- Convention: Close-to-close primary (v1.2.3), overnight decomposition reported alongside
- Data: Parquet cache in `data/` (2026-10-12 vintage pinned in `data/vintages.json`, 2026-10-11 committed for specific drivers)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Next Steps
- Run `SEED=42 python3 run_all_verification.py --skip-slow` for convention-only check
- Or `SEED=42 python3 run_all_verification.py` for full quick verification
- Review `ledger/RESEARCH_LEDGER.md` for strategy dispositions