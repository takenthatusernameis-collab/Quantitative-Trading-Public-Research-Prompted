# Agentic Handoff | 2026-10-30T03:22:39Z

## Initial Task (start here)
Verify baseline integrity and environment readiness before making any changes.

### Required steps
1. [ ] **Check guards**: `SEED=42 bash scripts/check.sh`
   Must pass (py_compile, goldens clean vs HEAD, golden baseline match, data coverage, tests).
   If it fails, follow AGENTS.md "Baseline Integrity" before committing.
2. [ ] **Recover if needed**: If a previous verification was interrupted, check for `.verify_snapshot/ACTIVE.json`.
   If present/stale, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
3. [ ] **Confirm state**: Review `ledger/RESEARCH_LEDGER.md` and `ledger/golden_baseline.json` to understand current baseline.

## Key Constraints
- **Never leave verification half-finished** - snapshot lives in `.verify_snapshot/` with `ACTIVE.json`; always restore on interrupt.
- **Goldens are authoritative** - `ledger/golden_baseline.json` pins every artifact. Only re-pin with `python3 scripts/check_golden_baseline.py --update` if there is clear justification (do not do it as a side effect of verification).
- **Data coverage enforced** - `ledger/data_baseline.json` requires caches to exist and match. Add data by committing files and re-pinning coverage.
- **E041 drift is open** - ill-conditioned QP causes numeric drift (133 diffs) even after optimizer fix. Do **not** re-pin to silence it.
- **Offline reproducibility** - E029/E030 are reproducible via pinned data/fundamentals; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

## Quick References
- Fast check: `SEED=42 make check`
- Quick verify: `SEED=42 make verify-quick`
- Extended verify: `SEED=42 make verify-extended`
- Full verify: `SEED=42 make verify-full`
- Recovery only: `SEED=42 python3 run_all_verification.py --restore-only`
