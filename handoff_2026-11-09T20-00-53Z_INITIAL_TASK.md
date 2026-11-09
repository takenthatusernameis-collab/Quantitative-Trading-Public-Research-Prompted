# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-09T20:00:53Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `000e88c2` (`chore(kilo): checkpoint agent session`, 2026-11-09 20:00:53 +0000)
**Remote:** `origin/main` in sync (0 ahead, 0 behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: **clean** (`## main...origin/main`, no uncommitted changes). Only `.pyc` cache files modified (gitignored).
- `.verify_snapshot/`: **absent in repo root**; stale snapshot exists in `/home/runner/work/_temp/kilo-tmp/tmphcg0b7f2/.verify_snapshot` (owned by dead pid 999999). If the working tree shows modified goldens, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) before other work.
- `SEED=42 bash scripts/check.sh`: **exit 0, ALL CHECKS PASSED** (convention robustness, golden baseline, data coverage, unit tests, experiment imports). Negative-control fixture failures (`experiments/d.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json`) are intentional and expected.
- **Note:** `check.sh` reports `experiments/e001.json` differs from HEAD and a stale verification snapshot — both appear to be transient state from the temp snapshot; `git diff HEAD -- experiments/e001.json` shows no diff. If in doubt, run `--restore-only`.
- **Note:** `data/panel.parquet` is **missing from working tree** and **not git-tracked** (gitignored). It is pinned in `ledger/data_baseline.json` but absent on disk; a driver needing it will re-download from yfinance (non-bit-reproducible). This is a known coverage gap — see `AGENTS.md` cache coverage invariant.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043**); dispositions/history in `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.

## Environment note (important for the next session)

- Python dependencies installed (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0). If environment resets, run `pip install -r requirements.txt` before `check.sh`.
- `check.sh`'s `FAIL experiments/d.json`, `experiments/b.json`, `experiments/x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json` lines are **intentional negative-control fixtures** consumed by `tests/test_json_guard` — they are not real artifacts and are not a problem.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent in repo root. If stale/interrupted (or goldens modified): `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
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

- **Durable artifact (this session):** `handoff_2026-11-09T20-00-53Z_INITIAL_TASK.md` (root), mirrored via `handoff_CURRENT*` / `HANDOFF_CURRENT*` symlinks.
- **Supersedes (operationally):** `handoff_2026-11-09T18-02-50Z_INITIAL_TASK.md` (and earlier timestamped handoffs, retained as history).