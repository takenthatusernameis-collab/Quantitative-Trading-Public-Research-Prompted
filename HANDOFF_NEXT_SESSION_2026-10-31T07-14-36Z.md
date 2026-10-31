# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-31T07:14:36Z
**Branch:** `main`
**HEAD:** `8eebade`
**Working tree:** clean.
**Verification snapshot:** none active (`.verify_snapshot/` absent).

---

## INITIAL TASK (do first)

**Repository is fully verified and stable. No new research is warranted. Your primary task is to confirm stability, not to change anything.**

1. Run the fast baseline integrity check:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0.
2. **Note:** running `check.sh` recompiles the tracked `__pycache__/*.pyc` artifacts (they are tracked despite `.gitignore` listing `__pycache__/`), so afterward restore them to keep the tree clean:
   ```bash
   git checkout -- scripts/__pycache__ src/__pycache__ tests/__pycache__
   ```
3. Do not run `git checkout -- experiments/` — pinned baseline in `ledger/golden_baseline.json` is authoritative.
4. If any pinned artifact differs from its SHA-256, restore from matching commit; never re-pin without justification.
5. After green checks, idle awaiting explicit user direction. Do not modify goldens, re-pin baselines, or run extended/full verification without explicit instruction.

## Constraints
- Always use `SEED=42`.
- Honor pinned cache vintages.
- Never leave a verification run half-finished.
- Do not commit verification outputs.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.

(End of handoff)
