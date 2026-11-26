# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T23:55:33Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

- **Research Phase**: Complete (experiments E001–E043)
- **Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite**: Operational with multiple tiers (check, verify-quick, verify-extended, verify-full)

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Individual experiment drivers
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Critical Conventions

1. **Always use `SEED=42`** for reproducibility (walk-forward + placebo RNG)
2. **Golden files**: `experiments/*.json` are canonical artifacts — never commit verification output
3. **Recovery**: If verification interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
4. **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`
5. **Cache coverage invariant**: All driver data downloads must be cached and SHA-256 pinned

## Important Files

- `ledger/RESEARCH_LEDGER.md` — Surviving strategies and dispositions
- `ledger/golden_baseline.json` — SHA-256 fingerprints of canonical artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of cached data inputs
- `scripts/check_golden_baseline.py` — Validates artifacts against pinned hashes
- `scripts/check_data_coverage.py` — Enforces cache coverage invariant
- `.github/workflow-templates/verification-gate.yml` — CI template (maintainer must create via GitHub UI)

## Next Session Suggestions

- Run `make check` to verify baseline integrity before any changes
- Consult `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
- Any new experiments require pre-registration with falsification expectations
- Negative results (REJECTED/PARTIAL) must be recorded honestly with evidence