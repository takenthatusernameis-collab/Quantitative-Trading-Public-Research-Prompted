# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T00:21:48Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

## Critical Integrity Notes

1. **Golden artifacts**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them during re-run and restores them afterward. **Never leave a verification run half-finished**.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement. Run `scripts/check.sh` before committing.

4. **Data cache**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant via `scripts/check_data_coverage.py`.

5. **Optimizer determinism**: Portfolio optimizer validates on problem constraints, not solver exit status (ledger E049). E050 fix (exact KKT active-set enumeration) made E041/E042 bit-reproducible.

## Current State

- Research phase complete (E001–E043)
- All experiment drivers committed
- Verification suite operational
- Golden baselines pinned in `ledger/golden_baseline.json`
- Data baselines pinned in `ledger/data_baseline.json`

## Next Steps for New Session

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` to confirm reproducibility
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Any new experiments must follow pre-registration protocol

---

*This handoff was created automatically at session start. Update as needed during work.*