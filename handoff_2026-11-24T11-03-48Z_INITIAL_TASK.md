# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T12:55:13Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates
- Golden artifacts in `experiments/*.json` are canonical baselines

## Verification Commands

```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Recovery if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Conventions

- **Seed**: Always use `SEED=42` for reproducibility
- **Convention**: Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (pinned vintages 2026-10-12, 2026-10-11)
- **Cache coverage**: Enforced invariant via `scripts/check_data_coverage.py`
- **Golden baseline**: Pinned in `ledger/golden_baseline.json` — never re-pin without ledger entry

## Active Context

- Optimizer determinism fixed via E050 exact active-set enumeration (commit 72dc947)
- E029 fundamentals pinned offline-reproducible since 2026-10-20
- E030 16-ETF panel committed and pinned
- E041/E042 bit-reproducible across environments (0 differences at 2026-11-23 measurement)

## Next Session Starting Point

Run `SEED=42 bash scripts/check.sh` to verify environment integrity before any work.