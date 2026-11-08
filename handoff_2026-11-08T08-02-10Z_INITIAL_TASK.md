# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T08:02:10Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `5b5ede32` (`chore(kilo): checkpoint agent session`, 2026-11-08 08:02:10 +0000)
**Remote:** `origin/main` == local `HEAD` — in sync at handoff creation.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state:** clean working tree at handoff creation. `.verify_snapshot/` absent. This session adds only this timestamped durable handoff and canonical pointer updates.

---

## Current State (verified at handoff)

- No technical research work was performed this session — only this durable handoff was written per explicit request. No verification run, no experiment, no code change, no baseline/golden/ledger modification.
- Canonical baselines remain authoritative: tracked `experiments/*.json` goldens (138 artifacts, all match HEAD), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E110** recorded; see `ledger/RESEARCH_LEDGER.md`). Last ledger entry: **E110** (Durable Handoff Refresh). No open research items. No OPEN/PENDING/BLOCKED/TODO markers anywhere in the ledger.
- **Correction vs prior handoffs:** earlier durable handoffs incorrectly stated "E001–E043". The research phase actually runs **E001–E110**. Carry forward E110's closure state.
- **Closed/resolved — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)
**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands; **never commit verification output**. Restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
```

## Guardrails
- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use template/manual maintainer path per repo docs).
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and a ledger update.

## Handoff Provenance
- **Supersedes (operationally):** `handoff_2026-11-08T08-00-13Z_INITIAL_TASK.md` and earlier handoffs; retained as history.
- **This durable artifact:** `handoff_2026-11-08T08-02-10Z_INITIAL_TASK.md`
