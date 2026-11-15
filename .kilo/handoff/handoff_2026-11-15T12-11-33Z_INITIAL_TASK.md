# Agent Handoff — Initial Task (2026-11-15T12:11:33Z)

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E051); surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Branch / HEAD**: `main` @ `3bd296241a5c1305e839b99a3f434cdd50976a54` ("chore(kilo): checkpoint agent session")
- **Sync**: `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync)
- **Supersedes**: prior durable handoff `handoff_2026-11-15T12-10-20Z_INITIAL_TASK.md` (HEAD `9eb5e287`); last ledgered refresh is E376.

## Verified This Session (no verification run performed)
- `scripts/check_json_artifacts.py` → exit 0 (114 committed JSON artifacts parse).
- `scripts/check_goldens_clean.py` → exit 0 (committed goldens match HEAD).
- `scripts/check_golden_baseline.py` → exit 0 (all 107 pinned goldens match `ledger/golden_baseline.json`).
- `scripts/check_data_coverage.py` → exit 0 (all 35 pinned data inputs present, tracked, unchanged).
- `verify_convention_robustness.py` → exit 0.
- `scripts/validate_template.py` → exit 0.
- `scripts/check_experiment_imports.py` → exit 0.
- Working tree: only tracked `__pycache__/*.pyc` modifications (pre-existing, byte-identical rewrites) plus this handoff deliverable. No `.verify_snapshot/`, no `.verify_reports/`; no interrupted verification run.

## Delta vs Prior Durable Handoff (`9eb5e287` → `3bd29624`)
- `git diff --name-only 9eb5e287..3bd29624` filtered to research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, excl `__pycache__`/`*.pyc`) → **0 paths**.
- Changes are exclusively: checkpoint commit `3bd29624`, `ledger/RESEARCH_LEDGER.md` (this E377 entry), generic handoff symlink/pointer files repointed by `scripts/repoint_handoff.py`, and `__pycache__/*.pyc`. **No research substance changed.**

## Environment Blocker (read first)
- The system interpreter `/usr/bin/python3` (3.12) has **none** of the scientific stack: `numpy`, `pandas`, `scipy`, `pyarrow`, `statsmodels`, `yfinance` are missing; `pytest` is also absent.
- Therefore `make verify-quick` / `run_all_verification.py` and every experiment driver will fail with `ModuleNotFoundError` until dependencies are installed. `SEED=42 bash scripts/check.sh` exits 1 in this sandbox solely on pandas/numpy/pytest-dependent unit tests.
- Static guards that do not import pandas still pass (see list above).

## Critical Integrity Notes
- **Golden artifacts**: `experiments/*.json` are canonical. Verification overwrites then restores them. **Never leave a verification run half-finished** — recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates every `data.download()` call site against `ledger/data_baseline.json`; the suite runs with `QUANT_RESEARCH_OFFLINE=1`.
- **Baseline pinning**: `ledger/golden_baseline.json` holds SHA-256 fingerprints. Re-pinning requires an explicit, diffed `--update`; never as a side effect of re-running the suite.
- Always use `SEED=42`. Pre-registration, multiple-testing discipline ("reported, not gated"), and honest negative results are mandatory. Do not commit verification output or bytecode churn.

## Known Drift (Extended Verification — do NOT re-pin to silence)
- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP, ledger E049); its 3 structural diffs are already fixed; extended block still reports drift.
- **E030 / E042 grids**: accepted 1-ulp ill-conditioned QP drift (ledger E048/E049).
- **E029**: offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`, ledger E045).

## Initial Task for Next Session
1. **Restore the runtime first:** `pip install -r requirements.txt`; confirm `python3 -c "import pandas, numpy, scipy, statsmodels"`.
2. **Baseline health check (required before any other work):** `SEED=42 make check`. If it reports a golden mismatch, a stale `.verify_snapshot/`, or dirty tracked artifacts, fix/restore before proceeding; do **not** commit a captured verification state.
3. **Assess open reproducibility items without re-pinning:** E041 (~133 numeric diffs), E030/E042 grid drift, and the ill-conditioned QP note (ledger E048/E049). Review `ledger/RESEARCH_LEDGER.md` for open items.
4. **Choose next action from evidence:** if baseline is clean, `SEED=42 make verify-quick` for confidence; use `--extended` / `--full` only when needed. Any optimizer/data/golden change must follow pre-registration and re-pin rules and be documented in the ledger.
5. **Handoff out:** leave a new timestamped handoff summarizing commands run, outcomes, and any drift/baseline decisions.

## Key Verification Commands (SEED=42)
```bash
pip install -r requirements.txt
SEED=42 make check            # fast convention-robustness + template validation (~seconds)
SEED=42 make verify-quick     # ~8 min: 8 drivers + batch_run + validate + E042 n_sim=2
SEED=42 make verify-extended  # +18 committed drivers vs goldens (drift report)
SEED=42 make verify-full      # E042 n_sim=50 + 96-config sensitivity grid
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

---
*Generated by agentic session at 2026-11-15T12:11:33Z*