# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-30T00:46:28Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `8465f87`
**Working tree:** clean of tracked changes (only `__pycache__/*.pyc`, gitignored). No `.verify_snapshot/` active.

## Initial Task (Start Here)

Before doing any new work, establish a clean baseline:

1. **Verify guards pass**
   `SEED=42 bash scripts/check.sh`
   Must complete with all checks green (goldens clean vs HEAD, golden baseline SHA-256 match, data coverage, portfolio-opt tests, py_compile, etc.).

2. **Confirm tree state**
   `git status --short` && `git diff --name-only` — only untracked `__pycache__/*.pyc` allowed.

3. **Recover if interrupted**
   If `experiments/*.json` are dirty from a previous interrupted run, restore:
   `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout -- experiments/`).

## Context

- **Research phase:** Complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Convention:** Close-to-close is v1.2.3 primary; overnight decomposition reported alongside.
- **Baselines:** `experiments/*.json` are canonical. Never re-pin goldens/data baselines to silence drift.
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals and specific vintage pins are enforced by coverage checks.

## Constraints (Do Not Violate)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished. `.verify_snapshot/` with `ACTIVE.json` is used for recovery.
- Do **not** re-pin goldens or `ledger/golden_baseline.json` / `ledger/data_baseline.json` to silence drift — committed baselines are authoritative.
- Do **not** commit verification outputs. Only commit intentional source/data changes.
- Follow `AGENTS.md` conventions; consult `ledger/RESEARCH_LEDGER.md` for research state.

## Suggested Next Actions

1. Read `AGENTS.md` (quick start, baseline integrity, reproducibility) and `ledger/RESEARCH_LEDGER.md` to understand current state.
2. Run baseline verification (`SEED=42 bash scripts/check.sh`). If guards fail or goldens are dirty, recover first.
3. If clean, proceed with the user's requested task. Do not modify baselines unless explicitly requested with justification and proper re-pinning workflow.

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py           # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full      # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
```
