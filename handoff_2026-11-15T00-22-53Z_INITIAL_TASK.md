# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T00:24:32Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043)**. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Critical Notes for Next Session

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them while re-running drivers and restores them afterwards. A verification run must never be left half-finished.

2. **Recovery**: If a run is interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` to restore golden artifacts.

3. **Golden Baseline**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints pinned in `ledger/golden_baseline.json`. Never re-pin as a side effect of running verification.

4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant - `scripts/check_data_coverage.py` validates every download call site.

5. **Reproducibility**: Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention. Overnight decomposition reported alongside.

## Next Steps for New Session

- Run `make check` to verify current state
- Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
- Check if any experiments need re-running or validation
- Verify data cache coverage with `python3 scripts/check_data_coverage.py`

## Key Files to Review

- `AGENTS.md` - Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies documentation
- `ledger/golden_baseline.json` - SHA-256 fingerprints for golden artifacts
- `data/vintages.json` - Pinned data vintages
- `data/fundamentals_vintages.json` - Pinned fundamentals snapshots