# Agentic Handoff — 2026-11-27T06:46:04Z

## Initial task message for the next session

No specific coding task was assigned in this session. The only deliverable was
this durable handoff note itself.

## Repo state at handoff

- Working tree: clean except `src/__pycache__/cache_keys.cpython-312.pyc` (untracked build artifact, safe to ignore).
- HEAD: `d1027ccc chore(kilo): checkpoint agent session`
- Recent commits: a series of `chore(kilo): checkpoint agent session` checkpoints.

## Conventions to honor (per AGENTS.md)

- Always run with `SEED=42` for reproducibility.
- `experiments/*.json` are canonical golden artifacts — never commit verification output; restore via `python3 run_all_verification.py --restore-only` if interrupted.
- `make check` = fast convention-robustness check + template validation.
- `make verify-quick` / `make verify-extended` / `make verify-full` for verification runs.
- Cache coverage is enforced: every `data.download()` call site must resolve to a committed, SHA-256-pinned cache file (see `ledger/data_baseline.json`, `scripts/check_data_coverage.py`).
- Run `python3 -m py_compile` on changed Python files (no separate linter configured).

## Suggested next steps

1. Pick up any outstanding experiment driver or research task from `ledger/RESEARCH_LEDGER.md`.
2. If starting a verification run, ensure no other live run owns `.verify_snapshot/` (the suite refuses to start while a live run owns it).
3. Re-pin any new data input with `python3 scripts/check_data_coverage.py --update` before committing.

-- handoff created 2026-11-27T06:46:04Z --
