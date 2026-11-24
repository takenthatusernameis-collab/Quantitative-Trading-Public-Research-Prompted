# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-24T04:06:19Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Phase:** Research complete (E001–E043)
**Status:** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`

---

## Quick Reference

### Reproduction Commands
```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; 18 more drivers + structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

### Individual Experiment Drivers
```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

---

## Critical Conventions (from AGENTS.md)

1. **Seed**: Always `SEED=42` (walk-forward + placebo RNG)
2. **Golden files**: `experiments/*.json` are canonical artifacts — verification overwrites then restores them
3. **Never commit verification output**: interrupted runs leave driver output in working tree; restore with `--restore-only` or `git checkout -- experiments/`
4. **Data cache**: Pinned vintages in `data/` (2026-10-12, 2026-10-11) and `data/fundamentals/` per `data/fundamentals_vintages.json`
5. **Offline reproducibility**: Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache = hard failure
6. **Baseline integrity**: `scripts/check_golden_baseline.py` compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json`; re-pinning requires ledger entry first

---

## Key Files to Know

| File | Purpose |
|------|---------|
| `ledger/RESEARCH_LEDGER.md` | Surviving validated strategies & dispositions |
| `ledger/golden_baseline.json` | SHA-256 fingerprints of canonical experiment outputs |
| `ledger/data_baseline.json` | SHA-256 fingerprints of pinned data cache files |
| `data/vintages.json` | Pinned data cache keys (2026-10-12 vintage) |
| `data/fundamentals_vintages.json` | Pinned fundamentals cache for E029 |
| `src/portfolio_opt.py` | Optimizer with exact KKT active-set (E050 fix) |
| `tests/test_portfolio_opt.py` | Validates solver answer on constraints, not exit status |

---

## Current State Notes

- **E041/E042**: Bit-reproducible since E050 exact-solver fix (commit `72dc947`); 0 differences at 2026-11-23 measurement
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned)
- **E030**: Offline-reproducible since 2026-10-20 (16-ETF panel committed)
- **Extended verification (18 drivers)**: All 0 differences as of 2026-11-23T05:17Z
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI)

---

## Suggested Next Steps

1. Run `SEED=42 python3 run_all_verification.py --skip-slow` to confirm baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion candidates
3. If adding new experiments: pre-register with falsification expectations, run drivers, verify, then commit goldens
4. For data additions: commit cache file, then `python3 scripts/check_data_coverage.py --update`

---

*This handoff was created automatically at session start. Update as work progresses.*