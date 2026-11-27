# Durable Handoff — Initial Task Message

## Message Timestamp
Created: 2026-11-27T04:59:29Z

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. All experiments are pre-registered with falsification
expectations and promotion gates. **Research phase complete (E001–E043).**
Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Git State (verified this session, 2026-11-27T04:59Z)
- Branch: `main`; HEAD `a8e4a282` ("chore(kilo): checkpoint agent session"); `main...origin/main` up to date.
- Working tree: only `__pycache__/*.pyc` churn (no source/ledger/artifact changes); effectively clean.
- No `.verify_snapshot/` and no `.verify_reports/` — no verification run in progress.
- Python scientific stack absent (pandas/numpy/scipy/pyarrow/statsmodels/yfinance not installed); `scripts/check.sh` cannot pass until installed (see prior handoff).

## What Was Done This Session
None to code/data/ledger/artifacts. This session's only action was writing this
durable handoff (explicit user request); no commit was made.

## Next Steps for the Next Session
1. `python3 -m pip install -r requirements.txt` (stack currently absent).
2. Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md`.
3. Run `SEED=42 bash scripts/check.sh` to confirm a clean baseline before starting work.
4. Do not commit verification output or re-pin goldens as a side effect of a run.
5. If modifying an experiment driver, update its `pre_registered` JSON block and record gate changes in the ledger first.

## Key Files
- `AGENTS.md` — project commands & conventions
- `requirements.txt` — pinned deps; install before running the suite
- `ledger/RESEARCH_LEDGER.md` — surviving strategies & gate dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

(End of file)