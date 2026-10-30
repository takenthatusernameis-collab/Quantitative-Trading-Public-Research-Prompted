# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T10:26:07Z (UTC)
**Branch:** main
**Working tree:** `experiments/` matches HEAD exactly (0 diffs). No source edits pending. No `.verify_snapshot/` dir, no `ACTIVE.json` marker — no interrupted verification run to recover.

---

## INITIAL TASK (do first)

1. **Confirm baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0.

2. **Nothing to recover:** no `.verify_snapshot/ACTIVE.json` and `experiments/` == HEAD, so `--restore-only` is not needed unless a verification run is started and interrupted.

3. **If checks fail:** restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (`git checkout <commit> -- experiments/<file>`). Never re-pin to silence drift.

4. **Do not make changes or commit without explicit user direction.** Goldens are authoritative.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **No stale snapshot pending.**
- **Known open item:** E041 numeric drift (133 diffs) exceeds 1e-4 tolerance in extended verification; do not re-pin. E029 and E030 offline-reproducible with 0 differences.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints, not solver exit status; pinned by `tests/test_portfolio_opt.py`.

## Immediate priorities for next session

1. Run `SEED=42 bash scripts/check.sh` (must exit 0).
2. Do not touch `experiments/`/goldens; they are the authoritative baseline.
3. Await explicit user direction before any code changes or commits.
