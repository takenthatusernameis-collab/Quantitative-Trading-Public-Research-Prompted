# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-09T21:17:42Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `0eb2a479` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` in sync at time of check (0 ahead, 0 behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: **source clean** (`## main...origin/main`). Only 15 `__pycache__/*.pyc` modifications present (build artifacts); no uncommitted source/test/ledger/experiment changes.
- `.verify_snapshot/`: **absent** (no interrupted verification restore pending).
- `SEED=42 bash scripts/check.sh`: **exit 0, ALL CHECKS PASSED** (run 2026-11-09T21:17Z). JSON artifacts parse; golden artifacts match `HEAD` and `ledger/golden_baseline.json` fingerprint; pinned data inputs present/tracked/unchanged; unittest modules OK; convention robustness OK; experiment imports OK.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions/history in `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- **Known data issue:** `data/panel.parquet` is pinned in `ledger/data_baseline.json` but missing from the working tree (gitignored), differs from its pinned fingerprint, and is not git-tracked. A driver needing it will re-download. This is a known cache-coverage gap; do not re-pin without explicit direction.

## Environment note

- Pinned Python stack is expected (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0). If the environment is reset, run `pip install -r requirements.txt` before `check.sh`.
- `check.sh` `FAIL experiments/d.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json` lines are **intentional negative-control fixtures** for `tests/test_json_guard` — not real artifacts.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean source and note `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output**. Restore goldens after any interrupted run. If `scripts/check.sh` reports a golden/baseline mismatch, fix/restore before committing.

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
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-09T21-17-42Z_INITIAL_TASK.md` (repo root).
- **Operational pointer:** `handoff_CURRENT` / `handoff_CURRENT.md` updated to this artifact.
- **Supersedes (operationally):** prior timestamped handoffs (retained as history).

(End of file - total 66 lines)