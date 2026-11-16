# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T08:41:34Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `ad116037` (`chore(kilo): checkpoint agent session`) on `main`
**Remote:** `origin` = `https://github.com/takenthatusernameis-collab/Quantitative-Trading-Public-Research-Prompted`. `origin/main` currently equals `HEAD` (`ad116037`); re-confirm before any push.

## Project state (at handoff)

- Research phase **complete (E001–E051)**; all experiments are pre-registered with fixed gates/falsification expectations. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Convention v1.2.3: **close-to-close primary**; overnight decomposition reported alongside every strategy.
- `experiments/*.json` are **canonical golden artifacts**. Never capture or commit verification output as a new baseline.
- Working tree: **no research/content changes**. The only modified tracked files are pre-existing `__pycache__/*.pyc` files (`scripts/`, `src/`, `tests/`). **Do not commit .pyc files.**
- No interrupted verification observed: `.verify_snapshot/` and `.verify_reports/` are absent.
- **Dependency state (important this session):** the Python environment is **missing project dependencies** (`python3 -c "import pandas"` → `ModuleNotFoundError: No module named 'pandas'`). As a result `SEED=42 bash scripts/check.sh` exits **1**, but the failure is entirely in `tests.test_data_coverage` (3 errors, all `ModuleNotFoundError: No module named 'pandas'`). Every research-integrity check that ran before that point **passed**: all committed JSON artifacts parse, all committed goldens match HEAD, all 107 pinned golden artifacts match the baseline fingerprint, and all 35 pinned data inputs are present, tracked and unchanged. The `test_json_guard`, `test_goldens_guard`, `test_golden_baseline` and `test_drift_report` unit tests are OK. **Install dependencies (step 1 below) before treating `check.sh` as a pass/fail signal.**
- Delta since prior durable handoff (`handoff_2026-11-16T08-39-00Z_INITIAL_TASK.md`, HEAD `d5a8d726`): a single checkpoint commit `ad116037` advanced HEAD; it touches only handoff files and pointer symlinks (540 paths, predominantly symlinks) — **no research content** (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, ledgers/baselines) changed.
- Prior durable handoff: `handoff_2026-11-16T08-39-00Z_INITIAL_TASK.md`.

## Initial task for the next agent (do first, in order)

1. **Dependencies (required in this sandbox — pandas is currently absent):**
   ```bash
   python3 -m pip install --break-system-packages -r requirements.txt
   python3 -c "import pandas, numpy, scipy, statsmodels; print('deps ok')"
   ```
2. **Confirm baseline integrity (fast, offline):**
   ```bash
   SEED=42 bash scripts/check.sh        # or: make check
   ```
   Expect exit 0 and `=== All checks passed ===`. If it still fails, read the failing step: the `tests.test_data_coverage` `ModuleNotFoundError` means step 1 did not take effect; any other failure is a real integrity issue.
3. **If integrity/baseline issues are reported, recover deliberately:**
   - Dirty goldens / stale `.verify_snapshot/` / interrupted run:
     ```bash
     SEED=42 python3 run_all_verification.py --restore-only
     ```
     (or restore pinned artifacts per `ledger/golden_baseline.json`). Never leave a verification run half-finished; never commit captured verification output.
   - Golden/data fingerprint mismatch: resolve intentionally against `ledger/golden_baseline.json` / `ledger/data_baseline.json`. **Do not re-pin** as a side effect of running verification.
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

- **Primary:** `handoff_2026-11-16T08-41-34Z_INITIAL_TASK.md`
- Generic canonical handoff pointers repointed to this file via `scripts/repoint_handoff.py` (mirrored through the generic symlinks under `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`).

*Generated 2026-11-16T08:41:34Z. No research artifacts modified.*