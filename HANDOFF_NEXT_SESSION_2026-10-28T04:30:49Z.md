# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T04:30:49Z
- **Branch:** main
- **HEAD:** 558fe30c027b60140722657c39dfa2ac18c7f017
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T04:30:49Z.md (this file); update `HANDOFF_CURRENT.md` to point to this file.
- **Working tree:** 4 modified files (see `git diff --name-only`)

## Initial Task (do this first)

1. **Verify repo health** (convention-robustness + integrity guards):
   ```bash
   SEED=42 bash scripts/check.sh
   ```

2. **Confirm clean baseline integrity**:
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   python3 scripts/check_goldens_clean.py
   ```

3. **Review state**:
   - If all pass: Review `ledger/RESEARCH_LEDGER.md` for open items (research phase complete E001–E043). No verification rerun needed.
   - If goldens/guards fail: Restore from snapshot (`SEED=42 python3 run_all_verification.py --restore-only`) or from HEAD as appropriate; never re-pin baselines as a side effect of verification. Check for stale `.verify_snapshot/ACTIVE.json`.

## Key Constraints

- Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution.
- Never modify `experiments/*.json` as a side effect of verification — use `--restore-only` if interrupted.
- Baseline integrity guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Research artifacts are canonical; replacing them requires explicit re-pinning with justification (use the `--update` flags on guard scripts only when intentionally updating baselines).
- Verification suite overwrites/restores `experiments/*.json` via local snapshot in `.verify_snapshot/` (gitignored). A run must never be left half-finished.

## Quick References

- Verification: `make verify-quick` / `make verify-extended` / `make verify-full` or `SEED=42 python3 run_all_verification.py [--extended|--full|--skip-slow|--restore-only]`
- Individual runs: see `README.md` and `AGENTS.md`
- Ledger: `ledger/RESEARCH_LEDGER.md` (research complete E001–E043)
- Prior handoffs: `HANDOFF_NEXT_SESSION_*.md`, `HANDOFF_CURRENT.md`
