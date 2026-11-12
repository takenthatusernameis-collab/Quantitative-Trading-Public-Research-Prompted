# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T18:56:05Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a949390a` (`chore(kilo): checkpoint agent session`, 2026-11-12 18:55:29 +0000) — in sync with `origin/main` (`+0 -0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff time)

- **Working tree:** one tracked modification only — `src/__pycache__/cache_keys.cpython-312.pyc` (Python bytecode regeneration, 3462 bytes, no source/logic change). Build noise: handle explicitly (restore/discard/commit) and never let it contaminate a substantive commit. No source, experiment, script, test, or baseline artifact changes pending.
- **`.verify_snapshot/`:** absent — no interrupted verification run pending, no recovery needed.
- **Baseline guards re-run just now:** `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**; `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**. `git diff HEAD -- experiments/ data/` → empty. `git ls-files experiments/` → 138 tracked entries (107 golden JSONs + 31 drivers).
- **Delta vs prior durable handoff (E176/E177, HEAD `0e3881c2` → `2e3b9898` → `a949390a`):** two checkpoint commits, handoff artifacts/symlinks and `ledger/RESEARCH_LEDGER.md` only. Filtered for research substance (`experiments/`, `data/`, `src/`, `tests/`, `scripts/`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`) → **0 paths**.
- **Research phase:** complete (E001–E043). Authoritative dispositions and open items in `ledger/RESEARCH_LEDGER.md`; ranking in `ledger/PRIORITIZATION.md`. Last research entry E051; E052–E176 are durable-handoff refreshes only. `grep -E 'OPEN|PENDING|BLOCKED|TODO'` over the ledger → 0 actionable markers (matches are historical closure notes).
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.
- **Environment caveat (this sandbox):** `/usr/bin/python3` lacks `requirements.txt` packages (`ModuleNotFoundError: No module named 'numpy'`). The fast guards above are stdlib-only and pass; `scripts/check.sh`, `tests/`, and the verification suite need an interpreter with numpy/pandas/scipy/statsmodels/yfinance. Install via `pip install -r requirements.txt` before any verification run — this is environmental, not a repository defect.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

If work is requested, verify state first:
1. `git status --short --branch` — confirm HEAD/remote alignment; treat the tracked `__pycache__` modification explicitly.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

If asked to run verification: always `SEED=42`; use `run_all_verification.py` (quick), `--extended`, or `--full`; **never commit verification output** over `experiments/*.json`; restore goldens after any interrupted run; if guards report a golden/baseline mismatch, fix or restore before committing — **do not re-pin to silence it**.

## Reproduction / verification commands (run only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 scripts/check_golden_baseline.py      # 107 pinned goldens vs ledger/golden_baseline.json
SEED=42 python3 scripts/check_data_coverage.py        # 35 pinned data inputs
SEED=42 python3 run_all_verification.py               # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config sensitivity grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-12T18-56-05Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-12T18-49-45Z_INITIAL_TASK.md`, `handoff_2026-11-12T18-49-14Z_INITIAL_TASK.md`, and all earlier timestamped handoffs (retained for history).
- Generic canonical pointers (`HANDOFF`, `CURRENT`, `CURRENT.md`, `LATEST`, `NEXT`, `latest`, `next`, `next_session`, `initial_task`, plus `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/` aliases) are repointed to this artifact via `scripts/repoint_handoff.py`. No code, experiments, ledgers, or baselines were modified.