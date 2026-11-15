# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T11:10:08Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `b196ce62` ("chore(kilo): checkpoint agent session")
**Sync:** `main...origin/main` → `0 0` (in sync at handoff time)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## TL;DR — Repository state

Independent, reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. **Research phase complete (E001–E051).** All experiments are pre-registered with falsification expectations and promotion gates; negative results are recorded honestly. Surviving validated strategies and dispositions are documented in `ledger/RESEARCH_LEDGER.md`.

**There is no open research task.** This handoff session performed no research work; it only inspected state and produced this durable handoff.

---

## Clear initial task for the next session

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, move goalposts, or modify canonical baselines/goldens without explicit direction.

### 1) Baseline integrity / environment check (before substantive work)
```bash
git status --short --branch
# Confirm no interrupted verification:
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
SEED=42 bash scripts/check.sh
# or: make check
```
Note: this sandbox has **no `numpy`, `pandas`, or `pytest`** installed. The repo-level guard
scripts (`scripts/check_json_artifacts.py`, `scripts/check_goldens_clean.py`,
`scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`,
`verify_convention_robustness.py`, `scripts/validate_template.py`,
`scripts/check_experiment_imports.py`) all pass with exit 0; only
pandas/numpy/pytest-dependent unit tests fail, and `SEED=42 bash scripts/check.sh`
exits 1 in this environment solely for that reason. Install deps with
`pip install -r requirements.txt` (plus `pytest` for the unit-test suite) before
running the full `check.sh` / verification suite.

### 2) If verification/reproduction is explicitly requested
Always use **`SEED=42`**.
```bash
make verify          # convention robustness only (reads JSONs, no writes)
make verify-quick    # ~8 min
make verify-extended # ~21 min
make verify-full     # ~15 min
```
- `run_all_verification.py` overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted/stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per AGENTS.md).
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

### 3) If new research work is explicitly requested
- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**.
- Use `SEED=42`; keep data/cache/baseline invariants intact (`QUANT_RESEARCH_OFFLINE=1` expectations, pinned inputs).
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts as appropriate.
- Do not reopen closed E049/E050 or treat E041/E042 residual drift as a re-pin target.

---

## Observed state at handoff creation

- **HEAD:** `b196ce62` on `main`, in sync with `origin/main` (`0 0` ahead/behind).
- **No interrupted verification markers observed:** neither `.verify_snapshot/` nor `.verify_reports/` present.
- **Working tree:** tracked `__pycache__/*.pyc` modifications present in `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/` (incidental bytecode churn; no source edits made in this handoff session). Treat as uncommitted environment noise unless intentionally regenerated — do not commit casually.
- **Repo-level guards (this session, per-step isolation, no verification run):**
  - `scripts/check_json_artifacts.py` → exit 0 (all committed JSON artifacts parse)
  - `scripts/check_goldens_clean.py` → exit 0 (goldens match HEAD)
  - `scripts/check_golden_baseline.py` → exit 0 (all pinned goldens match)
  - `scripts/check_data_coverage.py` → exit 0 (all 35 pinned data inputs present/tracked/unchanged)
  - `verify_convention_robustness.py` → exit 0
  - `scripts/validate_template.py` → exit 0
  - `scripts/check_experiment_imports.py` → exit 0
  - Unit tests (`tests.test_json_guard`, `test_goldens_guard`, `test_golden_baseline`,
    `test_drift_report`, `test_data_coverage`, `test_portfolio_opt`) → cannot run:
    **`No module named 'pytest'` / `'numpy'` / `'pandas'`** (environment-only; not a code failure).
- **Delta since prior durable handoff (`handoff_2026-11-15T11-07-31Z_INITIAL_TASK.md`, HEAD `606f3c06` → `b196ce62`):** `git diff --name-only 606f3c06..b196ce62` filtered for research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, excl `__pycache__`/`*.pyc`/handoff/`*.md`) → **0 paths**. Only checkpoint commit(s), generic handoff symlink/pointer files, and `__pycache__/*.pyc` changed; no research substance changed.

---

## Key guardrails (from AGENTS.md / project conventions)

- **Seed:** always `SEED=42`.
- **Golden artifacts:** `experiments/*.json` are canonical; verification backs up/restores them — never leave a run half-finished.
- **Baseline/data integrity:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` pin fingerprints; `scripts/check_data_coverage.py` enforces tracked/pinned inputs. Add data only by committing + re-pinning (`python3 scripts/check_data_coverage.py --update`). Re-pin goldens only deliberately (never as a side effect of verification).
- **Optimizer determinism:** validate solver answers on problem constraints, not solver exit status (see ledger E049 / `tests/test_portfolio_opt.py`).
- **Offline verification:** suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`; missing cache/input must fail hard.
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.
- **CI:** `.github/workflows/verification-gate.yml` cannot be created by automated agents; maintainer must create from `.github/workflow-templates/`.
- **Commits:** do not commit unless explicitly requested by the user.

---

## Key references

- `AGENTS.md` — commands, verification modes, baseline/integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions, completed experiments, standing notes
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `data/vintages.json`, `data/fundamentals_vintages.json` — pinned data snapshots
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints

---

## Provenance

- Created as a durable handoff artifact for continuity; prior `handoff_*` / `HANDOFF_*` files retained for history.
- No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff session.