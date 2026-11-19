# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-19T19:04:28Z
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase:** Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

## Current State

- **Verification suite**: Ready to run (`SEED=42 python3 run_all_verification.py`)
- **Golden artifacts**: `experiments/*.json` are canonical baselines (pinned in `ledger/golden_baseline.json`)
- **Data**: Cached parquet in `data/` (2026-10-12 and 2026-10-11 vintages pinned). E029 fundamentals pinned in `data/fundamentals/`.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Key Commands

```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min, 18 more drivers)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full

# Restore goldens after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores them after. If killed, run `--restore-only` or `git checkout -- experiments/`.
2. **Golden baseline integrity**: `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires explicit `--update`.
3. **Cache coverage invariant**: Every `data.download()` call site must have a committed, SHA-256-pinned cache file (see `ledger/data_baseline.json`).
4. **Optimizer determinism**: Tangency QP is ill-conditioned (1-ulp moves min_var ~1e-05). E041/E042 grid artifacts drift but decisions unchanged. Do not re-pin to silence drift.

## Next Steps (if any)

- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Run verification suite to confirm reproducibility
- Consider promotion of any PARTIAL results with dedicated confirmatory runs