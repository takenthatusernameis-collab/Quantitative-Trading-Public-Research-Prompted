# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T20:09:06Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Session Context

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

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

## Key Files

- `ledger/RESEARCH_LEDGER.md` - Documented surviving strategies
- `ledger/golden_baseline.json` - SHA-256 fingerprints for experiment artifacts
- `experiments/*.json` - Canonical research artifacts (committed)
- `data/vintages.json` - Pinned data cache vintages
- `data/fundamentals_vintages.json` - Pinned fundamentals for E029
- `scripts/check_goldens_clean.py` - Working tree vs HEAD check
- `scripts/check_golden_baseline.py` - Artifacts vs pinned SHA-256 check
- `scripts/check_data_coverage.py` - Cache coverage invariant

## Critical Notes

1. **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores after. If killed, recover with `--restore-only` or `git checkout -- experiments/`
2. **Baseline integrity**: `scripts/check.sh` runs `check_goldens_clean.py` (working tree vs HEAD) AND `check_golden_baseline.py` (artifacts vs pinned SHA-256). Fix mismatches BEFORE committing.
3. **Data cache coverage enforced**: All `data.download()` call sites must have committed cache files matching `ledger/data_baseline.json`
4. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
5. **Optimizer determinacy** (ledger E049/E050): `src/portfolio_opt.py` validates on constraints, not solver exit status. Exact KKT active-set enumeration (commit `72dc947`) makes E041/E042 bit-reproducible.

## Pending / Next Steps

- [ ] No active verification run (check with `ls -la .verify_snapshot/` if unsure)
- [ ] All experiments in `experiments/` match `ledger/golden_baseline.json`
- [ ] Ready for next research cycle or CI gate setup

---
*This handoff was created automatically at session start. Update as work progresses.*