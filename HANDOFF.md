# Handoff — 2026-10-28T09:16:19Z

## Initial task (do first)
1. **Verify baseline integrity** (must be clean before any changes):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Must pass: goldens clean vs HEAD, `ledger/golden_baseline.json` match, data coverage, tests.
   - If a stale snapshot exists or goldens are dirty: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

2. **Confirm state**:
   - `experiments/` matches HEAD
   - No active verification snapshot (`.verify_snapshot/ACTIVE.json` absent)

## Context
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Verification suite overwrites/restores `experiments/` — never leave a run half-finished.
- Known: E041/E042 numeric drift from ill-conditioned QP (optimizer determinism fixed per E049). Do **not** re-pin to silence; see ledger.
- E029/E030 offline-reproducible via pinned data/fundamentals; cache coverage is enforced.
- CI workflow cannot be created by agents (template at `.github/workflow-templates/verification-gate.yml`).

## Next steps
- Only proceed after baseline is clean.
- If adding data inputs, commit files and re-pin via `python3 scripts/check_data_coverage.py --update`.
- If changing experiments, follow pre-registration/gates and multiple-testing discipline. Never re-pin baselines as a side effect of verification.
