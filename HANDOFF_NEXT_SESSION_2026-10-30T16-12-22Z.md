# Initial Task Message (for next agentic session) — 2026-10-30T16-12-22Z

> **START HERE:** Repository is fully verified and in a stable state. No new research is warranted. Your primary task is to verify stability by running the baseline integrity check, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. All constraints from below still apply.
>
> **Durable handoff:** FILE_NAME (this file). The prior canonical file `handoff_next_session.md` was reviewed at session start; older timestamped duplicates may be ignored if superseded.

---

## Next Task: Repository is fully verified — no new research warranted

## Context

Handoff written 2026-10-30T16-12-22Z. The repository is in a clean, fully-verified state (confirmed at start of this session):

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Market-neutral-total-portfolio line is CLOSED.
- HEAD `2ef3c89` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- Working tree clean of tracked changes (only gitignored `__pycache__/*.pyc`).
- No live verification snapshot (`.verify_snapshot/` absent). No run in progress.
- All guards passing: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, experiment-script imports.
- `src/portfolio_opt.py`: exact active-set KKT solver (`exact_qp`, `exact_tangency_kkt`) is primary for `max_sharpe`/`min_var`; SLSQP fallback only when no KKT point found. Feasibility judged on problem constraints (E049), never solver exit status.

## Evidence gathered this session (2026-10-30T16-12-22Z)

- `git status --short | grep -v __pycache__`: empty.
- `git rev-parse --short HEAD`: `2ef3c89`.
- `ls .verify_snapshot/ 2>&1 | head -2`: absent.
- Reviewed `handoff_next_session.md` (canonical context).

## Known pre-existing drift (reporting-only, decisions unchanged — do NOT re-pin)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP; optimizer determinism fixed per E049). 3 structural differences gone. Decision REJECTED 3/5 unchanged.
- **E030**: numeric diffs on near-zero quantities. Decision unchanged.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned.

## Precise task (bounded)

Run the baseline integrity check to confirm stability:

```bash
SEED=42 bash scripts/check.sh
```

Expect exit 0 with pre-existing E030/E041 drift unchanged. Do **not** weaken tolerances, skip drivers, modify committed goldens, or change gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals in `data/fundamentals/`).
- Never leave verification run half-finished (suite backs up/restores `experiments/*.json`).
- Do not commit verification outputs.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Offline mode `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- CI workflow creation maintainer-gated (`.github/workflow-templates/verification-gate.yml`).
- Run `python3 -m py_compile` on changed files.

(End of file)
