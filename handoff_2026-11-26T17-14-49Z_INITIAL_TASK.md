# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T20:19:36Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates.

**Research Phase**: Complete (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

## Key Commands for Next Session

### Quick Verification (Recommended First Step)
```bash
SEED=42 bash scripts/check.sh
# or
make check
```

### Full Verification Suite
```bash
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min, E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

### Individual Experiment Commands
```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Critical Conventions

1. **Always use `SEED=42`** for reproducibility (walk-forward + placebo RNG)
2. **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward.
3. **Never commit verification output** - if a run is interrupted, restore with `run_all_verification.py --restore-only` or `git checkout -- experiments/`
4. **Data cache**: Parquet files in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Important Notes

- **Baseline Integrity**: The verification suite overwrites `experiments/*.json` while re-running drivers and restores them afterwards. A verification run must never be left half-finished.
- **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only`
- **Golden Baseline**: Compare tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json` using `scripts/check_golden_baseline.py`
- **Cache Coverage**: Enforced invariant - all `data.download()` call sites must have committed cache files matching SHA-256 in `ledger/data_baseline.json`

## Recent Context

- Extended verification (18 additional drivers) reproduces with 0 differences (measured 2026-11-23T05:17Z)
- E041/E042 ill-conditioned-QP drift resolved by E050 fix (exact KKT active-set enumeration, commit `72dc947`)
- E029 and E030 now fully offline-reproducible with pinned data (2026-10-20)
- Optimizer determinism validated: `src/portfolio_opt.py` validates solver answers on problem constraints, not solver exit status

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment and baseline integrity
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. Review any open issues or planned experiments

---
*This handoff was created automatically at session start. Update as needed during work.*