# Agent Handoff — 2026-11-16T03:50:35Z

## Session Context
**Project**: Quantitative-Trading-Public-Research-Prompted
**Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Critical Baseline Integrity Notes
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites and restores them.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Never commit verification output** — interrupted runs leave driver output in place of goldens.
- **Golden baseline pinned in** `ledger/golden_baseline.json` (SHA-256). Re-pinning requires explicit `scripts/check_golden_baseline.py --update`.
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates all `data.download()` call sites against `ledger/data_baseline.json`.

## Known Drift (Extended Block)
- **E030**: 28 numeric diffs on near-zero quantities (fixed since 2026-10-20 with pinned 16-ETF panel)
- **E041**: 133 numeric diffs (1-ulp QP ill-conditioning, optimizer defect fixed per ledger E049). **Do not re-pin**.
- **E042/E041 grid**: 29-133 differences from ill-conditioned tangency QP. **Do not re-pin** — open ledger item.

## Optimizer Determinism (Ledger E049)
`src/portfolio_opt.py` validates on problem constraints, not solver exit status. SLSQP status 8 is scipy-build dependent; gating on it caused environment-dependent tangency portfolio.

## Data Vintages
- **2026-10-12**: Pinned in `data/vintages.json`
- **2026-10-11**: Committed (E026/E028/E029/E030/E034/E036/E037 explicit end date)
- **E029 fundamentals**: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — offline reproducible

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Run `SEED=42 python3 run_all_verification.py --skip-slow` for quick convention check
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
4. Check `scripts/check_golden_baseline.py` and `scripts/check_data_coverage.py` for any pending updates

## Environment
- Python 3, deps: `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- cvxpy/cvxopt optional (fallback to scipy.optimize)
- Offline mode: `QUANT_RESEARCH_OFFLINE=1` (used by verification suite)