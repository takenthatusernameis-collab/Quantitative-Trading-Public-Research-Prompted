# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T04:51:17Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State Summary

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden Artifacts**: `experiments/*.json` (canonical baseline)
- **Data Vintages**:
  - 2026-10-12 pinned in `data/vintages.json`
  - 2026-10-11 committed (E026/E028/E029/E030/E034/E036/E037)
  - E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Verification Commands

```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Notes for Next Session

1. **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores them after. Use `--restore-only` if interrupted.
2. **Golden baseline integrity** - `scripts/check_golden_baseline.py` compares against SHA-256 in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
3. **Cache coverage invariant** - `scripts/check_data_coverage.py` enforces all data inputs are pinned. Run with `--update` only when deliberately adding data.
4. **E041/E042 optimizer** - Fixed by E050 (exact KKT active-set enumeration, commit `72dc947`). Artifacts are now bit-reproducible (0 differences measured 2026-11-23T05:17Z).
5. **CI workflow** - Cannot be created by agents (controller restores `.github/workflows/`). Template at `.github/workflow-templates/verification-gate.yml`.

## Reproducibility

- **Seed**: Always `SEED=42`
- **Convention**: Close-to-close v1.2.3 primary, overnight decomposition reported alongside
- **Dependencies**: `pip install -r requirements.txt` (cvxpy/cvxopt optional)

## Next Steps (if any)

[Add specific tasks or context for the next session here]