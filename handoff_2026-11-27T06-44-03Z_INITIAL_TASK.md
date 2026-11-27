# Handoff - 2026-11-27T07:45:04Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Verification Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, includes E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification backs them up and restores after.
- **Never leave verification half-finished** — use `--restore-only` if interrupted
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates all data inputs pinned
- **Optimizer determinacy fixed** (E050): Exact KKT active-set enumeration in `src/portfolio_opt.py` makes E041/E042 bit-reproducible

## Recent State
- Research phase complete, ledger updated
- All 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)
- E029 fundamentals pinned offline in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E030 16-ETF panel committed and golden re-pinned

## Next Steps (if any)
- Run verification suite before any commits
- Check `scripts/check.sh` passes (includes golden baseline + convention + optimizer tests)
- Consult `ledger/RESEARCH_LEDGER.md` for strategy dispositions