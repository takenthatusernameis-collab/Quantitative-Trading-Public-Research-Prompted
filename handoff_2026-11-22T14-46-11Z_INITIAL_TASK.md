# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T14:46:24Z
**Session**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Notes

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are committed artifacts. Verification suite backs them up before re-running and restores them afterward.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.
- **Recovery**: If verification is interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` to recover golden artifacts.

## Next Steps for New Session

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for quick verification
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Check `scripts/check_golden_baseline.py` and `scripts/check_data_coverage.py` for any drift

## Active Concerns

- E041 shows numeric drift (133 differences) due to ill-conditioned QP in optimizer — do NOT re-pin to silence
- E030 now reproduces with 0 differences (pinned panel)
- E029 is fully offline-reproducible (pinned fundamentals snapshot)
- Optimizer determinism validated by `tests/test_portfolio_opt.py` — solver exit status is NOT gated