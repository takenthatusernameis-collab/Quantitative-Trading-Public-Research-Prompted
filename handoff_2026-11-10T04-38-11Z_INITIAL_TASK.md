# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T04:38:11Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a8866363` (`chore(kilo): checkpoint agent session`, 2026-11-10 04:37:00 +0000)
**Remote:** `origin/main` in sync (0 ahead, 0 behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: **clean source** (`## main...origin/main`). Only 12 tracked `__pycache__/*.pyc` modifications present (ignored by `.gitignore`). No uncommitted source changes.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Research phase complete (**E001–E043**); authoritative dispositions/history in `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift (~1e-05, 1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- **Known data issue:** `data/panel.parquet` is pinned in `ledger/data_baseline.json` but missing from the working tree (gitignored), differs from its pinned fingerprint, and is not git-tracked. A driver needing it will re-download. This is a known cache-coverage gap; do not re-pin without explicit direction.

## Environment note (important for the next session)

- The pinned Python stack is installed (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0). If the environment is ever reset, re-run `pip install -r requirements.txt` before `check.sh`.
- `check.sh`'s `FAIL experiments/d.json`, `experiments/b.json`, `experiments/x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json` lines are **intentional negative-control fixtures** consumed by `tests/test_json_guard` — they are not real artifacts and are not a problem.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note `HEAD` vs `origin/main`.
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
- Do not stage, commit, or "fix" bytecode artifacts (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T04-38-11Z_INITIAL_TASK.md` (root), mirrored via canonical symlinks.
- **Supersedes (operationally):** `handoff_2026-11-10T04-37-01Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).