# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T04-29-00Z
- **Branch:** main
- **HEAD:** 8870f0ce6062c96d312362fa45d7cf98921f668c (2026-10-28 04:28:23 +0000, "chore(kilo): checkpoint agent session")
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T04-29-00Z.md (this file); `HANDOFF_CURRENT.md` symlinks here.
- **Working tree:** 4 modified files (see `git diff --name-only`); no `.verify_snapshot/` present, no live verification run.

## Initial Task (do this first)

1. **Verify repo health** (convention-robustness + guards):
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

3. **If all pass**: Review `ledger/RESEARCH_LEDGER.md` for open items (research phase complete E001–E043). No verification rerun needed.
   **If goldens fail**: Restore from snapshot (`SEED=42 python3 run_all_verification.py --restore-only`) or from HEAD; never re-pin baselines as a side effect of verification.

## Key Constraints

- Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution.
- Never modify `experiments/*.json` as a side effect of verification — use `--restore-only` if interrupted.
- Baseline integrity guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Research artifacts are canonical; replacing them requires explicit re-pinning with justification.
- Verification suite overwrites/restores `experiments/*.json` via local snapshot in `.verify_snapshot/` (gitignored).

## Quick References

- Verification: `make verify-quick` / `make verify-extended` / `make verify-full`
- Individual runs: see `README.md` and `AGENTS.md`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- Prior handoffs: `HANDOFF_NEXT_SESSION_*.md`
