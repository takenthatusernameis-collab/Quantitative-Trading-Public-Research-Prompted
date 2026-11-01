# Agentic Session Handoff

Created: 2026-11-01T08:18:49Z

## Current state

- Branch: `main`, up to date with `origin/main`. No local commits pending.
- Working tree: source is clean. Only `__pycache__/*.pyc` files show as modified
  (pre-existing tracked bytecode; not source changes — ignore).
- No verification run is in progress. `.verify_snapshot/` contains no `ACTIVE.json`
  marker, so no stale snapshot is pending.
- `experiments/*.json` goldens match HEAD (no golden drift).

## Recommended first task for the next session

Run the fast convention check to confirm nothing regressed:

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

If `check.sh` passes cleanly, the session is free to pick up the next research item
from `ledger/RESEARCH_LEDGER.md` (research phase E001–E043 is complete; see the
ledger for surviving validated strategies and any open items).

## Key commands (from AGENTS.md)

- `SEED=42 python3 run_all_verification.py` — quick verification (~8 min, 8 drivers)
- `SEED=42 python3 run_all_verification.py --extended` — extended (~21 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after an
  interrupted run (never leave a verification run half-finished)
- `python3 scripts/check_data_coverage.py --update` — re-pin after adding a data input
- `python3 scripts/check_golden_baseline.py --update` — re-pin a golden artifact

## Rules to remember

- Always use `SEED=42`.
- Never commit verification output; restore goldens before committing.
- The committed golden in `ledger/golden_baseline.json` is authoritative — do not
  re-pin to silence drift.
- The CI gate workflow cannot be created by automated agents (see AGENTS.md CI section).
