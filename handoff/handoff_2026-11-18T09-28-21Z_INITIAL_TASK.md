# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T09:28:21Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- `HEAD`: `1766a9a33e545fe2ea0ec43fe62729b58bb718bc` (`1766a9a3`, `main` == `origin/main`, 0 ahead / 0 behind)
- Working tree at session start: clean (no `.verify_snapshot/ACTIVE.json`, no `.verify_reports/`)
- `git diff --name-only HEAD -- experiments/` → empty (107 golden artifacts match HEAD)

## Project status (authoritative)
- Research phase **complete (E001–E051)**; dispositions (REJECTED / PARTIAL / ACCEPTED) documented in `ledger/RESEARCH_LEDGER.md` (through E488). Repository is in a **closed, reproducibility-focused** state.
- `experiments/*.json` are canonical golden artifacts; `ledger/golden_baseline.json` pins SHA-256 fingerprints. Replacing an artifact requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`) with the change visible in the diff — **never** re-pin as a side effect of verification.
- `data/` inputs pinned per `ledger/data_baseline.json` and `data/vintages.json`; cache coverage enforced by `scripts/check_data_coverage.py`. Verification re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`.
- Known open technical note (ledger E049): E041/E042 grid artifacts exhibit 1-ulp QP sensitivity and can exceed the 1e-4 structural-match tolerance in `--extended`; **do not re-pin them to silence this.**

## Environment / prerequisites (observed)
- Core deps import OK on this runner: pandas 3.0.6, numpy 2.5.4, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0. If a future runner reports `ModuleNotFoundError`, run `python3 -m pip install -r requirements.txt`.
- Always run with `SEED=42`.
- Never leave verification half-finished. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifact per `AGENTS.md` if HEAD already captured a run).

## Recommended starting checklist for the next session
1. **Orient:** read `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md`, and this handoff; confirm `git status --short`, `git rev-parse HEAD`, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Fast integrity gate (offline, ~seconds):** `SEED=42 bash scripts/check.sh` (or `make check`). Resolve any golden/baseline/coverage issue **before** committing anything.
3. **If deeper verification is needed:** `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full` as appropriate; ensure artifacts are restored/clean afterward and **do not commit verification output**.
4. **Only proceed with new work if explicitly requested and pre-registered.** Do not invent tasks, move goalposts, or re-pin baselines/goldens opportunistically.

## Constraints to honor
- No golden/data baseline re-pinning without explicit justification and a diff-visible update.
- No committing verification output or interrupted-run state; keep `experiments/` matching pinned baselines and HEAD.
- No new research/driver changes unless requested and aligned with pre-registration / multiple-testing discipline.
- Do not commit `__pycache__` churn or unrelated files.

## Handoff deliverable
- This file is the durable, timestamped initial task message for the next agentic work session. Mirror byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and repoint generic `*handoff*/*next*/*latest*/*current*/*initial_task*` pointers via `python3 scripts/repoint_handoff.py handoff_2026-11-18T09-28-21Z_INITIAL_TASK.md`.
