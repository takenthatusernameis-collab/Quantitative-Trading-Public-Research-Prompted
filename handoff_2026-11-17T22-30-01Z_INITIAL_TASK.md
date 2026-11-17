# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T22:31:23Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: COMPLETE (E001–E043 executed)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

## Verification Commands (SEED=42 required for reproducibility)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
make verify-full

# Convention robustness only (reads JSONs, no writes)
make verify

# Skip slow batch/regression steps (convention only)
make verify-skip-slow

# Recover golden artifacts after interrupted verification
make verify-restore-only
```

## Key Artifacts

- **Golden baselines**: `experiments/*.json` (canonical research artifacts, must not be modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (surviving strategies with dispositions)
- **Golden baseline pins**: `ledger/golden_baseline.json` (SHA-256 fingerprints)
- **Data baseline pins**: `ledger/data_baseline.json` (SHA-256 for cached parquet)
- **Data vintages**: `data/vintages.json` (pinned 2026-10-12), `data/fundamentals_vintages.json` (E029 fundamentals)
- **Verification snapshot**: `.verify_snapshot/` (gitignored, holds backups during verification with ACTIVE.json marker)

## Critical Integrity Rules

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If killed, recover with `make verify-restore-only` or `git checkout -- experiments/`
2. **Never commit verification output** — working tree holds driver output instead of goldens when interrupted
3. **Golden baseline is authoritative** — `scripts/check_golden_baseline.py` compares against `ledger/golden_baseline.json`. Re-pinning requires explicit `--update` and shows in diff
4. **Cache coverage is enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site resolves to a committed, SHA-256-pinned parquet file
5. **Offline reproducibility** — Verification runs with `QUANT_RESEARCH_OFFLINE=1`; missing cache = hard fail

## Known Drift (Extended Verification)

- **E030**: 28 numeric diffs on near-zero quantities (was re-pinned 2026-10-20 per ledger E048)
- **E041**: 133 numeric differences (1-ulp sensitivity of ill-conditioned QP in min-var optimizer, per ledger E049). **Do not re-pin** — open item in ledger
- 15 of 18 extended drivers reproduce with 0 differences

## Dependencies

```bash
pip install -r requirements.txt  # numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional; optimizer falls back to scipy.optimize
```

## Individual Experiment Drivers (all require SEED=42)

```bash
python3 src/batch_run.py --universe large_liquid
python3 src/validate.py --universe large_liquid
python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Next Session Priority

Run `make check` to verify baseline integrity before any other work. If clean, proceed with `make verify-quick` for full verification cycle.

---

*This handoff was created automatically at session initialization.*