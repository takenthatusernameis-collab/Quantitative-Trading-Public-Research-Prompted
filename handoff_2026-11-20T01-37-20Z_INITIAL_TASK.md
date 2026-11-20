# Handoff — Initial Task Message

**Timestamp:** 2026-11-20T01:37:20Z

## Task

Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.

## Context

- Repository: Quantitative-Trading-Public-Research-Prompted
- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- See `AGENTS.md` for project commands, conventions, and verification suite usage.
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Current HEAD: `73e68bde chore(kilo): checkpoint agent session`
- Stable aliases repointed to this artifact: `HANDOFF.md`, `INITIAL_TASK.md`, `LATEST.md`, `NEXT_SESSION.md`, plus `.handoff/` mirrors.

## Instructions for Next Session

1. Read `AGENTS.md` for project conventions.
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status.
3. If a new task is provided, begin by exploring the relevant code and data directories.

## Key Commands

```bash
# Fast convention check (offline, seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
```

## Critical Integrity Notes

- Never leave verification half-finished — it overwrites `experiments/*.json` and restores after.
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry.