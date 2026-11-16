# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T08:34:46Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `baa3d32d` (`chore(kilo): checkpoint agent session`) on `main`
**Remote:** `origin` = `https://github.com/takenthatusernameis-collab/Quantitative-Trading-Public-Research-Prompted`. Re-confirm `git status` before any push.

## Project state (at handoff)

- Research phase **complete (E001–E051)**; all experiments are pre-registered with fixed gates/falsification expectations. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Convention v1.2.3: **close-to-close primary**; overnight decomposition reported alongside every strategy.
- `experiments/*.json` are **canonical golden artifacts**. Never capture or commit verification output as a new baseline.
- No interrupted verification: `.verify_snapshot/` and `.verify_reports/` are absent; goldens intact.
- Working tree: only tracked `__pycache__/*.pyc` files are modified (produced by this session's read-only checks). `experiments/e042_quick.json` exists but is gitignored. **Do not commit .pyc files.**
- Delta since prior handoff (`handoff_2026-11-16T08-32-36Z_INITIAL_TASK.md`, HEAD `112a12b9`): HEAD advanced `112a12b9` → `baa3d32d` (a `chore(kilo): checkpoint agent session` commit). The non-`__pycache__` diff is empty; no changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `ledger/`. This handoff is a fresh timestamped durable entry point.

## Dependency state in this sandbox (read before running the suite)

- `numpy` and `pandas` are **not installed** here (`ModuleNotFoundError`).
- The standard-library repo guards were verified green this session (see below).
- Dependency-gated unit tests cannot run until deps are installed:
  - `tests.test_portfolio_opt` → `ModuleNotFoundError: No module named 'numpy'`
  - `tests.test_data_coverage` → `ModuleNotFoundError: No module named 'pandas'` (3 errors)
  These are environmental, not repository defects.
- `scripts/check.sh` uses `set -euo pipefail` and stops at `test_portfolio_opt` until dependencies are installed. Install first:

  ```bash
  python3 -m pip install --break-system-packages -r requirements.txt
  ```

## Verified this session (read-only; no verification run)

- `python3 scripts/check_json_artifacts.py` → 114 committed JSON artifacts parse OK
- `python3 scripts/check_goldens_clean.py` → all committed golden artifacts match HEAD
- `python3 scripts/check_golden_baseline.py` → all 107 pinned golden artifacts match the baseline fingerprint
- `python3 scripts/check_data_coverage.py` → all 35 pinned data inputs present, tracked and unchanged
- `python3 -m unittest tests.test_json_guard` → OK
- `python3 -m unittest tests.test_goldens_guard` → OK
- `python3 -m unittest tests.test_golden_baseline` → OK (9 tests)
- `python3 -m unittest tests.test_drift_report` → OK (22 tests)
- `python3 verify_convention_robustness.py` → ALL VERIFICATIONS PASSED
- `python3 scripts/validate_template.py` → OK
- `python3 scripts/check_experiment_imports.py` → ALL EXPERIMENT SCRIPT IMPORTS OK

## Initial task for the next agent (do first, in order)

1. **Dependencies (fresh sandbox only):**
   ```bash
   python3 -m pip install --break-system-packages -r requirements.txt
   ```
2. **Confirm baseline integrity (fast, offline):**
   ```bash
   SEED=42 bash scripts/check.sh        # or: make check
   ```
   Expect exit 0 and `=== All checks passed ===`.
3. **If integrity/baseline issues are reported, recover deliberately:**
   - Dirty goldens / stale `.verify_snapshot/` / interrupted run:
     `SEED=42 python3 run_all_verification.py --restore-only`
     (or restore the pinned artifacts per `ledger/golden_baseline.json`).
     Never leave a verification run half-finished; never commit captured verification output.
   - Golden fingerprint mismatch: resolve intentionally against `ledger/golden_baseline.json` / `ledger/data_baseline.json`. **Do not re-pin** as a side effect of running verification.
   - Re-run `SEED=42 bash scripts/check.sh` after any recovery.
4. **Then stop and await explicit user direction.**
   - Do not run long verification (`make verify-quick/extended/full`), invent experiments, move gates/outcomes, or alter research artifacts unprompted.
   - Do not modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without an explicit request and a justified diff.

## Quick reference

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py                # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Open items (do not resolve silently)

- **E041:** 133 numeric diffs remain (1-ulp QP sensitivity) after the optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin.** (ledger E049)
- **E042 lead:** PARTIAL (3/5 gates); min-var confirmatory (n_sim=50) passes convention robustness but the tangency grid drifts. (ledger E049)
- **CI gate:** only the template `.github/workflow-templates/verification-gate.yml` exists; a maintainer must create the real workflow via the GitHub UI (repo `GITHUB_TOKEN` lacks `workflows` push permission).
- **Promotion discipline:** any sensitivity-grid-clearing config requires a dedicated pre-registered confirmatory run with a full placebo before promotion.

## Artifact

- **Primary:** `handoff_2026-11-16T08-34-46Z_INITIAL_TASK.md`
- Mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Generic canonical handoff pointers repointed to this file via `scripts/repoint_handoff.py`.

*Generated 2026-11-16T08-34-46Z. No research artifacts modified.*

(End of file - total 92 lines)