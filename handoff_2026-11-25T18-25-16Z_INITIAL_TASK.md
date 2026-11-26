# Agent Handoff — 2026-11-26T00:30:26Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Current commit**: Check `git log --oneline -1`

## Verification Suite Status
- **Golden artifacts**: `experiments/*.json` are canonical baselines
- **Snapshot location**: `.verify_snapshot/` (gitignored, with `ACTIVE.json` marker)
- **Quick verify**: `SEED=42 python3 run_all_verification.py` (~8 min)
- **Extended verify**: `SEED=42 python3 run_all_verification.py --extended` (~21 min)
- **Full verify**: `SEED=42 python3 run_all_verification.py --full` (~15 min)

## Key Conventions
- **Seed**: Always `SEED=42`
- **Convention**: Close-to-close primary (v1.2.3), overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (2026-10-12 vintage pinned in `data/vintages.json`, 2026-10-11 committed)
- **E029 fundamentals**: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Cache coverage**: Enforced invariant — `scripts/check_data_coverage.py` validates all download sites

## Recovery Commands
```bash
# Restore goldens after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/

# Convention robustness check only
SEED=42 python3 verify_convention_robustness.py

# Fast check (offline, seconds)
SEED=42 bash scripts/check.sh
```

## Critical Notes
1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
2. **Golden baseline integrity**: `scripts/check_golden_baseline.py` compares against `ledger/golden_baseline.json` SHA-256 pins
3. **Do not re-pin artifacts** to silence tolerance violations — only deliberate code changes warrant re-pinning (recorded in ledger)
4. **Optimizer determinism**: `src/portfolio_opt.py` validates on constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`)

## Next Steps (if any)
- Run `SEED=42 bash scripts/check.sh` to verify current state
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and dispositions
- Review any open issues in the verification suite