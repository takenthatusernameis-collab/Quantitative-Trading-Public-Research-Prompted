# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T09:27:40Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- `HEAD`: `a98fa03a` (`main`, working tree clean)
- Working tree: clean except this handoff artifact. No `.verify_snapshot/ACTIVE.json` and no `.verify_reports/` present.
- `git diff --name-only HEAD -- experiments/` → empty at session start.

## Project status (authoritative)
- Research phase **complete (E001–E051)**; dispositions documented in `ledger/RESEARCH_LEDGER.md`. Repository is in a **closed, reproducibility-focused** state.
- `experiments/*.json` are canonical golden artifacts; `ledger/golden_baseline.json` pins SHA-256 fingerprints. Replacing an artifact requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`) with the change visible in the diff — never re-pin as a side effect of verification.
- `data/` inputs pinned per `ledger/data_baseline.json` and `data/vintages.json`; coverage enforced by `scripts/check_data_coverage.py`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Known open note (ledger E049): E041/E042 grid artifacts show 1-ulp QP sensitivity; **do not re-pin them to silence this.**

## Environment / prerequisites
- Core deps import OK (pandas, numpy, scipy, pyarrow, statsmodels, yfinance). If `ModuleNotFoundError`, run `python3 -m pip install -r requirements.txt`.
- Always run with `SEED=42`. Never leave verification half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Recommended starting checklist for the next session
1. **Orient:** read `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md`, and this handoff; confirm `git status --short`, `git rev-parse HEAD`, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Fast integrity gate (offline):** `SEED=42 bash scripts/check.sh` (or `make check`). Resolve any golden/baseline/coverage issue before committing anything.
3. **Deeper verification:** `SEED=42 python3 run_all_verification.py` (quick / `--extended` / `--full`) as needed; restore artifacts afterward and **do not commit verification output**.
4. **Only proceed with new work if explicitly requested and pre-registered.** Do not invent tasks or move goalposts.

## Constraints to honor
- No golden/data baseline re-pinning without explicit justification and a diff-visible update.
- No committing verification output or interrupted-run state; keep `experiments/` matching pinned baselines and HEAD.
- No new research/driver changes unless requested and aligned with pre-registration / multiple-testing discipline.

## Handoff deliverable
- This file is the durable, timestamped initial task message for the next agentic work session.
