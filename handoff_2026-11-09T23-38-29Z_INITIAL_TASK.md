# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-09T23:38:29Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `4b9d1461` (`chore(kilo): checkpoint agent session`) — in sync with `origin/main` (0 ahead, 0 behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Session Summary (this handoff)

- **No substantive research, code, or artifact changes were made.** This session verified repository state and left a durable, timestamped handoff for the next agentic work session.
- `git status --short --branch`: clean (`## main...origin/main`); no tracked/uncommitted source changes.
- `.verify_snapshot/`: **absent** (no interrupted verification restore pending).
- Canonical baselines remain authoritative and untouched: `experiments/*.json` (138 committed goldens), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions/history in `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- Prior handoffs retained as history: `handoff_2026-11-09T23-37-34Z_INITIAL_TASK.md`, `handoff_2026-11-09T23-36-21Z_INITIAL_TASK.md`, `handoff_2026-11-09T23-35-49Z_INITIAL_TASK.md`, and earlier.

## Environment

- Pinned Python stack per `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). If the environment is reset, run `pip install -r requirements.txt` before checks.
- `check.sh` `FAIL experiments/d.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json` lines are **intentional negative-control fixtures** for `tests/test_json_guard` — not real artifacts.
- `research_state/workflow_run_diagnostics.jsonl` exists (session diagnostics only, not a research artifact).
- `workflow_backups/` holds historical `.github/workflows/main.yml` backups (not active).

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)
1. `git status --short --branch` — confirm HEAD/origin and local state.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

### If asked to run verification
- Use `SEED=42`. **Never commit verification output** over `experiments/*.json`.
- `run_all_verification.py` backs up/restores goldens; if interrupted, restore before committing.
- If `check.sh` reports golden/baseline mismatch, fix/restore before committing. Do not blindly `git checkout -- experiments/` if HEAD is already contaminated; restore pinned artifacts per `ledger/golden_baseline.json` / ledger process.

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
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer path: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- `check.sh` `FAIL experiments/d.json,b.json,x.json,e2.json,badlist.json,u.json,d2.json` lines are intentional `tests/test_json_guard` fixtures, not real artifacts.

## Handoff Provenance

- **Durable artifact:** `handoff_2026-11-09T23-38-29Z_INITIAL_TASK.md` (repo root).
- **Operational pointers updated:** `handoff_CURRENT`, `handoff_CURRENT.md`, `handoff_LATEST`, `handoff_LATEST.md`, `handoff_current`, `handoff_current.md`, `handoff_latest`, `handoff_latest.md`, `handoff_next`, `handoff_next.md`, `handoff_next_session`, `handoff_next_session.md`, `handoff_next_session_HANDOFF`, `handoff_next_session_HANDOFF.md`, `handoff_next_session_handoff`, `handoff_next_session_handoff.md` → this artifact.
- **Supersedes operationally:** `handoff_2026-11-09T23-37-34Z_INITIAL_TASK.md` and prior handoffs (retained as history).

(End of file)