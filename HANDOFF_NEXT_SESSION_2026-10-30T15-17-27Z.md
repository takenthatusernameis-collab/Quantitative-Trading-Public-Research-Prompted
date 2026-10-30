# Initial Task Message (for next agentic session) — 2026-10-30T15:17:27Z

> **START HERE:** Repository is fully verified and in a stable state. No new research is warranted. Your primary task is to verify stability by running the baseline integrity check, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. All constraints from below still apply.
>
> **Durable handoff:** `HANDOFF_NEXT_SESSION_2026-10-30T15-17-27Z.md` (this file). The prior canonical file `HANDOFF_NEXT_SESSION_2026-10-30T15-16-33Z.md` is superseded; older duplicates (`HANDOFF_NEXT_SESSION_2026-10-30T15-12-24Z.md`, `...T15-11-00Z.md`, `...T15-12-03Z.md`, `NEXT_HANDOFF.md`, `NEXT_SESSION_HANDOFF.md`) describe the identical standing task and may be ignored.

---

## Next Task: Repository is fully verified — no new research warranted

## Context

Handoff written 2026-10-30T15:17:27Z. The repository is in a clean, fully-verified state:

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Market-neutral-total-portfolio line is CLOSED.
- HEAD `39a3b3f` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- Working tree clean of tracked changes; only `__pycache__/*.pyc` artifacts (gitignored; ignore them).
- No live verification snapshot (`.verify_snapshot/` absent, no `ACTIVE.json`). No run is in progress; nothing to recover.
- All guards in place and passing: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, and experiment-script imports.
- `src/portfolio_opt.py`: exact active-set KKT solver (`exact_qp`, `exact_tangency_kkt`) is the primary path for `max_sharpe` and `min_var`; SLSQP fallback only when exact enumeration finds no KKT point. Feasibility judged on problem constraints (E049 fix preserved), never solver exit status.

## Evidence gathered this session (2026-10-30T15:17:27Z)

- `git status --short | grep -v __pycache__`: empty (no tracked changes).
- `git rev-parse --short HEAD`: `39a3b3f`.
- `ls .verify_snapshot/`: absent → no interrupted run to recover.
- Prior handoffs (`HANDOFF_NEXT_SESSION_2026-10-30T15-16-33Z.md`, `HANDOFF_NEXT_SESSION_2026-10-30T15-12-24Z.md`, `NEXT_HANDOFF.md`) all describe the identical standing task; this file is the current canonical handoff.

## Known pre-existing drift (reporting-only, decisions unchanged — do NOT re-pin)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Decision REJECTED 3/5 unchanged.
- **E030**: numeric diffs on near-zero quantities (documented). Decision unchanged.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

## Precise task (bounded, optional)

Re-run the baseline integrity check to confirm stability:

```bash
SEED=42 bash scripts/check.sh
```

Expect exit 0 with the pre-existing E030/E041 drift unchanged. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

Optional confirmatory item (deterministic-solver verification, reporting-only; no research conclusions may change):
Verify the exact KKT path (not SLSQP) is the effective solver for the tangency QP (N ≤ 5) on every rebalance fold, keeping `_tangency_feasible` constraint-based validation. If any golden changed as a result, re-pin deliberately via `scripts/check_golden_baseline.py --update` so the replacement appears in the diff; do NOT re-pin to silence drift without a solver change. Affected candidates: E041 portfolio/grid, E042 primary/grid.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).
- Run `python3 -m py_compile` on changed files; no separate linter configured.

(End of file)