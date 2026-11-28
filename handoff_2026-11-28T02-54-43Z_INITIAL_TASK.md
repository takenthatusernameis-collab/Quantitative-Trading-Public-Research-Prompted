# Agent Handoff — 2026-11-28T04:55:02Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands (from AGENTS.md)
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, includes E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Critical Integrity Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores them after. Use `--restore-only` if interrupted.
- **Golden baseline** pinned in `ledger/golden_baseline.json` (SHA-256). Do not re-pin without ledger entry.
- **Data coverage** enforced via `scripts/check_data_coverage.py` — all cache files must exist and match SHA-256 in `ledger/data_baseline.json`.
- **Optimizer determinacy** (ledger E049/E050): SLSQP status 8 is valid at constrained optimum; exact active-set enumeration (E050 fix) makes E041/E042 bit-reproducible.

## Current State
- No active verification run (checked: no `.verify_snapshot/ACTIVE.json`)
- All experiment goldens at HEAD match `ledger/golden_baseline.json`
- Data cache coverage validated per `ledger/data_baseline.json`

## Next Session Starting Points
1. Run `SEED=42 bash scripts/check.sh` to validate conventions
2. If clean, run `SEED=42 python3 run_all_verification.py --extended` for full driver reproduction
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion gates