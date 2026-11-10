# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T08:21:25Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `8bfbd661` (`chore(kilo): checkpoint agent session`)
**Remote:** verify `HEAD` vs `origin/main` on session start
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- Research phase complete (**E001–E043**). Authoritative dispositions, findings, and history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative and must remain stable unless an explicit, intentional re-baseline is requested: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- No interrupted verification known at handoff time; confirm `.verify_snapshot/` is absent on start.
- Closed/resolved — do not reopen: E049/E050 and the E041/E042 residual ill-conditioned QP drift (~1e-05, 1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Known data note: `data/panel.parquet` may be missing/untracked in some environments (gitignored) while pinned in `ledger/data_baseline.json`; treat as a cache-coverage environment issue, not a license to re-pin without explicit direction.
- Supersedes prior operational handoff: `handoff_2026-11-10T08-20-31Z_INITIAL_TASK.md` (earlier handoffs retained as history).

## Initial Task for Next Session (CLEAR)

**Default:** wait for explicit user instructions. Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**On session start (before substantive work):**
1. `git status --short --branch` — confirm clean state and `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If present/stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. If asked to make changes, run `SEED=42 bash scripts/check.sh` (or `make check`) before committing.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over canonical goldens. If `scripts/check.sh` or baseline guards report mismatch, restore/fix before committing.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Do not stage/commit bytecode (`__pycache__/*.pyc`) unless explicitly instructed.

**Next agent action:** await explicit user task.
