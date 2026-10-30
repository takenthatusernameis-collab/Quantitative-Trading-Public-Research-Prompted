# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T08-26-56Z (UTC)
**Branch:** main
**Last commit:** `99a31b6` — chore(kilo): checkpoint agent session
**Working tree:** only `__pycache__/*.pyc` changes (gitignored). No source edits pending.

---

## INITIAL TASK (do first)

1. **Recover the stale verification snapshot before anything else**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (Fallback: `git checkout -- experiments/`.) Snapshot owned by dead pid 33924; `scripts/check.sh` reports it as interrupted. Do not leave it half-finished.

2. **Verify baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests.

3. **If checks fail**
   - Goldens differ from HEAD after restore → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - Never re-pin to silence drift; re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.

4. **Do not make changes or commit without explicit user direction.** Goldens are authoritative; never modify them as a side effect of verification.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Stale snapshot pending recovery** at write time.
- **Known open item:** E041 numeric drift (133 diffs) exceeds 1e-4 tolerance in extended verification; do not re-pin. E029 and E030 offline-reproducible with 0 differences.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints, not solver exit status; pinned by `tests/test_portfolio_opt.py`.

## Immediate priorities for next session

1. Recover stale verification snapshot, then run `SEED=42 bash scripts/check.sh` (must exit 0).
2. Do not touch experiments/goldens; they are the authoritative baseline.
3. Await explicit user direction before any code changes or commits.
