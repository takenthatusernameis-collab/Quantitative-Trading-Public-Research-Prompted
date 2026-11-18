# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T11:38:29Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- Branch: `main` (tracking `origin/main`)
- `HEAD`: `5e742e98` (`5e742e98`, "chore(kilo): checkpoint agent session")
- Working tree at handoff creation: clean (no modified/staged tracked changes observed)
- No `.verify_snapshot/` or `.verify_reports/` present

## Project status (authoritative)
- Research phase **complete (E001–E051)**; dispositions (REJECTED / PARTIAL / ACCEPTED) are documented in `ledger/RESEARCH_LEDGER.md`. Repository is in a **closed, reproducibility-focused** state.
- `experiments/*.json` are canonical golden artifacts; `ledger/golden_baseline.json` pins SHA-256 fingerprints. Replacing an artifact requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`) with the change visible in the diff — **never** re-pin as a side effect of verification.
- Data inputs are pinned per `ledger/data_baseline.json` and `data/vintages.json`; cache coverage is enforced by `scripts/check_data_coverage.py`. Verification re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`.
- Known open technical note (ledger E049): E041/E042 grid artifacts exhibit 1-ulp QP sensitivity and can exceed the 1e-4 structural-match tolerance in `--extended`; **do not re-pin them to silence this.**

## Initial task for the next agentic work session
1. **Orient (read-only):** read `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md`, and this handoff. Confirm `git status --short`, `git rev-parse --short HEAD`, branch/sync state, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Fast integrity gate (offline, ~seconds):** run `SEED=42 bash scripts/check.sh` (or `make check`). If it reports golden/baseline/coverage issues, resolve them **before** any commit; do not commit interrupted verification state.
3. **If deeper verification is explicitly needed:** run `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full` as appropriate. Always finish or recover with `SEED=42 python3 run_all_verification.py --restore-only`; **do not commit verification output**. If `HEAD` already contains a captured run, restore pinned artifacts per `AGENTS.md` rather than relying on `git checkout -- experiments/`.
4. **Do not start new research or code changes unless explicitly requested and pre-registered.** Preserve multiple-testing discipline, negative-result recording, and baseline integrity. Avoid opportunistic re-pinning, dependency changes, or committing `__pycache__`/unrelated files.

## Handoff deliverable
- This file is the durable, timestamped initial task message for the next agentic work session: `handoff_2026-11-18T11-38-29Z_INITIAL_TASK.md`.