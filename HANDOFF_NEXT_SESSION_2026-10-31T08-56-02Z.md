# HANDOFF: Next Agentic Work Session

**Timestamp (UTC):** 2026-10-31T08-56-02Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes
**Branch:** main
**HEAD:** f5d8936 chore(kilo): checkpoint agent session
**Working tree:** clean of tracked changes (no modifications pending).
**Verification snapshot:** none active (`.verify_snapshot/` absent, no `ACTIVE.json`). No run in progress; nothing to recover.

---

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
   This runs py_compile, convention checks, `check_goldens_clean.py`, `check_golden_baseline.py`, and related guards.

3. **If `check.sh` passes, run quick verification (restores goldens)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   (~8 min). This re-runs the 8 drivers in the quick block and validates batch/regression. Goldens are backed up and restored; do not interrupt.

4. **Report outcome**
   - If any guard fails (golden mismatch vs HEAD/baseline, stale snapshot, missing data cache), **stop and report**. Do not re-pin goldens as a side effect of verification. If you need to recover from a stale snapshot, use:
     ```bash
     SEED=42 python3 run_all_verification.py --restore-only
     ```
   - If all pass, report: git state, `check.sh` result, `run_all_verification.py` summary, and confirmation that `experiments/*.json` are unchanged vs baseline.

**Notes / Gotchas:**
- Always use `SEED=42`.
- Never leave verification half-finished. If interrupted, restore with `--restore-only` or `git checkout -- experiments/` as appropriate (see AGENTS.md).
- Do not commit verification output.
- Do not modify committed goldens, weaken tolerances, skip drivers, or change any gate logic.
- Do not change validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).

---

## Key Files to Read First
- `AGENTS.md` (project commands, conventions, baseline integrity)
- `ledger/RESEARCH_LEDGER.md` (experiment history and decisions)
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` (pinned fingerprints)
- `run_all_verification.py` (verification flow)
- `scripts/check.sh` (fast guards)
- `HANDOFF_REPRO_CAVEAT.md` (E041/E042 reproducibility caveat documentation)

---

## Handoff Metadata
- **Created by:** Kilo (agentic session)
- **Reason:** Durable handoff for next agentic work session
- **Next action:** Execute the initial task above
