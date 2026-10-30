# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-30T19:15:25Z (UTC)
**Branch:** `main` (up to date with origin/main)
**HEAD:** `d88e0b9`
**Working tree:** clean of source/data changes; only tracked `__pycache__/*.pyc` build artifacts modified (gitignored, not source).
**Verification snapshot:** none active (`.verify_snapshot/` absent).

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

This session performed no technical work — it only wrote this handoff. Before making any changes or running verification:

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD** → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py --restore-only`, or `git checkout -- experiments/`).
   - **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** `git status --short | grep -v __pycache__` shows no changes.
- **Verification state:** No active verification snapshot in `.verify_snapshot/` (check with `ls .verify_snapshot/ 2>&1 | head -3`).
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json` pins 107 tracked artifacts. `ledger/data_baseline.json` enforces cache coverage.
