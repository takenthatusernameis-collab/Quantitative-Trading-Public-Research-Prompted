# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T00:24:59Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
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

## Key Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Convention**: Close-to-close is v1.2.3 primary convention. Overnight decomposition reported alongside.

## Baseline Integrity
- Backup lives in repo-local `.verify_snapshot/` with `ACTIVE.json` marker
- `scripts/check_goldens_clean.py` fails when tracked artifact under `experiments/` differs from HEAD
- `scripts/check_golden_baseline.py` compares every tracked artifact with SHA-256 in `ledger/golden_baseline.json`
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current experiment dispositions
3. Run verification suite as needed: `make verify-quick`, `make verify-extended`, or `make verify-full`