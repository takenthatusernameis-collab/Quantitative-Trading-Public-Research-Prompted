# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T05:23:17Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `5cf73b42` (`chore(kilo): checkpoint agent session`) — in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: **source clean** (`## main...origin/main`, no staged/unstaged tracked changes, no `__pycache__/*.pyc` working-tree modifications; only `.kilo/.gitignore` is ignored).
- `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/`: **empty**.
- `git ls-files experiments/`: **138 tracked golden artifacts, all matching HEAD**.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Research phase complete (**E001–E043**). Authoritative history/dispositions: `ledger/RESEARCH_LEDGER.md` (last durable-handoff entry E129, HEAD `19c18381`, 2026-11-10T05:19Z).
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1e-05, 1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- **Known data note:** `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be missing from a fresh working tree (gitignored); a driver needing it may re-download. Known cache-coverage gap — do not re-pin without explicit direction.

## Delta vs Prior Durable Handoff (E129, HEAD `30819ec3`)

HEAD advanced `30819ec3` → `5cf73b42` via one checkpoint commit (`chore(kilo): checkpoint agent session`). The only working-tree change vs `30819ec3` is the handoff file tree: `handoff_2026-11-10T05-22-22Z_INITIAL_TASK.md` was removed and `handoff_2026-11-10T05-23-17Z_INITIAL_TASK.md` added. No research artifacts, baselines, source, tests, scripts, or ledger substance changed. Prior closed/conformance state adopted.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean source and note `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report a golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

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

- **Durable artifact (this session):** `handoff_2026-11-10T05-23-17Z_INITIAL_TASK.md` (root), mirrored to `handoff/` and `.kilo/handoff/`; primary symlinks `handoff_CURRENT*`/`handoff_LATEST*`/`handoff_latest*`/`handoff_next*` updated to this file.
- **Supersedes (operationally):** `handoff_2026-11-10T05-19-53Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).