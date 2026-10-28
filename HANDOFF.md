# Handoff - 2026-10-28T05:25:51Z

## Durable Handoff

`HANDOFF_NEXT_SESSION_2026-10-28T05:25:51Z.md` (also pointed to by `HANDOFF_CURRENT.md`).

## Initial Task Message for Next Agentic Work Session

**Continue quantitative research verification and maintenance — repository is clean and fully verified; no bounded in-session research task currently outstanding.**

No new research task was requested this session. Standing state:

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All experiment goldens in `experiments/*.json` are canonical artifacts.
- Verification suite must preserve goldens — never leave a verification run half-finished.

### Priority Tasks (if a task is desired)

1. **Verify repo health** — `SEED=42 bash scripts/check.sh` (confirmed ALL CHECKS PASSED at handoff: 107 JSON artifacts, goldens match HEAD, convention robustness PASS, all driver imports OK).
2. **Confirm clean baseline integrity** — `git diff --name-only`, `python3 scripts/check_golden_baseline.py`, `python3 scripts/check_data_coverage.py`, `python3 scripts/check_goldens_clean.py`.
3. **Review state** — If all pass, review `ledger/RESEARCH_LEDGER.md` for open items; no verification rerun needed. If goldens/guards fail, restore via `SEED=42 python3 run_all_verification.py --restore-only`; never re-pin baselines as a side effect of verification; check for stale `.verify_snapshot/ACTIVE.json`.

### If a Bounded Research Task Is Assigned

Load the relevant `E*_TASK_SPEC.md`, implement the driver in `experiments/run_e*.py` with a `pre_registered` block (gates, falsification expectations, sensitivity grid), run with `SEED=42`, then verify with `SEED=42 python3 run_all_verification.py`. Preserve pre-registered outcomes and promotion gates; never move goalposts post-hoc.

### Important Notes

- Always use `SEED=42` for reproducibility.
- If a verification run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- Never re-pin goldens to silence numeric drift — document in ledger if issues arise.
- Cache coverage is enforced — missing data files will fail hard in offline mode.
- Extended verification (`--extended`) is environment-nondeterministic on BLAS/numpy; pre-existing drift class (e029/e030/e041) documented in ledger E041/E048/E049 disposition. Do not weaken tolerances or modify committed goldens.

### Context

Quantitative trading research repo focused on reproducible strategy research on 2014–2026 US equities, futures, and macro data.