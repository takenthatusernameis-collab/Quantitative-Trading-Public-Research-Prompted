# Durable Handoff — Kilo session

**Last updated:** 2026-11-23T19:04:35Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Task for next session

No active task was provided yet. The user's initial message was:

> "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"

This file (`HANDOFF.md`) is that durable handoff. Clear it / overwrite it with the actual task details when the next session begins.

## Repository context

- Quantitative-strategy research repo on 2014–2026 US equities, futures, and macro data.
- Research phase complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are committed golden artifacts — never commit verification output.
- Convention: `SEED=42`; offline mode `QUANT_RESEARCH_OFFLINE=1`.
- Key commands (from `AGENTS.md`):
  - `SEED=42 bash scripts/check.sh` — convention robustness + template validation (~seconds, offline)
  - `SEED=42 python3 run_all_verification.py --quick` — 8 drivers (~8 min)
  - `SEED=42 python3 run_all_verification.py --extended` — +18 drivers, compares to committed goldens
  - `SEED=42 python3 run_all_verification.py --full` — E042 n_sim=50 + sensitivity grid
  - `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after interrupted run
- `python3 -m py_compile <file>` for syntax checks on changed files.
- `cvxpy`/`cvxopt` optional; portfolio optimizer falls back to `scipy.optimize`.
- Cache coverage invariant: `scripts/check_data_coverage.py` pins all driver data inputs in `ledger/data_baseline.json`.

## Where to start next session

1. Read `AGENTS.md` (baseline integrity rules above).
2. Read `ledger/RESEARCH_LEDGER.md` for standing dispositions / driver decisions.
3. Check `git status` — if `experiments/` holds driver output instead of goldens, run `--restore-only`.
4. Then run `SEED=42 bash scripts/check.sh` as the convention gate before any code change.
