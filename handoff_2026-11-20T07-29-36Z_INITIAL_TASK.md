# Agentic Work Session Handoff

**Timestamp**: 2026-11-20T07:34:33Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: COMPLETE (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates
- Negative results recorded honestly (REJECTED / PARTIAL) with evidence

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

## Critical Reproducibility Notes

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts — verification backs them up before re-running and restores them afterward
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- **E029 fundamentals**: Separately pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — offline-reproducible when SEED is set
- **Cache coverage**: Enforced invariant — `scripts/check_data_coverage.py` requires every `data.download()` call site to have a committed, SHA-256 pinned cache file
- **Never commit verification output**: If a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`

## Key Files to Understand

- `AGENTS.md` — Project commands, conventions, and verification details
- `ledger/RESEARCH_LEDGER.md` — Surviving validated strategies and dispositions
- `ledger/golden_baseline.json` — SHA-256 fingerprints of canonical experiment artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data cache files
- `scripts/check.sh` — Fast convention-robustness check (first-class CI step)
- `src/portfolio_opt.py` — Optimizer with determinism rule (validates on constraints, not solver exit status)
- `tests/test_portfolio_opt.py` — Pins optimizer determinism rule

## Known Drift Items (from extended verification)

- **E030**: 28 numeric diffs on near-zero quantities (was re-pinned 2026-10-20, now reproduces with 0 diffs)
- **E041**: 133 numeric differences (1-ulp sensitivity of ill-conditioned QP), 3 structural diffs resolved — DO NOT re-pin (see ledger open item)
- **E042**: Grid artifacts still drift by 29-133 differences due to ill-conditioned tangency QP — DO NOT re-pin

## Next Session Suggestions

1. Run `make check` to verify current state
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
3. Consider running `make verify-quick` if changes were made
4. Check for any unpinned data dependencies with `python3 scripts/check_data_coverage.py`