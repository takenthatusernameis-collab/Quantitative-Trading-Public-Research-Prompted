# Agentic Work Session Handoff

**Timestamp:** 2026-11-15T00:32:41Z
**Session ID:** Initial handoff for next agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** 4b0bc45c (main, in sync with origin/main; `git rev-list --left-right --count origin/main...HEAD` → `0 0`)

## Project Status

**Research Phase:** COMPLETE (Experiments E001–E043)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite:** Operational with multiple tiers (check, verify-quick, verify-extended, verify-full)

## Baseline Integrity (verified this session)

- `SEED=42 bash scripts/check.sh` → **exit 0, "=== All checks passed ==="**
  (py_compile, 114 JSON artifacts parse, goldens clean vs HEAD, 107 pinned
  goldens match baseline, 35 pinned data inputs present/tracked/unchanged,
  portfolio_opt tests, convention robustness, template validation, experiment
  imports).
- `scripts/check_json_artifacts.py` → 114 committed JSON artifacts parse OK
- `scripts/check_goldens_clean.py` → all committed golden artifacts match HEAD
- `scripts/check_golden_baseline.py` → all 107 pinned golden artifacts match baseline
- `scripts/check_data_coverage.py` → all 35 pinned data inputs present, tracked, unchanged
- Working tree: only tracked `__pycache__/*.pyc` build artifacts modified; no
  `.verify_snapshot/` or `.verify_reports/` present; no interrupted verification run.
- Delta vs prior durable handoff (E345 artifact `handoff_2026-11-15T00-29-20Z_INITIAL_TASK.md`,
  HEAD `9eef652a` → `4b0bc45c`): one checkpoint commit only; 1 path changed,
  **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`,
  `research_state/`. No research substance changed.

## Clear Initial Task for the Next Session

1. **Re-confirm environment**: run `SEED=42 bash scripts/check.sh`. If any module
   is missing (`ModuleNotFoundError` for pandas/yfinance/scipy/statsmodels), install
   with `pip3 install --break-system-packages -r requirements.txt` and re-run.
   Do **not** treat a missing-dependency error as a baseline failure.
2. **Read the ledger** `ledger/RESEARCH_LEDGER.md` (now through E345) to confirm
   current strategy dispositions. The repo is closed: E001–E051 research complete;
   durable-handoff refreshes run through E345 (E344 is a documented unrecorded-artifact gap).
3. **Do not change research substance** unless explicitly directed: no gates,
   pre-registration, falsification expectations, sensitivity grids, or validated
   constructions; do not re-pin any golden; do not commit verification output.
4. If the task is another durable-handoff refresh, follow the established routine:
   stamp a new `handoff_<TS>Z_INITIAL_TASK.md`, mirror it to `handoff/`, `HANDOFFS/`,
   `.handoff/`, `.kilo/`, `.kilo/handoff/` (both `handoff_`-prefixed and bare-timestamp
   names), run `python3 scripts/repoint_handoff.py <new-file>` to repoint generic
   pointers, and append a dated ledger record.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Recover goldens after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Baseline Integrity Notes

1. **`experiments/*.json`** are canonical research artifacts - the verification suite
   overwrites and restores them while it re-runs the drivers.
2. **Never leave a verification run half-finished** - use `--restore-only` to recover
   if interrupted (`git checkout -- experiments/` restores whatever HEAD holds; if HEAD
   carries a captured run, restore the pinned artifact from the last commit whose SHA-256
   matches `ledger/golden_baseline.json`).
3. **Golden baseline** pinned in `ledger/golden_baseline.json` - compare with
   `scripts/check_golden_baseline.py`. **Do not re-pin** as a side effect of running the
   verification suite.
4. **Data cache coverage** enforced via `scripts/check_data_coverage.py` - all inputs must
   be pinned. To add a data input, commit the file and re-pin with
   `python3 scripts/check_data_coverage.py --update`.
5. **Do not commit verification output** - restore goldens before committing.

## Reproducibility Requirements

- **Seed:** Always use `SEED=42`.
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside.
- **Data:** Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11
  vintages); E029 fundamentals separately pinned in `data/fundamentals/`.
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow,
  statsmodels, yfinance). `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.

## Known Drift Items (reporting-only; from ledger)

- **E030:** Reproduces with 0 diffs since 2026-10-20 (ledger E048).
- **E041:** 133 numeric differences (1-ulp sensitivity of ill-conditioned tangency QP;
  optimizer determinism fixed in ledger E049) — still exceeds 1e-4 tolerance.
- **E042/E041 grid artifacts:** Drift by 29-133 differences due to ill-conditioned QP.
- **Do NOT re-pin** E041/E042 to silence drift - see open items in the ledger.

## Environment

- Python 3 research repository.
- No separate linter configured (uses `python3 -m py_compile` + reproducibility checks).
- CI gate template at `.github/workflow-templates/verification-gate.yml` (a maintainer
  must create the actual workflow via the GitHub UI; the repo token lacks `workflows` push).

---

*This handoff was created at session initialization. Update as work progresses.*