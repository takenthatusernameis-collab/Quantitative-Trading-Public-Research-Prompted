# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-03T12:08:22Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** 0c462a8 chore(kilo): checkpoint agent session
**State:** Research phase complete (E001–E043, plus E044–E050 closed items). Working tree clean. No live verification snapshot. No open task in queue.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the repository is closed. There is currently no open task in the queue. Wait for explicit user instructions before taking any action. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items. Follow all standing constraints in AGENTS.md.

## Standing constraints (must follow)

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- Golden files (`experiments/*.json`) are canonical. Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and updating `ledger/golden_baseline.json` via `scripts/check_golden_baseline.py --update`.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`). Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions in AGENTS.md (SEED=42, close-to-close primary convention, offline verification).
- Do not create/modify GitHub workflows (`.github/workflows/` is controller-managed; template at `.github/workflow-templates/verification-gate.yml`).

## Current state (verified at handoff time)

- `git status --short`: empty — working tree clean.
- `.verify_snapshot/`: absent, no ACTIVE marker — no live verification run.
- Ledger: `ledger/RESEARCH_LEDGER.md` (E001–E043 complete; surviving validated strategies documented). `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `ledger/PRIORITIZATION.md` present.
- Known closed items (do not re-open): E049/E050 optimizer determinism, E041/E042 ill-conditioned QP drift (1e-5 scale). E029/E030 offline-reproducible via pinned caches.
- Dependencies: not necessarily installed in the active environment; run `pip install -r requirements.txt` before verification.

## Quick Start for next session

1. Confirm state: `git log -1 --oneline` and `git status --short`
2. Read AGENTS.md (baseline integrity, verification rules, constraints)
3. Read `ledger/RESEARCH_LEDGER.md` for context if needed
4. **Do not run verification** unless explicitly requested by the user
5. Wait for explicit user task/instructions

## Quick Start / Verify commands

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py` or `make verify`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes & Guardrails

- Never modify `experiments/*.json` as a side effect of verification without following the re-pinning process; the committed golden is authoritative.
- Follow all verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Do not create unprompted handoffs or re-open closed items.
- Pre-registration, multiple-testing discipline, and falsification expectations remain in force if new experiments are ever requested.

**Handoff created:** 2026-11-03T12:08:22Z (UTC)
