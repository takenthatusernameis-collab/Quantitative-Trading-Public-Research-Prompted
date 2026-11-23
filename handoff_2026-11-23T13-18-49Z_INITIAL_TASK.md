# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T13:24:09Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Current State
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden artifacts in `experiments/*.json` are canonical baselines

## Quick Commands
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
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — never re-pin without ledger entry
- Data cache coverage enforced via `scripts/check_data_coverage.py` and `ledger/data_baseline.json`
- Optimizer determinism: exact KKT active-set enumeration (E050 fix, commit `72dc947`)

## Next Session Suggestions
- Run `make check` to verify current state
- Consider `make verify-quick` for full reproduction check
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items