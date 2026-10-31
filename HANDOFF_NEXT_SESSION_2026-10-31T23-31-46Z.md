# HANDOFF_NEXT_SESSION_2026-10-31T23-31-46Z

**Created:** 2026-10-31T23:31:46Z
**Type:** Durable handoff (initial task message for next agentic work session)
**Status:** Ready for pickup

## Initial task for next session (do first, in order)

1. **Verify repo health** - Run integrity checks before making changes:
   ```bash
   git status --short
   SEED=42 bash scripts/check.sh
   ```
   - If `scripts/check_goldens_clean.py` reports a stale snapshot (`.verify_snapshot/ACTIVE.json` exists from a dead PID), recover first: `SEED=42 python3 run_all_verification.py --restore-only`
   - If golden integrity fails, restore from HEAD: `git checkout -- experiments/` or use `run_all_verification.py --restore-only`. Never re-pin goldens as a side effect of running verification.
   - If any artifact differs from `ledger/golden_baseline.json` (pinned SHA-256), do not overwrite it.

2. **Confirm verification baseline** - Ensure the repo is in verified state:
   ```bash
   SEED=42 python3 verify_convention_robustness.py
   ```
   All guards must pass cleanly.

## Constraints (must follow)
- Do **not** modify `experiments/*.json` (committed goldens). Verification suite restores them automatically.
- Do **not** weaken tolerances or change gate logic.
- Follow project conventions in `AGENTS.md` - pre-registration, multiple-testing discipline, negative results recorded honestly.
- If interrupted during any verification run, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Notes
- Research phase complete (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Known pre-existing drifts in extended verification (E030, E041) are documented; do not "fix" by regenerating goldens.
- This handoff supersedes previous timestamped handoffs.
- Symlink `HANDOFF_NEXT_SESSION.md` to this file if not already pointing.
