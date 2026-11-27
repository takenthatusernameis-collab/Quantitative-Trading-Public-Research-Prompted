# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T16:49:54Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Notes for Next Session

- **Baseline Integrity**: `experiments/*.json` are canonical artifacts. Verification suite overwrites and restores them. Never leave a verification run half-finished.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden Baseline**: SHA-256 fingerprints pinned in `ledger/golden_baseline.json`. Re-pinning requires deliberate action via `scripts/check_golden_baseline.py --update`.
- **Data Coverage**: Enforced invariant. All `data.download()` call sites must have committed, SHA-256 pinned cache files per `ledger/data_baseline.json`.
- **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.

## Recent Ledger Entries

- **E049**: Optimizer determinism fix — SLSQP status-gating removed, validated by `tests/test_portfolio_opt.py`
- **E050**: Exact KKT active-set enumeration as primary tangency solver — made E041/E042 bit-reproducible
- **E048**: Cache coverage enforcement — E030 16-ETF panel now committed
- **E045**: E029 fundamentals snapshot pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Verification Status (2026-11-23T05:17Z measurement)

- **8 quick drivers**: 0 differences (E012, E023, E024 --merge, E027, E035, E037, E039, E042-lead)
- **18 extended drivers**: 0 differences (E011, E013, E015, E016, E017, E018, E019, E020, E021, E022, E025, E026, E028, E029, E030, E034, E036, E041)
- All drivers reproduce with numeric_tol=1e-4

## Next Steps Available

1. Run `make check` for fast convention robustness
2. Run `make verify-quick` for 8-driver verification
3. Run `make verify-extended` for 26-driver verification
4. Run `make verify-full` for full sensitivity grid (96 configs) + E042 n_sim=50
5. Investigate any REJECTED/PARTIAL strategies in ledger for potential follow-up
6. Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies