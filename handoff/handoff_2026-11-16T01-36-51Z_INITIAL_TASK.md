# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-16T01-36-51Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `751b1498d90e4cd042927cafb7856e312d758463` (`chore(kilo): checkpoint agent session`) on `main`
**Sync:** in sync with `origin/main` (`0 0`)

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase **complete (E001–E051)**; surviving
validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. All experiments
are pre-registered — never move goalposts post-hoc. Close-to-close is the v1.2.3
primary convention; overnight decomposition is reported alongside.

## Current state (as of this handoff)

- **Working tree:** clean except pre-existing modified tracked `__pycache__/*.pyc`
  files (under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`) —
  do **not** commit them. No research/source/data/experiment changes.
- **No interrupted verification:** `.verify_snapshot/` and `.verify_reports/` are absent;
  canonical `experiments/*.json` goldens are intact.
- **Baseline integrity verified this session:** `SEED=42 bash scripts/check.sh` →
  exit 0, `=== All checks passed ===`. This covers JSON-artifact parse (114 artifacts),
  `check_goldens_clean.py` (goldens match HEAD), `check_golden_baseline.py` (107 pinned
  goldens match), `check_data_coverage.py` (35 pinned data inputs present/tracked/unchanged),
  all guard unit tests, `verify_convention_robustness.py` (all strategy blocks PASS),
  template validation and experiment call/import checks.
- **Dependency note (important):** the sandbox starts **without** `numpy`/`pandas`/
  `scipy`/`statsmodels`/`yfinance`, and `scripts/check.sh` then fails inside
  `tests.test_data_coverage` with `ModuleNotFoundError`. Install first:
  `python3 -m pip install --break-system-packages -r requirements.txt`
  (done in this session; `check.sh` green afterwards). Without deps the
  repo-level guard scripts still pass individually — the failures are environmental,
  not repo-content failures.
- **Delta vs prior durable handoff** (`handoff_2026-11-16T01-32-13Z_INITIAL_TASK.md`,
  HEAD `cdcd9595`): only `research_state/workflow_run_diagnostics.jsonl` (workflow-run
  diagnostics capture) plus handoff bookkeeping changed. No research content
  (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`) changed.

## Initial task for the next agent (do first)

1. **Install deps if needed:** `python3 -m pip install --break-system-packages -r requirements.txt`.
2. **Confirm baseline:** `SEED=42 bash scripts/check.sh` (or `make check`).
   Expect exit 0 / `=== All checks passed ===`.
3. **If a real baseline issue appears:**
   - Dirty goldens / stale `.verify_snapshot/`: `SEED=42 python3 run_all_verification.py --restore-only`
     (or restore pinned artifacts per `ledger/golden_baseline.json`). Never commit captured verification output.
   - Golden fingerprint mismatch: resolve deliberately against `ledger/golden_baseline.json`;
     do not re-pin as a side effect of verification.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
4. **Then await explicit user direction.** Do not run long verification, invent experiments,
   or change gates/outcomes unprompted. Do not modify or re-pin `experiments/*.json`,
   `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`,
   or `data/` without explicit request and justified diff. Never leave a verification run
   half-finished.

## Quick reference

```bash
python3 -m pip install --break-system-packages -r requirements.txt  # deps (first run in a fresh sandbox)
SEED=42 bash scripts/check.sh                          # fast convention + guard checks
SEED=42 python3 run_all_verification.py                # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 verify_convention_robustness.py        # convention robustness only
SEED=42 python3 run_all_verification.py --restore-only # recover after interrupted run
```

## Open items (do not resolve silently)

- **E041 drift:** 133 numeric diffs (1-ulp QP sensitivity) remain post optimizer fix;
  decision REJECTED 3/5 unchanged. **Do not re-pin.** (ledger E049)
- **E042 lead:** PARTIAL (3/5 gates); min-var confirmatory (n_sim=50) passes convention
  robustness but tangency grid drifts. (ledger E049)
- **CI gate:** template `.github/workflow-templates/verification-gate.yml`; a maintainer
  must create the real workflow via the GitHub UI (automated agents cannot).
- **Promotion:** any sensitivity-grid-clearing config needs a dedicated pre-registered
  confirmatory run with full placebo before promotion.

## Handoff artifact

- Primary: `handoff_2026-11-16T01-36-51Z_INITIAL_TASK.md`
- Mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Generic canonical pointers repointed to this file via
  `python3 scripts/repoint_handoff.py handoff_2026-11-16T01-36-51Z_INITIAL_TASK.md`.

---
*Generated 2026-11-16T01-36-51Z for durable handoff to the next agentic work session.*