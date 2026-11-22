# Agentic Work Session Handoff

**Timestamp:** 2026-11-22T01:01:00Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden artifacts in `experiments/*.json` are canonical baselines
- Research standing: E041 REJECTED 3/5; E042 PARTIAL; E041/E042 grid artifacts drift (ill-conditioned QP, ~1e-05 min_var movement per 1-ulp input) — do NOT re-pin to silence

## Verification Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Conventions
- **Seed:** Always use `SEED=42` for reproducibility
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages)
- **Cache coverage:** Enforced invariant — all `data.download()` calls must have pinned SHA-256 in `ledger/data_baseline.json`
- **Golden files:** Never modified by verification; backed up to `.verify_snapshot/` and restored after
- **Do not commit verification output** — restore with `--restore-only` if interrupted

## Recent Context
- E029 fundamentals snapshot pinned in `data/fundamentals/` (offline-reproducible since 2026-10-20)
- E030 16-ETF panel committed (reproducible since 2026-10-20)
- E041 optimizer determinism issue root-caused (ledger E049) — 133 numeric diffs remain from ill-conditioned QP
- Optimizer validates on problem constraints, not solver exit status (pinned by `tests/test_portfolio_opt.py`)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
3. Review any open ledger items (E041/E042 grid drift, E049 optimizer determinism)
4. Consider extended verification if making changes to drivers or data pipeline
