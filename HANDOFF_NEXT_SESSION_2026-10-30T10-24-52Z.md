# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T10:24:52Z (UTC)
**Branch:** main
**Last commit:** `02e4c21` — chore(kilo): checkpoint agent session
**Working tree:** `experiments/` matches HEAD exactly (0 diffs). No source edits pending. No `.verify_snapshot/` dir, no `ACTIVE.json` marker — no interrupted verification run to recover.

---

## INITIAL TASK (do first)

1. **Confirm baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match (`ledger/golden_baseline.json`), data coverage (`ledger/data_baseline.json`), `tests/test_portfolio_opt.py`.

2. **Nothing to recover:** no `.verify_snapshot/ACTIVE.json` and `experiments/` == HEAD, so `--restore-only` is not needed unless a verification run is started and interrupted.

3. **If checks fail**
   - Goldens differ from HEAD → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (`git checkout <commit> -- experiments/<file>`).
   - Never re-pin to silence drift; re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.

4. **Do not make changes or commit without explicit user direction.** Goldens are authoritative; never modify them as a side effect of verification.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **No stale snapshot pending.**
- **Known open item:** E041 numeric drift (133 diffs) exceeds 1e-4 tolerance in extended verification; do not re-pin. E029 and E030 offline-reproducible with 0 differences.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints, not solver exit status; pinned by `tests/test_portfolio_opt.py`.

## Pre-existing working-tree noise (ignore, do not commit)

- 11 tracked `__pycache__/*.pyc` files show as modified (binary, −1 byte each in `git diff --numstat`). They are stale build artifacts. `__pycache__/` is in `.gitignore` but these were force-tracked before the ignore rule. They are unrelated to any current task; leave them alone.

## Immediate priorities for next session

1. Run `SEED=42 bash scripts/check.sh` (must exit 0).
2. Do not touch `experiments/`/goldens; they are the authoritative baseline.
3. Await explicit user direction before any code changes or commits.
