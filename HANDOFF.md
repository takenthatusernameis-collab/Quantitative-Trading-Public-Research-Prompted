# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T15:00:18Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Important Notes for Next Session

1. **Baseline Integrity**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. Never leave a verification run half-finished.

2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Golden Baseline**: Compare tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json` using `scripts/check_golden_baseline.py`

4. **Data Coverage**: Cache coverage is enforced invariant. Use `scripts/check_data_coverage.py` to verify all cache files exist and match pinned SHA-256 in `ledger/data_baseline.json`

5. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention. Data cached in `data/` (gitignored except pinned vintages).

## Current State

- Research phase: COMPLETE (E001–E043)
- Verification suite: Available and tested
- Golden artifacts: Committed in `experiments/`
- Ledger: Updated through E049 (optimizer determinism fix)

## Next Steps for New Session

1. Run `make check` to verify environment and baseline integrity
2. Run `make verify-quick` for fast verification
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Review any open items in ledger (E041/E042 grid drift, optimizer determinism)

---
*This handoff was created automatically at session start. Update as work progresses.*