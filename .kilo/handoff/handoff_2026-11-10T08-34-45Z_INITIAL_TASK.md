# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T08:34:45Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `c4a60647e4d31c49baf0e5f473c47f89864a33f5` (`chore(kilo): durable handoff for next agentic work session (2026-11-10T08:30:29Z)`, 2026-11-10 08:33:59 +0000) — in sync with `origin/main` (identical SHA)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: **source clean** (`## main...origin/main`, no staged/unstaged tracked changes). Only untracked/modified item: `src/__pycache__/cache_keys.cpython-312.pyc` (tracked bytecode, pre-existing modification — **do not stage/commit** per guardrail).
- `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/`: **empty** (the `.pyc` diff is outside the substantive tree; it is bytecode, not a research artifact).
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Research phase complete (**E001–E043**). Authoritative history/dispositions: `ledger/RESEARCH_LEDGER.md`.
- Baseline guards pass: `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH**; `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS PRESENT, TRACKED AND UNCHANGED**.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1e-05, 1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Known data note: `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be missing from a fresh working tree (gitignored); a driver needing it may re-download. `QUANT_RESEARCH_OFFLINE=1` is enforced during verification, so a missing cache entry fails hard instead of silently downloading.
- Ledger tail: last substantive entry **E131** (2026-11-10T08:30Z, HEAD `4f07f4e5`). Delta since E131: 1 checkpoint commit (`c4a60647`, `chore(kilo): durable handoff for next agentic work session (2026-11-10T08:30:29Z)`) touching only the handoff symlink tree; no research artifacts, baselines, source, tests, scripts, or ledger substance changed. This handoff supersedes `handoff_2026-11-10T08-30-29Z_INITIAL_TASK.md` operationally (retained as history).

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
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never introduce logging of secrets.
- Do not stage/commit bytecode (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T08-34-45Z_INITIAL_TASK.md` (mode 0600, SHA-256 to be computed after mirroring).
- **Supersedes (operationally):** `handoff_2026-11-10T08-30-29Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).

(End of file - total 60 lines)