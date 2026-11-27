# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-27T07:41:16Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Supersedes**: `handoff_2026-11-27T07-40-35Z_INITIAL_TASK.md`

## Initial Task (for the next agentic work session)

Start from a verified-clean baseline, then stop. This handoff was created at the
explicit request of the user (not a self-manufactured refresh). Do **not**
manufacture further handoff refreshes or re-pin/overwrite golden artifacts unless
a deliberate code change is requested and recorded in the ledger first.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist.
   If a live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `numpy`, `scipy`, and `pandas` are NOT installed in this environment; the
   full suite and `scripts/check.sh` need them.
3. **Confirm goldens match HEAD** —
   `SEED=42 python3 scripts/check_goldens_clean.py`.
4. **Confirm goldens match pinned baseline** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (all pinned artifacts unchanged).
5. **Confirm data coverage** —
   `SEED=42 python3 scripts/check_data_coverage.py` (all pinned inputs present/tracked/unchanged).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds)
   — only after step 2, otherwise the pandas-dependent unit tests error out.

No code changes are requested yet. The goal of this handoff is to hand the next
session a verified-clean starting point.

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Git State (2026-11-27T07:41:16Z)

HEAD: see `git log --oneline -1`.
" filePath">
/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff_2026-11-27T07-41-16Z_INITIAL_TASK.md