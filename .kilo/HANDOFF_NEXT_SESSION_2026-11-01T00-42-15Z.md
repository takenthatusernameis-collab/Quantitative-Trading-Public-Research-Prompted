# Handoff - 2026-11-01T00:42:15Z

## Current state
- Repo: Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014–2026)
- Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Live verification run (PID 37259, `--extended`) has **finished**: process gone, `.verify_snapshot/` cleaned, `git status` shows only `__pycache__/*.pyc` (no experiment JSONs modified). Baseline intact.
- Baseline integrity guards present: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` (SHA-256 in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py`.

## Initial task for next session
**FOCUS: Golden integrity + reproducibility preservation. No new experiments planned.**

### Immediate actions (in order)
1. **Run fast integrity check** — `SEED=42 bash scripts/check.sh`. Must pass cleanly (goldens, data coverage, portfolio-opt tests).
2. **Review open ledger items** — `ledger/RESEARCH_LEDGER.md` E049 (optimizer determinism / numeric drift in E041/E042 tangency grids). Do **not** re-pin goldens to silence numeric drift.
3. **Confirm stability** — if clean, optionally `SEED=42 python3 verify_convention_robustness.py` (offline). Only run extended/full verification if explicitly needed.

## Known critical constraints
- **Goldens are canonical**: `experiments/*.json` must match HEAD or the pinned baseline. Never overwrite via verification. If interrupted, restore before committing.
- **Snapshot safety**: `.verify_snapshot/` is gitignored with `ACTIVE.json` tracking ownership. Recovery: `--restore-only` or `git checkout -- experiments/`.
- **Baseline pinning**: `ledger/golden_baseline.json` pins SHA-256 of every tracked artifact under `experiments/`. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` with justification — never as a side effect of running verification.
- **Data coverage**: All driver inputs must be git-tracked and pinned in `ledger/data_baseline.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`; missing/unpinned inputs fail hard.
- **E049 / optimizer**: SLSQP "positive directional derivative" (status 8) is not used to reject feasible optimal points (`src/portfolio_opt.py`). Tangency QP remains ill-conditioned causing small numeric drift in E041/E042 grids — **do not** re-pin to silence it. Enforced by `tests/test_portfolio_opt.py`.
- **CI**: Cannot create `.github/workflows/` via agents (controller restores it). Template at `.github/workflow-templates/verification-gate.yml`.

## Quick verification commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py          # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full   # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes
- Do **not** commit verification outputs or modify goldens/tolerances/gates.
- If you make any source changes, run `python3 -m py_compile` on touched files and re-run `scripts/check.sh`.
- Preceding handoffs remain for history; this file is now the durable handoff target.

**START HERE:** Run `SEED=42 bash scripts/check.sh` and report integrity status before making any changes.
