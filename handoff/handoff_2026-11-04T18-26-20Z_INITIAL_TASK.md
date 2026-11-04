# Handoff — 2026-11-04T19:25:37Z

## State
- Branch: clean working tree (git status empty)
- HEAD: b6bfd31 `chore(kilo): checkpoint agent session`
- Board: empty (no pending peer messages)
- Repo: quantitative-strategy research (2014–2026 US equities/futures/macro); research phase complete E001–E043; see `ledger/RESEARCH_LEDGER.md`

## Conventions to honor
- Seed: always `SEED=42`
- `experiments/*.json` are canonical goldens — verification overwrites then restores them; never leave a run half-finished; never commit verification output
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
- Lint: `python3 -m py_compile` on changed files (no separate linter)
- Offline: drivers run with `QUANT_RESEARCH_OFFLINE=1`; data inputs must be pinned per `ledger/data_baseline.json`

## Clear initial task for next session
TBD — no specific task was assigned in this session. The next agentic session should:
1. Read this HANDOFF.md and the board.
2. Confirm the intended task/objective with the user (or proceed if one was given out-of-band).
3. Execute the task following repo conventions above.
4. Leave an updated HANDOFF.md with the new timestamp and status before ending.

## Quick commands
- Convention check: `SEED=42 bash scripts/check.sh`
- Verify quick: `SEED=42 python3 run_all_verification.py`
- Single driver example: `SEED=42 python3 experiments/run_e042.py --n-sim 50`
