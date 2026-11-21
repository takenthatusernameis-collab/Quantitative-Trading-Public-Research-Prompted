# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T08:04:49Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: Complete (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

## Quick Commands Reference

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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify
```

## Critical Integrity Notes

- **Golden artifacts**: `experiments/*.json` are canonical research artifacts
- **Verification suite** backs up and restores goldens automatically — never leave a run half-finished
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Baseline integrity**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`
- **Data coverage**: Enforced invariant — all `data.download()` call sites must have committed, SHA-256-pinned cache files (see `ledger/data_baseline.json`)

## Key Files to Understand

- `AGENTS.md` — Project commands, conventions, reproducibility rules
- `ledger/RESEARCH_LEDGER.md` — Surviving validated strategies documentation
- `ledger/golden_baseline.json` — SHA-256 pinned artifact fingerprints
- `ledger/data_baseline.json` — SHA-256 pinned data cache fingerprints
- `scripts/check.sh` — Fast convention-robustness check (first-class gate)
- `run_all_verification.py` — Main verification orchestrator

## Reproducibility Requirements

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Offline mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1`
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Next Session Suggestions

1. Run `make check` to verify baseline integrity before any changes
2. Review `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Check `scripts/check_goldens_clean.py` output for any working tree vs HEAD mismatches
4. Consider running `make verify-quick` for a full reproduction check

---

*This handoff was created automatically at session start. Update as needed during work.*