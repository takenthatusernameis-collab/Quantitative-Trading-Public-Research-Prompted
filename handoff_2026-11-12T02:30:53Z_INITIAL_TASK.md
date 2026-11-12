# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T02:30:53Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `58c6b30b1889f45af2845871d2a6d7b75f5903cb` (`chore(kilo): checkpoint agent session`, 2026-11-12 02:30:07 +0000) — tracking `origin/main`, in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (observed at handoff)

- `git status --short --branch`: `## main...origin/main`; tracked worktree otherwise clean except 12 pre-existing unstaged `__pycache__/*.pyc` modifications under `scripts/`, `src/`, `tests/` (build artifacts, timestamp drift; **do not stage or commit**).
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- No source, experiment, ledger, script, or test changes were made in this session beyond this handoff artifact and canonical-pointer repointing.
- **Research phase complete (E001–E043).** Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md` (last research entry E051; E052–E165 are durable-handoff refreshes only).
- Canonical baselines are authoritative: `experiments/*.json` (tracked artifacts, 138 entries = 107 pinned goldens + 31 drivers), `ledger/golden_baseline.json`, `ledger/data_baseline.json` (35 pinned data inputs). **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Baseline guards verified at last refresh: `check_golden_baseline.py` → all 107 pinned goldens match; `check_data_coverage.py` → all 35 pinned data inputs present, tracked, unchanged.
- This supersedes `handoff_2026-11-12T02:29:19Z_INITIAL_TASK.md` operationally; earlier timestamped handoffs are retained as history.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean source state and `HEAD`/remote alignment.
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
- Do not commit pre-existing tracked `__pycache__/*.pyc` working-tree modifications unless explicitly instructed.