# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-09T15:10:03Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `0fa2b69b` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (at handoff creation)

- `.verify_snapshot/`: **absent** (no interrupted verification recovery pending).
- `git status` shows **tracked `__pycache__/*.pyc` modifications** in `scripts/`, `src/`, `tests/`, and `__pycache__/run_all_verification.cpython-312.pyc` present in the worktree. **Do not stage or commit bytecode artifacts.** Treat them as local noise; restore/discard only if explicitly instructed and safe.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not overwrite** with routine/verification output.
- Research phase complete (**E001–E043**). Dispositions: `ledger/RESEARCH_LEDGER.md`.
- Closed/resolved — **do not reopen**: E049/E050 optimizer/status issues; E041/E042 residual ill-conditioned QP numeric drift — **do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.**
Do **not** invent new experiments, run verification unprompted, change promotion gates/outcomes, modify golden/baseline artifacts, or commit verification output/bytecode without explicit direction.

### If the user requests work, verify state first
1. `git status --short --branch` — confirm branch/HEAD; note any `__pycache__`/bytecode noise and any unexpected diffs under `experiments/`, `data/`, `ledger/`, `src/`, `scripts/`, `tests/`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. If tracked files under `experiments/`, `data/`, or `ledger/` differ unexpectedly, **stop and restore** pinned state before proceeding (see `AGENTS.md` baseline integrity).
4. Before committing any substantive change: `SEED=42 bash scripts/check.sh` (or `make check`).

### If asked to run verification (only when explicitly requested)
```bash
SEED=42 bash scripts/check.sh                        # fast guards
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
```
**Never commit verification output** over canonical goldens (`experiments/*.json`). If a run is interrupted, restore goldens before committing.

## Guardrails

- **Never commit** driver verification output over canonical goldens, and **never commit** `__pycache__`/bytecode artifacts.
- **Never re-pin** `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction (keep the re-pin in the diff).
- **Do not reopen** closed E049/E050 or E041/E042 drift items.
- **Do not create** `.github/workflows/` CI gates as an automated agent (maintainer/UI path; see `VERIFICATION_GATE_TEMPLATE.md`).
- Pre-registered gates, sensitivity grids, and outcomes must not change without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff/HANDOFF_NEXT_SESSION_2026-11-08T10-07-06Z.md` and earlier handoffs (retained as history).
- **This durable artifact:** `handoff/HANDOFF_NEXT_SESSION_2026-11-09T15-10-03Z.md`
