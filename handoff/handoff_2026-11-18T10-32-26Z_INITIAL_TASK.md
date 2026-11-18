# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T10:32:26Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- `HEAD`: `6fdceb5d8e8e853b20b52ec4c3d251119f6f0326` (`6fdceb5d`, `main` == `origin/main`)
- Ahead/behind: 0 / 0
- Working tree: clean (`git status --short` empty). **Do not commit `__pycache__` changes if they appear.**
- No `.verify_snapshot/ACTIVE.json` and no `.verify_reports/` present (clean state).
- `git diff --name-only HEAD -- experiments/` → empty (goldens match HEAD).

## Project status (authoritative)
- Research phase **complete (E001–E051)**; surviving validated strategies and every disposition (REJECTED / PARTIAL / ACCEPTED) are documented in `ledger/RESEARCH_LEDGER.md` (handoff refreshes through E491). This repo is in a **closed, reproducibility-focused** state.
- `experiments/*.json` are the canonical golden artifacts. `ledger/golden_baseline.json` pins their SHA-256 fingerprints. Replacing an artifact requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`) with the change visible in the diff — **never** re-pin as a side effect of running verification.
- `data/` inputs are pinned per `ledger/data_baseline.json` and `data/vintages.json`; cache coverage is enforced (`scripts/check_data_coverage.py`). The verification suite re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`, so an unpinned input fails hard instead of silently downloading.
- Known open technical note (ledger E049): E041/E042 grid artifacts exhibit 1-ulp QP sensitivity (133/29 numeric diffs in `--extended` runs) and still exceed the 1e-4 structural-match tolerance in `--extended`; **do not re-pin them to silence this.** E029/E030 are offline-reproducible after their respective pinning fixes (E048).

## Environment / prerequisites (verified on this runner)
- This runner has a bare system interpreter: `/usr/bin/python3` (Python 3.12.3). Core deps are **not** importable here (`import pandas` → `ModuleNotFoundError`; numpy/scipy/pyarrow/statsmodels/yfinance absent). Fix with `python3 -m pip install -r requirements.txt` before running any driver or verification.
- Always run with `SEED=42`.
- Verification must never be left half-finished. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifact per `AGENTS.md` if HEAD already captured a run).

## Recommended starting checklist for the next session
1. **Orient:** read `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md` (through E491), and this handoff; confirm `git status --short`, `git rev-parse HEAD`, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Fast integrity gate (offline, ~seconds):** `SEED=42 bash scripts/check.sh` (or `make check`). Resolve any golden/baseline/coverage issue **before** committing anything. If a golden mismatch appears, fix it before committing — never checkpoint a captured verification run.
3. **If deeper verification is needed:** `SEED=42 python3 run_all_verification.py` (quick) / `--extended` / `--full` as appropriate; ensure artifacts are restored/clean afterward and **do not commit verification output**.
4. **Only proceed with new work if explicitly requested and pre-registered.** Do not invent tasks, move goalposts, or re-pin baselines/goldens opportunistically.

## Constraints to honor
- No golden/data baseline re-pinning without explicit justification and a diff-visible update.
- No committing verification output or interrupted-run state; keep `experiments/` matching the pinned baselines and HEAD.
- No new research/driver changes unless requested and aligned with the pre-registration / multiple-testing discipline in `AGENTS.md` and the ledger.
- Do not commit `__pycache__` churn or unrelated files.

## Handoff deliverable
- This file is the durable, timestamped initial task message for the next agentic work session. It is mirrored byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and is the target of all generic `*handoff*/*next*/*latest*/*current*/*initial_task*` pointers, repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-18T10-32-26Z_INITIAL_TASK.md`.