# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T19:29:52Z
**Session ID**: Initial handoff
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Integrity Rules (Critical)

1. **Golden files**: `experiments/*.json` are canonical research artifacts. Verification suite backs them up before re-running and restores them afterward — the baseline is never modified by verification.
2. **Never commit verification output**: If a run is interrupted, the working tree holds driver output instead of goldens. Restore before committing: `run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
4. **Cache coverage**: Enforced invariant — `scripts/check_data_coverage.py` resolves every `data.download()` call site and requires cache file exists, is git-tracked, matches SHA-256 in `ledger/data_baseline.json`
5. **Golden baseline pinning**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`. Re-pinning requires deliberate ledger entry first.

## Recent Verification Status (per AGENTS.md)

- **All 18 extended drivers reproduce with 0 differences** (measured 2026-11-23T05:17Z, numpy 2.5.4, scipy 1.18.1)
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`)
- **E030**: Reproduces with 0 differences since 2026-10-20 (16-ETF panel committed)
- **E041/E042**: Bit-reproducible since E050 exact-solver fix (commit `72dc947`) — 0 differences confirmed 2026-11-23T05:17Z

## Next Session Suggested Starting Points

- Run `make check` to verify baseline integrity before any work
- Check `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
- Review any open items in the ledger (E045, E048, E049, E050 entries document reproducibility fixes)
- Verify data coverage with `python3 scripts/check_data_coverage.py`

## Environment

- Python 3 with numpy, pandas, scipy, pyarrow, statsmodels, yfinance
- cvxpy/cvxopt optional (fallback to scipy.optimize)
- Data cached in `data/` (gitignored except pinned vintages)
- Verification artifacts in `.verify_snapshot/` and `.verify_reports/` (gitignored)