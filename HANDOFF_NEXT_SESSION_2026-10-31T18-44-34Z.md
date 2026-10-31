# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-31T18:44:34Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** `7303475` (chore(kilo): checkpoint agent session)
**Working tree:** clean at handoff time (restored `__pycache__/*.pyc` to HEAD; they are tracked but only differ by build hash, so they are noise). No live verification run in progress; `.verify_snapshot/` absent.

## Initial Task (Start Here)

**Task:** Repository is fully verified and in a stable state. No new research is warranted. Verify stability by running the baseline integrity check, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Evidence gathered this session

1. **Working tree was not clean on arrival.** `git status` showed 14 modified files, all `__pycache__/*.pyc`. These are *tracked* (force-added at some earlier point) despite `__pycache__/` being in `.gitignore`. Each diff is purely a build-hash/timestamp byte change at identical size (e.g. `check_data_coverage.cpython-312.pyc`: Bin 50361 -> 50361 bytes). Restored all of them with `git checkout -- scripts/__pycache__ src/__pycache__ tests/__pycache__`; tree is now clean.
2. **Baseline integrity check passed.** `SEED=42 bash scripts/check.sh` exits **0** ("=== All checks passed ===", "ALL VERIFICATIONS PASSED", "OK").
   - The only `FAIL` lines in the output are **intentional negative-test fixtures** generated on the fly by `tests/test_json_guard.py` in a temp dir (`experiments/b.json`, `x.json`, `e2.json`, `u.json`, `d.json`, `d2.json`, `badlist.json`) and the stale-snapshot / missing-manifest / missing-pinned-file guards (`pid 999999`, `nope.json`). These files do not exist in the repo; they are part of the guard's own self-test. Confirmed by grepping `scripts/check.sh` (it calls `check_json_artifacts.py` + `tests.test_json_guard`) — no hardcoded fixture paths.
3. **Known pre-existing drift is unchanged** (reporting-only; decisions unaffected):
   - **E041**: residual numeric diffs from 1-ulp sensitivity of the ill-conditioned tangency QP (optimizer determinism was fixed per ledger E049; the exact active-set KKT solver `exact_qp` was added per E050 but the QP itself remains ill-conditioned). Do **not** re-pin.
   - **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
   - **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.
   - E042 lead: `/primary` reproduces to 5e-9; `/placebo_constrained` was deliberately re-pinned (z 1.9568 -> 1.8121, still below the G2 bar of 3.0, so `decision` REJECTED 4/5 is unchanged).

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json` via `.verify_snapshot/`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Do not re-pin goldens without ledger justification.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Quick reference

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Open item from the ledger (for whoever picks up the E049 follow-up)

The tangency QP in `src/portfolio_opt.py` is still ill-conditioned: `exact_qp` (exact active-set KKT enumeration, deterministic) is the primary solver for `max_sharpe`/`min_var`/`risk_parity` and for `project_onto_beta_cap`, with SLSQP kept only as a fallback. But `exact_qp` still uses loose internal tolerances (`tol_eff = max(tol, 1e-8)`, feasibility checks at `tol_eff * 1000`, a `1e-12` ridge when `cond(Q) > 1e15`, and a projection step that rescales `w` to hit `sum(w)=1` only when `|sum - b_eq| < 1e-6`). On the real E042/E041 covariance these are what leave the 29-133 residual diffs. Tightening them (and removing the conditional ridge/projection) is the documented next step — but it must be done as a **deliberate re-pin** with `python3 scripts/check_golden_baseline.py --update`, never as a silent side effect of a verification run, and the ledger's standing disposition is that the committed golden is authoritative, not the latest re-run.