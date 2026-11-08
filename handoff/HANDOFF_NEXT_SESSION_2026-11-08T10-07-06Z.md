# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-08T10:07:06Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `c33696f5` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (at handoff creation)

- `git status`: **clean** (no modified tracked files observed at handoff time).
- `.verify_snapshot/`: **not present** (no interrupted verification recovery pending).
- Canonical baselines remain authoritative and must not be overwritten by routine runs: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- Research phase complete (**E001–E043**). Dispositions: `ledger/RESEARCH_LEDGER.md`.
- Closed/resolved — **do not reopen**: E049/E050 optimizer/status issues; E041/E042 residual ill-conditioned QP numeric drift — **do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.**
Do **not** invent new experiments, run verification unprompted, change promotion gates/outcomes, modify golden/baseline artifacts, or commit verification output without explicit direction.

### If the user requests work, verify state first
1. `git status --short --branch` — confirm branch/HEAD and that the tree is clean (watch for `__pycache__`, `experiments/`, `data/`, `ledger/` diffs).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. If any tracked files under `experiments/`, `data/`, or `ledger/` differ unexpectedly, **stop and restore** pinned state before proceeding (see `AGENTS.md` baseline integrity).
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

- **Never commit** driver verification output over canonical goldens.
- **Never re-pin** `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction (and keep the re-pin in the diff).
- **Do not reopen** closed E049/E050 or E041/E042 drift items.
- **Do not create** `.github/workflows/` CI gates as an automated agent (maintainer/UI path; see `VERIFICATION_GATE_TEMPLATE.md`).
- **Do not commit** `__pycache__`/bytecode artifacts.
- Pre-registered gates, sensitivity grids, and outcomes must not change without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff/HANDOFF_NEXT_SESSION_2026-11-08T08-58-12Z.md` and earlier handoffs (retained as history).
- **This durable artifact:** `handoff/HANDOFF_NEXT_SESSION_2026-11-08T10-07-06Z.md`
