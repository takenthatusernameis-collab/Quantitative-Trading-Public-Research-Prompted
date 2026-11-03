# Initial Task Message for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-03T11-16-40Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** cecd473
**Git status:** clean (no tracked changes; no `.verify_snapshot/` -> no interrupted verification run)

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the repository is closed (research phase E001–E043 complete; all ledger items CLOSED). There is currently **no open task in the queue**. Wait for explicit user instructions before taking any action. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items. Follow all standing constraints in AGENTS.md.

## Context

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification suite and baseline-integrity guards are in place.
- Repository is CLOSED: no OPEN/PENDING/BLOCKED/TODO markers exist in the ledger.
- Confirmed at handoff time: `git status` clean; HEAD cecd473; no `.verify_snapshot/`.

## Standing constraints (must follow)

- Never commit verification output. Restore goldens first if interrupted.
- Golden files (`experiments/*.json`) are canonical. Never re-pin artifacts to silence numeric drift.
- Honor pinned cache vintages. Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Follow repo conventions in AGENTS.md (SEED=42, close-to-close primary convention, offline verification).
- Do not create/modify GitHub workflows.

## Quick Start / Verify commands

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
