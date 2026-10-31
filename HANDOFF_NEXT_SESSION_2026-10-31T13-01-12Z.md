# HANDOFF: Next Agentic Work Session

**Timestamp (UTC):** 2026-10-31T13:01:12Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes
**Branch:** main
**HEAD:** 90c61f3 chore(kilo): checkpoint agent session (2026-10-31 12:57:57 +0000)
**Working tree:** modified tracked files only — 15 `__pycache__/*.pyc` binaries (stale bytecode caches, no source changes). No untracked source files. No staged changes.
**Verification snapshot:** `.verify_snapshot/` present but contains no `ACTIVE.json` marker. No run in progress; nothing to recover.

---

## Current State (from AGENTS.md)

- Research phase complete (E001–E049). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts live in `experiments/*.json` (goldens). Verification overwrites them during runs and restores them afterwards; a verification run must never be left half-finished.
- Baseline integrity is enforced by:
  - `scripts/check_goldens_clean.py` (working tree vs HEAD; detects stale `.verify_snapshot/`)
  - `scripts/check_golden_baseline.py` (compares tracked artifacts to `ledger/golden_baseline.json` SHA-256)
  - `scripts/check_data_coverage.py` (ensures every `data.download()` cache exists, is git-tracked, and matches `ledger/data_baseline.json`)
- Data: cached parquet in `data/` (gitignored except pinned vintages). Fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (makes E029 offline-reproducible). `QUANT_RESEARCH_OFFLINE=1` is used by verification.
- Optimizer determinism note (ledger E049): tangency QP can have ill-conditioned behavior; E041/E042 grid artifacts may show numeric drift (accepted up to tolerance in some blocks) — do **not** re-pin goldens to silence optimizer drift.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`). Template at `.github/workflow-templates/verification-gate.yml`.

## Known pre-existing drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.
- **E042 lead**: `/placebo_constrained` block deliberately re-pinned 2026-10-20 (ledger E049); `/primary` reproduces to 5e-9. Do **not** re-pin.

## Recent commit activity

HEAD `90c61f3` is a `chore(kilo): checkpoint agent session`. It added only `HANDOFF_NEXT_SESSION_2026-10-31T12-59-43Z.md`. No source code, strategy, gate, or research decision changed; the working tree carries only stale tracked `__pycache__/*.pyc` bytecode modifications.

---

## Clear Initial Task (for next session)

**Goal:** Confirm baseline integrity and confirm the repo is in a clean, reproducible state before making any changes.

**Steps (in order):**

1. **Check git state**
   ```bash
   git status --short
   git log -1 --oneline
   ```
   Expected: only the 15 stale `__pycache__/*.pyc` modifications shown above. If any source file or `experiments/*.json` differs from HEAD, stop and report.

2. **Run fast integrity checks (offline, no golden writes)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs py_compile, convention checks, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, the unittest suite (json/goldens/golden_baseline/drift_report/data_coverage/portfolio_opt), `verify_convention_robustness.py`, `validate_template.py`, and `check_experiment_imports.py`.

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
- The 15 modified `__pycache__/*.pyc` files are tracked in git (unusual for this repo) and are stale bytecode; they are not source changes. Leave them alone unless you intentionally recompile.

---

## Key Files to Read First

- `AGENTS.md` (project commands, conventions, baseline integrity)
- `ledger/RESEARCH_LEDGER.md` (experiment history and decisions; tail at E049)
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` (pinned fingerprints)
- `run_all_verification.py` (verification flow)
- `scripts/check.sh` (fast guards)
- `HANDOFF_REPRO_CAVEAT.md` (E041/E042 reproducibility caveat documentation)

---

## Handoff Metadata

- **Created by:** Kilo (agentic session)
- **Reason:** Durable handoff for next agentic work session; timestamped initial task message per request.
- **Next action:** Execute the initial task above.