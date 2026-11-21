# Agent Handoff — 2026-11-21T18:10:00Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Verification Commands
```bash
# Fast check (convention robustness + template validation)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config sensitivity)
SEED=42 python3 run_all_verification.py --full
```

## Critical Integrity Notes
- **Golden artifacts** in `experiments/*.json` are canonical baselines
- Verification suite backs up goldens to `.verify_snapshot/` and restores after
- **Never leave a verification run half-finished** — use `--restore-only` to recover
- `scripts/check_golden_baseline.py` compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json`
- Cache coverage is enforced via `scripts/check_data_coverage.py` (pinned in `ledger/data_baseline.json`)

## Current State
- No active verification run (snapshot clean)
- All experiments committed through E043
- Ledger entries through E049 (optimizer determinism fix, E029/E030 offline reproducibility)

## Recommended Next Steps
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. If clean, proceed with `SEED=42 python3 run_all_verification.py` for quick verification
3. Review `ledger/RESEARCH_LEDGER.md` for open items (E041 ill-conditioned QP drift, E042 sensitivity grid)

## Environment
- Python 3, dependencies in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- Optional: cvxpy/cvxopt (falls back to scipy.optimize)
- Offline mode enforced via `QUANT_RESEARCH_OFFLINE=1` during verification