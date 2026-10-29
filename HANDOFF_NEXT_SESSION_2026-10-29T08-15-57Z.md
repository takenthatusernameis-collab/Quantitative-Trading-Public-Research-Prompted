# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T08:15:57Z
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification infrastructure hardened (golden baselines pinned, cache coverage enforced, optimizer determinism fixed).

## Initial Task (Clear & Actionable)

**Focus: Close out the open items blocking promotion/readiness and harden reproducibility before any new strategy exploration.**

This is a maintenance/hardening pass first. Do **not** re-pin baselines or modify `experiments/*.json` to silence drift. Follow the ledger's disposition (goldens are authoritative).

## Current Known Blockers / Open Items

- **E041 drift (open in ledger):** Extended verification still reports E041 drifting (133 numeric diffs, down from 354). Root cause identified as 1-ulp sensitivity of ill-conditioned QP in `src/portfolio_opt.py` (optimizer fix applied; status-8 gating removed). Do **not** re-pin. Investigate if we can make the tangency solve more numerically stable (regularization/scaling/reformulation) without changing economic decisions (REJECTED 3/5, gates unchanged). See `ledger/RESEARCH_LEDGER.md` E049.
- **Golden baseline integrity:** Any change to tracked artifacts under `experiments/` requires re-pinning via `scripts/check_golden_baseline.py --update` with justification. `scripts/check_goldens_clean.py` fails on unstaged changes vs HEAD; `scripts/check_golden_baseline.py` enforces pinned SHA-256s in `ledger/golden_baseline.json`. Never let verification overwrite goldens.
- **Data coverage:** `scripts/check_data_coverage.py` enforces all `data.download()` inputs are tracked and pinned in `ledger/data_baseline.json`. Adding any new data requires committing and re-pinning.
- **Cache reproducibility:** E029/E030 made offline-reproducible via pinned fundamentals/panels. Maintain `QUANT_RESEARCH_OFFLINE=1` discipline in verification.

## Concrete Next Steps

1. **Verify repo state is clean before starting**
   - `SEED=42 bash scripts/check.sh` (must pass; includes py_compile, golden clean check, golden baseline check, portfolio opt tests, template validation, convention robustness).
   - If it reports golden mismatch, restore: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. If HEAD already captured a bad run, restore from the commit matching `ledger/golden_baseline.json`.

2. **Triage E041 numerical stability (highest priority)**
   - Reproduce extended drift locally: `SEED=42 python3 run_all_verification.py --extended` and inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` for E041 worst diffs.
   - Profile `src/portfolio_opt.py` tangency path (conditioning, scaling). Consider: column/row scaling, adding tiny ridge to ill-conditioned blocks only if it doesn't change gate decisions, solver options, or reformulating to more stable form.
   - Add a focused unit test in `tests/test_portfolio_opt.py` capturing the specific ill-conditioned case if found.
   - Goal: reduce numeric drift below tolerance without re-pinning goldens or changing economic outcomes. If not possible without changing decisions, document conclusion in ledger and leave as open (do not re-pin).

3. **Harden verification/reporting (if time permits)**
   - Review `scripts/check.sh` flow and ensure snapshot recovery is robust.
   - Confirm `run_all_verification.py --restore-only` works from a dirty state.
   - Document any fixes in ledger with pre-registration style notes.

4. **Only if (1)-(2) stable: consider blend optimization** (deferred)
   - Previous handoff suggested TSM+DN blend weight optimization (E015). Only do this after stability work is complete and clean verification passes. If pursued, pre-register gates/sensitivity, use `SEED=42`, follow cost model, and never touch goldens.

## Verification Commands (use these)

```bash
# Fast integrity check
SEED=42 bash scripts/check.sh

# Quick verification (restores goldens)
SEED=42 python3 run_all_verification.py

# Extended (shows E041 drift)
SEED=42 python3 run_all_verification.py --extended

# Full if needed
SEED=42 python3 run_all_verification.py --full

# Recovery if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Key References
- `ledger/RESEARCH_LEDGER.md` — authoritative state (E041/E049, golden policy)
- `AGENTS.md` — baseline integrity, reproducibility, cache coverage rules
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py` — optimizer determinism
- `scripts/check_*.py`, `run_all_verification.py` — guards and recovery
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints

## Guardrails
- Always use `SEED=42`
- Never re-pin baselines as side effect of verification runs
- Never modify `experiments/*.json` golden files without explicit justification + `--update`
- Follow offline discipline (`QUANT_RESEARCH_OFFLINE=1` in verification)
- Pre-register any new experiment before running; no goalpost moving
- Cost model: tc=0.5bps + slippage=0.2bps, next-day open execution
