# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T08:25:03Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `2d89917553203c317873ddbdcee1a8cf53d64c31` (`chore(kilo): checkpoint agent session`, 2026-11-10 08:23:10 +0000) — in sync with `origin/main` (identical SHA)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: **source clean** (`## main...origin/main`, no staged/unstaged tracked changes).
- `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/`: **empty**.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Research phase complete (**E001–E043**). Authoritative history/dispositions: `ledger/RESEARCH_LEDGER.md`.
- Baseline guards pass: `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH**; `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS PRESENT, TRACKED AND UNCHANGED**.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1e-05, 1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Known data note: `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be missing from a fresh working tree (gitignored); a driver needing it may re-download. `QUANT_RESEARCH_OFFLINE=1` is enforced during verification, so a missing cache entry fails hard instead of silently downloading.
- Ledger tail: last substantive entry **E129** (2026-11-10T05:19Z, HEAD `19c18381`). Delta since E129: 30+ checkpoint commits touching only the handoff symlink tree + one ledger append (E129 entry); no research artifacts, baselines, source, tests, scripts, or ledger substance changed.
- Handoff hygiene: canonical pointers at repo root all resolve OK (`next_session`, `next_session.md`, `next_handoff`, `next_handoff.md`, `handoff_latest`, `handoff_latest.md`, `handoff_next`, `handoff_next.md`, `initial_task`, `initial_task.md` → `handoff_2026-11-10T08:22:20Z_INITIAL_TASK.md`). Repo-wide 2144 symlinks / 464 broken — all pre-existing historical pointers left untouched to preserve history; none introduced by this refresh.

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

- **Durable artifact (this session):** `handoff_2026-11-10T08-25-03Z_INITIAL_TASK.md` (SHA-256 computed after mirroring).
- **Supersedes (operationally):** `handoff_2026-11-10T08:22:20Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).

(End of file - total 65 lines)