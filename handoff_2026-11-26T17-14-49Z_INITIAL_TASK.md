# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T18:16:51Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands

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

## Critical Notes

- **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite overwrites them during runs and restores afterward — never leave a verification run half-finished.
- **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Baseline integrity**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
- **Data cache**: Pinned vintages in `data/vintages.json` (2026-10-12) and committed 2026-10-11 vintage. E029 fundamentals pinned separately in `data/fundamentals/`.
- **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

## Recent Context

- E050 fix (commit `72dc947`): Exact KKT active-set enumeration as primary tangency solver — made E041/E042 artifacts bit-reproducible (0 differences at 2026-11-23T05:17Z measurement)
- Cache coverage enforced invariant (ledger E048): all `data.download()` call sites must have committed, SHA-256 pinned cache files
- Optimizer determinism rule pinned by `tests/test_portfolio_opt.py` (validates on constraints, not solver exit status)

## Next Session Suggestions

1. Run `make check` to verify baseline integrity before any changes
2. If continuing research, check `ledger/RESEARCH_LEDGER.md` for surviving strategies and next experiment ideas
3. If modifying code, run relevant verification tier after changes