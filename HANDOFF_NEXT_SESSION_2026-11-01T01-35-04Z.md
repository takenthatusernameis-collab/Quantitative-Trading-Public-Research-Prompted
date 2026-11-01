# Handoff - Initial Task - 2026-11-01T01:35:04Z

Durable detail: `.handoff/2026-11-01T01:35:04Z_DETAIL_INITIAL_TASK.md`

## Initial task for next session
**START HERE:** Run `SEED=42 bash scripts/check.sh` and confirm golden/integrity status is clean before making any changes. If a verification snapshot is pending/stale, recover via `SEED=42 python3 run_all_verification.py --restore-only` first.

## Quick context
- Repo: Quantitative-Trading-Public-Research-Prompted (research phase complete E001–E049).
- Goldens are canonical; never overwrite via verification. Do not re-pin to silence numeric drift.
- If interrupted, restore before committing. Run `python3 -m py_compile` on touched files.
- Known: E041 has residual numeric drift from ill-conditioned QP (do not re-pin).
- Integrity guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` enforced.

**START HERE:** Integrity check first; no edits until clean.
