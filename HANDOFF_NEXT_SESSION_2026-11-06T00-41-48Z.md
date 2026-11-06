# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-06T00:41:48Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** fede534 chore(kilo): checkpoint agent session
**State:** Research phase complete (E001–E043, plus closed E044–E050 items). Working tree clean at handoff time. No `.verify_snapshot/` / `ACTIVE.json` marker. No open task in queue.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified/closed and this repository is in a handoff-ready state. **There is no open task in the queue.** Wait for explicit user instructions before taking any action.
> Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, modify `experiments/*.json` goldens, re-pin baselines, or re-open closed items (E049/E050 optimizer determinism notes, E041/E042 ill-conditioned QP drift). Follow all standing constraints in `AGENTS.md`.

## Standing constraints (must follow)

- Never commit verification output. If verification is interrupted, restore goldens first: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD is known-clean).
- Golden files (`experiments/*.json`) are canonical. Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and `python3 scripts/check_golden_baseline.py --update`.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`). Verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions: `SEED=42`, close-to-close primary convention, offline verification where applicable.
- Do not create/modify GitHub workflows (`.github/workflows/` is controller-managed; template at `.github/workflow-templates/verification-gate.yml`).

## Current state (verified at handoff time)

- `git status --short`: clean (no output).
- `.verify_snapshot/`: absent; no `ACTIVE.json` — no live verification run.
- Key references: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `ledger/PRIORITIZATION.md`.
- Known closed/non-actionable items (do not re-open): E049/E050 optimizer determinism; E041/E042 remaining ill-conditioned QP numeric drift (1-ulp sensitivity, ~1e-5 scale) — do **not** re-pin to silence.
- Dependencies may not be installed in the active environment; run `pip install -r requirements.txt` before any verification requested by the user.

## Quick Start for next session

1. `git log -1 --oneline` and `git status --short`
2. Read `AGENTS.md` (baseline integrity, verification rules, constraints)
3. Read `ledger/RESEARCH_LEDGER.md` if context is needed
4. **Do not run verification** unless explicitly requested by the user
5. Wait for explicit user task/instructions

## Verification commands (only when explicitly requested)

- Fast check: `SEED=42 bash scripts/check.sh` / `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` / `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` / `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` / `make verify-full`
- Convention robustness: `SEED=42 python3 verify_convention_robustness.py` / `make verify`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes & Guardrails

- Treat the committed golden as authoritative; verification output is transient and must not be committed.
- Follow verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Pre-registration, multiple-testing discipline, and falsification expectations remain in force if new experiments are ever requested.

**Handoff created:** 2026-11-06T00:41:48Z (UTC)
