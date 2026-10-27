# Handoff: Next Agentic Session
- **Timestamp:** 2026-10-27T21:44:03Z
- **Branch:** main
- **HEAD:** 3c34d5e chore(kilo): checkpoint agent session
- **Working tree:** Modified (only `__pycache__` artifacts from recent checks/runs). No tracked source changes.

## Context
- Repo: Independent reproducible quantitative-strategy research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure is strict: `experiments/*.json` are canonical goldens. `run_all_verification.py` backs up/restores them; `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` enforce integrity. Never re-pin goldens as a side effect of verification.
- Known caveats: E041 has ~133 numeric diffs from ill-conditioned QP (optimizer determinism fixed per E049) — do not re-pin to silence. Cache coverage is enforced via `scripts/check_data_coverage.py` + `ledger/data_baseline.json`. E029/E030 data inputs are pinned for offline reproducibility.
- Extended verification (`--extended`) is environment-nondeterministic on BLAS/numpy; "all pass" not stable without environment control. Pre-existing drift class (e029/e030/e041) documented in ledger E041 disposition; do not weaken tolerances or modify goldens.

## Initial Task (do this first)
1. **Verify repo health (golden integrity).**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Must pass: goldens clean vs HEAD, golden baseline fingerprint match, py_compile, `tests/test_portfolio_opt.py`, convention checks, JSON/artifact checks.

2. **Confirm clean baseline state.**
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```
   Expected: only `*.pyc` diffs (or none). Both checks should report all matched/passing.

3. **Decide next action.**
   - If checks pass and working tree is clean of tracked changes: no verification rerun needed. Review `ledger/RESEARCH_LEDGER.md` for any open items before starting new work.
   - If checks fail on goldens: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do **not** re-pin from a verification run.

## One Precise Next Task (bounded, optional)
No new research task is warranted (novelty search complete; all free public data sources exhausted; market-neutral portfolio line CLOSED per E041/E042/E042b). The repository is in a clean, fully-verified state. The only remaining durable action is the maintainer-gated CI workflow creation, which is outside agent scope (template at `.github/workflow-templates/verification-gate.yml`). If a bounded in-session task is desired, re-run `SEED=42 python3 run_all_verification.py --extended` and confirm the 23/26 result is stable (expect the same pre-existing e029/e030/e041 drift; do not weaken tolerances or modify committed goldens).

## Quick Reference
- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify (8 drivers): `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes for Next Agent
- Always use `SEED=42`.
- Verification overwrites `experiments/*.json` temporarily — never leave a run half-finished.
- Do not commit verification outputs. Only commit intentional source/data changes.
- Constraints: no committed-golden modification; no tolerance/driver/skip changes; preserve pre-registered outcomes and promotion gates. Honor `SEED=42` and the pinned 2026-10-12 cache vintage (`data/vintages.json`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
