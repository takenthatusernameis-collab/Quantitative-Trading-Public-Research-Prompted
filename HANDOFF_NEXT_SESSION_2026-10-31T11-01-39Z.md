# HANDOFF: Next Agentic Work Session

**Timestamp (UTC):** 2026-10-31T11-01-39Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes
**Branch:** main
**HEAD:** dbf1b25 chore(kilo): checkpoint agent session
**Working tree:** 12 stale `__pycache__/*.pyc` modifications only (tracked bytecode caches, no source changes). No source files, no `experiments/*.json`, no staged changes, no untracked source files.
**Verification snapshot:** none active (`.verify_snapshot/` absent, no `ACTIVE.json`). Nothing to recover.

---

## Clear Initial Task (for next session)

**Goal:** Confirm baseline integrity and a clean, reproducible repo state before making any changes.

**Steps (in order):**

1. **Check git state**
   ```bash
   git status --short
   git log -1 --oneline
   ```
   Expected: only the 12 stale `__pycache__/*.pyc` modifications above. If any source file or `experiments/*.json` differs from HEAD, stop and report.

2. **Run fast integrity checks (offline, no golden writes)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs py_compile, convention checks, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, the unittest suite, `verify_convention_robustness.py`, `validate_template.py`, and `check_experiment_imports.py`.

3. **If `check.sh` passes, run quick verification (restores goldens)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   (~8 min). Re-runs the 8 drivers in the quick block and validates batch/regression. Goldens are backed up and restored; do not interrupt.

4. **Report outcome**
   - If any guard fails (golden mismatch vs HEAD/baseline, stale snapshot, missing data cache), **stop and report**. Do not re-pin goldens as a side effect of verification. To recover from an interrupted/stale snapshot:
     ```bash
     SEED=42 python3 run_all_verification.py --restore-only
     ```
   - If all pass, report: git state, `check.sh` result, `run_all_verification.py` summary, and confirmation that `experiments/*.json` are unchanged vs baseline.

**Notes / Gotchas:**
- Always use `SEED=42`.
- Never leave verification half-finished. Never commit verification output.
- Do not modify committed goldens, weaken tolerances, skip drivers, or change gate logic.
- Do not change validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Leave the 12 `__pycache__/*.pyc` modifications alone unless you intentionally recompile.

**Known open context:**
- E041/E042 sensitivity grids show residual numeric drift (ill-conditioned QP, 1-ulp sensitivity; ledger E049). Structural differences are resolved; decisions unaffected. Do **not** re-pin to silence drift.
- CI workflow `.github/workflows/verification-gate.yml` requires maintainer creation via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.

---

## Handoff Metadata

- **Created by:** Kilo (agentic session)
- **Reason:** Durable handoff for next agentic work session; timestamped initial task message per request.
- **Next action:** Execute the initial task above.
