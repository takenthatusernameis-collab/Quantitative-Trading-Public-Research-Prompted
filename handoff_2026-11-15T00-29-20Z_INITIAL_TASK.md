# Agentic Work Session Handoff

**Timestamp:** 2026-11-15T00:31:02Z
**Session ID:** Initial handoff for next agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase:** COMPLETE (Experiments E001–E043)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite:** Operational with multiple tiers (check, verify-quick, verify-extended, verify-full)

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
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

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Baseline Integrity Notes

1. **`experiments/*.json`** are canonical research artifacts - verification suite overwrites and restores them
2. **Never leave a verification run half-finished** - use `--restore-only` to recover if interrupted
3. **Golden baseline** pinned in `ledger/golden_baseline.json` - compare with `scripts/check_golden_baseline.py`
4. **Data cache coverage** enforced via `scripts/check_data_coverage.py` - all inputs must be pinned
5. **Do not commit verification output** - restore goldens before committing

## Reproducibility Requirements

- **Seed:** Always use `SEED=42`
- **Convention:** Close-to-close v1.2.3 primary, overnight decomposition reported alongside
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Known Drift Items (from ledger)

- **E030:** 28 numeric diffs on near-zero quantities (reproduces with 0 diffs since 2026-10-20, ledger E048)
- **E041:** 133 numeric differences (1-ulp sensitivity of ill-conditioned QP, optimizer determinism fixed in ledger E049, but still exceeds 1e-4 tolerance)
- **E042/E041 grid artifacts:** Drift by 29-133 differences due to ill-conditioned tangency QP
- **Do NOT re-pin** E041/E042 to silence drift - see open items in ledger

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Review any open items in ledger (E049 optimizer determinism, E041/E042 drift)
4. Determine if new experiments or verification runs are needed

## Environment

- Python 3 research repository
- No separate linter configured (uses py_compile + reproducibility checks)
- CI gate template at `.github/workflow-templates/verification-gate.yml` (maintainer must create actual workflow)

---

*This handoff was created automatically at session initialization. Update as work progresses.*