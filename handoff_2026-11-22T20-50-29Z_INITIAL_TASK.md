# Agent Handoff — 2026-11-22T20:51:14Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands (from AGENTS.md)
```bash
# Fast check (seconds, offline)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min + 50 sims)
SEED=42 python3 run_all_verification.py --full
# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Critical Integrity Notes
- **Never leave verification half-finished**: `experiments/*.json` are backed up to `.verify_snapshot/` with `ACTIVE.json` marker. If killed, recover with `SEED=42 python3 run_all_verification.py --restore-only`
- **Golden baseline pinned in `ledger/golden_baseline.json`** — do not re-pin without ledger entry
- **Data cache coverage enforced**: `scripts/check_data_coverage.py` validates all `data.download()` call sites against `ledger/data_baseline.json`
- **CI workflow cannot be created by agents** — template at `.github/workflow-templates/verification-gate.yml`

## Current State
- No active verification run (check `scripts/check_goldens_clean.py` for stale snapshots)
- All experiments committed to `experiments/*.json`
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E030 16-ETF panel committed (ledger E048)
- E041 optimizer defect fixed (ledger E049) — 133 numeric diffs remain (ill-conditioned QP), do not re-pin

## Next Steps (if resuming)
1. Run `SEED=42 bash scripts/check.sh` to verify clean state
2. Choose verification tier based on time budget
3. Check `ledger/RESEARCH_LEDGER.md` for open items before any re-pinning