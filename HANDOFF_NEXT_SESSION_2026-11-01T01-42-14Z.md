# Handoff - Initial Task - 2026-11-01T01:42:14Z

Durable detail: `.handoff/20261101T014214Z_INITIAL_TASK.md`

## Initial task for next session
**START HERE:** Run `SEED=42 bash scripts/check.sh` and confirm golden/integrity status is clean before making any changes. If a verification snapshot is pending/stale, recover via `SEED=42 python3 run_all_verification.py --restore-only` first.

## State at handoff (2026-11-01T01:42:14Z)
- `git status`: no tracked changes. Only `__pycache__/*.pyc` modified (gitignored; byte-size drift from recompilation, ignore).
- No live verification snapshot (`.verify_snapshot/` absent). Nothing to recover.
- HEAD `03e92766359cc5809b1efb592a21f628a89084b2`, branch `main`, up to date with `origin/main`.

## Known pre-existing drift (reporting-only, decisions unchanged)
- **E041**: residual numeric drift (~133 diffs, 1-ulp sensitivity of ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

## Constraints
- Always use `SEED=42`.
- Never overwrite goldens via verification; never re-pin to silence numeric drift.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- On any file edits, run `python3 -m py_compile` on touched files.