# HANDOFF — Next Agentic Work Session

**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ) (UTC)
**Branch:** main
**Last commit:** `f7e270a` — chore(kilo): checkpoint agent session
**Working tree:** clean (no pending changes)

---

## INITIAL TASK (do first)

1. **Recover the stale verification snapshot before anything else**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (Fallback: `git checkout -- experiments/`.) Check for any active snapshots with `ls -la .verify_snapshot/` if needed. Do not leave it half-finished.

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
- **Known open item:** E041 numeric drift (133 diffs) exceeds 1e-4 tolerance in extended verification; do not re-pin. E029 and E030 offline-reproducible with 0 differences.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints, not solver exit status; pinned by `tests/test_portfolio_opt.py`.
- **Cache coverage enforced (E048):** `scripts/check_data_coverage.py` validates all data inputs are pinned in `ledger/data_baseline.json`.

## Immediate priorities for next session

1. Recover stale verification snapshot, then run `SEED=42 bash scripts/check.sh` (must exit 0).
2. Do not touch experiments/goldens; they are the authoritative baseline.
3. Await explicit user direction before any code changes or commits.
