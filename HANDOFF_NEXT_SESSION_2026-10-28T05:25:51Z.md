# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T05:25:51Z
- **Branch:** main
- **HEAD:** 986c900
- **Durable handoff:** this file; `HANDOFF_CURRENT.md` points here.
- **Working tree:** clean except `__pycache__/*.pyc` (no source changes). No `.verify_snapshot/` leftover.

## Initial Task Message for the Next Agentic Work Session

**Continue quantitative research verification and maintenance — repository is clean and fully verified; no bounded in-session research task currently outstanding.**

No new research task was requested this session. The standing state is:

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All experiment goldens in `experiments/*.json` are canonical artifacts.
- Verification suite must preserve goldens — never leave a verification run half-finished.

### Priority Tasks (if a task is desired)

1. **Verify repo health** (convention-robustness + integrity guards):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Confirmed passing at handoff: ALL CHECKS PASSED (107 JSON artifacts, goldens match HEAD, convention robustness PASS, all driver imports OK).

2. **Confirm clean baseline integrity**:
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   python3 scripts/check_goldens_clean.py
   ```

3. **Review state**:
   - If all pass: Review `ledger/RESEARCH_LEDGER.md` for open items. No verification rerun needed.
   - If goldens/guards fail: Restore from snapshot (`SEED=42 python3 run_all_verification.py --restore-only`) or from HEAD as appropriate; never re-pin baselines as a side effect of verification. Check for stale `.verify_snapshot/ACTIVE.json`.

### If a Bounded Research Task Is Assigned

Use the standard workflow: load the relevant `E*_TASK_SPEC.md`, implement the driver in `experiments/run_e*.py` with a `pre_registered` block (gates, falsification expectations, sensitivity grid), run with `SEED=42`, then verify with `SEED=42 python3 run_all_verification.py`. Preserve pre-registered outcomes and promotion gates; never move goalposts post-hoc.

### Key Constraints

- Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution.
- Never modify `experiments/*.json` as a side effect of verification — use `--restore-only` if interrupted.
- Baseline integrity guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Research artifacts are canonical; replacing them requires explicit re-pinning with justification (use `--update` flags on guard scripts only when intentionally updating baselines).
- Verification suite overwrites/restores `experiments/*.json` via local snapshot in `.verify_snapshot/` (gitignored). A run must never be left half-finished.
- Extended verification (`--extended`) is environment-nondeterministic on BLAS/numpy; pre-existing drift class (e029/e030/e041) documented in ledger E041/E048/E049 disposition. Do not weaken tolerances or modify committed goldens.

### Quick References

- Verification: `make verify-quick` / `make verify-extended` / `make verify-full` or `SEED=42 python3 run_all_verification.py [--extended|--full|--skip-slow|--restore-only]`
- Individual runs: see `README.md` and `AGENTS.md`
- Ledger: `ledger/RESEARCH_LEDGER.md` (research complete E001–E043)
- Prior handoffs: `HANDOFF_NEXT_SESSION_*.md`, `HANDOFF_CURRENT.md`, `HANDOFF.md`