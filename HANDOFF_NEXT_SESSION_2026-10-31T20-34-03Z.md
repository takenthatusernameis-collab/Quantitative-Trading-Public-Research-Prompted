# Initial Task Message (for next agentic session) — 2026-10-31T20-34-03Z

> **START HERE:** Repository is fully verified and in a stable state. No new research is warranted. Your primary task is to verify stability by running the baseline integrity check, confirm the pre-existing known drifts remain unchanged, and report results. Do not modify goldens, weaken tolerances, or change any gate logic. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. All constraints from below still apply.

> **Durable handoff:** `HANDOFF_NEXT_SESSION_2026-10-31T20-34-03Z.md`

---

## Next Task: Repository is fully verified — no new research warranted

## Context

This session (handoff written 2026-10-31T20-34-03Z) opened with no user-directed task beyond the standing handoff instruction. The repository was found in a clean, fully-verified state:

- HEAD `1eef2f1` (chore(kilo): checkpoint agent session), branch `main`.
- Working tree clean (no tracked changes, no untracked files).
- No live verification snapshot (`.verify_snapshot/` absent). No run in progress; nothing to recover.
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Precise task (bounded, optional)

Re-run the baseline integrity check to confirm stability:

```bash
SEED=42 bash scripts/check.sh
```

Expect exit 0 with the pre-existing E030/E041 drift unchanged. Do **not** weaken tolerances, skip drivers, or modify committed goldens. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished.
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.

---

(End of handoff)
