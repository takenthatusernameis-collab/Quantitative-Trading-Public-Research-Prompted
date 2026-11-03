# Initial Task Message for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-03T09-14-12Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** 16693d70 (2026-11-03 09:12:45 +0000) "chore(kilo): checkpoint agent session"
**Git status:** clean (no tracked changes; no `.verify_snapshot/` -> no interrupted verification run)

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the repository is closed (research phase E001–E043 complete; all ledger items CLOSED). There is currently **no open task in the queue**. Wait for explicit user instructions before taking any action. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items. Follow all standing constraints in AGENTS.md.

## Context

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification suite and baseline-integrity guards are in place (golden baseline pinning, data cache coverage enforcement, optimizer-determinism rule pinned by `tests/test_portfolio_opt.py`).
- Repository is CLOSED: no OPEN/PENDING/BLOCKED/TODO markers exist in the ledger (last entry E069, Durable Handoff Refresh, 2026-11-02T23:26:16Z).
- Confirmed at handoff time: `git status` clean; `git diff --stat HEAD -- experiments/` empty; HEAD a620065; no `.verify_snapshot/`.

## Standing constraints (must follow)

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- Golden files (`experiments/*.json`) are canonical. Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and updating `ledger/golden_baseline.json` via `scripts/check_golden_baseline.py --update`.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`). Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions in AGENTS.md (SEED=42, close-to-close primary convention, offline verification).
- Do not create/modify GitHub workflows (`.github/workflows/` is controller-managed; template at `.github/workflow-templates/verification-gate.yml`).

## Quick Start / Verify commands

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py` or `make verify`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Working Tree

Clean working tree. `experiments/` matches `ledger/golden_baseline.json` pins.

**Handoff created:** 2026-11-03T09-14-12Z (UTC)