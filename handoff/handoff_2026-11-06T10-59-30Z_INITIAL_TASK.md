# Handoff — Initial Task Message

**Created:** 2026-11-06T13:57:47Z

## Task

No active task yet. This is the durable handoff placeholder for the next agentic work session.

## Repository context

Quantitative-strategy research repo (US equities, futures, macro; 2014–2026). Research phase complete (E001–E043); validated strategies in `ledger/RESEARCH_LEDGER.md`.

Key conventions (see `AGENTS.md`):
- `experiments/*.json` are canonical golden artifacts — never left half-finished after a verification run.
- `SEED=42` always; verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Do not commit verification output; restore goldens with `run_all_verification.py --restore-only`.
- Run `python3 -m py_compile` on changed files (no separate linter).

Common commands:
- `SEED=42 bash scripts/check.sh` (fast convention-robustness check)
- `SEED=42 python3 run_all_verification.py` (verify-quick, ~8 min)
- `SEED=42 python3 run_all_verification.py --extended`
- `SEED=42 python3 run_all_verification.py --full`

## Notes for next session

Replace this file with a concrete, timestamped task when work begins.
