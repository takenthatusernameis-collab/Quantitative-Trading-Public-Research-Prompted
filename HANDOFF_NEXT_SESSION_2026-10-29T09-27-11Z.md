# Handoff for Next Agentic Work Session

**Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification infrastructure hardened (golden baselines pinned, cache coverage enforced, optimizer determinism fixed).

## Initial Task (Clear & Actionable)

**Focus: Maintain verification integrity and address open numerical stability items before any new strategy exploration.**

This is a maintenance/hardening pass. Do **not** re-pin baselines or modify `experiments/*.json` to silence drift. Follow the ledger's disposition (goldens are authoritative).

## Current State (verified at handoff time)

- Working tree clean at recent checkpoint (see git log)
- No live verification snapshot (`.verify_snapshot/` absent)
- `scripts/check.sh` expected to pass with known pre-existing drifts (E041) documented
- All guards in place: golden clean check, golden baseline pinning, data coverage enforcement, portfolio opt tests

## Open Items

- **E041 drift (open in ledger E049):** Extended verification still reports E041 drifting (~133 numeric diffs). Root cause is 1-ulp sensitivity of ill-conditioned QP in `src/portfolio_opt.py` (optimizer fix applied; status-8 gating removed). Do **not** re-pin. Investigate numerical stability improvements without changing economic decisions (REJECTED 3/5, gates unchanged).
- **Baseline integrity:** Any change to tracked artifacts under `experiments/` requires re-pinning via `scripts/check_golden_baseline.py --update` with justification.
- **Data coverage:** All `data.download()` inputs must be tracked and pinned in `ledger/data_baseline.json`. New data requires committing and re-pinning.

## Concrete Next Steps

1. **Verify repo health**
   - `SEED=42 bash scripts/check.sh` (must pass)
   - If golden mismatch reported, recover: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. If HEAD captured bad run, restore from commit matching `ledger/golden_baseline.json`.

2. **Triage E041 numerical stability (highest priority)**
   - Reproduce: `SEED=42 python3 run_all_verification.py --extended` and inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` for E041 worst diffs
   - Profile `src/portfolio_opt.py` tangency path (conditioning/scaling). Consider scaling, targeted regularization, solver options, or reformulation without changing gate decisions
   - Add focused test in `tests/test_portfolio_opt.py` if specific ill-conditioned case found
   - Goal: reduce drift below tolerance without re-pinning goldens or changing economic outcomes. If impossible without changing decisions, document in ledger and leave as open

3. **Harden verification/reporting if time permits**
   - Review snapshot recovery robustness
   - Confirm `run_all_verification.py --restore-only` works from dirty state
   - Document fixes in ledger with pre-registration style notes

4. **Only if (1)-(2) stable: consider blend optimization** (deferred)
   - TSM+DN blend weight optimization (E015) only after stability complete and clean verification passes. If pursued, pre-register gates/sensitivity, use `SEED=42`, follow cost model, never touch goldens.

## Verification Commands

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
