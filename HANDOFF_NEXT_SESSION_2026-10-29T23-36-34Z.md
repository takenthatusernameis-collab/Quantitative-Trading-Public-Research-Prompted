# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T23:36:34Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `2eb14e2` (working tree clean of tracked source/data changes except `__pycache__/*.pyc`; no `.verify_snapshot/` active; no interrupted run to recover).

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — all guards must pass with no golden diffs.
2. Run `git status --short` / `git diff --name-only` — confirm clean tree (only `__pycache__/*.pyc`, gitignored).
3. If an interrupted verification left dirty `experiments/*.json`, restore:
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative.
Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Known Open Items (Do Not "Fix" By Re-Pinning)

- **E041 numeric drift (open):** ~133 numeric differences remain (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism gating fixed per ledger E049). Do **not** re-pin `experiments/e041_*.json`. See `ledger/RESEARCH_LEDGER.md` (E049).
- **E042 grid artifacts:** 1-ulp sensitivity can appear; do not re-pin goldens.
- **E030:** numeric diffs on near-zero quantities (documented). Do not re-pin.
- **Data coverage:** Inputs must remain tracked and pinned in `ledger/data_baseline.json`. Never re-pin as a side-effect of verification.

## Quick Verification

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
```

# Next Task: Repository is fully verified — no new research warranted

## Context

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Baseline integrity guards enforced. All guards in place and passing: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, experiment-script imports.

## Precise task (bounded, optional)

Re-run the verification suite to confirm stability:

```bash
SEED=42 python3 run_all_verification.py --extended
```

Expect the pre-existing E030/E041 drift above. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Recommended Next Research-Engineering Task

Replace SLSQP QP solves in `src/portfolio_opt.py` with a well-conditioned, deterministic solver (for N <= 5, exact active-set enumeration of all KKT points is feasible and already used as a reference oracle), then deliberately re-pin affected artifacts. See ledger E049 and the `src/portfolio_opt.py:253` start-point defect.
