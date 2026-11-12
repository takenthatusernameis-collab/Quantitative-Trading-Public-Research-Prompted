# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T19:00:15Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `b9f5f994d4fe619c931e1388b55b17b043f124ec` (`chore(kilo): checkpoint agent session`) — in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff time)

- **Working tree:** tracked modifications only in `scripts/__pycache__/*.pyc`, `src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc` (bytecode artifacts, no source/experiment/script/test/baseline logic changes). No untracked files. **Do not stage or commit `__pycache__` changes as substantive work** (restore/discard if not intentional).
- **`.verify_snapshot/`:** absent — no interrupted verification run pending.
- **Baseline guards (re-run, stdlib-only):**
  - `python3 scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
  - `python3 scripts/check_data_coverage.py` → ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED
- **Inventory:** `git ls-files experiments/` = 138 (107 golden JSONs + 31 drivers). `git diff HEAD -- experiments/ data/` empty.
- **Research phase:** complete (E001–E043). Authoritative dispositions/evidence: `ledger/RESEARCH_LEDGER.md`; ranking: `ledger/PRIORITIZATION.md`. Last research entry E051; subsequent entries are durable-handoff refreshes only. No actionable OPEN/PENDING/BLOCKED/TODO research items.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Environment caveat:** full `scripts/check.sh`/tests/verification require `numpy`, `pandas`, `scipy`, `statsmodels`, `yfinance` (`pip install -r requirements.txt`). Missing scientific deps in this sandbox are environmental, not a repo defect.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

If work is requested, verify state first:
1. `git status --short --branch` — confirm HEAD/remote alignment; handle tracked `__pycache__` modifications explicitly (do not commit as substantive change).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

## Reproduction / verification (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 scripts/check_golden_baseline.py      # 107 goldens vs ledger/golden_baseline.json
SEED=42 python3 scripts/check_data_coverage.py        # 35 pinned data inputs
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-12T19-00-15Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-12T18-58-33Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained for history).
- Generic canonical pointers repointed to this artifact via `scripts/repoint_handoff.py`. No code, experiments, ledgers, or baselines modified.
