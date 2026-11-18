# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T09-33-34Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- `HEAD`: `6abf3eb116c9f68ec039f4b31aa800386a2fe0f1` (`6abf3eb1`, `main` == `origin/main`, 0 ahead / 0 behind).
- Working tree at session start: clean (`git status --short` empty).
- No `.verify_snapshot/ACTIVE.json` and no `.verify_reports/` present (clean state).
- `git diff --name-only HEAD -- experiments/` → empty (golden artifacts match HEAD).

## Project status (authoritative)
- Research phase **complete (E001–E051)**; dispositions (REJECTED / PARTIAL / ACCEPTED) and every surviving validated strategy are documented in `ledger/RESEARCH_LEDGER.md` (through E489; this refresh is logged as E490). Repository is in a **closed, reproducibility-focused** state.
- `experiments/*.json` are the canonical golden artifacts. `ledger/golden_baseline.json` pins their SHA-256 fingerprints. Replacing an artifact requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`) with the change visible in the diff — **never** re-pin as a side effect of running verification.
- `data/` inputs are pinned per `ledger/data_baseline.json` and `data/vintages.json`; cache coverage is enforced by `scripts/check_data_coverage.py`. The verification suite re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`, so an unpinned input fails hard instead of silently downloading.
- Known open technical note (ledger E049): E041/E042 grid artifacts exhibit 1-ulp QP sensitivity and can exceed the 1e-4 structural-match tolerance in `--extended`; **do not re-pin them to silence this.** E029/E030 are offline-reproducible after their pinning fixes (E048).

## Environment / prerequisites (observed on this runner)
- Bare system interpreter is `/usr/bin/python3` (Python 3.12.3). **Core deps are NOT importable here**: `import pandas` → `ModuleNotFoundError` (numpy/scipy/pyarrow/statsmodels/yfinance likewise absent). If a future runner hits this, install dependencies first: `python3 -m pip install -r requirements.txt`.
- Always run with `SEED=42`.
- Never leave verification half-finished. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifact per `AGENTS.md` if HEAD already captured a run).

## Recommended starting checklist for the next session
1. **Orient:** read `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md` (through E490), and this handoff; confirm `git status --short`, `git rev-parse HEAD`, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Provision deps if needed:** `python3 -m pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; `cvxpy`/`cvxopt` optional).
3. **Fast integrity gate (offline, ~seconds):** `SEED=42 bash scripts/check.sh` (or `make check`). Resolve any golden/baseline/coverage issue **before** committing anything. If a golden mismatch appears, fix it before committing — never checkpoint a captured verification run.
4. **If deeper verification is needed:** `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full` as appropriate; ensure artifacts are restored/clean afterward and **do not commit verification output**.
5. **Only proceed with new work if explicitly requested and pre-registered.** Do not invent tasks, move goalposts, or re-pin baselines/goldens opportunistically.

## Constraints to honor
- No golden/data baseline re-pinning without explicit justification and a diff-visible update.
- No committing verification output or interrupted-run state; keep `experiments/` matching the pinned baselines and HEAD.
- No new research/driver changes unless requested and aligned with the pre-registration / multiple-testing discipline in `AGENTS.md` and the ledger.
- Do not commit `__pycache__` churn or unrelated files.

## Handoff deliverable
- This file is the durable, timestamped initial task message for the next agentic work session. It is mirrored byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and is the target of all generic `*handoff*/*next*/*latest*/*current*/*initial_task*` pointers, repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-18T09-33-34Z_INITIAL_TASK.md`.