# HANDOFF — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-31T15:41:46Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes
**Branch:** main
**HEAD:** 10c366c chore(kilo): checkpoint agent session
**Working tree:** clean (no tracked changes, no untracked files). No `.verify_snapshot/` present — no interrupted verification run to recover.
**Durable handoff target:** this file (`HANDOFF_NEXT_SESSION_2026-10-31T15-41-46Z.md`). All `HANDOFF_*`/`handoff_*` symlinks (root and `.kilo/`) are repointed here.

---

## Current State (from AGENTS.md)

- Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts live in `experiments/*.json` (goldens). Verification overwrites them during runs and restores them afterwards; a verification run must never be left half-finished.
- Baseline integrity is enforced by:
  - `scripts/check_goldens_clean.py` (working tree vs HEAD; detects stale `.verify_snapshot/`)
  - `scripts/check_golden_baseline.py` (compares tracked artifacts to `ledger/golden_baseline.json` SHA-256)
  - `scripts/check_data_coverage.py` (ensures every `data.download()` cache exists, is git-tracked, and matches `ledger/data_baseline.json`)
- Data: cached parquet in `data/` (gitignored except pinned vintages). Fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (makes E029 offline-reproducible). `QUANT_RESEARCH_OFFLINE=1` is used by verification.
- Optimizer determinism note (ledger E049): tangency QP can have ill-conditioned behavior; E041/E042 grid artifacts may show numeric drift — do **not** re-pin goldens to silence optimizer drift.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`). Template at `.github/workflow-templates/verification-gate.yml`.

## Known pre-existing drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.
- **E042 lead**: `/placebo_constrained` block deliberately re-pinned 2026-10-20 (ledger E049); `/primary` reproduces to 5e-9. Do **not** re-pin.

## Recent commit activity

HEAD `10c366c` is a `chore(kilo): checkpoint agent session`. No source code, strategy, gate, or research decision changed; the working tree is clean.

---

## CLEAR INITIAL TASK (Start Here)

**Objective:** Verify repo integrity and establish clean baseline before any changes.

### Step 1: Check Git State
```bash
git status --short
git log -1 --oneline
git branch -a | head -5
```
**Expected:** Clean working tree, on main branch, HEAD `10c366c`. If dirty or unexpected commits, report and stop.

### Step 2: Run Fast Integrity Checks (offline, no golden writes)
```bash
SEED=42 bash scripts/check.sh
```
Runs py_compile, convention checks, golden/baseline/data-coverage guards, unittest suite, convention robustness, template validation, import checks.

### Step 3: Run Quick Verification (~8 min)
```bash
SEED=42 python3 run_all_verification.py
```
Re-runs 8 quick-block drivers, validates batch/regression. Goldens backed up and restored. Do not interrupt.

### Step 4: Report Results
Report: git state, check.sh pass/fail, verification summary, confirmation experiments unchanged vs baseline. If guards fail (stale snapshot, golden mismatch), stop and use `SEED=42 python3 run_all_verification.py --restore-only` to recover.

---

## Constraints
- Always use `SEED=42`
- Never leave verification half-finished
- Never commit verification output
- Never re-pin goldens, weaken tolerances, skip drivers, or change gate logic
- Never modify validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`)
- If unsure, read AGENTS.md first

---

(End of handoff)