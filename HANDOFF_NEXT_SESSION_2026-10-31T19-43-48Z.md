# Durable Handoff — Next Agentic Session

**Timestamp:** 2026-10-31T19:43:48Z
**Branch:** `main` (up to date with `origin/main`)
**Working tree:** clean — no uncommitted source changes (only gitignored `__pycache__/*.pyc`).
**Last commit:** `a84f0bc chore(kilo): checkpoint agent session` (adds `HANDOFF-2026-10-31T18-53-00Z.md`)

## Repository state

Research phase complete (E001–E043). Five validated components: equity TSM flagship, DN low-beta sort, futures TSM 18m, futures realized-roll-yield carry, macro momentum. Market-neutral-total-portfolio line is CLOSED (E042 PARTIAL 4/5, E042b REJECTED 4/5; no blend is simultaneously market-neutral and placebo-significant).

`src/portfolio_opt.py` fixed (E049): `max_sharpe` tangency branch and `project_onto_beta_cap` judge the solver answer on the QP constraints (new `_tangency_feasible`), never on `res.success`. `tests/test_portfolio_opt.py` added (5 tests, first-class step of `scripts/check.sh`). One golden deliberately re-pinned via `scripts/check_golden_baseline.py --update` (E042 lead `/placebo_constrained` block; decision unchanged).

## Clear initial task for the next agentic session

**Primary objective:** Establish a clean, trustworthy verification baseline. Do **NOT** start new research.

**Concrete steps (in order):**

1. **Inspect state**
   - `git log -1 --oneline`
   - `git status --short | grep -v __pycache__`
   - Confirm no `.verify_snapshot/` with an `ACTIVE.json` marker (no live run to recover).

2. **Run integrity guards**
   - `SEED=42 bash scripts/check.sh` (or `make check`) — already passing as of this handoff.
   - If guards report a pending snapshot or golden mismatch, recover first: `SEED=42 python3 run_all_verification.py --restore-only`

3. **Quick verification**
   - `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
   - **Watch item:** this run exceeded the 10-minute timeout in the prior session before completing. Consider running it in the background with `background_process` (monitor action) or splitting via `--skip-slow` so the harness does not kill it mid-run. The suite self-recovers on interruption, so a killed run is safe — just re-run or `--restore-only`.
   - Ensure it completes successfully with goldens restored. Do **not** commit verification outputs.

4. **Review open items**
   - Read `ledger/RESEARCH_LEDGER.md` (focus E041, E048, E049).
   - Known pre-existing drift: E041 ~133 numeric diffs (1-ulp QP sensitivity, ill-conditioned), E030 numeric diffs on near-zero quantities. Do **not** re-pin to silence.
   - Item 1 (from prior handoff): replace SLSQP QP solves with a deterministic KKT-enumeration solver, then deliberately re-pin affected artifacts via `--update`. Do not re-pin without the solver change.

## Success criteria

`make check` passes, `verify-quick` passes with no uncommitted changes to `experiments/` (goldens intact), and you have a clear plan before modifying code/data.

## Key artifacts to read first

- `AGENTS.md` — full commands, baseline integrity rules, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — pre-registered goals, gates, results, open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `run_all_verification.py` — verification flow and recovery logic
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

## Quick reference commands

```bash
# Integrity
SEED=42 make check
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py

# Verify
SEED=42 make verify-quick
SEED=42 make verify-extended
SEED=42 make verify-full

# Recover
SEED=42 python3 run_all_verification.py --restore-only

# Clean build artifacts
find . -name "*.pyc" -path "*/__pycache__/*" -delete
```

## Notes & guardrails

- Always use `SEED=42`. Never move goalposts, change tolerances/drivers/skips, or change research decisions as a side effect of verification.
- Never re-pin goldens as a side effect of running verification. Re-pinning is a deliberate action via `--update` and must be visible in the diff.
- `experiments/*.json` are canonical; `run_all_verification.py` backs up and restores them — never commit verification output. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard (cache coverage invariant).
- Python 3; no separate linter — run `python3 -m py_compile` on changed files.
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.

## Session work performed just prior to this handoff

- Ran `SEED=42 bash scripts/check.sh` — **ALL VERIFICATIONS PASSED** (integrity guards, experiment script imports, E042 PARTIAL 4/5 gate report).
- Started `SEED=42 python3 run_all_verification.py`; it was killed at the 10-minute harness timeout.
- The interrupted run left 5 modified artifacts (`blend_tsm_dnlowbeta_large_liquid.json`, `cointegration_large_liquid.json`, `e012_market_neutral.json`, `pairs_large_liquid.json`, `validation_summary.json`) and a valid `.verify_snapshot/` with `ACTIVE.json` (pid 47445, now defunct).
- Ran `SEED=42 python3 run_all_verification.py --restore-only` — **RESTORE COMPLETE**, 107 goldens restored, snapshot cleaned, working tree back to 0 modifications.
- Did **not** re-run the full verification to completion (would have exceeded the session time budget); the next session should finish it.