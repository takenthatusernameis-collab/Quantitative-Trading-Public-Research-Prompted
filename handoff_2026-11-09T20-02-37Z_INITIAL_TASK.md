# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-09T20:02:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `000e88c2` (`chore(kilo): checkpoint agent session`, 2026-11-09 20:00:53 +0000)
**Remote:** `origin/main` in sync with local `main` at handoff time (verify with `git status -sb`).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` with **tracked `__pycache__/*.pyc` modifications** present in the worktree (15 files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`). No source/golden/config changes were made in this handoff session. Treat these as incidental bytecode changes; do not commit them unless explicitly requested.
- `.verify_snapshot/`: **absent in repo root**. Prior notes mentioned a stale snapshot under `/home/runner/work/_temp/kilo-tmp/...` (dead pid) — not actionable from repo root, but if you see modified `experiments/*.json` goldens or an active/stale snapshot marker, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) **before** other work.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions/history in `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- `data/panel.parquet` may be absent from the working tree (gitignored, pinned in `ledger/data_baseline.json`); drivers requiring it may trigger non-bit-reproducible yfinance downloads if missing — see `AGENTS.md` cache coverage invariant.

## Environment

- Python deps expected per `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). If reset: `pip install -r requirements.txt`.
- `scripts/check.sh` negative-control fixture `FAIL` lines (`experiments/d.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json`) are **intentional** (consumed by `tests/test_json_guard`) — not real failures.

## INITIAL TASK (clear)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm `HEAD` vs `origin/main`; note any incidental `*.pyc` changes or unexpected diffs.
2. Confirm `.verify_snapshot/` is absent in repo root. If stale/interrupted or `experiments/*.json` modified: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output**. Restore goldens after any interrupted run. If `scripts/check.sh` reports a golden/baseline mismatch, fix/restore before committing.

## Verification Commands (only if explicitly requested)

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

- **Durable artifact (this session):** `handoff_2026-11-09T20-02-37Z_INITIAL_TASK.md` (repo root).
- **Supersedes (operationally):** `handoff_2026-11-09T20-00-53Z_INITIAL_TASK.md` (and earlier timestamped handoffs, retained as history).
