# Handoff - Initial Task - 2026-11-01T01-36-14Z

Durable detail: .handoff/20261101T013614Z_INITIAL_TASK.md

## Initial task for next session
**START HERE:** Run `SEED=42 bash scripts/check.sh` and confirm golden/integrity status is clean before making any changes. If a verification snapshot is pending/stale, recover via `SEED=42 python3 run_all_verification.py --restore-only` first.

## Quick context
- Repo: Quantitative-Trading-Public-Research-Prompted (research phase complete E001–E049).
- Goldens are canonical; never overwrite via verification. Do not re-pin to silence numeric drift.
- If interrupted, restore before committing. Run `python3 -m py_compile` on touched files.
- Known: E041 has residual numeric drift from ill-conditioned QP (do not re-pin).

**START HERE:** Integrity check first; no edits until clean.
