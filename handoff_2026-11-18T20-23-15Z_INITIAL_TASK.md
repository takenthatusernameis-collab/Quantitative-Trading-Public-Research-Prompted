# Agentic Handoff — Initial Task Message

## Timestamp
2026-11-18T20:23:15Z

## Purpose
Leave a clear initial task message for the next agentic work session.

## Repo context
Quantitative-Trading-Public-Research-Prompted — independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043).

## Baseline integrity (READ BEFORE RUNNING)
`experiments/*.json` are canonical research artifacts. `run_all_verification.py` backs them up and restores them — never commit verification output.

- `.verify_snapshot/` (gitignored) holds backups; stale snapshots fail `check_goldens_clean.py`.
- `ledger/golden_baseline.json` pins SHA-256 fingerprints of tracked artifacts. Replacing an artifact requires `python3 scripts/check_golden_baseline.py --update`.
- `ledger/data_baseline.json` pins SHA-256 of cached parquet inputs. Adding a data input: commit the file, then `python3 scripts/check_data_coverage.py --update`.
- Runs use `SEED=42` and `QUANT_RESEARCH_OFFLINE=1` (missing cache entry fails hard).

## Available verification commands
```bash
SEED=42 bash scripts/check.sh          # convention robustness + template validation (~seconds)
SEED=42 python3 run_all_verification.py --skip-slow   # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # extended (~21 min)
SEED=42 python3 run_all_verification.py --full         # full (~15 min)
SEED=42 python3 run_all_verification.py --restore-only # recover goldens after interrupted run
```

## Experiment drivers (8 in 5a block)
E012, E023, E024 (--merge), E027, E035, E037, E039, E042-lead. Extended adds E011, E013, E015–E022, E025–E026, E028–E030, E034, E036, E041.

## Lint / typecheck
`python3 -m py_compile` on changed Python files (no separate linter configured). `requirements.txt`: numpy, pandas, scipy, pyarrow, statsmodels, yfinance (cvxpy optional).

## Next task
None specified yet — awaiting user task for the next session. Status: idle, ready for instructions.