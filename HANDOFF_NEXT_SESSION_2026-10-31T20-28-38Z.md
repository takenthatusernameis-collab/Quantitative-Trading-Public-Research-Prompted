# Initial Task Message (for next agentic session) — 2026-10-31T20:28:38Z

> **START HERE:** Repository is fully verified and in a stable state. No new research is warranted. Your primary task is to verify stability by running the baseline integrity check, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. All constraints from below still apply.

> **Durable handoff chain:** This file (`HANDOFF_NEXT_SESSION_2026-10-31T20-28-38Z.md`) is the latest. Common entry points: `HANDOFF_NEXT_SESSION_LATEST.md`, `handoff.md`, `handoff_next.md`, `HANDOFF_CURRENT.md`, `NEXT_HANDOFF.md`, `NEXT_SESSION_HANDOFF.md`.

---

## Next Task: Repository is fully verified — no new research warranted

## Context

This session (handoff written 2026-10-31T20:28:38Z) opened with no user-directed task beyond the standing handoff instruction. The repository was found in a clean, fully-verified state:

- HEAD `45b236d` (chore(kilo): checkpoint agent session), branch `main`.
- Working tree has no tracked changes except `__pycache__/*.pyc` artifacts (gitignored; ignore them).
- No live verification snapshot (`.verify_snapshot/` absent). No run in progress; nothing to recover.
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Pre-existing known drifts (unchanged): E030 and E041 show numeric drift under extended comparison (documented in AGENTS.md and ledger). Do not re-pin to silence them.

## Precise task (bounded, optional)
Re-run the baseline integrity check to confirm stability:

```bash
SEED=42 bash scripts/check.sh
```

Expect exit 0 with the pre-existing E030/E041 drift unchanged. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Never leave a verification run half-finished (backup in `.verify_snapshot/` with `ACTIVE.json` if a run is live).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Do not re-pin baselines as a side effect of running verification.
- Respect cache coverage invariant (`scripts/check_data_coverage.py`).

## Quick Reference
- Full verification: `SEED=42 python3 run_all_verification.py` (quick/extended/full flags as needed)
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`
- Convention-robustness only: `SEED=42 python3 verify_convention_robustness.py`

(End of file)
