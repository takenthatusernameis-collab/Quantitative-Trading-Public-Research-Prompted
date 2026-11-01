# Handoff - Initial Task - 2026-11-01T00:37:54Z

Durable detail: `.handoff/20261101T003754Z_INITIAL_TASK.md`

## Initial task for next session
**START HERE: Verify golden/integrity status is clean before making any changes.**

1. `git status --short` and `git log -1 --oneline` — confirm clean baseline, no leaked verification output in `experiments/`.
2. `SEED=42 bash scripts/check.sh` — must pass cleanly (goldens, data coverage, portfolio-opt tests).
3. If `.verify_snapshot/` exists with `ACTIVE.json` or `check.sh` reports a pending/stale snapshot, recover first: `SEED=42 python3 run_all_verification.py --restore-only`.

## Critical constraints
- Goldens are canonical (`experiments/*.json` must match HEAD / pinned baseline). Never overwrite via verification; restore before committing if interrupted.
- Do not re-pin goldens to silence numeric drift (E049 / ill-conditioned tangency QP).
- Data coverage: all driver inputs git-tracked and pinned in `ledger/data_baseline.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- If you make source changes, run `python3 -m py_compile` on touched files and re-run `scripts/check.sh`.

## Quick commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --restore-only
```
