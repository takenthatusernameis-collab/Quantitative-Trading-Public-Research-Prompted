# Handoff — 2026-11-08T20:53:40Z

## Project State
- **Research phase**: Complete (E001–E043)
- **Validated strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Baseline artifacts**: `experiments/*.json` (canonical, pinned in `ledger/golden_baseline.json`)
- **Data cache**: Pinned vintages 2026-10-12 (`data/vintages.json`) and 2026-10-11 (committed for specific experiments)

## Quick Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh
# or: make check

# Quick verification (~8 min; 8 drivers)
SEED=42 python3 run_all_verification.py
# or: make verify-quick

# Extended verification (~21 min; 26 drivers + structural match)
SEED=42 python3 run_all_verification.py --extended
# or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
# or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or: make verify

# Individual drivers
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

## Critical Rules (Read Before Running)
1. **Never leave verification half-finished** — it backs up goldens to `.verify_snapshot/` and restores after; interrupted run = working tree holds driver output, not goldens. Recover with `--restore-only` or `git checkout -- experiments/`.
2. **Golden mismatch in `scripts/check.sh`** → fix before committing. A checkpoint commit capturing verification output silently replaces canonical baseline (has happened 4×, all reverted).
3. **`scripts/check_golden_baseline.py`** guards against committed baseline replacement — compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json`. Re-pin only via `--update` with intent.
4. **Cache coverage invariant** — every `data.download()` call site must have committed parquet matching `ledger/data_baseline.json`. Unpinned input = live yfinance download (not bit-reproducible). Add data: commit file + `python3 scripts/check_data_coverage.py --update`.
5. **Optimizer determinism** (ledger E049): `src/portfolio_opt.py` validates on problem constraints, not solver exit status. Tangency QP is ill-conditioned; 1-ulp input drift → ~1e-05 weight drift. Do not re-pin E041/E042 grid artifacts to silence this.

## Extended Verification Drift Notes (2026-10-20)
- 15/18 extended drivers reproduce with 0 differences
- E030: 28 numeric diffs on near-zero quantities (was re-pinned to committed 16-ETF panel)
- E041: 133 numeric diffs (1-ulp ill-conditioned QP sensitivity), 0 structural diffs (3 fixed in optimizer). **Do not re-pin** — open ledger item.

## Next Session — Initial Task
Run `make verify-quick` to confirm baseline integrity. If all green, review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items, then check `scripts/check.sh` output for golden mismatches or coverage gaps before committing anything.
