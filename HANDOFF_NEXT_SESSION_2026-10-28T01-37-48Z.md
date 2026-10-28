# Handoff: Next Agentic Session
- **Timestamp:** 2026-10-28T01:37:48Z
- **Branch:** main
- **HEAD:** 846f1d0
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T01-37-48Z.md
- **Working tree:** Only `__pycache__/*.pyc` bytecode changes (untracked/ignored). No tracked source, data, or golden changes.

## Context
- Repo: Independent reproducible quantitative-strategy research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure is strict: `experiments/*.json` (107 files) are canonical goldens. Never re-pin goldens as a side effect of verification. E030 and E041 have documented reporting-only drift — do not re-pin to silence.
- Cache coverage enforced via `scripts/check_data_coverage.py` + `ledger/data_baseline.json`. All caches pinned per baseline.

## Initial Task (Do This First)
1. **Verify repo health (golden integrity).**
   ```bash
   SEED=42 bash scripts/check.sh
   ```

2. **Confirm clean baseline state.**
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```

3. **Act on results.**
   - If all checks pass and only `__pycache__` differs: repo is clean. Review `ledger/RESEARCH_LEDGER.md` for open items; no verification rerun required.
   - If golden integrity fails: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do not re-pin artifacts as a side effect of verification.

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
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Known drift (E030, E041) is reporting-only. Do not weaken tolerances or re-pin goldens to silence it.
- Only working-tree changes expected are `__pycache__/*.pyc` bytecode files — ignore or clean, do not commit.
