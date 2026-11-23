# Agent Handoff — 2026-11-23T07:30:01Z

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/HEAD: `8eab5ab1` chore(kilo): checkpoint agent session
- Environment: Linux, Python 3, research repo (quantitative strategies 2014–2026)

## Convention reminders (read AGENTS.md before acting)
- `experiments/*.json` are canonical research artifacts — never commit verification output.
- Use `SEED=42` for all runs.
- `make check` / `make verify-quick` / `make verify-extended` for verification.
- Golden baselines pinned in `ledger/golden_baseline.json`; data coverage pinned in `ledger/data_baseline.json`.
- `scripts/check.sh` runs convention-robustness check + template validation.

## Open task for next session
No specific task assigned yet. The working tree is clean at `8eab5ab1`. When a task arrives:
1. Read AGENTS.md fully.
2. Reproduce/verify against pinned goldens before making changes.
3. Never leave a verification run half-finished (restore with `--restore-only` if interrupted).
4. Commit only when explicitly asked.
