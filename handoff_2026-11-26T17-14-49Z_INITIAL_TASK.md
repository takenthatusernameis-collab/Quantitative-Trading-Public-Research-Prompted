# Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-26T18:12:28Z

## Status
Repo is a Python quantitative-strategy research project. AGENTS.md documents commands:
- `SEED=42 bash scripts/check.sh` — convention robustness + template validation (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended (~21 min)

## Initial task
No task specified yet. The next agentic session should pick up a task from the user and:
1. Read `AGENTS.md` before running anything.
2. Use `SEED=42` for reproducibility.
3. Never leave `experiments/*.json` artifacts in a half-finished state; restore with `SEED=42 python3 run_all_verification.py --restore-only` if interrupted.
4. Run `python3 -m py_compile` on changed files (no separate linter configured).
5. Never commit unless explicitly asked.
