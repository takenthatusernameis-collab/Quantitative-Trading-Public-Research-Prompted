# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T00:44:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `90204c1f` (`chore(kilo): checkpoint agent session`) — in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: source tree clean relative to tracked source/artifacts; **only `__pycache__/*.pyc` bytecode modifications** are present (no source, test, ledger, or `experiments/` changes). No research commit was made in this session.
- `.verify_snapshot/`: **absent** (no interrupted verification restore pending).
- Canonical baselines remain authoritative: `experiments/*.json` (committed goldens), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions/history in `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- Known data note: `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be missing from a fresh working tree (gitignored); do not re-pin without explicit direction.

## Environment

- Pinned Python stack expected per `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). If the environment is reset, run `pip install -r requirements.txt` before checks.
- `check.sh`’s `FAIL experiments/d.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json` lines are **intentional negative-control fixtures** used by `tests/test_json_guard` — not real artifacts.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### If the user requests work, verify state first
1. `git status --short --branch` — confirm `HEAD`/origin state and note any local changes (treat stray `__pycache__` diffs as non-source noise).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If asked to run verification
- Use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`.
- `run_all_verification.py` backs up/restores goldens; if interrupted, restore before committing.
- If `scripts/check.sh` reports a golden/baseline mismatch, fix/restore before committing.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and proper process.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T00-44-00Z_INITIAL_TASK.md` (root), mirrored to `handoff/` and `.kilo/handoff/`; primary `handoff_CURRENT*`/`handoff_LATEST*`/`handoff_current*`/`handoff_latest*`/`handoff_next*` symlinks updated to this file.
- **Supersedes (operationally):** `handoff_2026-11-10T00-42-50Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
