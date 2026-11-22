# Agent Handoff — 2026-11-22T23:30:22Z

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

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Critical Notes
- **Golden artifacts**: `experiments/*.json` are canonical. Verification overwrites then restores them.
- **Never leave verification half-finished** — use `--restore-only` to recover if interrupted.
- **Seed**: Always `SEED=42` for reproducibility.
- **Data**: Cached in `data/` (gitignored except pinned vintages). Offline mode enforced via `QUANT_RESEARCH_OFFLINE=1`.
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` — maintainer must create via GitHub UI.

## Recent State
- Research phase complete. Ledger documents surviving validated strategies.
- E029, E030 now offline-reproducible (pinned data vintages).
- E041 optimizer determinism issue identified (ledger E049) — 133 numeric diffs remain, do not re-pin.
- Cache coverage enforced via `scripts/check_data_coverage.py` + `ledger/data_baseline.json`.

## Next Steps (if any)
- Review `ledger/RESEARCH_LEDGER.md` for open items.
- Run `make check` before any commits to verify baseline integrity.