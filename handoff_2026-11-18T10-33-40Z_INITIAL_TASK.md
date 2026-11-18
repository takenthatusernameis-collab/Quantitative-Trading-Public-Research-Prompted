# Handoff — Agentic Work Session

**Timestamp:** 2026-11-18T11:26:34Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Current State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

## Quick Commands Reference

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --skip-slow

# Extended verification (~21 min; structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Key Artifacts

- **Golden baselines:** `experiments/*.json` (canonical research artifacts)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (validated strategies + dispositions)
- **Golden baseline pins:** `ledger/golden_baseline.json` (SHA-256 fingerprints)
- **Data baseline pins:** `ledger/data_baseline.json` (cache file SHA-256s)
- **Data vintages:** `data/vintages.json`, `data/fundamentals_vintages.json`

## Important Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only`
2. **Seed is always 42** for reproducibility (walk-forward + placebo RNG)
3. **Cache coverage is enforced invariant** — all data downloads must be pinned (see `scripts/check_data_coverage.py`)
4. **E029, E030 now offline-reproducible** (pinned data committed 2026-10-20)
5. **E041 optimizer determinism fixed** (ledger E049) — remaining 133 numeric diffs are 1-ulp ill-conditioned QP sensitivity, do not re-pin

## Next Steps (if continuing)

- Run `SEED=42 python3 run_all_verification.py --extended` to verify all 26 committed drivers
- Check `ledger/RESEARCH_LEDGER.md` for open items (E041/E042 grid drift, E042 confirmatory)
- Consider adding CI gate via `.github/workflow-templates/verification-gate.yml` (maintainer action required)