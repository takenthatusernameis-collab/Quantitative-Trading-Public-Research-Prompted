# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T12-35-23Z
- **Branch:** main
- **HEAD:** 6d284c6
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T12-35-23Z.md (this file); `HANDOFF_CURRENT.md` and `HANDOFF_NEXT_SESSION.md` symlink here.
- **Working tree:** Clean of tracked changes except `__pycache__/*.pyc` (gitignored in practice; can ignore).

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
3. If all pass: review `ledger/RESEARCH_LEDGER.md` for any remaining open items. If goldens fail: restore (`SEED=42 python3 run_all_verification.py --restore-only`), never re-pin as side effect.

## Context

- Research phase complete (E001–E043). See `ledger/RESEARCH_LEDGER.md` for validated strategies and final status.
- Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution.
- Never modify `experiments/*.json` as a side effect of verification; use `--restore-only` if interrupted.
- Baseline integrity guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Convention: v1.2.3 — close-to-close primary; mixed-convention portfolios are prohibited; overnight decomposition required.

(End of file)
