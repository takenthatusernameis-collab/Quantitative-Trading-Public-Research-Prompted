# HANDOFF — 2026-10-31T22:38:09Z

## Session State
- Branch: main
- HEAD: 33ba745 (chore(kilo): checkpoint agent session)
- Recent: 33ba745, 768a30a, bb50fe1 (checkpoint commits)
- Working tree: modified `__pycache__/*.pyc` only (uncommitted). No source changes.
- Repo: https://github.com/... (local checkout)

## Project Status
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Canonical artifacts: `experiments/*.json` are goldens. Never modify them via verification runs.
- Strict guards active: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

## Known Issues / Drift (do not "fix" by re-pinning)
- **E041**: 133 numeric diffs remain (ill-conditioned QP). Structural diffs resolved. Do **not** re-pin. See ledger E049.
- **Optimizer**: SLSQP status 8 treated as feasible if constraints satisfied (scipy-build dependent). Fixed per E049.
- **Offline reproducibility**: E029 fundamentals pinned (`data/fundamentals/`), E030 panel pinned. Cache coverage enforced.

## Initial Task For Next Session
**Verify baseline integrity before making any changes.**

### Step 1: Fast checks (must pass)
```bash
SEED=42 bash scripts/check.sh
```

### Step 2: Quick verification (if Step 1 clean)
```bash
SEED=42 python3 run_all_verification.py
```

### Step 3: If interrupted/stale snapshot
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```

## Rules
- If `check_goldens_clean.py` or `check_golden_baseline.py` fails → restore from HEAD / pinned commit before committing. Do not re-pin goldens as side effect of verification.
- If verification would overwrite `experiments/*.json`, ensure snapshot recovery path is intact (`.verify_snapshot/ACTIVE.json`).
- Only commit when explicitly requested. Do not commit `__pycache__` or verification outputs.
- Extended: `SEED=42 python3 run_all_verification.py --extended` (~21m), Full: `--full` (~15m).
