# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-30T00:34:07Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `90e974f`
**Working tree:** only `__pycache__/*.pyc` modified (build artifacts from compile checks); no tracked source changes. No `.verify_snapshot/` active.

## Initial Task (Start Here)

Before doing any new work, establish a clean baseline:

1. **Verify guards pass**
   `SEED=42 bash scripts/check.sh`
   Must complete with all checks green (goldens clean vs HEAD, golden baseline SHA-256 match, data coverage, portfolio-opt tests, py_compile, etc.).

2. **Confirm tree state**
   `git status --short` and `git diff --name-only` — only untracked/build-artifact `__pycache__/*.pyc` allowed; no tracked source modifications.

3. **Recover if interrupted**
   If `experiments/*.json` are dirty from a previous interrupted run, restore:
   `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout -- experiments/`).

## Constraints (Do Not Violate)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished. `.verify_snapshot/` with `ACTIVE.json` is used for recovery.
- Do **not** re-pin goldens or `ledger/golden_baseline.json` / `ledger/data_baseline.json` to silence drift — committed baselines are authoritative.
- Do **not** commit verification outputs. Only commit intentional source/data changes.
- Follow project conventions in `AGENTS.md`; consult `ledger/RESEARCH_LEDGER.md` for research state.

## Suggested Next Actions

- Read `AGENTS.md` (quick start, baseline integrity, reproducibility) and `ledger/RESEARCH_LEDGER.md` to understand current state (research phase complete; surviving strategies documented).
- If clean, proceed with the user’s requested task. If guards fail or goldens are dirty, fix recovery first.

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # (~21 min)
SEED=42 python3 run_all_verification.py --full       # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover if interrupted
```
