# Agent Handoff — 2026-11-15T02:16:20Z

## Session Context
- **Project**: Quantitative-Trading-Public-Research-Prompted
- **Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts — never commit verification output
- **Recovery**: If verification interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage enforced via `scripts/check_data_coverage.py`
- **Optimizer determinism**: E041/E042 grid artifacts drift due to ill-conditioned QP — do not re-pin to silence

## Next Steps
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Run verification suite as needed (`verify-quick`, `verify-extended`, or `verify-full`)
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions