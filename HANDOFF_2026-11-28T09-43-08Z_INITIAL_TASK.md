# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T10:36:11Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden Baseline**: Pinned in `ledger/golden_baseline.json` (SHA-256 fingerprints)
- **Data Vintages**: 2026-10-12 (primary), 2026-10-11 (E026/E028/E029/E030/E034/E036/E037), E029 fundamentals pinned separately

## Verification Commands (SEED=42)

```bash
# Fast convention check (~seconds)
make check

# Quick full verification (~8 min, 8 drivers)
make verify-quick

# Extended verification (~21 min, 26 drivers + structural match)
make verify-extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
make verify-full
```

## Key Invariants (must hold)

1. **Golden files never modified by verification** — `run_all_verification.py` backs up/restores `experiments/*.json`
2. **Cache coverage enforced** — `scripts/check_data_coverage.py` validates all driver cache files exist and match `ledger/data_baseline.json`
3. **Optimizer determinism** — SLSQP exit status ignored; feasibility/optimality validated on constraints (see `tests/test_portfolio_opt.py`)
4. **No tolerance-violation re-pinning** — E041/E042 are bit-reproducible via E050 exact-solver fix; re-pinning only for deliberate code changes recorded in ledger

## Current Status

- All 26 committed drivers reproduce with 0 differences (2026-11-23T05:17Z measurement)
- E029, E030 offline-reproducible since 2026-10-20 (pinned data)
- E041/E042 optimizer drift fixed by E050 (exact KKT active-set enumeration)

## Next Session Starting Points

- Run `make check` to verify baseline integrity before any changes
- Consult `ledger/RESEARCH_LEDGER.md` for experiment dispositions (REJECTED/PARTIAL/VALIDATED)
- New experiments require pre-registration with gates/falsification expectations before execution