# Durable Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-26T19:07:40Z
**Session owner:** Kilo (agentic work session)
**Branch:** `main`
**Last commit:** `f91731e8` chore(kilo): checkpoint agent session

## Working tree state
Clean except `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (compiled `.pyc` files only — no source changes). No uncommitted source edits.

## Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

Canonical research artifacts live under `experiments/*.json` and must never be left half-finished by a verification run. The verification suite backs them up into the gitignored `.verify_snapshot/` (with `ACTIVE.json` pid marker) and restores them afterwards.

Key convention: always run with `SEED=42` and `QUANT_RESEARCH_OFFLINE=1` for verification (cache coverage is an enforced invariant — see `scripts/check_data_coverage.py`).

## Primary commands
- `SEED=42 bash scripts/check.sh` — fast convention-robustness check + template validation (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended verification (~21 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after interrupted run
- `python3 -m py_compile <changed_file>` — lint/typecheck equivalent (no separate linter configured)

## Next agentic work session — initial task
No explicit task was assigned in this session. The next session should:
1. Read `.kilo/handoff.md` (this file) for state and context.
2. Confirm the working tree is clean (only `__pycache__` expected).
3. Ask the user for the next task, or run `SEED=42 bash scripts/check.sh` to confirm baseline integrity before starting new work.
4. Never commit unless explicitly asked; never leave a verification run half-finished — always restore goldens with `--restore-only` if interrupted.

## References
- `AGENTS.md` — full project conventions, baseline integrity rules, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — validated strategies and experiment dispositions
- `.kilo/command/*.md`, `.kilo/agent/*.md` — Kilo commands and agents
