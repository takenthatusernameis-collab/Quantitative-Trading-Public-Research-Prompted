# Agentic Work Session Handoff

**Timestamp:** 2026-11-11T07:27:52Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

- **Research Phase:** Complete (E001–E043)
- **Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden Artifacts:** Committed in `experiments/*.json` (canonical research artifacts)

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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify
```

## Critical Integrity Notes

1. **Golden files** in `experiments/*.json` are canonical — verification suite backs them up, re-runs drivers, and restores them. Never leave a verification run half-finished.

2. **Recovery:** If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Cache coverage** is an enforced invariant (ledger E048). All data inputs must be pinned in `ledger/data_baseline.json` and committed.

4. **Optimizer determinism** (ledger E049): `src/portfolio_opt.py` validates on problem constraints, not solver exit status. E041/E042 grid artifacts drift due to 1-ulp sensitivity of ill-conditioned QP — do NOT re-pin to silence this.

5. **CI gate** cannot be created by automated agents — maintainer must create `.github/workflows/verification-gate.yml` via GitHub UI using template at `.github/workflow-templates/verification-gate.yml`

## Key Files to Reference

- `ledger/RESEARCH_LEDGER.md` — Surviving validated strategies
- `ledger/golden_baseline.json` — SHA-256 fingerprints for golden artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints for data cache
- `data/vintages.json` — Pinned data vintage (2026-10-12)
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot
- `scripts/check_golden_baseline.py` — Compares tracked artifacts to pinned SHA-256
- `scripts/check_data_coverage.py` — Enforces cache coverage invariant

## Next Session Suggestions

- Run `make check` to verify baseline integrity before any work
- Review `ledger/RESEARCH_LEDGER.md` for open items (E041 optimizer drift, E042 sensitivity grid)
- Consider running `make verify-quick` to confirm reproducibility