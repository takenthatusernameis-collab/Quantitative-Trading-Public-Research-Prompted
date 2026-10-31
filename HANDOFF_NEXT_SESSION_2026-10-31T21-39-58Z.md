# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-31T21-39-58Z (UTC)
**Branch:** main (up to date with origin/main)
**Working tree:** modified
**Last commit:** 8aaf728 chore(kilo): checkpoint agent session
**Snapshot state:** does NOT exist — no live run to recover

## Clear initial task for the next agentic session

**Primary objective:** Establish a clean, verified baseline before starting any new work. Validate repository integrity and confirm all golden artifacts match the pinned baselines.

**Concrete steps (in order):**

1. **Inspect state**
   - `git log -1 --oneline`
   - `git status --short | grep -v __pycache__`
   - Confirm no `.verify_snapshot/ACTIVE.json` marker

2. **Run integrity guards**
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - This validates: py_compile, golden baseline fingerprints, data coverage, convention robustness, optimizer tests
   - If guards report pending snapshot or golden mismatch, recover first: `SEED=42 python3 run_all_verification.py --restore-only`

3. **Quick verification**
   - `SEED=42 python3 run_all_verification.py --skip-slow` (or `make verify-quick`)
   - Verifies 8 experiment drivers + batch_run + validate + E042 lead
   - Must complete successfully with goldens restored; do **not** commit verification outputs

4. **Review open research items**
   - Read `ledger/RESEARCH_LEDGER.md` focusing on E041, E048, E049
   - Known pre-existing drift (do **not** re-pin): E041 has ~133 numeric diffs due to 1-ulp QP sensitivity (ill-conditioned tangency), E030 has numeric diffs on near-zero quantities
   - Standing follow-up: replace SLSQP with deterministic KKT-enumeration solver for small N (≤5 assets), then re-pin affected artifacts via `scripts/check_golden_baseline.py --update` only after solver change

## Success criteria

- `make check` passes
- `make verify-quick` passes with no uncommitted changes to `experiments/` (goldens intact)
- Clear plan established before modifying code/data

## Key artifacts to read first

- `AGENTS.md` — commands, baseline integrity rules, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — pre-registered goals, gates, results, open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `run_all_verification.py` — verification flow and recovery logic
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`

## Quick reference

```bash
SEED=42 make check                    # Integrity guards
SEED=42 make verify-quick             # Quick verification
SEED=42 python3 run_all_verification.py --restore-only  # Recover goldens
```
