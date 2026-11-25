# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T01:21:43Z
**Session ID**: Initial handoff for next session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

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
```

## Key Files & Directories

- `experiments/` - Canonical research artifacts (JSON files, git-tracked)
- `ledger/RESEARCH_LEDGER.md` - Documented surviving validated strategies
- `ledger/golden_baseline.json` - SHA-256 fingerprints for experiment artifacts
- `ledger/data_baseline.json` - SHA-256 fingerprints for data cache files
- `src/` - Core research modules (batch_run.py, validate.py, portfolio_opt.py, etc.)
- `data/` - Cached parquet data (gitignored except pinned vintages)
- `scripts/` - Verification and validation scripts
- `tests/` - Unit tests (including test_portfolio_opt.py)

## Critical Integrity Notes

1. **Never leave verification half-finished** - It overwrites `experiments/*.json` and restores them after. Use `--restore-only` to recover if interrupted.
2. **Golden baseline protection** - `scripts/check_golden_baseline.py` compares artifacts against pinned SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires deliberate action with `--update` flag and ledger entry.
3. **Data cache coverage** - All `data.download()` call sites must have committed cache files matching `ledger/data_baseline.json`. Unpinned inputs fail hard under `QUANT_RESEARCH_OFFLINE=1`.
4. **Seed discipline** - Always use `SEED=42` for reproducibility.
5. **Convention** - Close-to-close is v1.2.3 primary convention; overnight decomposition reported alongside.

## Recent Verification Status

- **E049 (Optimizer determinism)**: Fixed via E050 exact active-set enumeration (commit `72dc947`). E041/E042 now bit-reproducible (0 differences at 2026-11-23T05:17Z measurement).
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- **E030**: Reproduces with 0 differences since 2026-10-20 (16-ETF panel committed).
- **Extended verification**: All 18 extended drivers reproduce with 0 differences (numeric_tol=1e-4).

## Next Session Suggestions

- Run `SEED=42 python3 run_all_verification.py --extended` to verify current state
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and their status
- Review any pending items in the ledger that need follow-up
- Consider running `make check` for quick convention-robustness validation

---

*This handoff was created automatically at session initialization.*