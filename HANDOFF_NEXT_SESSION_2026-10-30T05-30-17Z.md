# HANDOFF — 2026-10-30T06:28:03Z

## Initial Task
**No outstanding task. Next session: run baseline integrity check before any changes.**

## Context
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts in `experiments/*.json` are golden baselines; never leave verification half-finished.

## Required Steps
1. `SEED=42 bash scripts/check.sh` — must pass (goldens clean, baseline pinned, data coverage pinned, tests pass).
2. Only then proceed with any requested work.

## Recovery
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

## Read First
- `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.

## Rules
- Never commit verification output; restore before committing.
- Do not re-pin goldens/data as a side effect; only via explicit `--update`.
- Always use `SEED=42`.
