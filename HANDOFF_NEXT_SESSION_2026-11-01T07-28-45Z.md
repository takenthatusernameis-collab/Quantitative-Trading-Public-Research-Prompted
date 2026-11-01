# Handoff — 2026-11-01T07-28-45Z

## Initial task for next session

Establish a clean, verified baseline before any new research work:

1. `SEED=42 bash scripts/check.sh` (or `make check`) — runs `check_json_artifacts.py`, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, the unittest suite (`test_json_guard`, `test_goldens_guard`, `test_golden_baseline`, `test_drift_report`, `test_data_coverage`, `test_portfolio_opt`), `verify_convention_robustness.py`, template validation, and experiment-script imports. Expected: EXIT 0 with "=== All checks passed ===".
2. `git status --short` — confirm only `__pycache__` modifications remain (no stray `experiments/*.json`, no `.verify_snapshot/` artifacts, no source changes). If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
3. Only after steps 1–2 pass cleanly, address the open item below.

## Current state (verified this session)

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` (last entries E044–E049).
- **HEAD:** `aa28674` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- **Working tree:** clean of tracked changes — only `__pycache__/*.pyc` modifications (gitignored; ignore them). No `.verify_snapshot/` present, no `ACTIVE.json` → no live verification run, nothing to recover.
- **Baseline integrity:** `SEED=42 bash scripts/check.sh` exits 0 with "=== All checks passed ===". All FAIL lines in the log are intentional negative self-tests inside the check scripts themselves (tempdir fixtures `experiments/d.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json`, a missing-manifest path, a stale-snapshot pid 999999, and a missing pinned data file) — they are not repository defects. The suite's own unittest blocks and `verify_convention_robustness.py` all pass.
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`.
- **Fixed (E049, 2026-10-20):** E042-lead root cause — `src/portfolio_opt.py` now validates tangency answers on the problem's constraints, not the solver's exit status. Primary (quick) gate green; E042 lead `/primary` reproduces committed golden to 5e-9. `/placebo_constrained` deliberately re-pinned (visible in diff). Regression test `tests/test_portfolio_opt.py` added.
- **Open item (highest value):** the tangency QP in `src/portfolio_opt.py` `max_sharpe` branch is still ill-conditioned (SLSQP at `ftol=1e-12` on `min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y`); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs (down from 360–9273). **Do not re-pin to silence.** Research-engineering decision needed: replace SLSQP QP solves with a well-conditioned deterministic solver (exact active-set enumeration of all KKT points is feasible for N <= 5 and is already implemented as `exact_qp` / `exact_tangency_kkt` in `src/portfolio_opt.py` and used as the reference oracle), then re-pin affected artifacts deliberately.
- **Second open item (E049, smaller):** `y0 = w_feas / max(mu_s'w_feas, 1e-12)` (`src/portfolio_opt.py` SLSQP start-point branch) masks a negative denominator, so at the 2019-10-16 rebalance the initial point has magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09. SLSQP returns garbage there (objective 3.7e+20), which the feasibility check correctly rejects, so the shipped code falls back to the LP vertex exactly as the golden did. Fixing the start point (a max-`mu_s'w` LP on the feasible simplex) makes SLSQP converge to the exact optimum there and would **change the published numbers**, so it is left for the same deliberate re-pin decision.
- **E041 (left as-is):** 133 numeric diffs remain on the ill-conditioned QP; decision REJECTED 3/5, gate flags unchanged. Not explained by the E049 defect.
- **Known reproducible offline:** E029, E030. `QUANT_RESEARCH_OFFLINE=1` for driver runs.
- **Recovery:** `.verify_snapshot/ACTIVE.json`; `SEED=42 python3 run_all_verification.py --restore-only`.
- **CI:** workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Immediate priorities

1. `SEED=42 bash scripts/check.sh` (or `make check`).
2. `git status --short` — restore if verification left artifacts.
3. Decide on the ill-conditioned tangency QP (route the `max_sharpe` branch through the existing `exact_qp`/`exact_tangency_kkt` active-set enumeration instead of SLSQP, fix the `y0` start point, or leave SLSQP as-is), implement, and re-pin affected artifacts deliberately (never silently).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 experiments/run_e0XX.py ...`
- `QUANT_RESEARCH_OFFLINE=1` for offline driver runs.
- Ledger: `ledger/RESEARCH_LEDGER.md` (E044–E049 cover the recent verification/optimizer work).