# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T14:29:57Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `30d3cf5b2537ad13dd76b971e422d7cb6380b781` (`origin/main` in sync at handoff creation)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified)

- `git status --short experiments/ data/`: **clean** (no canonical artifact modifications).
- `.verify_snapshot/`: **absent** (no interrupted/pending verification restore).
- Research phase is complete (**E001–E043**). Dispositions and open/closed items live in `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 and E041/E042 residual ill-conditioned QP drift items. **Do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and `HEAD == origin/main` (or explain divergence).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and any explicitly open items.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands; **never commit verification output**. The suite backs up/restores `experiments/*.json`; if interrupted, restore before committing (`--restore-only` / `git checkout -- experiments/` per `AGENTS.md`).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
```

## Guardrails

- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction following repo process.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use template/manual maintainer path per repo docs).
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and a ledger update.
- Always use `SEED=42`; close-to-close is the v1.2.3 primary convention.

## Handoff Provenance

- **Supersedes (latest prior pattern):** recent `handoff/*INITIAL_TASK*` entries including `handoff_2026-11-07T13-32-11Z_INITIAL_TASK.md` and the prior `handoff/HANDOFF_20261104T134939Z.md`-style handoffs.
- **Durable copies written:** `handoff/handoff_2026-11-07T14-29-57Z_INITIAL_TASK.md`, root `handoff_2026-11-07T14-29-57Z_INITIAL_TASK.md`, `.kilo/handoff/handoff_2026-11-07T14-29-57Z_INITIAL_TASK.md`.

(End of file)
