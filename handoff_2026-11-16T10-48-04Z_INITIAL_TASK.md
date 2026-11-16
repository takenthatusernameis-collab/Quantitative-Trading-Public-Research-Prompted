# Handoff: Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T10:48:04Z
**Workspace:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD context:** Inspect with `git status --short` and `git log -1 --oneline` before changes.

## Project state (as of this handoff)
- Research phase complete (E001–E043). Validated surviving strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`.
- Canonical experiment artifacts: `experiments/*.json` (golden baselines pinned in `ledger/golden_baseline.json` / `ledger/data_baseline.json`).
- Durable handoff pointers (`LATEST*`, `NEXT*`, `current*`, `handoff_LATEST*`, etc.) should reference this file.

## Initial task for next session
1. **Establish baseline health (no artifact drift):**
   - Run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm golden/data guards, JSON/template checks, and convention robustness are clean.
   - If any golden mismatch or stale `.verify_snapshot/ACTIVE.json` is reported, **do not proceed with new work** until recovered (`SEED=42 python3 run_all_verification.py --restore-only` or restore the pinned commit artifact per `AGENTS.md`).
2. **Review context before acting:**
   - Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md` (recent entries, esp. E045/E048/E049/open items), and `git status --short`.
   - Note: workspace may show modified `*/__pycache__/*.pyc` files; avoid committing bytecode/cache churn.
3. **Execute the user-requested objective (if provided in session):** perform the requested work with minimal, reproducible changes; follow pre-registration/golden-baseline conventions for any experiment or artifact edits.
4. **If no specific objective is given:** run `make check` (or `make verify-quick` if time/resources allow) and report status, including whether `experiments/*.json` remain clean vs HEAD and any known drift (e.g. extended-block E041 numeric sensitivity noted in `AGENTS.md`).
5. **Leave a durable handoff:** write/update a timestamped `handoff_*_INITIAL_TASK.md` (and pointer symlinks if appropriate) summarizing actions taken, verification results, and the next concrete task.

## Key constraints / reminders
- Always use `SEED=42` for verification/repro runs.
- Verification overwrites `experiments/*.json` during runs and must restore them; never leave a run half-finished. Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of verification; re-pin only with explicit intent and documented reason.
- E041/E042 exhibit known optimizer/QP 1-ulp numeric sensitivity in extended checks; do not "fix" by re-pinning goldens (see `AGENTS.md` / ledger E049).
- Prefer `make` targets / documented commands; do not commit secrets or generated verification reports outside intended locations.

## Suggested starting commands
```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

**End of handoff.**
