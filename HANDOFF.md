# Handoff — initial task message

**Timestamp:** 2026-10-28T08:39:05Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Status

No prior task context established yet. This is the initial handoff for the next agentic work session.

## Next agentic task

Define and begin the first concrete software-engineering task for this repository (quantitative-strategy research, `experiments/*.json` canonical artifacts).

Before touching anything:

1. Read `AGENTS.md` — baseline integrity, verification commands, and project conventions.
2. Confirm dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
3. Run a convention-only check: `SEED=42 bash scripts/check.sh` (or `make check`).
4. Only then pick a task (bug fix, experiment driver, refactor, test, or new data input).

## Repo commands

| Purpose | Command |
|---|---|
| Convention-robustness check | `SEED=42 bash scripts/check.sh` |
| Quick verification (~8 min) | `SEED=42 python3 run_all_verification.py` |
| Extended verification | `SEED=42 python3 run_all_verification.py --extended` |
| Restore goldens after interrupted run | `SEED=42 python3 run_all_verification.py --restore-only` |
| Typecheck changed Python files | `python3 -m py_compile <file>` |

## Critical constraints

- `experiments/*.json` are canonical artifacts — verification overwrites then restores them; never leave a run half-finished, never commit verification output.
- Reproducibility: always use `SEED=42`; run with `QUANT_RESEARCH_OFFLINE=1` where applicable; data inputs must be committed and pinned in `ledger/data_baseline.json`.
- Do not commit unless explicitly asked.
- No separate linter; `python3 -m py_compile` on changed files.
