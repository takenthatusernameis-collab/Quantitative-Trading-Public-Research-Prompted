# Agentic Handoff

**Created:** 2026-11-12T05:05:20Z
**Session:** New session - 2026-11-12T05:05:18.534Z
**Status:** Initial — no work completed yet.

## Repository state

- Repo: quantitative trading research (2014–2026 US equities/futures/macro)
- Research phase complete (E001–E043). Validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Committed experiment artifacts under `experiments/*.json` are canonical goldens; verification suite backs them up and restores them.
- `.kilo/` is empty (no commands/agents yet). Board is empty.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).

## Clear initial task (next session)

Run the fast convention-robustness check + template validation and confirm baseline integrity:

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

This runs `py_compile`, `check_goldens_clean.py` (working tree vs HEAD under `experiments/`), `check_golden_baseline.py` (SHA-256 vs `ledger/golden_baseline.json`), `check_data_coverage.py`, and `tests/test_portfolio_opt.py`. It is offline, seconds-long, and writes nothing to `experiments/`.

**Success criterion:** `scripts/check.sh` exits 0 with no golden mismatch or coverage failure. If a mismatch is reported, fix it before committing (do not let a verification run capture output into `experiments/`).

## Notes

- Never commit verification output; interrupted runs leave driver output in `experiments/` — restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- To re-pin a golden: `python3 scripts/check_golden_baseline.py --update` (puts replacement in the diff).
- To add a data input: commit the file and re-pin with `python3 scripts/check_data_coverage.py --update`.
