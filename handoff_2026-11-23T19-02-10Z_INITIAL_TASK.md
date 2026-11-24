# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T02:12:00Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Overview

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Current State

- Research phase: **COMPLETE** (E001–E043)
- Verification suite: Available via `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`
- Golden artifacts: Located in `experiments/*.json` (canonical research artifacts)
- Data: Cached parquet in `data/` (gitignored except pinned vintages)
- Key ledger entries: E045 (E029 offline-reproducible), E048 (E030 data pinned), E049 (optimizer determinism), E050 (exact KKT active-set fix)

## Quick Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Important Notes

1. **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores after. If interrupted, run `--restore-only` or `git checkout -- experiments/`
2. **Golden baseline integrity** - `scripts/check_golden_baseline.py` compares artifacts against SHA-256 fingerprints in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
3. **Data coverage invariant** - All `data.download()` call sites must have committed cache files matching `ledger/data_baseline.json`. Use `scripts/check_data_coverage.py --update` to add new inputs.
4. **Optimizer determinicity** - `src/portfolio_opt.py` validates on constraints, not solver exit status. E050 exact active-set enumeration makes E041/E042 bit-reproducible.
5. **CI workflow** - Cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml`

## Key Files to Reference

- `AGENTS.md` - Project commands & conventions (this file's source)
- `ledger/RESEARCH_LEDGER.md` - Surviving validated strategies
- `ledger/golden_baseline.json` - Pinned SHA-256 for experiments artifacts
- `ledger/data_baseline.json` - Pinned SHA-256 for data cache files
- `data/vintages.json` - Pinned data vintage (2026-10-12)
- `data/fundamentals_vintages.json` - E029 fundamentals snapshot
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Main verification suite

## Next Session Suggestions

- Run `SEED=42 make check` to verify baseline integrity
- Run `SEED=42 make verify-quick` for quick verification
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Check if any new experiments need to be added post-E043