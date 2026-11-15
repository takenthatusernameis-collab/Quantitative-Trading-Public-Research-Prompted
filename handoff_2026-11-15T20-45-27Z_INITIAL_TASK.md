# Agentic Handoff

**Timestamp:** 2026-11-15T20:47:07Z
**Branch / commit:** See `git log --oneline -5` and `git status`
**Working tree:** quantitative-trading research repo (2014–2026 US equities/futures/macro)

## Current task (next session)
Leave a timestamped clear initial task message for the next agentic work session in a durable handoff. — DONE (this file). No further code changes requested in this session.

## Repo conventions (from AGENTS.md)
- Reproduce / verify: `SEED=42 bash scripts/check.sh` or `make check`
- Full: `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`
- Never commit verification output; experiments/*.json are canonical goldens restored by the suite
- `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy optional)
- Lint: `python3 -m py_compile` on changed files
- CI workflow cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml`

## Key open items (ledger)
- E041 (min-var confirmatory): optimizer fix landed; 133 numeric drifts remain above 1e-4 tolerance (ill-conditioned QP). Do NOT re-pin to silence. See ledger E049.
- E042 n_sim=50 grid artifact drifts 29–133 differences. Do NOT re-pin.

## Snapshot recovery (if verification interrupted)
- `SEED=42 python3 run_all_verification.py --restore-only` restores experiments/ goldens
- `git checkout -- experiments/` restores HEAD baseline
