# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T11:29:07Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**HEAD at handoff:** `73eb1857` (`73eb18574b92156db31aa8b043663cb96eb9b654`, `main...origin/main`, clean at inspection except untracked handoff artifacts created by this session)

## Project state (authoritative context)
- Research phase complete (E001–E051). Validated/rejected/partial dispositions are authoritative in `ledger/RESEARCH_LEDGER.md`; do not reopen or start new research without an explicit, pre-registered request per `AGENTS.md`.
- Canonical artifacts are pinned: experiment goldens in `experiments/*.json` ↔ `ledger/golden_baseline.json`; data inputs/coverage in `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json` (see `scripts/check_data_coverage.py`). Verification runs with `QUANT_RESEARCH_OFFLINE=1` and `SEED=42`.
- Known open technical note: E041/E042 grid artifacts show 1-ulp QP sensitivity in `--extended` (numeric drift beyond 1e-4 tolerance). Do **not** re-pin to silence; see ledger E049/RESEARCH_LEDGER.

## Integrity & recovery rules (must follow)
- Never leave a verification run half-finished. Snapshot/marker lives in `.verify_snapshot/` (`ACTIVE.json`). If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
- Do **not** commit verification output, restored-run churn, `.verify_snapshot/`, `.verify_reports/`, `__pycache__`, or unpinned data.
- `scripts/check.sh` / `scripts/check_goldens_clean.py` / `scripts/check_golden_baseline.py` must be clean before committing. `git checkout -- experiments/` restores `HEAD` only (if `HEAD` is contaminated, restore the SHA-256-pinned artifact referenced in `ledger/golden_baseline.json`).

## Initial task for the next session
1. **Orient (read-only):**
   - `git status --short`
   - `git rev-parse --short HEAD`
   - confirm no `.verify_snapshot/ACTIVE.json`
   - skim `AGENTS.md`, tail of `ledger/RESEARCH_LEDGER.md`, and this handoff.
2. **Fast integrity gate (offline, required before changes):**
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - If any golden/baseline/coverage/template issue appears, diagnose and fix it without re-pinning artifacts opportunistically.
3. **Deeper verification only if needed/requested:**
   - `SEED=42 python3 run_all_verification.py` (quick), or `--extended` / `--full` as appropriate.
   - Do not run in a way that risks an unrecoverable partial state; prefer recoverability and stop if the environment cannot complete safely.
4. **Default posture:** no new experiments/drivers/artifact changes. Proceed with additional work only if explicitly requested, pre-registered, and consistent with ledger/AGENTS constraints (no goalpost moves, no unrequested re-pinning).

## Suggested quick commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --skip-slow   # if a light suite pass is useful
SEED=42 python3 run_all_verification.py --restore-only  # only if a run was interrupted
```

## Handoff pointers
- Canonical timestamped handoff: `handoff_2026-11-18T11:29:07Z_INITIAL_TASK.md`
- Generic pointers (`latest*`, `next*`, `handoff_next*`, etc.) and copies in `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` should reference this file for discoverability.
