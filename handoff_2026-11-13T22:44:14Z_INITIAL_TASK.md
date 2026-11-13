# Agentic Handoff — Initial Task Message

**Created:** 2026-11-13T22:45:01Z
**Session:** previous agentic work session
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task for next session

Run the convention-robustness + template validation check and report the result:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If it passes, proceed to quick verification:

```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```

## Repo context

- Quantitative-strategy research repo on 2014–2026 US equities, futures, macro data.
- Research phase complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` — never commit verification output; restore via `run_all_verification.py --restore-only` if interrupted.
- `scripts/check.sh` includes `check_goldens_clean.py` and `check_golden_baseline.py`; a golden mismatch must be fixed before committing.
- Lint: `python3 -m py_compile` on changed files (no separate linter configured).
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).

## Notes

- Do not invent or guess URLs; use URLs from user messages/local files only.
- Peer coordination via the shared board if multiple agents run.
