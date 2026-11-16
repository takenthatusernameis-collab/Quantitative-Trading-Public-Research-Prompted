# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T04:49:54Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Files
- `AGENTS.md` - Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies
- `experiments/*.json` - Canonical research artifacts (golden files)
- `data/vintages.json` - Pinned data cache vintages
- `scripts/check.sh` - Convention robustness check

## Critical Notes
1. **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores after. Use `--restore-only` to recover if interrupted.
2. **Golden baseline integrity** - `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
3. **Cache coverage invariant** - All data inputs must be pinned in `ledger/data_baseline.json`. Run `scripts/check_data_coverage.py --update` to add new inputs.
4. **SEED=42** required for all reproducibility.
5. **No CI workflow creation** - template at `.github/workflow-templates/verification-gate.yml` but maintainer must create via GitHub UI.

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy status
3. Review any open items in ledger (E049 optimizer determinism, E041 drift)
4. Proceed with intended research/verification task