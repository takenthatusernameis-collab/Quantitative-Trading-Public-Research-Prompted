# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T09:22:02Z
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification infrastructure hardened (golden baselines pinned, cache coverage enforced, optimizer determinism fixed). Repo working tree clean.

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
   - `SEED=42 bash scripts/check.sh` (must pass).
   - If golden mismatch, restore: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

2. **Triage E041 numerical stability (highest priority)**
   - Reproduce extended drift: `SEED=42 python3 run_all_verification.py --extended`; inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`.
   - Profile `src/portfolio_opt.py` tangency path (conditioning, scaling). Consider column/row scaling, tiny ridge on ill-conditioned blocks only if it doesn't change gate decisions, solver options, or reformulation.
   - Add focused unit test in `tests/test_portfolio_opt.py` for the ill-conditioned case.
   - Goal: reduce numeric drift below tolerance without re-pinning goldens or changing economic outcomes. If not possible, document conclusion in ledger and leave open (do not re-pin).

3. **Harden verification/reporting (if time permits)**
   - Review `scripts/check.sh` flow; ensure snapshot recovery robust.
   - Confirm `run_all_verification.py --restore-only` works from dirty state.
   - Document fixes in ledger with pre-registration style notes.

4. **Only if (1)-(2) stable: consider blend optimization (deferred)**
   - TSM+DN blend weight optimization (E015). Pre-register gates/sensitivity, use `SEED=42`, follow cost model, never touch goldens.

## Verification Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
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

(End of file)
