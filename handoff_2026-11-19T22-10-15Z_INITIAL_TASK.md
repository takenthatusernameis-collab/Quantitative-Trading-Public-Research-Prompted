# Agent Handoff - 2026-11-19T22:10:49Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast convention check (offline, seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, includes E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Critical Integrity Notes
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Cache coverage enforced via `scripts/check_data_coverage.py` — all data inputs must be pinned

## Current State
- Repository at commit: Check `git log --oneline -1`
- No active verification run (check `.verify_snapshot/ACTIVE.json` if uncertain)
- E041 optimizer determinism issue documented in ledger E049 (133 numeric diffs remain, 3 structural resolved)

## Next Steps (if continuing)
1. Run `SEED=42 bash scripts/check.sh` to verify clean state
2. Choose verification level based on need
3. Review `ledger/RESEARCH_LEDGER.md` for open items before new experiments