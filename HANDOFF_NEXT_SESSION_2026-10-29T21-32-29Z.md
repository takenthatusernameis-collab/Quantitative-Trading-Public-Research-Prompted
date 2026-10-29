# Handoff for Next Agentic Session

**Timestamp:** 2026-10-29T21:38:10Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/State:** Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Goal
Start the next session by picking up from the current state and executing the most important open work without modifying golden artifacts.

## Current State (quick)
- Verification guards are in place: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, snapshot recovery via `.verify_snapshot/` (gitignored). Never leave a verification run half-finished.
- Extended verification drift is known and tracked: E041 has remaining numeric drift (133 diffs) due to ill-conditioned tangency QP + SLSQP build sensitivity; structural differences are fixed (optimizer fix in `src/portfolio_opt.py`, tested by `tests/test_portfolio_opt.py`). Do **not** re-pin E041/E042 to silence this.
- Data coverage enforced by `scripts/check_data_coverage.py` (all inputs pinned in `ledger/data_baseline.json`). E029/E030 reproducibility fixed via pinned inputs.
- CI workflow cannot be auto-created; template at `.github/workflow-templates/verification-gate.yml`.

## Recommended Initial Task
**Investigate and close the E041 optimizer determinism drift (open item).**

Why: ledger E049 notes 133 remaining numeric diffs exceed 1e-4 tolerance in extended verification. Goal is to reduce drift below tolerance or find an acceptable, pre-registered resolution without re-pinning artifacts.

### Concrete steps
1. **Verify current baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   (should pass: py_compile, tests/test_portfolio_opt.py, check_goldens_clean.py, check_golden_baseline.py, convention robustness)

2. **Reproduce E041 drift explicitly**
   ```bash
   SEED=42 python3 experiments/run_e041.py
   ```
   Compare against `experiments/e041_minvar_grid.json` (ignore timestamps; focus on numeric diffs). Also run via extended path mentally: `run_all_verification.py --extended` reports drift summary to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored).

3. **Diagnose source**
   - Inspect `src/portfolio_opt.py` (SLSQP usage, constraint validation, solver settings). Note: validation is on problem constraints (not exit status) — this is correct per E049.
   - Check for non-determinism: tie-breaking, numpy/scipy version sensitivity, floating point order, random seeds (walk-forward uses SEED). E041 grid uses the tangency/min-var paths.
   - Look at `tests/test_portfolio_opt.py` for expected behavior.
   - Consider conditioning: ill-conditioned QP -> 1-ulp changes matter. Possible fixes: tighten tolerances, add small regularization, fix scaling, or use a more stable formulation. Any change must be pre-registered in effect or justified without moving goalposts.

4. **Fix or propose resolution**
   - Prefer fixes that improve numerical stability without changing economic logic/gates.
   - If fix reduces diffs below tolerance: update code, re-run E041, verify extended comparison passes for E041.
   - If not fully resolvable without changing solver behavior in a way that affects gates: document in `ledger/RESEARCH_LEDGER.md` (E049 follow-up) with evidence, propose pre-registered confirmatory approach. **Do not re-pin `experiments/e041_minvar_grid.json` to silence drift.**

5. **Verify**
   ```bash
   SEED=42 python3 -m py_compile src/portfolio_opt.py experiments/run_e041.py tests/test_portfolio_opt.py
   SEED=42 python3 run_all_verification.py --extended  # or at least ensure E041 no longer reported as drifting
   ```
   Also ensure `scripts/check.sh` still passes.

## Guardrails
- **Never** modify `experiments/*.json` as a side effect of verification runs. Use `run_all_verification.py --restore-only` if working tree was clobbered.
- **Never** re-pin goldens to hide drift; use `scripts/check_golden_baseline.py --update` only if there's an intentional, documented baseline change (and it will show in diff).
- **Offline**: verification uses `QUANT_RESEARCH_OFFLINE=1` for drivers; respect data coverage.
- **Seed**: always `SEED=42`.
- **Pre-registration**: no post-hoc goalpost moves.

## Useful References
- `ledger/RESEARCH_LEDGER.md` (E049, E041 status)
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`
- `run_all_verification.py`, `scripts/check.sh`
- `experiments/run_e041.py`, `experiments/e041_minvar_grid.json`
- `AGENTS.md` (full conventions)

## Handoff Notes
- Snapshot mechanism active; check `.verify_snapshot/ACTIVE.json` if unsure about running verification.
- Extended drift report: `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) has per-driver diff details.
- If you need to understand optimizer status 8 behavior, see ledger E049 and the test.
