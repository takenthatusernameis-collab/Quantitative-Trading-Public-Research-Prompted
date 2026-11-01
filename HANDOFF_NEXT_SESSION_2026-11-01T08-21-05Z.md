# Handoff — 2026-11-01T08-21-05Z

## Initial task for next session

**Establish a clean, verified baseline before any new research work.**

1. `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.
2. `SEED=42 bash scripts/check.sh` (or `make check`) — expected EXIT 0 with "=== All checks passed ===".
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain; restore if verification left artifacts (`SEED=42 python3 run_all_verification.py --restore-only`).
4. Only after steps 1–3 pass cleanly, address the open item below.

## Open item

Ill-conditioned tangency QP in `src/portfolio_opt.py` (`max_sharpe` branch, SLSQP at `ftol=1e-12`). Route through the existing `exact_qp`/`exact_tangency_kkt` active-set enumeration instead of SLSQP; fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point; re-pin affected artifacts deliberately (never silently). See `ledger/RESEARCH_LEDGER.md` E049.

(End of handoff)
