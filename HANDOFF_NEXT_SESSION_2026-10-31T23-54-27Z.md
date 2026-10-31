# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-31T23:54:27Z (UTC)
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** `.verify_snapshot/` present with `ACTIVE.json` — a verification run is live/interrupted.
**Last commit:** `6612453 chore(kilo): checkpoint agent session`

## Clear initial task for the next agentic session

**Primary objective:** Recover baseline integrity from the live verification snapshot before any new work. Do NOT start new research.

**Concrete steps (in order):**

1. **Inspect snapshot**
   - Read `.verify_snapshot/ACTIVE.json` (pid, started).
   - Check whether pid 37259 is still alive: `kill -0 37259 2>/dev/null`.

2. **Recover**
   - If run is dead/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
   - If run is live: wait for completion; do not start a second run.

3. **Verify clean**
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - Confirm no stale snapshot, no golden mismatch.

4. **Quick verification**
   - `SEED=42 python3 run_all_verification.py --skip-slow` (or `make verify-quick`)
   - Ensure goldens restored; do not commit verification outputs.

5. **Review open items**
   - Read `ledger/RESEARCH_LEDGER.md` (focus E041, E048, E049).
   - Known pre-existing drift: E041 ~133 numeric diffs (1-ulp QP sensitivity), E030 numeric diffs on near-zero quantities. Do not re-pin to silence.
   - Standing follow-up: replace SLSQP QP solves with deterministic KKT-enumeration solver for small N (<=5 assets), then deliberately re-pin affected artifacts via `--update`.

## Success criteria

`.verify_snapshot/` absent, `make check` passes, `verify-quick` passes with no uncommitted changes to `experiments/` (goldens intact), clear plan before modifying code/data.

## Key artifacts to read first

- `AGENTS.md` — full commands, baseline integrity rules, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — pre-registered goals, gates, results, open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `run_all_verification.py` — verification flow and recovery logic
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `.verify_snapshot/ACTIVE.json`

## Quick reference commands

```bash
# Recover
SEED=42 python3 run_all_verification.py --restore-only

# Integrity
SEED=42 make check

# Verify
SEED=42 make verify-quick
```
", "filePath">
/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/HANDOFF_NEXT_SESSION_2026-10-31T23-54-27Z.md