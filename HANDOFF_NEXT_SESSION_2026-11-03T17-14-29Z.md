# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-03T17:14:29Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete (E001–E070). Working tree clean. No live verification snapshot. No open task in queue.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the repository is closed. There is currently no open task in the queue. Wait for explicit user instructions before taking any action. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items. Follow all standing constraints in AGENTS.md.

## Standing constraints (must follow)

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- Golden files (`experiments/*.json`) are canonical. Never re-pin artifacts to silence numeric drift from verification runs.
- Honor pinned cache vintages. Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions in AGENTS.md (SEED=42, close-to-close primary convention, offline verification).
- Do not create/modify GitHub workflows.

## Quick Start for next session

1. Confirm state: `git log -1 --oneline` and `git status --short`
2. Read AGENTS.md
3. Read `ledger/RESEARCH_LEDGER.md` for context if needed
4. **Do not run verification** unless explicitly requested
5. Wait for explicit user task/instructions

**Handoff created:** 2026-11-03T17:14:29Z (UTC)
