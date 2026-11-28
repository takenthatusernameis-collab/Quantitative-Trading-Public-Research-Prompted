# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T02:48:03Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Key Notes

- **Seed**: Always use `SEED=42` for reproducibility
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/`.
- **Do not commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Cache coverage**: Enforced invariant - all `data.download()` call sites must have committed cache files matching SHA-256 in `ledger/data_baseline.json`

## Recent Context

- E050 fix (commit `72dc947`): Exact KKT active-set enumeration as primary tangency solver - made E041/E042 artifacts bit-reproducible
- E029 offline-reproducible since 2026-10-20 (fundamentals snapshot pinned)
- E030 offline-reproducible since 2026-10-20 (16-ETF panel committed)
- Optimizer determinism: `src/portfolio_opt.py` validates solver answers on problem constraints, not solver exit status

## Next Steps / Available Tasks

- Run verification suite (`make verify-quick`, `make verify-extended`, or `make verify-full`)
- Individual experiment drivers: `python3 experiments/run_e025.py`, `python3 experiments/run_e041.py`, `python3 experiments/run_e042.py --n-sim 50`
- Batch validation: `SEED=42 python3 src/batch_run.py --universe large_liquid` and `SEED=42 python3 src/validate.py --universe large_liquid`