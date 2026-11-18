# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T06:43:34Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- `HEAD`: `384450e176a20c347467398a18b4fe9f95812470` (`main`, `origin/main`)
- Ahead/behind: 0 / 0
- Working tree: 12 tracked `__pycache__/*.pyc` files modified (unstaged); no `.verify_snapshot/` or `.verify_reports/` present. Do **not** commit `__pycache__` changes.

## Project status (authoritative)
- Research phase **complete (E001–E043)**; surviving validated strategies and dispositions are documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical golden artifacts. `ledger/golden_baseline.json` is the pinned SHA-256 baseline; replacing an artifact requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`) — **never** re-pin as a side effect of running verification.
- `data/` inputs are pinned per `ledger/data_baseline.json` and `data/vintages.json`; cache coverage is enforced (`scripts/check_data_coverage.py`). Verification re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`.
- Known open technical note (see ledger E049): E041/E042 grid artifacts exhibit 1-ulp QP sensitivity (133/29 numeric diffs in extended runs) and still exceed the 1e-4 structural-match tolerance in `--extended`; **do not re-pin them to silence this**. E029/E030 are offline-reproducible after their respective pinning fixes.

## Baseline/integrity checks performed in this session
- `git diff --name-only HEAD -- experiments/` → empty (no golden drift vs HEAD).
- No active `.verify_snapshot/ACTIVE.json`.
- Existing handoff symlinks pointed to `handoff_2026-11-18T06-00-43Z_INITIAL_TASK.md` (E485); this session creates and repoints to a fresh timestamped handoff.

## Environment / prerequisites (verify before running gates)
- Always run with `SEED=42`.
- Core deps expected: `numpy`, `pandas`, `scipy`, `pyarrow`, `statsmodels`, `yfinance` (`pip install -r requirements.txt`). If a runner reports `ModuleNotFoundError`, install deps before running `scripts/check.sh` or the verification suite.
- Verification must never be left half-finished. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifact per AGENTS.md if HEAD already captured a run).

## Recommended starting checklist for the next session
1. **Orient:** read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md` (tail/recent entries), and this handoff; confirm `git status --short`, `git rev-parse HEAD`, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Fast integrity gate (offline, ~seconds):** `SEED=42 bash scripts/check.sh` (or `make check`). Resolve any golden/baseline/coverage issues **before** committing anything.
3. **If deeper verification is needed:** `SEED=42 python3 run_all_verification.py` (quick) / `--extended` / `--full` as appropriate; ensure artifacts are restored/clean after completion and do not commit verification output.
4. **Only proceed with new work if explicitly requested and pre-registered.** The repo is in a closed, reproducibility-focused state — do not invent tasks, move goalposts, or re-pin baselines/goldens opportunistically.

## Constraints to honor
- No golden/data baseline re-pinning without explicit justification and diff-visible update.
- No committing verification output or interrupted-run state; keep `experiments/` matching pinned baselines.
- No new research/driver changes unless requested and aligned with pre-registration/multiple-testing discipline in `AGENTS.md` and the ledger.
- Do not commit `__pycache__` churn or unrelated files.

## Handoff deliverable
- This file is the durable, timestamped initial task message for the next agentic work session. It should be mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and made the target of all canonical `*handoff*/*next*/*latest*` pointers via `python3 scripts/repoint_handoff.py handoff_2026-11-18T06-43-34Z_INITIAL_TASK.md`.
