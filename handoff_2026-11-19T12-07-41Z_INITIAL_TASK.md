# Agent Handoff - 2026-11-19T12:07:41Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git Status**: Clean repo, verification suite available

## Key Commands
```bash
# Fast check (offline, seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Golden files**: `experiments/*.json` are canonical artifacts — never commit verification output
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Baseline integrity**: `scripts/check_golden_baseline.py` compares against `ledger/golden_baseline.json` SHA-256 pins
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`
- **Seed**: Always use `SEED=42` for reproducibility

## Verification Suite Behavior
- Backs up goldens to `.verify_snapshot/` before re-running, restores after
- Runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache fails hard
- Extended block writes drift report to `.verify_reports/` (gitignored)
- Known drift: E030 (yfinance non-determinism), E041 (optimizer 1-ulp sensitivity)

## Next Steps
- Run `SEED=42 bash scripts/check.sh` to verify environment
- Run verification suite as needed
- Consult `ledger/RESEARCH_LEDGER.md` for experiment dispositions
