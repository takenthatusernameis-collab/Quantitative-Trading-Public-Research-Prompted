# Handoff — Initial Task Message

**Timestamp:** 2026-11-19T21:06:52Z
**Canonical SHA-256:** (computed after write)
**HEAD at creation:** `9191ac1445b6effbb7d562a5fa9a95a28eafb0c0` on `main` at `origin/main` (`chore(kilo): checkpoint agent session`)

## Task

No specific task was provided in this session. The next agentic work session should review this repository's current state and determine the next objective.

## Context

- Repository: Quantitative-Trading-Public-Research-Prompted
- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- See `AGENTS.md` for project commands, conventions, and verification suite usage.
- Research phase is complete (E001–E043). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.

## Instructions for Next Session

1. Read `AGENTS.md` for project conventions.
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status.
3. If a new task is provided, begin by exploring the relevant code and data directories.

## Verification Scopes

- `SEED=42 bash scripts/check.sh` — fast convention-robustness + template validation.
- `SEED=42 python3 run_all_verification.py --extended` — full driver re-execution vs committed goldens.
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only (no writes).

## Integrity Rules

- Never commit verification output; restore goldens before committing (`run_all_verification.py --restore-only`).
- Never re-pin goldens/data baseline as a side effect of running the suite.
- Never commit `__pycache__`.

## Key References

- `ledger/RESEARCH_LEDGER.md` — canonical research record.
- `ledger/golden_baseline.json` — SHA-256 fingerprint of the 107 pinned golden artifacts.
- `ledger/data_baseline.json` — data cache coverage baseline.
- `AGENTS.md` — project commands and conventions.

## Open Items

- E041/E042 grid artifacts drift by 29–133 numeric differences (ill-conditioned QP, 1-ulp sensitivity). Do **not** re-pin to silence.
- E030 drifts in extended verification (yfinance non-reproducibility); pinned panel committed.
- `numpy`/`pandas`/`scipy` are **not** importable on this runner at handoff time; `pip install -r requirements.txt` is required before any Python driver step.

## Recurring Handoff Procedure

1. Verify HEAD == `origin/main`; working tree clean apart from gitignored `__pycache__` churn.
2. Confirm no `.verify_snapshot/` or `.verify_reports/` (no interrupted verification run).
3. Run `python3 scripts/check_goldens_clean.py` and `python3 scripts/check_golden_baseline.py` (both must exit 0).
4. Write `handoff_<ISO8601>_INITIAL_TASK.md` at the repo root with this structure.
5. Mirror byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
6. Repoint stable aliases (`HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`, `handoff/CURRENT`, `.kilo/handoff/CURRENT`) to the new artifact.
7. Do not commit; leave uncommitted pending explicit direction.

## Constraints Honored

No golden/data baseline re-pinned, no verification output committed, no new research performed, `__pycache__` not committed, no commit made (left uncommitted pending explicit direction).