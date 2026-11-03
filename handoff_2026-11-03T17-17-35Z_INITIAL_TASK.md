# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-03T17-17-35Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** `b1c0cc1b52b20355c94613c4a0a004b8db392895` (2026-11-03 17:17:17 +0000) "chore(kilo): checkpoint agent session"
**State:** Research phase complete (E001–E070). Working tree clean. No live verification snapshot. No open task in queue.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the repository is closed. There is currently **no open task in the queue**.
>
> **Wait for explicit user instructions before taking any action.** Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items.
>
> If the user provides explicit instructions, read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first, follow all standing constraints, and proceed only within the scope of those instructions.

## Standing constraints (must follow)

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- Golden files (`experiments/*.json`) are canonical. Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and updating `ledger/golden_baseline.json` via `scripts/check_golden_baseline.py --update`.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`). Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions in AGENTS.md (SEED=42, close-to-close primary convention, offline verification).
- Do not create/modify GitHub workflows (`.github/workflows/` is controller-managed; template at `.github/workflow-templates/verification-gate.yml`).

## Current state (verified at handoff time)

- `git log -1 --format="%H %ci %s"` → `b1c0cc1b52b20355c94613c4a0a004b8db392895` (2026-11-03 17:17:17 +0000) "chore(kilo): checkpoint agent session".
- `git status --short` → empty; tracked tree clean.
- `git diff --stat HEAD -- experiments/` → empty; goldens match HEAD.
- `.verify_snapshot/` absent, no ACTIVE marker — no live verification run, nothing to recover.
- Ledger: `ledger/RESEARCH_LEDGER.md` (E001–E070 complete). `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `ledger/PRIORITIZATION.md` present.
- Known closed items (do not re-open): E049/E050 optimizer determinism (exact KKT enumeration), E041/E042 ill-conditioned QP drift (1e-5 scale), E029/E030 offline-reproducible via pinned caches, E048 data-coverage invariant (`scripts/check_data_coverage.py`, 35 pinned inputs).
- Dependencies: not necessarily installed in the active environment; run `pip install -r requirements.txt` before verification if needed.

## Quick Start for next session

1. Confirm state: `git log -1 --oneline` and `git status --short`
2. Read `AGENTS.md` (baseline integrity, verification rules, constraints)
3. Read `ledger/RESEARCH_LEDGER.md` for context if needed
4. **Do not run verification** unless explicitly requested by the user
5. Wait for explicit user task/instructions

## Quick verification commands (reference only)

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py` or `make verify`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

**Handoff created:** 2026-11-03T17-17-35Z (UTC)
