# Handoff — Next Agentic Session

Timestamp: 2026-10-28T05:28:40Z

## Initial Task Message for Next Agentic Work Session

Start next session by confirming baseline integrity: run `SEED=42 bash scripts/check.sh`. If it passes, review `ledger/RESEARCH_LEDGER.md` for open items before any new work. No bounded research task is currently outstanding; standing state is clean and fully verified.

## Context

- Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Golden artifacts under `experiments/*.json` are canonical; must remain untouched. Restore via `SEED=42 python3 run_all_verification.py --restore-only` if dirty.
- Do not commit verification output. Do not re-pin goldens to silence numeric drift; document in ledger instead.
- Working tree clean except `__pycache__/*.pyc` (non-source). Branch: main.

## Priority Tasks

1. **Verify repo health** — `SEED=42 bash scripts/check.sh` (goldens match HEAD, convention robustness PASS, driver imports OK).
2. **Confirm clean baseline integrity** — `git diff --name-only`, `python3 scripts/check_golden_baseline.py`, `python3 scripts/check_data_coverage.py`, `python3 scripts/check_goldens_clean.py`, `tests/test_portfolio_opt.py`.
3. **Review state** — If all pass, review `ledger/RESEARCH_LEDGER.md` for open items; no verification rerun needed. If goldens/guards fail, restore via `--restore-only`; check for stale `.verify_snapshot/ACTIVE.json`.

## If a Bounded Research Task Is Assigned

Load the relevant `E*_TASK_SPEC.md`, implement the driver in `experiments/run_e*.py` with a `pre_registered` block (gates, falsification expectations, sensitivity grid), run with `SEED=42`, then verify with `SEED=42 python3 run_all_verification.py`. Preserve pre-registered outcomes and promotion gates; never move goalposts post-hoc.

## Important Notes

- Always use `SEED=42` for reproducibility.
- If a verification run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- Never re-pin goldens to silence numeric drift — document in ledger if issues arise.
- Cache coverage is enforced — missing data files will fail hard in offline mode (`QUANT_RESEARCH_OFFLINE=1`).
- Extended verification (`--extended`) is environment-nondeterministic on BLAS/numpy; pre-existing drift class (e029/e030/e041) documented in ledger E041/E048/E049 disposition. Do not weaken tolerances or modify committed goldens.

## Key Files

- `AGENTS.md` (commands/conventions)
- `ledger/RESEARCH_LEDGER.md`
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `run_all_verification.py`, `scripts/check.sh`

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --restore-only   # if snapshot pending
find . -name "*.pyc" -delete && find . -type d -name __pycache__ -empty -delete   # clean pycache
```
