# Handoff — Next Agentic Work Session

**Created:** 2026-11-20T10:41:12Z

## Initial Task

No specific task was assigned yet. Pick up from here:

1. Read `AGENTS.md` for project commands and conventions (verification suite, golden files, baseline integrity).
2. Inspect `git status` / `git diff` to confirm whether `experiments/*.json` hold goldens or driver output from an interrupted run; restore via `SEED=42 python3 run_all_verification.py --restore-only` if needed.
3. Await user instruction before making changes.

**Constraints:** Do not commit verification output. Do not re-pin goldens as a side effect of running the suite. Always use `SEED=42`.
