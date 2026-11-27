# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-27T10:45:53Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task (for the next agentic work session)

Start from the verified-clean baseline recorded below, then stop. Do **not**
manufacture further handoff refreshes, re-pin artifacts, or overwrite goldens
unless a deliberate code change is requested and recorded in the ledger first.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist.
   If a live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `pandas` is NOT installed in this environment; the full suite needs it.
3. **Confirm goldens match HEAD** — `SEED=42 python3 scripts/check_goldens_clean.py`.
4. **Confirm goldens match pinned baseline** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (all 107 pinned artifacts unchanged).
5. **Confirm data coverage** —
   `SEED=42 python3 scripts/check_data_coverage.py` (all 35 pinned inputs present/tracked/unchanged).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

If all six steps pass, the baseline is clean: report that and stop. Do not
re-run the full verification suite or re-pin anything as a side effect. Only
make a code change if the user explicitly requests one, and record it in the
ledger before re-pinning any published number.

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Git State (2026-11-27T10:45:53Z)

- Branch: `main`; HEAD `8cd55e5e` (checkpoint commit).
- Working tree clean except `.pyc` cache files (untracked-ish modifications); no tracked source changes.
- `.verify_snapshot/` absent (no live run owns the snapshot).
" filePath="/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff_2026-11-27T10-45-53Z_INITIAL_TASK.md"