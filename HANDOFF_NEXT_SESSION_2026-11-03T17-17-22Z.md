# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-03T17-17-22Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** $(git log -1 --format='%h %s')
**State:** Research phase complete (E001–E043, plus E044–E050 closed items). Working tree as-is. No live verification snapshot assumed. Follow current repo state.

## Initial task message for the next agentic work session

> **START HERE:** This repository has completed its research phase (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
>
> **No queued tasks.** Wait for explicit user instructions before taking any action. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items. If the user provides a new task, read `AGENTS.md` and the relevant ledger entries first to understand constraints and historical context.

## Standing constraints (must follow)

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- Golden files (`experiments/*.json`) are canonical. Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and updating `ledger/golden_baseline.json` via `scripts/check_golden_baseline.py --update`.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`). Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions in AGENTS.md (SEED=42, close-to-close primary convention, offline verification).
- Do not create/modify GitHub workflows (`.github/workflows/` is controller-managed; template at `.github/workflow-templates/verification-gate.yml`).
- Pre-registration, multiple-testing discipline, and falsification expectations remain in force if new experiments are requested.

## Current state (at handoff time)

- `git status --short`: $(git status --short | wc -l) lines
- `git log -1`: $(git log -1 --oneline)
- `.verify_snapshot/`: check for ACTIVE marker — no live verification run assumed
- Key docs: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `ledger/PRIORITIZATION.md`
- Known closed items (do not re-open): E029/E030 offline-reproducible via pinned caches; E041/E042 ill-conditioned QP drift (1e-5 scale) documented (E049/E050); optimizer validation rules pinned.

## Quick Start for next session

1. Confirm state: `git log -1 --oneline && git status --short`
2. Read `AGENTS.md` (baseline integrity, verification rules, constraints)
3. Read `ledger/RESEARCH_LEDGER.md` for full context if starting new work
4. **Do not run verification** unless explicitly requested by the user
5. Wait for explicit user task/instructions

## Verification commands (if requested)

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py` or `make verify`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes

- Never modify `experiments/*.json` as a side effect of verification without following the re-pinning process.
- Follow all verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Do not create unprompted handoffs or re-open closed items.

**Handoff created:** 2026-11-03T17-17-22Z (UTC)
