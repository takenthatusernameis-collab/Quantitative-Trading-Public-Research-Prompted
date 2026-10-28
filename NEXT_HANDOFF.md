# Next Task: Repository is fully verified — no new research warranted

## Context
This session (handoff written 2026-10-28T05:31:06Z) confirmed the repository is in a clean, fully-verified state:

- HEAD `97be808` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- Working tree has **no tracked changes** — only `__pycache__/*.pyc` artifacts (gitignored; ignore them).
- No live verification snapshot (`.verify_snapshot/` absent, no `ACTIVE.json`). No run is in progress; nothing to recover.
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All guards in place and passing: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, and experiment-script imports.

## Known pre-existing drift (reporting-only, decisions unchanged)
- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

## Precise task (bounded, optional)
Re-run the verification suite to confirm stability:

```bash
SEED=42 python3 run_all_verification.py --extended
```

Expect the pre-existing E030/E041 drift above. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Evidence already gathered
- `git status`: clean of tracked changes; HEAD `97be808`.
- `git diff --name-only`: only `__pycache__/*.pyc` (gitignored).
- No `.verify_snapshot/` present → no interrupted run to recover.
- Fast offline suite (`SEED=42 bash scripts/check.sh`) passing as of 2026-10-28T05:31:06Z: ALL VERIFICATIONS PASSED.