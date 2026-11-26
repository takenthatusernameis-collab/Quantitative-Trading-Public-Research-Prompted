# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T17:06:39Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Artifacts

- **Golden files**: `experiments/*.json` — canonical research artifacts (never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` — validated strategies and dispositions
- **Data cache**: `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12)
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Verification Integrity Notes

- Verification suite backs up goldens to `.verify_snapshot/` with `ACTIVE.json` marker (pid)
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_goldens_clean.py` compares working tree vs HEAD (step in `scripts/check.sh`)
- `scripts/check_golden_baseline.py` compares tracked artifacts vs pinned SHA-256 in `ledger/golden_baseline.json`
- Never re-pin to silence tolerance violations — only for deliberate code changes recorded in ledger

## Reproducibility

- **Seed**: Always `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close primary (v1.2.3), overnight decomposition reported alongside
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Optimizer**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049)
- **E050 fix**: Exact KKT active-set enumeration for tangency QP — bit-reproducible across environments

## Next Session Suggestions

1. Run `make check` to verify baseline integrity before any changes
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategy statuses
3. Consider extended/full verification if modifying experiment drivers
4. Check `data/vintages.json` and `data/fundamentals_vintages.json` for data coverage

## Handoff Context

This handoff was created at the start of a new agentic work session. The project is in a verified state with all goldens matching `ledger/golden_baseline.json`. No active verification run is in progress (no `.verify_snapshot/ACTIVE.json` present).