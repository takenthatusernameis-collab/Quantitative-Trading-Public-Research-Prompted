# Agentic Work Session Handoff

**Timestamp:** 2026-11-21T11:56:48Z
**Session ID:** Current session
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Files & Structure

- **Experiments:** `experiments/*.json` (canonical research artifacts)
- **Source Code:** `src/` (batch_run.py, validate.py, portfolio_opt.py, etc.)
- **Drivers:** `experiments/run_e*.py` (individual experiment drivers)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data:** `data/` (cached parquet, gitignored except pinned vintages)
- **Verification:** `run_all_verification.py`, `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

## Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Important Notes

1. **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores them after. Use `--restore-only` if interrupted.
2. **Golden baseline integrity** - `ledger/golden_baseline.json` pins SHA-256 of canonical artifacts. Never re-pin as side effect of verification.
3. **Data cache coverage enforced** - `scripts/check_data_coverage.py` validates all cache files exist and match pinned SHA-256 in `ledger/data_baseline.json`.
4. **Offline reproducibility** - Set `SEED=42` and `QUANT_RESEARCH_OFFLINE=1` for verification runs.
5. **Optimizer determinism** - `src/portfolio_opt.py` validates solver answers on constraints, not exit status (see ledger E049).

## Individual Experiment Commands

```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Review any open items in the ledger (E041 drift, E049 optimizer determinism)
4. Run verification suite as needed for reproduction/validation

---

*This handoff was created automatically at session start. Update as needed during work.*