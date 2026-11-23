# Handoff — 2026-11-23T08:31:19Z

## Context
- **Project**: Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data
- **Phase**: Research phase complete (E001–E043)
- **Surviving strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

## Quick Commands
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

## Key Artifacts
- **Golden files**: `experiments/*.json` (canonical baseline, SHA-256 pinned in `ledger/golden_baseline.json`)
- **Data cache**: `data/` (parquet, gitignored except pinned vintages)
- **Fundamentals snapshot**: `data/fundamentals/` (pinned for E029 offline reproducibility)

## Verification State
- Last verified: 2026-11-23T05:17Z (numpy 2.5.4, scipy 1.18.1)
- All 18 extended drivers reproduce with 0 differences (numeric_tol=1e-4)
- E041/E042 tangency QP bit-reproducible via E050 exact active-set solver (commit `72dc947`)

## Critical Rules
1. **Never leave verification half-finished** — runs backup goldens to `.verify_snapshot/` and restore after; use `--restore-only` if interrupted
2. **Never re-pin goldens to silence tolerance violations** — re-pinning only for deliberate code changes recorded in ledger
3. **Cache coverage is enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site
4. **Optimizer validates on constraints, not solver status** — `src/portfolio_opt.py` rule tested in `tests/test_portfolio_opt.py`

## Next Steps (if any)
- Run `SEED=42 make verify-quick` to confirm baseline integrity
- Check `scripts/check_goldens_clean.py` for any working-tree drift vs HEAD
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation