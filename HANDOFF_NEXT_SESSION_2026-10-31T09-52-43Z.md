# HANDOFF: Next Agentic Work Session (LATEST)

**Timestamp (UTC):** 2026-10-31T09-58-59Z
**Source file:** `HANDOFF_NEXT_SESSION_2026-10-31T09-58-59Z.md`
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** 2e14a78 chore(kilo): checkpoint agent session
**Working tree:** 12 modified `__pycache__/*.pyc` binaries (stale bytecode caches, no source changes). No untracked source files. No staged changes.
**Verification snapshot:** none active. No run in progress; nothing to recover.

## Clear Initial Task (for next session)

**Goal:** Confirm baseline integrity and confirm the repo is in a clean, reproducible state before making any changes.

**Steps (in order):**

1. **Check git state**
   ```bash
   git status --short
   git log -1 --oneline
   ```

2. **Run fast integrity checks (offline, no golden writes)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```

3. **If `check.sh` passes, run quick verification (restores goldens)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   (~8 min). Goldens are backed up and restored; do not interrupt.

4. **Report outcome**
   - If any guard fails (golden mismatch vs HEAD/baseline, stale snapshot, missing data cache), **stop and report**. Recover with:
     ```bash
     SEED=42 python3 run_all_verification.py --restore-only
     ```
   - If all pass, report git state, `check.sh` result, verification summary, and confirmation `experiments/*.json` unchanged vs baseline.

**Notes / Gotchas:**
- Always use `SEED=42`. Never leave verification half-finished.
- Do not commit verification output. Do not re-pin goldens or change gate logic as a side effect of verification.
- Do not change validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).

**Key files:** `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `run_all_verification.py`, `scripts/check.sh`.

**Full detail:** see `HANDOFF_NEXT_SESSION_2026-10-31T09-58-59Z.md`.
