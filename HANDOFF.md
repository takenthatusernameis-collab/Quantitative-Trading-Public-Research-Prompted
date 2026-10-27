# Agent Handoff - 2026-10-27T23:42:47Z

## Current State
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Golden baselines in `experiments/*.json` are authoritative. Verification suite backs up/restores them; never re-pin as a side effect of running verification.
- Integrity guards active: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`. All must pass.
- Open items: E049 (optimizer determinism) - E041/E042 grid artifacts show numeric drift from ill-conditioned QP; do **not** re-pin to silence. E029/E030 offline-reproducible after pinning.

## Initial Task for Next Session
**Start here (baseline integrity):**
```bash
SEED=42 bash scripts/check.sh
```
- If failures: restore goldens (`SEED=42 python3 run_all_verification.py --restore-only`) or fix per AGENTS.md guidance. Do not commit verification artifacts.
- If clean: review `ledger/RESEARCH_LEDGER.md` open items and pick highest priority (likely E049).

**Follow-up (E049 investigation):**
- Root cause: `src/portfolio_opt.py` validates on problem constraints (not solver status). SLSQP status 8 is acceptable if feasible/optimal.
- Remaining drift: 1-ulp sensitivity on ill-conditioned QP causing numeric diffs in E041/E042 grids (133 diffs for E041). Extended verification reports them.
- Goal: reduce drift without re-pinning goldens. Consider solver options, conditioning, or tighter validation - but follow pre-registration/multiple-testing discipline.

## Quick Commands
```bash
# Convention + golden integrity (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended (includes drift report) (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Restore goldens if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes
- Always use `SEED=42`.
- Cache coverage is enforced - missing/unpinned data fails hard under `QUANT_RESEARCH_OFFLINE=1`.
- Do not move goalposts post-hoc. Negative results are recorded as-is.
- If stuck snapshot: check `.verify_snapshot/ACTIVE.json` (pid) and restore.
