# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T05:59:29Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

## Quick Verification Commands
```bash
# Fast convention-robustness check (~seconds)
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

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Key Integrity Notes
- **Never leave verification half-finished**: The suite backs up `experiments/*.json` to `.verify_snapshot/` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
- **Golden baseline**: `ledger/golden_baseline.json` pins SHA-256 of canonical artifacts. Never re-pin as side effect of verification.
- **Data cache**: Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029). Cache coverage enforced by `scripts/check_data_coverage.py`.
- **Optimizer determinacy**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049). E041/E042 grid artifacts have known 1-ulp drift — do not re-pin.

## Current Task Context
Initial handoff created. Next session should:
1. Run `make check` to verify baseline integrity
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
3. Determine next research or validation steps