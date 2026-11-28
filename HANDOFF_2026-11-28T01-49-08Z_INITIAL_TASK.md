# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-28T01:49:08Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `3c4076ca05a9bd86bf7d309a24933338e58f0fc2` (2026-11-28 01:49:01 +0000) == origin/main
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean except `src/__pycache__/cache_keys.cpython-312.pyc` (untracked build artifact). No `.verify_snapshot/`.

Written at the explicit request of the user: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*

This file supersedes `HANDOFF_2026-11-27T23-42-48Z_INITIAL_TASK.md`.

---

## CLEAR INITIAL TASK (do these in order, then stop)

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist.
2. **Provision environment** — `pip install -r requirements.txt` (`numpy`/`pandas` not importable here).
3. **Reproduce baseline failure** — `SEED=42 python3 scripts/check_golden_baseline.py` (expect 5 differing artifacts: `cointegration_large_liquid.json`, `dollar_neutral_lowbeta_large_liquid.json`, `e037_portfolio.json`, `e042_lead_config_confirmatory.json`, `pairs_large_liquid.json`).
4. **Recover canonical baseline** — `git checkout c5038332 -- experiments/` (c5038332 is the newest clean commit; HEAD carries the captured verification run). Then re-run step 3 → expect `ALL 107 PINNED GOLDEN ARTIFACTS MATCH`.
5. **Confirm** — `SEED=42 python3 scripts/check_goldens_clean.py` and `SEED=42 python3 scripts/check_data_coverage.py`.
6. **Fast sanity** — `SEED=42 bash scripts/check.sh`.

Do not re-pin artifacts, overwrite goldens, or write another handoff as a side effect. If all pass, report baseline clean and proceed to real work.

## Constraints

- `experiments/*.json` are committed goldens; never commit verification output.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`.
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- Do not manufacture another handoff-refresh as the deliverable.
