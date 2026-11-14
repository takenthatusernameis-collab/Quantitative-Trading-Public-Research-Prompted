# Agentic Work Session Handoff

**Timestamp**: 2026-11-14T04:40:28Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: Complete (E001–E043)
**Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

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

## Key Integrity Notes

- **Golden files**: `experiments/*.json` are canonical research artifacts
- **Verification suite** overwrites them during re-run and restores afterward
- **Never leave verification half-finished** — use `--restore-only` to recover
- **Baseline integrity**: `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`
- **Cache coverage**: Enforced invariant — all data inputs must be pinned (ledger E048)

## Known Drift Items (from verification suite)

- **E030**: 28 numeric diffs on near-zero quantities (offline-reproducible since 2026-10-20)
- **E041**: 133 numeric differences (1-ulp sensitivity of ill-conditioned QP, optimizer determinism per ledger E049) — **do not re-pin**
- **E029**: Fully offline-reproducible (fundamentals pinned in `data/fundamentals/`)

## Dependencies

```bash
pip install -r requirements.txt  # numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional; falls back to scipy.optimize
```

## Next Session Guidance

1. Run `make check` first to verify baseline integrity
2. Check `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
3. Any new experiments must be pre-registered with falsification expectations
4. Sensitivity grids are "reported, not gated" — dedicated confirmatory run required for promotion
5. Negative results recorded honestly (REJECTED / PARTIAL) with evidence

---
*This handoff was created automatically at session initialization.*