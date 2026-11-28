# Agentic Work Session — Initial Task (durable handoff)

**Timestamp (UTC):** 2026-11-28T04:53:39Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch / HEAD:** `main` — `4c567c48` (== `origin/main`)

## Initial Task

HEAD carries a contaminated golden baseline: 5 of 107 pinned artifacts under `experiments/` differ from `ledger/golden_baseline.json` (pure float drift, no structural/string/gate changes). Recovery source `c5038332` (ancestor of HEAD) blobs match the pinned SHA-256 exactly. Recover the 5 files; do NOT re-pin. Do not commit unless asked.

1. Provision deps: `python3 -m pip install -r requirements.txt` (numpy/pandas missing here).
2. `SEED=42 python3 scripts/check_golden_baseline.py` (expect FAIL on 5 files).
3. `git checkout c5038332 -- experiments/cointegration_large_liquid.json experiments/dollar_neutral_lowbeta_large_liquid.json experiments/e037_portfolio.json experiments/e042_lead_config_confirmatory.json experiments/pairs_large_liquid.json`
4. Re-verify: `SEED=42 python3 scripts/check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH".
5. `SEED=42 python3 scripts/check_data_coverage.py` (PASS, 35 inputs).
6. `SEED=42 bash scripts/check.sh` (fast offline sanity).
7. Run `SEED=42 python3 run_all_verification.py --extended` once deps present; confirm 0 diffs, no re-pinning.

Constraints: never re-pin to silence drift; never commit verification output; never leave a run half-finished; always SEED=42; commit only if user asks.

*This handoff was created for the next agentic work session.*