# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T22:23:31Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `9488a3d4 chore(kilo): checkpoint agent session` (`== origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status --short --branch`: **clean** (`## main...origin/main`).
- `HEAD == origin/main` (`9488a3d4`). No divergence observed.
- `.verify_snapshot/`: **absent** — no interrupted/pending verification restore marker detected.
- Canonical baselines are authoritative and **must not be modified or re-pinned** as a side effect of routine verification: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- Research phase is complete (**E001–E043**; dispositions in `ledger/RESEARCH_LEDGER.md`). Repository is in a closed/research-complete state unless explicit, pre-registered new work is requested.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification (only when explicitly requested):**
```bash
SEED=42 bash scripts/check.sh                        # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 committed drivers
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```
- **Never commit verification output** over canonical goldens (`experiments/*.json`).
- Restore goldens after any interrupted run. If `scripts/check.sh` reports a golden/baseline mismatch, fix/restore **before** committing.

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use template/manual maintainer path per repo docs).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-07T22:22:03Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **Durable artifact:** this file, mirrored to `handoff/` and `.kilo/handoff/`; common `LATEST`/next-session pointers updated to reference this handoff.

(End of handoff)
