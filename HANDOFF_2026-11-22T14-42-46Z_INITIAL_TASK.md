# Agentic Work Session Handoff — Initial Task Message

**Created:** 2026-11-22T14:42:46Z
**Status:** Ready for next agentic work session
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Task

No specific task defined yet. This file is the durable handoff marker for the next agentic work session. Define the actual task when the next session starts, then execute it.

## Repository context

- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (committed goldens). Verification re-runs drivers and restores them — never leave a run half-finished.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).
- Lint/typecheck: `python3 -m py_compile` on changed files (no separate linter configured).

## Key commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Open items (from AGENTS.md ledger)

- E041: remaining ~133 numeric differences (1-ulp QP sensitivity) still exceed 1e-4 tolerance — do NOT re-pin to silence. See ledger open item.
- E042: tangency portfolio solver determinism (SLSQP status 8 at constrained optimum) — fixed in `src/portfolio_opt.py` per `tests/test_portfolio_opt.py`.

## Ground rules

- Always use `SEED=42` (walk-forward + placebo RNG).
- Never leave a verification run half-finished; restore goldens with `--restore-only` before committing if interrupted.
- Do not commit verification output.
- Do not commit unless explicitly asked.

## Next step

Define the actual task for the next session, then execute it.