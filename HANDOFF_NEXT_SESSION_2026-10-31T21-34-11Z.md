# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-31T21:34:11Z (UTC)
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** clean — no tracked source/data changes. No uncommitted changes.
**Last commit:** `e585d58 chore(kilo): checkpoint agent session`
**Snapshot state:** `.verify_snapshot/` does **NOT** exist — no live run to recover.

## Clear initial task for the next agentic session

**Primary objective:** Confirm baseline integrity and establish a clean verification baseline before any new changes. Do NOT start new research.

**Concrete steps (in order):**

1. **Inspect state**
   - `git log -1 --oneline`
   - `git status --short | grep -v __pycache__`
   - Confirm no `.verify_snapshot/` with an `ACTIVE.json` marker.

2. **Run integrity guards**
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - If guards report a pending snapshot or golden mismatch, recover first: `SEED=42 python3 run_all_verification.py --restore-only`

3. **Quick verification**
   - `SEED=42 python3 run_all_verification.py --skip-slow` (or `make verify-quick`)
   - Ensure it completes successfully with goldens restored. Do **not** commit verification outputs.

4. **Review open items**
   - Read `ledger/RESEARCH_LEDGER.md` (focus E041, E048, E049).
   - Known pre-existing drift: E041 ~133 numeric diffs (1-ulp QP sensitivity, ill-conditioned), E030 numeric diffs on near-zero quantities. Do **not** re-pin to silence.
   - Standing follow-up: replace SLSQP QP solves with a deterministic KKT-enumeration solver for small N (<=5 assets), then deliberately re-pin affected artifacts via `--update`. Do not re-pin without the solver change.

## Success criteria

`make check` passes, `verify-quick` passes with no uncommitted changes to `experiments/` (goldens intact), and you have a clear plan before modifying code/data.

## Key artifacts to read first

- `AGENTS.md` — full commands, baseline integrity rules, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — pre-registered goals, gates, results, open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `run_all_verification.py` — verification flow and recovery logic
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`

## Quick reference commands

```bash
# Integrity
SEED=42 make check

# Verify
SEED=42 make verify-quick

# Recover
SEED=42 python3 run_all_verification.py --restore-only
```
