# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-27T06:45:05Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task (for the next agentic work session)

Start from a verified-clean baseline, then stop. Do **not** manufacture further
handoff refreshes or re-pin artifacts unless a deliberate code change is
requested and recorded in the ledger first.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist.
   If a live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `pandas` is NOT installed in this environment; the full suite needs it.
3. **Confirm goldens match HEAD** — `SEED=42 python3 scripts/check_goldens_clean.py`.
4. **Confirm goldens match pinned baseline** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (all pinned artifacts unchanged).
5. **Confirm data coverage** —
   `SEED=42 python3 scripts/check_data_coverage.py` (all pinned inputs present/tracked/unchanged).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

No code changes are requested yet. The goal of this handoff is to hand the next
session a verified-clean starting point.

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Git State (2026-11-27T06:45:05Z)

- Branch: `main`; HEAD `29e65476` (checkpoint commit).
- Working tree clean except `src/__pycache__/cache_keys.cpython-312.pyc` (generated).
- `.verify_snapshot/` absent (no live run owns the snapshot).

## Baseline Integrity (2026-11-27T06:45:05Z)

- ✅ No active verification run: `.verify_snapshot/` does not exist.
- ⚠️ Missing dependency: `pandas` is not installed. Run
  `pip install -r requirements.txt` before the full verification suite.
- Baseline last verified clean 2026-11-27T06:44:03Z; no tracked source changes since.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                    # fast convention + template validation (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md`
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Handoff Context

Created at the start of a new agentic work session. No snapshot recovery needed;
no code changes made. The only environment gap is the missing `pandas`
dependency.

(End of file)
