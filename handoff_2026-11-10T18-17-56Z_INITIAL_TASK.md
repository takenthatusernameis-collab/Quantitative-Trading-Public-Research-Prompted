# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T18:17:56Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `86c92607` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (observed at handoff)

- `git status --short --branch`: `## main` with a modified tracked bytecode artifact `M src/__pycache__/cache_keys.cpython-312.pyc` (unrelated to research baselines; do not stage/commit unless explicitly instructed).
- `.verify_snapshot/`: **absent** (no interrupted verification run requiring recovery).
- Research phase **complete (E001–E043)**. Authoritative dispositions and history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines remain authoritative and must not be modified by routine work: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Known note: some pinned data inputs (e.g. `data/panel.parquet` where applicable) may be absent in a fresh tree; verification enforces `QUANT_RESEARCH_OFFLINE=1`, so missing pinned cache fails hard rather than re-downloading.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm source state and note HEAD/remote alignment.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml`; maintainer action).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys or introduce logging of secrets.
- Do not stage/commit bytecode artifacts (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T18-17-56Z_INITIAL_TASK.md` (root).
- **Prior operational handoff:** `handoff_2026-11-10T18-15-58Z_INITIAL_TASK.md` (retained as history).
