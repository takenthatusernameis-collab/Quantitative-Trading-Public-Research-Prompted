# Handoff - Initial Task - 2026-11-01T01:39:37Z

Durable detail: .handoff/20261101T013937Z_INITIAL_TASK.md

## Initial task for next session
**START HERE:** Repository baseline is verified clean. Run `SEED=42 bash scripts/check.sh` to confirm golden/integrity status is still clean before making any changes. If a verification snapshot is pending/stale, recover via `SEED=42 python3 run_all_verification.py --restore-only` first.

## State at handoff (2026-11-01T01:39:37Z)
- `SEED=42 bash scripts/check.sh` → **exit 0, ALL VERIFICATIONS PASSED**.
- All guards green: committed JSON artifacts parse, goldens match HEAD, pinned goldens match baseline fingerprint, pinned data inputs present/tracked/unchanged, convention-robustness PASS (all strategies), experiment-script imports OK.
- `git status`: no tracked changes. Only `__pycache__/*.pyc` modified (gitignored; byte-size drift from recompilation, ignore).
- No live verification snapshot (`.verify_snapshot/` absent). Nothing to recover.
- HEAD `d480047` (chore(kilo): checkpoint agent session), branch `main`.

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
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).
- On any file edits, run `python3 -m py_compile` on touched files.

(End of file)
