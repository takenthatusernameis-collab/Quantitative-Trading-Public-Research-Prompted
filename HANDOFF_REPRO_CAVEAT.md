# Handoff: Reproducibility-caveat documentation for E041/E042 sensitivity grids

## What changed

No code, gate, decision, or validated construction was modified. Working
tree is clean except two documentation files:

- `ledger/RESEARCH_LEDGER.md` — E042 Erratum 4 (reproducibility caveat) + a
  correction to the E042b artifact-reconciliation claim.
- `README.md` — reproducibility section rewritten to state which drivers are
  byte-exact and which are environment-sensitive.

## What was actually verified (evidence)

Dependencies are installed and match `requirements.txt` exactly (numpy 2.5.4,
pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance
1.7.0) on Python 3.12.3. The 2026-10-12 data vintage is cached in `data/`.

| Driver | Golden | Fresh output | Result |
|--------|--------|--------------|--------|
| `run_e012.py` | 0 diffs | — | EXACT |
| `run_e023.py` | 0 diffs | — | EXACT |
| `run_e039.py` | 0 diffs | — | EXACT |
| `run_e037.py` | 28 numeric diffs, ~1e-7 rel | gate decisions unchanged | float drift |
| `run_e041.py` | grid 360 diffs, main 9273 diffs | — | NOT reproducible |
| `run_e042.py --n-sim 50` | grid 210 diffs, main 6592 diffs | — | NOT reproducible |
| `run_e042_lead.py` | 22 diffs (OOS 0.866->0.822, beta -0.001->+0.035) | deterministic across same-seed runs | NOT byte-exact |

- `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===` (107/107
  committed JSON artifacts parse; convention robustness 15 strategies; all
  27 experiment scripts import OK).
- `SEED=42 python3 run_all_verification.py --extended` -> **FAILURES
  DETECTED** (13 of 26 drivers exceed `numeric_tol=1e-4`; all are numeric
  drift, no structural/string differences, no missing goldens, no list
  length changes). The suite's snapshot/restore mechanism worked: after the
  run, `git status` showed only the two documentation files modified.
- Committed-baseline internal consistency confirmed: the E042 grid entry for
  `max_sharpe, beta<=0.1, 63d, macro_inclusive_3` (grid[15], OOS 0.866 /
  beta -0.001) matches the E042b lead golden; the E041 grid entry for the same
  config matches the E042 grid entry. The 7/96 (E042) and 8/96 (E041)
  market-neutral config counts recompute identically from the committed
  goldens.
- `python3 -m py_compile scripts/check_json_artifacts.py
  verify_convention_robustness.py run_all_verification.py` -> OK.

## What remains unresolved

- The E041/E042 sensitivity grids and the full E042 confirmatory golden are
  not byte-reproducible in this sandbox. Root cause is the SLSQP walk-forward
  optimizer in `src/portfolio_opt.py` (BLAS/LAPACK- and summation-order-
  sensitive); it is not a code regression and not a data-vintage shift. The
  exact reproduction environment that generated the committed goldens is not
  available here.
- No gate or decision is affected: E041 stays REJECTED (3/5, G3
  market-neutrality fails), E042 stays PARTIAL (4/5, G2 fails), E042b stays
  REJECTED (4/5, G2 fails) under both the committed and the drifted values.
- CI gate workflow (`.github/workflows/verification-gate.yml`) still requires
  maintainer action (GitHub UI) — automated agents cannot push workflows.

## Which approaches have already failed and why

- Regenerating the E041/E042 goldens from the current code: the fresh output
  is internally consistent and deterministic across same-seed runs, but it
  would replace the committed baseline with environment-specific numbers,
  breaking cross-artifact consistency (the E042 grid would no longer match
  the E042b lead golden). Prohibited by the "do not modify committed goldens"
  constraint and would destroy the grid's role as the ground-truth record of
  the grid-selected config.
- Weakening `numeric_tol` or skipping drivers: prohibited by task constraints.
- Claiming the goldens reproduce exactly: disproven by direct measurement
  (210/6592/360/9273 diffs), so the claim was corrected in the docs rather
  than left standing.

## One precise next task

The repository is in a clean, documented state. The only remaining durable
action outside agent scope is the maintainer-gated CI workflow creation
(template at `.github/workflow-templates/verification-gate.yml`). If a bounded
in-session task is desired, the lowest-risk option is to re-run
`SEED=42 bash scripts/check.sh` (already passing) and confirm `git diff`
contains only `README.md` and `ledger/RESEARCH_LEDGER.md`.

### Constraints
- Do NOT modify committed goldens; rely on `run_all_verification.py`'s
  backup/restore mechanism.
- Honor `SEED=42` and the cached 2026-10-12 parquet vintage.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or
  validated constructions (`src/backtest.py`, `src/strategies.py`,
  `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Do not weaken comparison tolerances or skip drivers to make the suite pass.