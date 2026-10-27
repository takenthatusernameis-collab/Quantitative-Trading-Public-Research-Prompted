# HANDOFF - Next Agentic Work Session

**Timestamp (UTC):** 2026-10-27T23:38:50Z
**From:** Glyph Cluster (Kilo)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**HEAD:** a71134a (chore(kilo): checkpoint agent session)

## Current State

- **Research phase complete** (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Market-neutral portfolio line CLOSED (E042/E042b):** E042 (min_variance β≤0.05 confirmatory) was PARTIAL 4/5 (G1/G3/G4/G5 pass; G2 β-constrained placebo z=2.11 < 3.0 failed). E042b (max_sharpe β≤0.1) also rejected (4/5). No blend of the 5 validated components is simultaneously market-neutral and placebo-significant on the free-public-data surface. Component strategies remain the surviving edges.
- **Verification hardening:** Golden baseline guards (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`), data coverage enforcement (`scripts/check_data_coverage.py`), optimizer determinism rules (treat status-8 as feasible if constraints satisfied), and artifact-vs-code reconciliation policy all in place.
- **Reproducibility notes:** E029 fundamentals pinned (`data/fundamentals/`), E030 16-ETF panel pinned, E029/E030 now offline-reproducible. E041 still shows numeric drift (133 diffs) despite fixes - do **not** re-pin to silence (ledger E049).

## Immediate Priorities for Next Session

1. **Verify clean baseline state** (must be clean before making changes)
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If goldens appear dirty from an interrupted run: `SEED=42 python3 run_all_verification.py --restore-only` (or inspect `.verify_snapshot/` ACTIVE.json).
2. **Review open items** - Read `ledger/PRIORITIZATION.md` and `ledger/RESEARCH_LEDGER.md` focusing on E049 (E041 drift policy) and any remaining falsification opportunities.
3. **Decide next direction** - Portfolio blends are closed. Only pursue component-level work that is pre-registrable with falsification expectations and gates. Do not move goalposts post-hoc.

## Guardrails

- **Never** let verification overwrite committed goldens. The suite backs up/restores; if interrupted, restore before committing.
- **Don't re-pin** artifacts to hide stochastic/numeric drift. Follow the reconciliation rule: assert pre-registered *outcomes* (pass/fail/decision), not fixed point estimates.
- **Data inputs:** If adding new downloaded inputs, commit the file and re-pin via `python3 scripts/check_data_coverage.py --update` (must satisfy data coverage invariant).
- **Optimizer:** Follow the pinned rule - validate solver answer against problem constraints, not solver exit status.
- **Reproducibility:** Always use `SEED=42`. Run lint/typecheck as appropriate; never commit secrets.

## Quick Commands

```bash
# Fast sanity check
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Recover if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes

- Stale snapshot protection is active (`.verify_snapshot/ACTIVE.json` tracks owning PID). Suite refuses to start if another live run owns it.
- CI workflow cannot be auto-created (controller restores `.github/workflows/`); template at `.github/workflow-templates/verification-gate.yml`.
- Extended drift report goes to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored).
