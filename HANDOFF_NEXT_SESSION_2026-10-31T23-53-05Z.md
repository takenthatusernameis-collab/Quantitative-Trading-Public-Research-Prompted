# Handoff - 2026-10-31T23:53:05Z

## Current state
- Repo: Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014–2026)
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Working tree: clean at handoff time (excluding tracked `__pycache__/*.pyc` and untracked handoff artifacts)
- No live verification snapshot in progress (`.verify_snapshot/` absent)
- Baseline integrity guards present: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` (SHA-256 in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py`

## Initial task for next session
**FOCUS: Verify golden integrity and preserve reproducibility. No new experiments planned.**

### Immediate actions (in order)
1. **Inspect repo state** — `git status --short` and `git log -1 --oneline`. Confirm clean baseline with no leaked verification output in `experiments/`.
2. **Run fast integrity check** — `SEED=42 bash scripts/check.sh`. Must pass cleanly (goldens, data coverage, portfolio-opt tests).
3. **Recover if snapshot is stale** — If `.verify_snapshot/` exists with an `ACTIVE.json` or `check.sh` reports a pending/stale snapshot, recover first: `SEED=42 python3 run_all_verification.py --restore-only`. Never leave a verification run half-finished.
4. **Review open ledger items** — Check `ledger/RESEARCH_LEDGER.md` for E049 (optimizer determinism / numeric drift in E041/E042 tangency grids). Do **not** re-pin goldens to silence numeric drift.
5. **Confirm stability** — If clean, optionally run `SEED=42 python3 verify_convention_robustness.py` (offline) to confirm convention robustness. Only run extended/full verification if explicitly needed.

## Known critical constraints
- **Goldens are canonical**: `experiments/*.json` must match HEAD or the pinned baseline. Never overwrite via verification. If interrupted, restore before committing.
- **Snapshot safety**: `.verify_snapshot/` is gitignored with `ACTIVE.json` tracking ownership. Recovery: `--restore-only` or `git checkout -- experiments/` (use pinned commit if HEAD already captured a bad run).
- **Baseline pinning**: `ledger/golden_baseline.json` pins SHA-256 of every tracked artifact under `experiments/`. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` with justification in the diff/ledger — never as a side effect of running verification.
- **Data coverage**: All driver inputs must be git-tracked and pinned in `ledger/data_baseline.json`. Run with `QUANT_RESEARCH_OFFLINE=1` in verification. Missing/unpinned inputs fail hard.
- **E049 / optimizer**: SLSQP "positive directional derivative" (status 8) is not used to reject feasible optimal points (`src/portfolio_opt.py`). Tangency QP remains ill-conditioned causing small numeric drift in E041/E042 grids — **do not** re-pin to silence it. Enforced by `tests/test_portfolio_opt.py`.
- **CI**: Cannot create `.github/workflows/` via agents (controller restores it). Template at `.github/workflow-templates/verification-gate.yml`.

## Quick verification commands
```bash
# Health/integrity
SEED=42 bash scripts/check.sh

# Full verification modes (only if needed)
SEED=42 python3 run_all_verification.py          # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full   # (~15 min)

# Offline checks
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes
- Do **not** commit verification outputs or modify goldens/tolerances/gates.
- If you make any source changes, run `python3 -m py_compile` on touched files and re-run `scripts/check.sh`.
- Preceding handoffs remain for history; this file is now the durable handoff target.

**START HERE:** Run step 1–3 above and report integrity status before making any changes.
