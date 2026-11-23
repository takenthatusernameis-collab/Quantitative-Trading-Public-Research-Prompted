# Agentic Work Session Handoff

**Timestamp:** 2026-11-23T18:54:53Z
**Session:** New session - 2026-11-23T18:54:51.013Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task (next session)

No specific task was provided in this session. The board is empty and no pending work was identified.

Recommended first actions for the next agentic session:
1. Check `git status` and `git diff` to confirm working tree cleanliness.
2. Run the convention-robustness check: `SEED=42 bash scripts/check.sh` (or `make check`).
3. If an experiment driver or verification is needed, pick one from `experiments/run_e*.py` and run with `SEED=42`.
4. Never commit verification output; restore goldens via `SEED=42 python3 run_all_verification.py --restore-only` if interrupted.

## Repo conventions (from AGENTS.md)
- `experiments/*.json` are committed golden artifacts; verification overwrites then restores them.
- Seed always `SEED=42`. Offline mode `QUANT_RESEARCH_OFFLINE=1` for verification.
- No separate linter; run `python3 -m py_compile` on changed Python files.
- `cvxpy`/`cvxopt` optional; portfolio optimizer falls back to `scipy.optimize`.

## Links
- Research ledger: `ledger/RESEARCH_LEDGER.md`
- Golden baseline: `ledger/golden_baseline.json`
- Data baseline: `ledger/data_baseline.json`
