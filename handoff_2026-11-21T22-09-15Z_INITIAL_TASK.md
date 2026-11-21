# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T22:09:15Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status Summary

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. **Research phase is complete.**

### Key Artifacts
- **Ledger**: `ledger/RESEARCH_LEDGER.md` - Documents surviving validated strategies
- **Golden Baselines**: `experiments/*.json` - Canonical research artifacts (committed)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Verification Suite**: `run_all_verification.py` with multiple modes

### Quick Commands
```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

### Important Notes
- **Never leave a verification run half-finished** - it overwrites `experiments/*.json` and restores them after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline integrity enforced by `scripts/check_golden_baseline.py` against `ledger/golden_baseline.json`
- Data cache coverage enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`
- Convention: Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- Seed: Always use `SEED=42` for reproducibility

### Known Drift (Extended Verification)
- E030: 28 numeric diffs on near-zero quantities (reproduces with 0 diffs since 2026-10-20 after pinning)
- E041: 133 numeric diffs (1-ulp sensitivity of ill-conditioned QP), 3 structural diffs resolved - **do not re-pin**
- E042 grid artifacts: 29-133 differences from same ill-conditioned QP - **do not re-pin**
- See ledger entries E045, E048, E049 for details

### Next Session Suggestions
1. Run `SEED=42 bash scripts/check.sh` to verify environment health
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. If continuing verification: choose appropriate tier (quick/extended/full)
4. Any new experiments require pre-registration with falsification expectations