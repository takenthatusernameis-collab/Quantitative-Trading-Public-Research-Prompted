# Initial Task Message (for next agentic session) — 2026-10-30T15:12:24Z

> **START HERE:** Repository is fully verified and in a stable state. No new research is warranted. Your primary task is to verify stability by running the baseline integrity check, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. All constraints from below still apply.
>
> **Durable handoff:** `HANDOFF_NEXT_SESSION_2026-10-30T15-12-24Z.md` (this file). The older files `HANDOFF_NEXT_SESSION_2026-10-30T15-11-00Z.md` and `HANDOFF_NEXT_SESSION_2026-10-30T15-12-03Z.md` are superseded duplicates of the same standing task and may be ignored.

---

## Next Task: Repository is fully verified — no new research warranted

## Context
Handoff written 2026-10-30T15:12:24Z. The repository is in a clean, fully-verified state:

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All guards in place and passing: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `tests/test_portfolio_opt.py`, `verify_convention_robustness.py`, template validation, and experiment-script imports.

## Evidence gathered this session (2026-10-30T15:12:24Z)
- `git status`: clean of tracked changes; no modified, staged, or untracked tracked files.
- HEAD `16944d3` (chore(kilo): checkpoint agent session), branch `main`, up to date with `origin/main`.
- No live verification snapshot (`.verify_snapshot/` absent, no `ACTIVE.json`). No run is in progress; nothing to recover.
- Prior handoffs `HANDOFF_NEXT_SESSION_2026-10-30T15-11-00Z.md` / `...T15-12-03Z.md` and `NEXT_HANDOFF.md` all describe the identical standing task; this file is the current canonical handoff.

## Known pre-existing drift (reporting-only, decisions unchanged)
- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

## Precise task (bounded, optional)
Re-run the baseline integrity check to confirm stability:

```bash
SEED=42 bash scripts/check.sh
```

Expect exit 0 with the pre-existing E030/E041 drift unchanged. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

(End of file)