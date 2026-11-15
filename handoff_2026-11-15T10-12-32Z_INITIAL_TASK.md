# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-15T10:12:32Z
**Session**: Durable handoff refresh (no research work performed)
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD**: `main` @ `d48d94a95f6fdb8e33e1b6d2602d8095dcb12838` ("chore(kilo): checkpoint agent session")
**Sync**: `origin/main...HEAD` → `0 0` (in sync at handoff time)
**Supersedes**: `handoff_2026-11-15T10-11-33Z_INITIAL_TASK.md`

---

## TL;DR — Repository state

Independent, reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. **Research phase complete (E001–E051).** All experiments are pre-registered with falsification expectations and promotion gates; negative results are recorded honestly. Surviving validated strategies and dispositions are documented in `ledger/RESEARCH_LEDGER.md`.

There is **no open research task**. This session created a durable handoff only.

---

## Clear initial task for the next session

1. **Verify environment/baseline integrity first (offline, seconds):**
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - In environments missing `numpy`/`pandas`, `check.sh` may fail only on dependency-bound unit tests; repo-level guard steps (goldens, baseline fingerprints, data coverage, JSON/template/import/convention checks) should still be green.
2. **Read context before acting:**
   - `ledger/RESEARCH_LEDGER.md` for strategy dispositions, completed experiments, and standing notes.
   - Note the standing open item on **E041/E042 tangency-QP drift** (ill-conditioned QP / 1-ulp sensitivity): do **not** re-pin those goldens to silence numeric drift.
3. **Run verification as needed (always `SEED=42`):**
   - `make verify-quick` (~8 min)
   - `make verify-extended` (~21 min)
   - `make verify-full` (~15 min)
4. **If doing new work:** it must be a **pre-registered experiment** with objective, gates, falsification expectations, and sensitivity grid declared before execution. Never move goalposts post-hoc. Record negative/partial outcomes honestly.
5. **Before committing anything (only if explicitly requested):**
   - Ensure `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass.
   - Never commit verification output/captured goldens by accident.
   - If a verification run is interrupted, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per AGENTS/ledger guidance).

---

## Observed state at handoff creation

- **HEAD unchanged**: `d48d94a95f6fdb8e33e1b6d2602d8095dcb12838` on `main`, in sync with `origin/main`.
- **Research substance unchanged in this session**: no edits made to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, or `ledger/RESEARCH_LEDGER.md`.
- **Working tree**: tracked `__pycache__/*.pyc` modifications present in `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/` (12 files). No source changes were made; treat as incidental bytecode churn unless intentionally regenerated — do not commit.
- **No interrupted verification markers observed**: no `.verify_snapshot/` / `.verify_reports/` present at handoff time.

---

## Key guardrails (from AGENTS.md / project conventions)

- **Seed**: always `SEED=42`.
- **Golden artifacts**: `experiments/*.json` are canonical; verification backs up/restores them — never leave a run half-finished.
- **Baseline/data integrity**: `ledger/golden_baseline.json` and `ledger/data_baseline.json` pin fingerprints; `scripts/check_data_coverage.py` enforces tracked/pinned inputs. Add data only by committing + re-pinning (`python3 scripts/check_data_coverage.py --update`). Re-pin goldens only deliberately (never as a side effect of verification).
- **Optimizer determinism**: validate solver answers on problem constraints, not solver exit status (see ledger E049 / `tests/test_portfolio_opt.py`).
- **Offline verification**: suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`; missing cache/input must fail hard.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.
- **CI**: `.github/workflows/verification-gate.yml` cannot be created by automated agents; maintainer must create from `.github/workflow-templates/`.
- **Commits**: do not commit unless explicitly requested by the user.

## Canonical artifacts

- `ledger/RESEARCH_LEDGER.md` — surviving strategies, experiment log, dispositions.
- `experiments/*.json` — pinned golden artifacts.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — SHA-256 baselines.
- `data/vintages.json`, `data/fundamentals_vintages.json` — pinned data snapshots.
- `AGENTS.md` — commands, verification modes, baseline/integrity rules.
- `run_all_verification.py`, `scripts/check.sh` — verification entrypoints.

---
*Durable handoff created for continuity; retain prior handoff files for history.*