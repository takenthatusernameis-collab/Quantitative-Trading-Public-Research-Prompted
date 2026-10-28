# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T07:34:04Z
- **Branch:** main
- **HEAD:** 1dd44320efe0fbfd8b54ff35b9f87e982669408e ("chore(kilo): checkpoint agent session")
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T07-34-04Z.md (this file); `HANDOFF_CURRENT.md` symlinks here.
- **Working tree:** clean except gitignored `__pycache__/*.pyc`.

## Initial Task (do this first)

1. Verify repo health.
   ```bash
   SEED=42 bash scripts/check.sh
   ```
2. Confirm clean baseline integrity.
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   python3 scripts/check_goldens_clean.py
   ```
3. If all pass: no verification rerun needed; review `ledger/RESEARCH_LEDGER.md` for open items (especially optimizer determinism/E049, data coverage). If goldens fail: restore (`SEED=42 python3 run_all_verification.py --restore-only`), never re-pin as side effect.

## Notes

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Always use `SEED=42`. Cost model: tc=0.5bps + slippage=0.2bps; next-day open execution.
- Never modify `experiments/*.json` as a side effect of verification; use `--restore-only` if interrupted.
- Baseline integrity guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Experiment drivers and task specs: `experiments/run_e*.py`, `E*_TASK_SPEC.md`.
