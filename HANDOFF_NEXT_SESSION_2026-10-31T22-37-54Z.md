# Handoff - 2026-10-31T22-37-54Z

## Current state
- Repo: Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014-2026)
- Research phase complete (E001-E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- HEAD: `fdb454a` (chore(kilo): checkpoint agent session), branch `main`.
- Working tree: clean of source/data changes. Only 12 `__pycache__/*.pyc` show as modified — all are recompilation noise. Do NOT commit them.
- No live verification snapshot (`.verify_snapshot/` absent). No run in progress; nothing to recover.
- No user-directed task beyond this standing handoff instruction.

## INITIAL TASK (START HERE)
**FOCUS: Verify golden integrity and preserve reproducibility.** No new experiments planned.

### Immediate actions (in order)
1. **Check golden integrity** - Run `SEED=42 bash scripts/check.sh`. Must pass cleanly (no snapshot/golden issues).
2. **Verify snapshot state** - If `.verify_snapshot/` has stale `ACTIVE.json`, recover with `SEED=42 python3 run_all_verification.py --restore-only` first.
3. **Review open ledger items** - Check `ledger/RESEARCH_LEDGER.md` for E049 (optimizer determinism/numeric drift in E041/E042). Do **not** re-pin to silence numeric drift.
4. **Confirm clean working tree** - Ensure no uncommitted changes to `experiments/*.json`. Don't commit `__pycache__` unless explicitly intended.

## Known critical constraints
- **Goldens are canonical**: `experiments/*.json` must match HEAD/pinned baseline. Never overwrite via verification.
- **Snapshot**: `.verify_snapshot/` (gitignored) with `ACTIVE.json`; if killed, recover via `--restore-only` or `git checkout -- experiments/`.
- **Guards**: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` (SHA-256 in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py`.
- **E049**: SLSQP status-gating fixed; tangency ill-conditioned causes numeric drift in E041/E042 grids - do NOT re-pin. Use `tests/test_portfolio_opt.py`.
- **Offline/data**: Use `QUANT_RESEARCH_OFFLINE=1` in verification. All driver inputs must be pinned.
- **Pre-existing drift (reporting-only, decisions unchanged)**: E041 ~133 numeric diffs, E030 numeric diffs on near-zero quantities. Do not re-pin.

## Quick verification commands
```bash
SEED=42 bash scripts/check.sh                    # fast (~seconds)
SEED=42 python3 run_all_verification.py          # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full   # (~15 min)
SEED=42 python3 verify_convention_robustness.py  # offline convention check
```

## Notes
- If verification interrupted, restore goldens before committing.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`); template at `.github/workflow-templates/verification-gate.yml`.
