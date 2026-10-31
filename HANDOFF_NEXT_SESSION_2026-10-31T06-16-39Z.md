# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-31T06:16:39Z
**Branch:** `main`
**HEAD:** `f59a274` (chore(kilo): checkpoint agent session)
**Working tree:** only `__pycache__/*.pyc` (gitignored); no tracked changes.
**Verification snapshot:** none active.

---

## INITIAL TASK (do first)

**Repository is fully verified and stable. No new research is warranted. Your primary task is to confirm stability, not to change anything.**

1. Run the fast baseline integrity check:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0.
2. Do not run `git checkout -- experiments/` — pinned baseline in `ledger/golden_baseline.json` is authoritative.
3. If any pinned artifact differs from its SHA-256, restore from matching commit; never re-pin without justification.
4. After green checks, idle awaiting explicit user direction. Do not modify goldens, re-pin baselines, or run extended/full verification without explicit instruction.

## Constraints
- Always use `SEED=42`.
- Honor pinned cache vintages.
- Never leave a verification run half-finished.
- Do not commit verification outputs.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.

(End of handoff)
