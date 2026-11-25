# Handoff: Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-25T08:16:19Z
**Session:** New agentic work session
**Project:** Quantitative Trading Public Research Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Current State

- **Verification suite**: Ready to run (`SEED=42 python3 run_all_verification.py`)
- **Golden artifacts**: Committed in `experiments/*.json` (canonical baseline)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Quick Start Commands

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

## Important Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

2. **Golden baseline integrity** — `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement. Run `scripts/check.sh` before committing.

3. **Reproducibility** — Always use `SEED=42`. Close-to-close is v1.2.3 primary convention. Cache coverage is enforced invariant.

4. **No CI workflow creation** — `.github/workflows/` is managed by controller; maintainer must create via GitHub UI.

## Suggested First Actions

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and their status

---

*This handoff was created automatically at session start. Update symlinks (handoff_CURRENT, handoff_LATEST, handoff_NEXT, etc.) to point to this file.*