# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-13T14:33:02Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `57c234ab65acc7dae61336b3e9e56def38cde63e` (`chore(kilo): checkpoint agent session`) on `main`, in sync with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working tree at handoff:** only tracked `__pycache__/*.pyc` bytecode files modified (by this session's `pip install -r requirements.txt` + `check.sh` run). **No source, data, experiment, or baseline changes.** `.verify_snapshot/` and `.verify_reports/` absent — no interrupted verification run to recover.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Validated survivors and decisions recorded in `ledger/RESEARCH_LEDGER.md` (E001–E043 research; E044+ are conformance/handoff refreshes; E051 is the last research entry).
- Canonical artifacts: `experiments/*.json` (138 tracked; 107 pinned goldens). Integrity pinned in `ledger/golden_baseline.json` and `ledger/data_baseline.json` (35 pinned data inputs).
- Supersedes prior durable handoff `handoff_2026-11-13T14-27-26Z_INITIAL_TASK.md` (HEAD `37fc5146`). Delta `37fc5146..57c234ab` over `experiments/ data/ src/ tests/ scripts/ ledger/AGENTS.md` is **empty** — the two intervening commits (`37fc5146`, `57c234ab`) touch only handoff bookkeeping (`.handoff/*` canonical pointers) and `research_state/workflow_run_diagnostics.jsonl`. No research/source/data/experiment/baseline substance changed.
- **Baseline guards re-verified at this handoff (deps installed first):**
  - `SEED=42 python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT** (exit 0)
  - `SEED=42 python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED** (exit 0)
  - `SEED=42 bash scripts/check.sh` → **ALL CHECKS PASSED** (exit 0). Note: the `data/panel.parquet` FAIL lines in that output are *internal to* `tests.test_data_coverage.TestCoverageGuard.test_missing_manifest_fails` (a unit test that deliberately breaks a manifest in a tempdir) — they are not a repository failure. The real guard, `check_data_coverage.py`, exits 0.

## Environment note (important for the next session)
- This session found the Python environment **missing pandas/numpy/scipy** (every `from src import data` import raised `ModuleNotFoundError: No module named 'pandas'`), which silently broke `tests.test_data_coverage` (3 errors) and would break any driver run.
- **Fixed by:** `pip install -r requirements.txt` (pinned: numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0). All now import cleanly and `check.sh` passes end-to-end.
- If the next session runs in a fresh environment, run `pip install -r requirements.txt` first.

## Initial task for the next session
1. **Establish baseline integrity before any changes**
   ```bash
   pip install -r requirements.txt   # if not already installed
   SEED=42 bash scripts/check.sh
   ```
   Confirms golden cleanliness/baselines, data coverage, compile/tests, and conventions. Do not commit if mismatches are reported.
2. **If verification/reproduction is requested**, run the appropriate suite (see `AGENTS.md`):
   - Quick: `SEED=42 python3 run_all_verification.py` (`make verify-quick`)
   - Extended/full as needed (`--extended`, `--full`)
   Suites overwrite and restore `experiments/*.json`; never leave a run half-finished. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
3. **Review context, then take only user-directed work**
   - Read: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and recent durable handoffs.
   - Proceed with maintenance or new research consistent with the completed phase and project conventions.

## Critical guardrails
- **Reproducibility:** always `SEED=42`; use pinned data vintages/caches (no live-network dependence in verification paths).
- **Goldens/baselines:** never replace `experiments/*.json` or re-pin `ledger/golden_baseline.json`/`ledger/data_baseline.json` as a side effect of verification. Re-pin only for genuine, reviewed changes (`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`).
- **Pre-registration & reporting:** new experiments must pre-register gates/falsification before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp optimizer sensitivity (`AGENTS.md`, ledger E049/open item) — do not re-pin to silence.
- **Do not commit verification output**; restore goldens before committing (`run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- **Do not commit `__pycache__/`** — the working tree shows tracked `.pyc` files modified by routine interpreter runs; these are noise, not substance.

## Pending work
- No explicit pending tasks recorded. Confirm baseline health, then await/execute user-directed work consistent with project conventions.