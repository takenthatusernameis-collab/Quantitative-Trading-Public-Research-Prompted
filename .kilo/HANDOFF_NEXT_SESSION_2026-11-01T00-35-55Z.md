# Handoff - 2026-11-01T00:35:55Z

## Current state
- Repo: Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014–2026)
- Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Working tree: source tree clean vs HEAD. Only `__pycache__/*.pyc` and 2 experiment JSONs show as modified (see "Live run" below) — these are expected mid-run and are restored on completion.
- Baseline integrity guards present: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` (SHA-256 in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py`.

## Live run (critical — do not kill)
- **PID 37259** (`python3 run_all_verification.py --extended`), started ~2026-11-01T19:47 UTC, ~1 hour elapsed. Currently on `experiments/run_e034.py`.
- Child: **PID 48717** = `experiments/run_e034.py` (Rl, ~2 min in).
- `.verify_snapshot/ACTIVE.json` owns the snapshot (pid 37259). `experiments/e029_fundamental_factors.json` and `experiments/e030_multiasset_tsm.json` currently differ from the snapshot because the run has already re-executed them; the suite restores them on completion. This is **expected and safe** — the baseline (HEAD) is untouched.
- If this run is killed mid-way, recover with `SEED=42 python3 run_all_verification.py --restore-only` (the suite self-recovers at startup and refuses to start while another live run owns the snapshot).

## Initial task for next session
**FOCUS: Golden integrity + reproducibility preservation. No new experiments planned.**

### Immediate actions (in order)
1. **Check whether the live run finished** — `ps -p 37259` / `ps --ppid 37259`. If gone, confirm `.verify_snapshot/` is cleaned and `git status --short` shows only `__pycache__/*.pyc`.
2. **Recover if a snapshot is stale/pending** — `SEED=42 python3 run_all_verification.py --restore-only`. Never leave a verification run half-finished.
3. **Run fast integrity check** — `SEED=42 bash scripts/check.sh`. Must pass cleanly (goldens, data coverage, portfolio-opt tests).
4. **Review open ledger items** — `ledger/RESEARCH_LEDGER.md` E049 (optimizer determinism / numeric drift in E041/E042 tangency grids). Do **not** re-pin goldens to silence numeric drift.
5. **Confirm stability** — if clean, optionally `SEED=42 python3 verify_convention_robustness.py` (offline). Only run extended/full verification if explicitly needed.

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

**START HERE:** Confirm the live run finished (or recover), then run step 3 above and report integrity status before making any changes.
