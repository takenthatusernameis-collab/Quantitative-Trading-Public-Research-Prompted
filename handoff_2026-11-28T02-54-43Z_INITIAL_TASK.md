# Handoff — 2026-11-28T04:01:55Z

## Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043), surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Quick Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min + 50 sims)
SEED=42 python3 run_all_verification.py --full
```

## Key Integrity Rules
- `experiments/*.json` are canonical golden artifacts — never commit verification output
- Verification backs up goldens to `.verify_snapshot/` and restores after
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
- `scripts/check_golden_baseline.py` compares working tree to pinned SHA-256 in `ledger/golden_baseline.json`
- Cache coverage enforced: `scripts/check_data_coverage.py` (pinned in `ledger/data_baseline.json`)

## Reproducibility
- Seed: `SEED=42` (walk-forward + placebo RNG)
- Data: Cached parquet in `data/` (gitignored except 2026-10-11/12 vintages)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Convention: Close-to-close primary (v1.2.3), overnight decomposition reported alongside

## Recent State
- E050 fix (exact KKT active-set enumeration) landed — E041/E042 now bit-reproducible (0 differences)
- Extended verification: 18 drivers reproduce with 0 differences (2026-11-23 measurement)
- No tolerance violations remain — do not re-pin artifacts

## Next Steps (if any)
- Run `make check` or `make verify-quick` to validate current state
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation
- No active experiments pending — research phase complete