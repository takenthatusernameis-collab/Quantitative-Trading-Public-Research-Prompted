# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-15T10:11:33Z
**Session**: Durable handoff refresh (E373)
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch / HEAD**: `main` @ `d48d94a95f6fdb8e33e1b6d2602d8095dcb12838` ("chore(kilo): checkpoint agent session")
**Sync**: `origin/main...HEAD` → `0 0` (in sync)
**Supersedes**: `handoff_2026-11-15T10-10-33Z_INITIAL_TASK.md` (HEAD `71de3ab0`, E372)

---

## TL;DR — What this repository is

Independent, reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. **Research phase complete (E001–E051).** All experiments
are pre-registered with falsification expectations and promotion gates; negative
results are recorded honestly. Surviving validated strategies are documented in
`ledger/RESEARCH_LEDGER.md`.

There is **no open research task**. This session was a durable-handoff refresh only.

---

## Clear initial task for the next session

1. **Verify environment integrity** (seconds, offline): `SEED=42 bash scripts/check.sh`
   (or `make check`). In a sandbox lacking pandas/numpy this exits 1 **only** on the
   numpy/pandas-dependent unit tests; every repo-level guard step is green.
2. **Read `ledger/RESEARCH_LEDGER.md`** for current strategy dispositions and the
   standing open item on E041/E042 tangency-QP drift (ill-conditioned QP; do **not**
   re-pin goldens to silence numeric drift).
3. **Run verification as needed**: `make verify-quick` (~8 min),
   `make verify-extended` (~21 min), `make verify-full` (~15 min) — all with `SEED=42`.
4. **Any new work must be a pre-registered experiment** with gates, falsification
   expectations, and a sensitivity grid declared before execution. Goalposts are
   never moved post-hoc.
5. **Before committing**: confirm `scripts/check_goldens_clean.py` and
   `scripts/check_golden_baseline.py` pass; restore the golden baseline if a
   verification run was interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).

---

## Verified state at handoff time (this session, no verification run)

Per-step guard isolation — all **exit 0**:
- `scripts/check_json_artifacts.py` (114 JSON artifacts parse)
- `scripts/check_goldens_clean.py` (committed goldens match HEAD)
- `scripts/check_golden_baseline.py` (all 107 pinned goldens match)
- `scripts/check_data_coverage.py` (all 35 pinned data inputs present/tracked/unchanged)
- `verify_convention_robustness.py`
- `scripts/validate_template.py`
- `scripts/check_experiment_imports.py`
- Unit guards: `tests.test_json_guard`, `tests.test_goldens_guard`,
  `tests.test_golden_baseline`, `tests.test_drift_report` → exit 0

Environment-only failure (this sandbox lacks numpy/pandas; **not** a code defect):
- `tests.test_portfolio_opt` → `ModuleNotFoundError: No module named 'numpy'`;
  `tests.test_data_coverage` → `ModuleNotFoundError: No module named 'pandas'`.
- `SEED=42 bash scripts/check.sh` exits 1 solely on those dependency-bound unit tests.

**Delta vs prior handoff** (`71de3ab0..d48d94a9`, research content only:
`experiments/ data/ src/ scripts/ tests/ research_state/`, excluding
`__pycache__`/`*.pyc`/handoff/`*.md`): **0 paths**. Only checkpoint commits,
`ledger/RESEARCH_LEDGER.md`, generic handoff pointer/symlink files, and
`__pycache__/*.pyc` changed. **No research substance changed.**

Working tree: only tracked `__pycache__/*.pyc` modifications plus this handoff
deliverable. No `.verify_snapshot/` / `.verify_reports/`; no interrupted verification run.

---

## Quick Start commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh          # or: make check

# Verification suite (always SEED=42)
SEED=42 python3 run_all_verification.py             # quick  (~8 min)  = make verify-quick
SEED=42 python3 run_all_verification.py --extended  # extended (~21 min) = make verify-extended
SEED=42 python3 run_all_verification.py --full      # full  (~15 min)   = make verify-full

# Recovery after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key guardrails

- **Seed**: always `SEED=42`.
- **Golden files**: `experiments/*.json` are committed canonical artifacts; never
  commit verification output. The suite backs up and restores them.
- **Cache coverage is an enforced invariant** (`scripts/check_data_coverage.py`):
  unpinned data = live download = non-reproducible. Add data inputs only by
  committing + re-pinning (`python3 scripts/check_data_coverage.py --update`).
- **Optimizer determinism** (ledger E049): solver answers are validated on the
  problem's constraints, not on solver exit status. Do not gate on SLSQP status.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy,
  pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.
- **CI**: `.github/workflows/verification-gate.yml` cannot be created by automated
  agents; a maintainer must create it from `.github/workflow-templates/`.
- **Commits**: do not commit unless the user explicitly asks.

## Canonical artifacts

- `ledger/RESEARCH_LEDGER.md` — surviving validated strategies + experiment log (through E373).
- `experiments/*.json` — 107 pinned golden artifacts.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — SHA-256 fingerprints.
- `data/vintages.json`, `data/fundamentals_vintages.json` — pinned data vintages.
- `scripts/repoint_handoff.py` — repoints the generic handoff symlinks to the latest artifact.

---
*Durable handoff — update for each new session; retain prior artifacts for history.*