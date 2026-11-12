# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T19:51:57Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `7d08f8cc` (`chore(kilo): checkpoint agent session`, 2026-11-12) — tracking `origin/main`

## Current state (verify before acting)

- **Working tree:** clean (`git status --short --branch` shows `## main...origin/main`). Confirm before acting; if tracked `__pycache__/*.pyc` or other non-substantive drift appears, restore/discard explicitly — do not commit bytecode as substantive change.
- **`.verify_snapshot/`:** expected absent (no interrupted verification run). If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
- **Research phase:** complete (E001–E043). Surviving strategies/dispositions: `ledger/RESEARCH_LEDGER.md`, `ledger/PRIORITIZATION.md`. E051 is the last research entry; subsequent entries are durable-handoff refreshes.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Baselines/inventory (as pinned):** 138 tracked under `experiments/` (107 golden JSONs + 31 drivers), 107 goldens pinned in `ledger/golden_baseline.json`, 35 data inputs pinned in `ledger/data_baseline.json`. Re-verify with guards below before substantive work.
- **Environment caveat:** full `scripts/check.sh`/tests/verification require `numpy`, `pandas`, `scipy`, `statsmodels`, `yfinance` (`pip install -r requirements.txt`). Missing scientific deps in a sandbox are environmental, not a repo defect.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes/sensitivity grids, or modify golden/baseline artifacts without explicit direction.

If work is requested:
1. `git status --short --branch` — confirm HEAD/remote alignment and clean state.
2. Confirm `.verify_snapshot/` is absent; recover first if needed.
3. Run baseline guards before substantive changes/commits:
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - `python3 scripts/check_golden_baseline.py`
   - `python3 scripts/check_data_coverage.py`
4. Implement only the explicitly requested change, following existing conventions (SEED=42, close-to-close v1.2.3 primary, no secrets). Run relevant verification for touched areas.

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
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-12T19-51-57Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** prior timestamped handoffs (retained for history); generic canonical pointers repointed to this artifact via `scripts/repoint_handoff.py`. No experiments, ledgers, baselines, or source modified by this handoff refresh.
