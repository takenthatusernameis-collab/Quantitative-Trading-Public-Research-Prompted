# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-31T23:56:17Z (UTC)
**Branch:** `main` @ `d32e61e chore(kilo): checkpoint agent session` (up to date with `origin/main`)
**Working tree:** clean except `__pycache__/*.pyc` (gitignored; no source/data changes pending; experiments/ intact)
**Snapshot state:** `.verify_snapshot/` present with `ACTIVE.json` — a verification run is LIVE (pid 37259, started 2026-10-31T23:36:26Z).

## Clear initial task for the next agentic session

**Primary objective:** Let the live verification run finish, then recover baseline integrity from its snapshot. Do NOT start new research until `experiments/` goldens are restored and `check.sh` passes.

**Concrete steps (in order):**

1. **Wait for the live run**
   - Confirm pid 37259 is still alive: `kill -0 37259 2>/dev/null && echo ALIVE || echo DONE`
   - If alive: wait; do NOT start a second verification run.
   - If dead: proceed to step 2.

2. **Recover baseline**
   - `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
   - Confirm `.verify_snapshot/` is gone afterwards.

3. **Verify clean**
   - `SEED=42 bash scripts/check.sh` (or `make check`) — expect `=== All checks passed ===`
   - `git status --short` — only `__pycache__/*.pyc` allowed; no changes under `experiments/`.

4. **Quick verification**
   - `SEED=42 python3 run_all_verification.py --skip-slow` (or `make verify-quick`)
   - Do not commit verification outputs.

5. **Only then review open items**
   - Read `ledger/RESEARCH_LEDGER.md` (E041, E048, E049).
   - Known pre-existing drift: E041 ~133 numeric diffs (1-ulp QP sensitivity), E030 numeric diffs on near-zero quantities. Do not re-pin to silence.
   - Standing follow-up: replace SLSQP QP solves with deterministic KKT-enumeration solver for small N (<=5 assets), then deliberately re-pin via `scripts/check_golden_baseline.py --update`.

## Success criteria

`.verify_snapshot/` absent, `make check` passes, `verify-quick` passes, `git status` clean except `__pycache__`, clear plan before modifying code/data.

## Key artifacts to read first

- `AGENTS.md` — full commands, baseline integrity rules, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — pre-registered goals, gates, results, open items
- `run_all_verification.py` — verification flow and recovery logic
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`

## Quick reference commands

```bash
# Wait/check
kill -0 37259 2>/dev/null && echo ALIVE || echo DONE

# Recover
SEED=42 python3 run_all_verification.py --restore-only

# Integrity
SEED=42 make check

# Verify
SEED=42 make verify-quick
```
