# HANDOFF — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-31T16:42:32Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git repo:** yes
**Branch:** main
**HEAD:** 894e484 chore(kilo): checkpoint agent session
**Working tree:** clean (no tracked changes, no untracked files). No `.verify_snapshot/` present — no interrupted verification run to recover.
**Durable handoff target:** this file (`HANDOFF_NEXT_SESSION_2026-10-31T16-42-32Z.md`). All `HANDOFF_*`/`handoff_*` symlinks (root and `.kilo/`) repointed here.

---

## Current State

- Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts live in `experiments/*.json` (goldens). Verification overwrites them during runs and restores them afterwards; never leave verification half-finished.
- Baseline integrity enforced by `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Data cached in `data/` (pinned vintages/fundamentals). `QUANT_RESEARCH_OFFLINE=1` used by verification.
- Optimizer determinism note (E049): tangency QP ill-conditioned — E041/E042 may show numeric drift; do **not** re-pin goldens.

## Known pre-existing drift (reporting-only)

- **E041**: ~133 numeric diffs (ill-conditioned QP). Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities. Do **not** re-pin.
- **E029/E030 inputs pinned** for offline reproducibility; do not "fix" by re-running.

---

## CLEAR INITIAL TASK (Start Here)

**Objective:** Verify repo integrity and establish clean baseline before any changes.

### Step 1: Check Git State
```bash
git status --short
git log -1 --oneline
git branch -a | head -5
```
**Expected:** Clean working tree, on main branch, HEAD `894e484`. If dirty or unexpected commits, report and stop.

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

## Known Caveat (read before extended runs)

E041/E042 sensitivity grids and the E042 confirmatory golden are not byte-reproducible in this sandbox (SLSQP/BLAS float drift in `src/portfolio_opt.py`). Committed goldens stand; gates/decisions unchanged (E041 REJECTED, E042 PARTIAL). See `HANDOFF_REPRO_CAVEAT.md`.

---

(End of handoff)
(End of file)
