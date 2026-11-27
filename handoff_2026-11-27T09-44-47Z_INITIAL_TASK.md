# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T10:51:13Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Rules

- **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites and restores them.
- **Never leave verification half-finished** — run `--restore-only` if interrupted.
- **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against silent baseline replacement.
- **Data cache coverage enforced**: `scripts/check_data_coverage.py` validates all download call sites have pinned cache files.

## Current State

- All 8 quick drivers + E042 lead reproduce bit-identically (0 differences at 2026-11-23T05:17Z measurement)
- 18 extended drivers reproduce with 0 differences (numeric_tol=1e-4)
- E029 fundamentals pinned offline in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E030 16-ETF panel committed and golden re-pinned
- E041/E042 optimizer drift resolved by E050 exact active-set enumeration (commit 72dc947)

## Next Session Suggestions

1. Run `SEED=42 make check` to verify baseline integrity before any changes
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion status
3. Consider running `verify-extended` or `verify-full` for comprehensive validation
4. Check `data/vintages.json` and `data/fundamentals_vintages.json` for cache currency

## Important Files

- `AGENTS.md` — Project commands & conventions (this file's source)
- `ledger/RESEARCH_LEDGER.md` — Validated strategies and dispositions
- `ledger/golden_baseline.json` — SHA-256 fingerprints for experiment artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints for data cache files
- `scripts/check.sh` — Fast validation suite (py_compile + convention robustness + golden guards)
- `run_all_verification.py` — Full verification orchestrator