# Agentic Work Session Handoff

**Created:** 2026-11-08T08:56:24Z
**Branch:** `main` (up to date with `origin/main`)
**Session:** `ses_e45a08211ffeyebK6mgx5FozV1` (this session)

## Current state

- Working tree is clean except for `__pycache__/*.pyc` bytecode noise (12 files, 0 insertions/deletions — ignorable, likely gitignored-noise from a prior run).
- No source files modified. No experiment drivers in progress.
- `experiments/*.json` goldens match HEAD; no stale `.verify_snapshot/` pending.
- Recent history: repeated `chore(kilo): checkpoint agent session` commits on `main`.

## Recommended initial task for the next session

Run the convention-robustness + template validation gate (fast, offline, seconds):

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

This is the first-class CI-equivalent gate. It runs `py_compile`, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `check_json_artifacts.py`, `check_experiment_imports.py`, `diff_golden.py`, `validate_template.py`, and `tests/test_portfolio_opt.py`.

If green, the next meaningful work is a verification run. Per `AGENTS.md`:

```bash
SEED=42 python3 run_all_verification.py --skip-slow   # convention + quick drivers (~8 min)
# or full:
SEED=42 python3 run_all_verification.py
```

**Critical constraints (from AGENTS.md):**
- Never leave a verification run half-finished; it overwrites `experiments/*.json` then restores them. Interrupted runs must be recovered with `SEED=42 python3 run_all_verification.py --restore-only`.
- Never commit verification output / replaced goldens as a side effect of running the suite. Re-pinning requires an explicit `--update` and a visible diff.
- Drivers run with `QUANT_RESEARCH_OFFLINE=1`; every `data.download()` input must be pinned in `ledger/data_baseline.json`.

## Open questions / notes

- No specific feature or bug task was assigned this session. The handoff is a state snapshot only; pick the next task from the verification gate above or from a new user request.
- Optional deps: `cvxpy`/`cvxopt` absent → `src/portfolio_opt.py` falls back to `scipy.optimize`.
