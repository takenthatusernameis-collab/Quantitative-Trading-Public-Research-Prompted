# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T10:33:40Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current state (verified)
- **HEAD:** `6fdceb5d` (`6fdceb5d8e8e853b20b52ec4c3d251119f6f0326`, `main == origin/main`, ahead/behind 0/0)
- **Working tree:** clean at handoff creation (no tracked/untracked changes expected). Do not commit `__pycache__` churn or unrelated files.
- **Integrity state:** no `.verify_snapshot/ACTIVE.json` or `.verify_reports/` observed; `git diff --name-only HEAD -- experiments/` empty.
- **Project status:** research phase complete (E001–E051). Surviving strategies and all dispositions (REJECTED/PARTIAL/ACCEPTED) are authoritative in `ledger/RESEARCH_LEDGER.md`. Repo is in a closed, reproducibility-focused state.
- **Canonical artifacts:** `experiments/*.json` are pinned in `ledger/golden_baseline.json`; data inputs/coverage pinned via `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json` and enforced by `scripts/check_data_coverage.py`. Verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Known open technical note:** E041/E042 grid artifacts show 1-ulp QP sensitivity in `--extended` (numeric drift beyond 1e-4 tolerance) — do **not** re-pin to silence (see ledger E049).

## Initial task for next session
1. **Orient (read-only first):** review `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md`, and this handoff. Confirm `git status --short`, `git rev-parse --short HEAD`, and absence of `.verify_snapshot/ACTIVE.json`.
2. **Run fast integrity gate (offline):** `SEED=42 bash scripts/check.sh` (or `make check`). If any golden/baseline/coverage issue appears, fix it before committing anything; never checkpoint a captured verification run.
3. **Deeper verification only if needed:** `SEED=42 python3 run_all_verification.py` (`--extended` / `--full` as appropriate). Never leave a run half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only` if interrupted. Do **not** commit verification output or restored-run churn.
4. **Do not start new research by default.** Proceed with additional work only if explicitly requested and pre-registered per `AGENTS.md`/ledger discipline (no goalpost moves, no opportunistic re-pinning, no unrequested driver/artifact changes).

## Constraints to honor
- Always use `SEED=42` for verification/repro steps.
- Preserve canonical baselines: no golden/data re-pinning without explicit justification and a diff-visible, intentional update.
- Keep `experiments/` matching pinned baselines/HEAD; `git checkout -- experiments/` restores HEAD (if HEAD was contaminated, restore the pinned artifact per `AGENTS.md`).
- Do not commit `__pycache__`, `.verify_snapshot/`, `.verify_reports/`, or other transient verification artifacts.

## Handoff pointers
- This file is the durable, timestamped initial task message for the next agentic work session.
- Generic handoff pointers/symlinks should target this file; mirror copies should be kept in `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, and `.kilo/handoff/` for discoverability.
