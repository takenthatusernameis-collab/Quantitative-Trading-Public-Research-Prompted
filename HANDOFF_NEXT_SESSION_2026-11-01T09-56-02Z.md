# Handoff — 2026-11-01T09-56-02Z

## Initial task for next session

Establish a clean, verified baseline before any new research work:

1. `SEED=42 bash scripts/check.sh` (or `make check`) — runs `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `py_compile`, and `test_portfolio_opt.py`. Expected: EXIT 0 with "=== All checks passed ===".
2. `git status --short` — confirm only `__pycache__` modifications remain (no stray `experiments/*.json`, no `.verify_snapshot/` artifacts, no source changes). If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
3. Only after steps 1–2 pass cleanly, address the open item below.

## Current state

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- **Fixed (E049, 2026-10-20):** E042-lead root cause — `src/portfolio_opt.py` now validates tangency answers on the problem's constraints, not the solver's exit status. Primary (quick) gate green; E042 lead `/primary` reproduces committed golden to 5e-9. `/placebo_constrained` deliberately re-pinned (visible in diff). Regression test `tests/test_portfolio_opt.py` added.
- **Open item (highest value):** the tangency QP in `src/portfolio_opt.py` max_sharpe branch is still ill-conditioned (SLSQP at `ftol=1e-12` on `min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y`); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs (down from 360–9273). **Do not re-pin to silence.** Research-engineering decision needed: replace SLSQP QP solves with a well-conditioned deterministic solver (exact active-set enumeration of all KKT points is feasible for N <= 5 and was used as the reference oracle), then re-pin affected artifacts deliberately.
- **E041 (left as-is):** 133 numeric diffs remain on the ill-conditioned QP; decision REJECTED 3/5, gate flags unchanged. Not explained by the E049 defect. Next bounded investigation if capacity allows.
- **Known reproducible offline:** E029, E030. `QUANT_RESEARCH_OFFLINE=1` for driver runs.
- **Recovery:** `.verify_snapshot/ACTIVE.json`; `SEED=42 python3 run_all_verification.py --restore-only`.
- **Git:** working tree clean except `__pycache__` (as of this handoff).

## Immediate priorities

1. `SEED=42 bash scripts/check.sh` (or `make check`).
2. `git status --short` — restore if verification left artifacts.
3. Decide on the ill-conditioned tangency QP (exact active-set enumeration vs. SLSQP), implement, and re-pin affected artifacts deliberately (never silently).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 experiments/run_e0XX.py ...`
- `QUANT_RESEARCH_OFFLINE=1` for offline driver runs.
