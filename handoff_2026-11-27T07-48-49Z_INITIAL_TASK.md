# Agentic Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-27T08:44:44Z
**Branch:** default (git repo)
**Status:** Working tree has modified `__pycache__/*.pyc` files under `scripts/`, `src/`, `tests/` (likely tracked bytecode caches). All other tracked files are clean.

## Next agentic work session — initial task

**Task:** Run the convention + baseline verification suite and leave the tree clean.

**Commands to run (in order):**
1. `SEED=42 bash scripts/check.sh` — convention-robustness check + template validation (seconds, offline). This runs `check_goldens_clean.py` (step 0.5c) which fails if any tracked artifact under `experiments/` differs from HEAD or if a stale `.verify_snapshot/` is pending.
2. `SEED=42 python3 run_all_verification.py --verify-quick` (i.e. `make verify-quick`) — ~8 min full verification re-executing the 8 drivers in the 5a block (E012, E023, E024 --merge, E027, E035, E037, E039, E042-lead) with `QUANT_RESEARCH_OFFLINE=1`.
3. If a verification run was interrupted or left driver output in `experiments/`, restore goldens: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
4. `python3 -m py_compile` on any changed `.py` files (no separate linter configured).
5. Commit only intended changes; never commit verification output. Do **not** re-pin goldens as a side effect of running the suite.

## Key conventions (from AGENTS.md)
- `experiments/*.json` are canonical research artifacts; never committed by verification.
- Cache coverage invariant: every `data.download()` call site must resolve to a git-tracked, SHA-256-pinned cache file in `data/` (see `ledger/data_baseline.json`, `scripts/check_data_coverage.py`).
- Seed: always `SEED=42`.
- Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Notes
- `__pycache__` modifications are the only dirty files; decide whether to commit or restore them before any commit.
- The CI verification-gate workflow cannot be created by automated agents (controller restores `.github/workflows/`; `GITHUB_TOKEN` lacks workflows push). Template at `.github/workflow-templates/verification-gate.yml`.
