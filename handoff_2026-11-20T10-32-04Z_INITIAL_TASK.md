# Durable Handoff — Initial Task Message

**Created:** 2026-11-20T10:44:14Z
**Session:** previous agentic work session (ended)
**Status:** no active task in progress

## Context

Repository: `Quantitative-Trading-Public-Research-Prompted` (quantitative-strategy research on 2014–2026 US equities, futures, macro).

Key conventions (see `AGENTS.md`):
- `experiments/*.json` are canonical research artifacts — never commit verification output over them.
- Reproducibility: always use `SEED=42`; offline runs use `QUANT_RESEARCH_OFFLINE=1`.
- Lint: `python3 -m py_compile` on changed files; no separate linter configured.
- Never commit unless explicitly asked.

Common commands:
- `SEED=42 bash scripts/check.sh` — convention-robustness check (~seconds, offline)
- `SEED=42 python3 run_all_verification.py --quick` (~8 min)
- `SEED=42 python3 run_all_verification.py --extended --skip-slow`

## Initial task for next session

None specified. The next agentic work session should:

1. Check `git status` and `git log --oneline -10` for the current state.
2. Confirm whether any verification run is half-finished (`.verify_snapshot/ACTIVE.json`); if so, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
3. Await the user's actual tasking before making changes.

This handoff is a placeholder. No code changes were requested or made in this session.
