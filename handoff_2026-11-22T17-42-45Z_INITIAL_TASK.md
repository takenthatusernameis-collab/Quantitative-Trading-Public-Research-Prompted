# Agent Handoff — 2026-11-22T17:44:24Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git Status**: Clean (verify with `git status`)

## Key Commands (from AGENTS.md)
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Notes
- **Never leave verification half-finished**: `run_all_verification.py` backs up `experiments/*.json` to `.verify_snapshot/` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
- **Golden baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement
- **Cache coverage enforced**: `scripts/check_data_coverage.py` requires all data inputs pinned in `ledger/data_baseline.json`
- **Reproducibility**: Always use `SEED=42`. Close-to-close is primary convention v1.2.3
- **Dependencies**: `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Current State
- Research ledger: `ledger/RESEARCH_LEDGER.md` (E001–E043 documented)
- Golden artifacts: `experiments/*.json` (canonical, committed)
- Data vintages: `data/vintages.json` (2026-10-12), `data/fundamentals_vintages.json` (E029)
- Verification reports: `.verify_reports/` (gitignored)

## Next Steps (if any)
- Review ledger for open items (E041 optimizer drift, E042 confirmatory)
- Run `make check` to validate conventions before any new work
- Consider `make verify-quick` for full regression test

---
*Generated automatically for agentic session continuity*