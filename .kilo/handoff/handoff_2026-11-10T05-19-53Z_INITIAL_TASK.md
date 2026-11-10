# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T05:19:53Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `19c18381` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` @ `19c18381` (in sync — verify with `git status -sb`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: **source clean** (`## main...origin/main`, no staged/unstaged tracked changes, no `__pycache__/*.pyc` working-tree modifications).
- `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/`: **empty**.
- `git ls-files experiments/`: **138 tracked golden artifacts, all matching HEAD**.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Research phase complete (**E001–E043**). Authoritative history/dispositions: `ledger/RESEARCH_LEDGER.md` (last entry E128, 2026-11-10T02:44Z).
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift (~1e-05, 1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- **Known data issue:** `data/panel.parquet` is pinned in `ledger/data_baseline.json` but missing from the working tree (gitignored) and differs from its pinned fingerprint; a driver needing it may re-download. Known cache-coverage gap — do not re-pin without explicit direction.

## Delta vs Prior Durable Handoff (E128, HEAD `0a2e002b`)

HEAD advanced `0a2e002b` → `19c18381` via two checkpoint commits (`chore(kilo): checkpoint agent session`); the only files that differ between the two commits are the handoff symlink tree (`handoff_2026-11-10T04-37-01Z_INITIAL_TASK.md`, `handoff_2026-11-10T05-18-23Z_INITIAL_TASK.md`, `handoff_latest.md`, `handoff_next_session.md`, `initial_task.md`, `next_session.md`). No research artifacts, baselines, source, tests, scripts, or ledger substance changed. Prior closed/conformance state adopted.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean source and note `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output**. Restore goldens after any interrupted run. If guards report a golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

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
- Do not stage, commit, or "fix" tracked `__pycache__/*.pyc` unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T05-19-53Z_INITIAL_TASK.md` (root).
- **Supersedes (operationally):** `handoff_2026-11-10T05-18-23Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **Convenience symlinks** in repo root (`handoff_latest.md`, `handoff_next_session.md`, `initial_task.md`, `next_session.md` and related aliases) repointed to this artifact.