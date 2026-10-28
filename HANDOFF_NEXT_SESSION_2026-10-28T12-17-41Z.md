# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T12-17-41Z
- **Branch:** main
- **HEAD:** $(git rev-parse HEAD)
- **Durable handoff:** 2026-10-28T12-17-41Z_FILE (this file); `HANDOFF_CURRENT.md` and `HANDOFF_NEXT_SESSION.md` symlink here.
- **Working tree:** Check with `git diff --name-only` (should be clean or only untracked/temp files).

## Initial Task (do this first)

1. **Verify environment and repo state**
   ```bash
   git log -1 --oneline
   git branch -v
   git diff --name-only
   ```

2. **Run baseline integrity checks (must pass)**
   ```bash
   SEED=42 bash scripts/check.sh
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   python3 scripts/check_goldens_clean.py
   ```

3. **If checks fail**
   - If verification left artifacts modified: restore goldens with `SEED=42 python3 run_all_verification.py --restore-only` (do **not** re-pin baselines).
   - If golden baseline mismatch: do **not** change `experiments/*.json` to match current run; restore from HEAD or the pinned golden per `ledger/golden_baseline.json`.
   - Investigate any data coverage issues before proceeding.

4. **Review context**
   - Read `ledger/RESEARCH_LEDGER.md` for validated strategies (E001–E043 complete) and open items.
   - Read `AGENTS.md` for conventions (SEED=42, tc/slippage, next-day open, offline verification expectations).
   - Check recent handoffs if needed for continuity.

## Constraints / Reminders
- Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution.
- Research phase complete; do not re-run full verification unless explicitly requested or fixing a regression.
- Never modify `experiments/*.json` as a side effect of verification. Use `--restore-only` if interrupted.
- Baseline integrity guards are enforced: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- If adding data inputs, commit them and re-pin via `scripts/check_data_coverage.py --update`.
