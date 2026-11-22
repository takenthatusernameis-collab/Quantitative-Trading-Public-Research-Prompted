# Durable Handoff — Next Agentic Work Session

**Created:** 2026-11-22T20:47:36Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Task

No new work requested yet. This is a clear initial task message placeholder for the next agentic work session.

When the next session begins:
1. Read `AGENTS.md` (project commands, conventions, verification gates).
2. Confirm the working tree is clean and no verification run is half-finished (no live `.verify_snapshot/ACTIVE.json`, no driver output under `experiments/`).
3. Ask the user for the actual task before taking any action.

## Repo conventions (from AGENTS.md)
- Never commit unless explicitly asked.
- `experiments/*.json` are committed goldens; verification overwrites then restores them. Never leave a verification run half-finished.
- `SEED=42` for all runs. `QUANT_RESEARCH_OFFLINE=1` during verification.
- Run `python3 -m py_compile` on changed files (no separate linter).
- Do not commit verification output.

## Quick commands
- `SEED=42 bash scripts/check.sh` — convention-robustness check (~seconds, offline)
- `SEED=42 python3 run_all_verification.py --skip-slow` — convention only
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after an interrupted run

## End of handoff
