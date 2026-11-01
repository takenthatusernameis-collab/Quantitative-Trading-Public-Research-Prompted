# Handoff — 2026-11-01T08-22-07Z

## Initial task for next session

**Establish a clean, verified baseline before any new research work.**

1. `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.
2. `SEED=42 bash scripts/check.sh` (or `make check`) — expected EXIT 0 with "=== All checks passed ===".
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain (gitignored; ignore them). No stray `experiments/*.json`, no `.verify_snapshot/` artifacts, no source changes. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
4. Only after steps 1–3 pass cleanly, address the open item below.

## Current state

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` (last entries E044–E049).
- **HEAD:** `2a5aff1` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- **Working tree:** clean of tracked changes — only `__pycache__/*.pyc` modifications (gitignored). No `.verify_snapshot/` present → no live verification run, nothing to recover.
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Fixed (E049, 2026-10-20):** E042-lead root cause — `src/portfolio_opt.py` now validates tangency answers on the problem's constraints, not the solver's exit status. Primary (quick) gate green.
- **Open item (highest value):** the tangency QP in `src/portfolio_opt.py` `max_sharpe` branch is still ill-conditioned (SLSQP at `ftol=1e-12`); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs. **Do not re-pin to silence.** Route `max_sharpe` through `exact_qp`/`exact_tangency_kkt` active-set enumeration (already implemented as reference oracle), fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point, then re-pin affected artifacts deliberately (never silently). See `ledger/RESEARCH_LEDGER.md` E049.
- **Known reproducible offline:** E029, E030. Run drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 experiments/run_e0XX.py ...`
- Ledger: `ledger/RESEARCH_LEDGER.md`
