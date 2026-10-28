# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T03-39-34Z
- **Branch:** main
- **HEAD:** 1bea5ba435d094a7e34f2abf272d0c57b5bb5737
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T03-39-34Z.md (this file); `HANDOFF_CURRENT.md` symlinks here.
- **Working tree:** Clean of tracked changes (only `__pycache__/*.pyc` churn). No `.verify_snapshot/` present.

## Initial Task (do this first)
1. Verify repo health.
   ```bash
   SEED=42 bash scripts/check.sh
   ```
2. Confirm clean baseline.
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```
3. If all pass: no verification rerun needed; review `ledger/RESEARCH_LEDGER.md` for open items. If goldens fail: restore (`SEED=42 python3 run_all_verification.py --restore-only`), never re-pin as side effect.

## Notes
- Research phase complete (E001–E043). See `ledger/RESEARCH_LEDGER.md` for validated strategies and open items.
- Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution.
- Never modify `experiments/*.json` as a side effect of verification; use `--restore-only` if interrupted.
- Baseline integrity guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
