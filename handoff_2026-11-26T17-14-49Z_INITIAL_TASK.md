# Handoff - Next Agentic Work Session

**Timestamp:** 2026-11-26T20:08:36Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Convention robustness check (seconds, offline)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts
- **Golden files:** `experiments/*.json` (committed baselines)
- **Data cache:** `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12)
- **Fundamentals:** `data/fundamentals/` (pinned per `data/fundamentals_vintages.json`)
- **Ledger:** `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Critical Notes
1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
2. **Seed always 42** for reproducibility (walk-forward + placebo RNG)
3. **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
4. **Cache coverage invariant:** Every `data.download()` call must have committed, SHA-256-pinned cache file (enforced by `scripts/check_data_coverage.py`)
5. **Optimizer determinacy:** SLSQP exit status ignored; validation is on constraints only (tested in `tests/test_portfolio_opt.py`)

## Recent State
- E041/E042 ill-conditioned QP drift resolved by E050 exact active-set enumeration (commit `72dc947`)
- E029/E030 offline-reproducible since 2026-10-20 (pinned data)
- Extended verification: 18 drivers, 0 differences at 2026-11-23T05:17Z measurement

## Next Steps (if any)
- Run `scripts/check.sh` to verify clean state before new work
- Consider any new experiment pre-registration per project conventions