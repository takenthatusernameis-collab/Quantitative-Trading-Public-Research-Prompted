# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T12-27-31Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- Branch: `main` (tracking `origin/main`, 0 ahead / 0 behind)
- `HEAD`: `77ff3690` (full `77ff3690...`)
- Working tree at handoff creation: clean (`git status --short` empty)
- No `.verify_snapshot/ACTIVE.json` and no `.verify_reports/` present
- `git diff --name-only HEAD -- experiments/` → empty (goldens match HEAD)

## Project status (authoritative)
- Research phase **complete (E001–E051)**; dispositions (REJECTED / PARTIAL / ACCEPTED) are documented in `ledger/RESEARCH_LEDGER.md`. Repository is in a **closed, reproducibility-focused** state. The ledger tail confirms durable-handoff refreshes through E492; this refresh is E493.
- `experiments/*.json` are canonical golden artifacts; `ledger/golden_baseline.json` pins SHA-256 fingerprints. Replacing an artifact requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`) with the change visible in the diff — **never** re-pin as a side effect of verification.
- Data inputs are pinned per `ledger/data_baseline.json` and `data/vintages.json`; cache coverage is enforced by `scripts/check_data_coverage.py`. Verification re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`.
- Known open technical note (ledger E049): E041/E042 grid artifacts exhibit 1-ulp QP sensitivity and can exceed the 1e-4 structural-match tolerance in `--extended`; **do not re-pin them to silence this.**

## Delta vs prior durable handoff
- Prior: `handoff_2026-11-18T12-26-45Z_INITIAL_TASK.md` (HEAD `875e08a9`) — superseded by this file.
- This session changed **no** research content: no changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`. Only this timestamped handoff artifact, its subdir mirrors, generic pointer symlinks, and a new ledger entry are added.

## Environment note (this runner)
- Bare system interpreter `/usr/bin/python3` (Python 3.12.3); core deps NOT importable here (`import pandas` → `ModuleNotFoundError`; numpy/scipy/pyarrow/statsmodels/yfinance absent). Fix if a future run needs them: `python3 -m pip install -r requirements.txt`. This is an environment caveat, not a code defect.

## Initial task for the next agentic work session
1. **Orient (read-only):** read `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md`, and this handoff. Confirm `git status --short`, `git rev-parse --short HEAD`, branch/sync state, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Fast integrity gate (offline, ~seconds):** run `SEED=42 bash scripts/check.sh` (or `make check`). If it reports golden/baseline/coverage issues, resolve them **before** any commit; do not commit interrupted verification state.
3. **If deeper verification is explicitly needed:** run `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full` as appropriate. Always finish or recover with `SEED=42 python3 run_all_verification.py --restore-only`; **do not commit verification output**. If `HEAD` already contains a captured run, restore pinned artifacts per `AGENTS.md` rather than relying on `git checkout -- experiments/`.
4. **Do not start new research or code changes unless explicitly requested and pre-registered.** Preserve multiple-testing discipline, negative-result recording, and baseline integrity. Avoid opportunistic re-pinning, dependency changes, or committing `__pycache__`/unrelated files.

## Handoff provenance
- **Durable artifact (this file):** `handoff_2026-11-18T12-27-31Z_INITIAL_TASK.md` (repo root), mirrored byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Canonical pointers:** repointed with `python3 scripts/repoint_handoff.py handoff_2026-11-18T12-27-31Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-18T12-26-45Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained for history).

_End of durable handoff. No new research is requested; awaiting explicit user instructions._