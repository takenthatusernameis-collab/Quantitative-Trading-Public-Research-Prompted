# Agentic Work Session — Initial Task (durable handoff)

**Timestamp (UTC):** 2026-11-28T07:32:40Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch / HEAD:** `main` — `b580e317` (== `origin/main`)

## TL;DR — the one real task

**HEAD carries a contaminated golden baseline.** 5 of the 107 pinned artifacts under
`experiments/` differ from `ledger/golden_baseline.json`. This is a verification-run capture
(last-digit float drift only — no structural, string, or gate-flag changes), exactly the
checkpoint-capture failure mode AGENTS.md warns about. **Recover the 5 files from commit
`c5038332`; do NOT re-pin.**

## Verified state (2026-11-28T07:32:40Z)

- **HEAD** `b580e317` == `origin/main`; branch `main`.
- **Golden baseline: BROKEN at HEAD.** `SEED=42 python3 scripts/check_golden_baseline.py` → **FAIL (5 files)**:
  - `experiments/cointegration_large_liquid.json`
  - `experiments/dollar_neutral_lowbeta_large_liquid.json`
  - `experiments/e037_portfolio.json`
  - `experiments/e042_lead_config_confirmatory.json`
  - `experiments/pairs_large_liquid.json`
  The other 102 pinned artifacts match. Diff is pure floating-point drift.
- **Recovery source**: `c5038332` is an ancestor of HEAD; its blobs for the 5 files hash to the
  exact pinned SHA-256 in `ledger/golden_baseline.json`. Restoring from it is correct.
- **No interrupted run**: `.verify_snapshot/` absent.
- **Environment gap**: `numpy` / `pandas` are NOT importable here. Run
  `python3 -m pip install -r requirements.txt` before any driver or suite.

## Initial Task (do these in order, then stop)

Do not re-pin artifacts, run `check_golden_baseline.py --update`, overwrite goldens, or write
another handoff as a side effect. Do not commit unless the user explicitly asks.

1. Confirm no active verification run (`.verify_snapshot/` must not exist).
2. Provision environment — `python3 -m pip install -r requirements.txt`.
3. Reproduce the baseline failure — `SEED=42 python3 scripts/check_golden_baseline.py` (expect FAIL on 5).
4. Recover the canonical baseline (surgical, 5 files):
   ```bash
   git checkout c5038332 -- \
     experiments/cointegration_large_liquid.json \
     experiments/dollar_neutral_lowbeta_large_liquid.json \
     experiments/e037_portfolio.json \
     experiments/e042_lead_config_confirmatory.json \
     experiments/pairs_large_liquid.json
   ```
5. Re-verify the baseline — `SEED=42 python3 scripts/check_golden_baseline.py` → expect "ALL 107 PINNED GOLDEN ARTIFACTS MATCH".
6. Surface the diff to the user; commit ONLY if asked.
7. Confirm data coverage — `SEED=42 python3 scripts/check_data_coverage.py`.
8. Fast sanity check — `SEED=42 bash scripts/check.sh`.

## Key Constraints

- `experiments/*.json` are committed goldens — never re-pin to silence drift; never commit verification output.
- Always `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents; use local `make check` / `make verify*`.

*This handoff was created for the next agentic work session.*