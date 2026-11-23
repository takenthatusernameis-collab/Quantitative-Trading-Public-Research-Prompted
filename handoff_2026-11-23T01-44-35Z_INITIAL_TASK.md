# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T02:32:28Z
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Notes for Next Session
- **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them while re-running and restores afterward. Never leave a verification run half-finished.
- **Reproducibility**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages).
- **Cache coverage**: Enforced invariant - `scripts/check_data_coverage.py` validates all cache files exist and match SHA-256 in `ledger/data_baseline.json`.

## Recent Verification Status
- E029: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`)
- E030: Offline-reproducible since 2026-10-20 (16-ETF input panel committed)
- E041: 133 numeric differences remain (ill-conditioned QP optimizer sensitivity); decision unchanged (REJECTED 3/5)
- E042: Partial confirmation, tangency QP ill-conditioned (~1e-05 drift on 1-ulp perturbation)

## Open Items (from ledger)
- E041/E042 grid artifacts drift by 29-133 differences - do NOT re-pin to silence
- Optimizer determinism: SLSQP status 8 at constrained optimum is scipy-build dependent; rule pinned by `tests/test_portfolio_opt.py`

## Next Steps
Run `SEED=42 python3 run_all_verification.py --extended` to verify extended driver coverage, or `make verify-quick` for fast verification.