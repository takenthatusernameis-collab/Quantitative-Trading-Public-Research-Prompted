# Handoff — 2026-11-01T08-16-41Z

## Initial task for next session

**Establish a clean, verified baseline before any new research work.** Dependencies may not be installed in a fresh environment.

1. `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional.
2. `SEED=42 bash scripts/check.sh` (or `make check`) — expected EXIT 0 with "=== All checks passed ===". If it fails on `ModuleNotFoundError: No module named 'pandas'`, step 1 was missed.
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain (gitignored; ignore them). No stray `experiments/*.json`, no `.verify_snapshot/` artifacts, no source changes. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
4. Only after steps 1–3 pass cleanly, address the open item below.

## Current state (verified this session)

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` (last entries E044–E049).
- **HEAD:** `d44d607` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- **Working tree:** clean of tracked changes — only `__pycache__/*.pyc` modifications (gitignored; ignore them). No `.verify_snapshot/` present, no `ACTIVE.json` → no live verification run, nothing to recover.
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`.
- **Fixed (E049, 2026-10-20):** E042-lead root cause — `src/portfolio_opt.py` now validates tangency answers on the problem's constraints, not the solver's exit status. Primary (quick) gate green.
- **Open item (highest value):** the tangency QP in `src/portfolio_opt.py` `max_sharpe` branch is still ill-conditioned (SLSQP at `ftol=1e-12` on `min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y`); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs (down from 360–9273). **Do not re-pin to silence.** Research-engineering decision needed: replace SLSQP QP solves with a well-conditioned deterministic solver (exact active-set enumeration of all KKT points is feasible for N <= 5 and is already implemented as `exact_qp` / `exact_tangency_kkt` in `src/portfolio_opt.py` and used as the reference oracle), then re-pin affected artifacts deliberately.
- **Second open item (E049, smaller):** `y0 = w_feas / max(mu_s'w_feas, 1e-12)` masks a negative denominator; fix the start point (max-`mu_s'w` LP on feasible simplex) would change published numbers — leave for same deliberate re-pin decision.
- **E041 (left as-is):** 133 numeric diffs remain on ill-conditioned QP; decision REJECTED 3/5, gate flags unchanged.
- **Known reproducible offline:** E029, E030. `QUANT_RESEARCH_OFFLINE=1` for driver runs.
- **Recovery:** `.verify_snapshot/ACTIVE.json`; `SEED=42 python3 run_all_verification.py --restore-only`.
- **CI:** workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Immediate priorities

1. `pip install -r requirements.txt` then `SEED=42 bash scripts/check.sh`.
2. `git status --short` — restore if verification left artifacts.
3. Decide on the ill-conditioned tangency QP (route `max_sharpe` through `exact_qp`/`exact_tangency_kkt` instead of SLSQP, fix `y0` start point, or leave SLSQP as-is), implement, and re-pin affected artifacts deliberately (never silently).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 experiments/run_e0XX.py ...`
- `QUANT_RESEARCH_OFFLINE=1` for offline driver runs.
- Ledger: `ledger/RESEARCH_LEDGER.md` (E044–E049)
