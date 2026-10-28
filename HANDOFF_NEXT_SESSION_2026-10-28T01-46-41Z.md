# Handoff: Next Agentic Session
- **Timestamp:** 2026-10-28T01-46-41Z
- **Branch:** main
- **HEAD:** 849b3c24e5efb5c04fc5e290749d6fd82bf2e3af
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T01-46-41Z.md
- **Working tree:** Only `__pycache__/*.pyc` bytecode changes (untracked/ignored). No tracked source, data, or golden changes. No `.verify_snapshot/` present — no interrupted verification run to recover.

## Context
- Repo: Independent reproducible quantitative-strategy research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure is strict: `experiments/*.json` (107 files) are canonical goldens. Never re-pin goldens as a side effect of verification. E041 (~133 numeric diffs) and E030 (28 numeric diffs) are documented reporting-only drift — do not re-pin to silence.
- Cache coverage enforced via `scripts/check_data_coverage.py` + `ledger/data_baseline.json`. All caches pinned per baseline.

## Initial Task (do this first)
1. Verify repo health (golden integrity).
   ```bash
   SEED=42 bash scripts/check.sh
   ```
2. Confirm clean baseline state.
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```
3. Decide next action.
   - If checks pass and working tree clean of tracked changes: no verification rerun needed. Review `ledger/RESEARCH_LEDGER.md` for open items.
   - If checks fail on goldens: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do not re-pin artifacts as a side effect of a verification run.

## One Precise Next Task (bounded, optional)
No new research task is warranted. Repository is in a clean, fully-verified state. If a bounded in-session task is desired, re-run `SEED=42 python3 run_all_verification.py --extended` and confirm stability (expect pre-existing e030/e041 drift; do not weaken tolerances or modify committed goldens).

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
- The only working-tree changes are `__pycache__/*.pyc` bytecode files — not tracked source; ignore or clean, do not commit.
(End of file)
