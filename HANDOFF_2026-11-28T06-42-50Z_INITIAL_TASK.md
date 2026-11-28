# Agentic Work Session Handoff

**Timestamp**: 2026-11-28T07:34:14Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Surviving Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden Artifacts**: `experiments/*.json` (canonical baselines, pinned in `ledger/golden_baseline.json`)
- **Data Cache**: `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages)
- **E029 Fundamentals**: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

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

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or
   git checkout -- experiments/
   ```

2. **Golden baseline protection**: `scripts/check_golden_baseline.py` compares artifacts to SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires deliberate ledger entry.

3. **Cache coverage invariant**: `scripts/check_data_coverage.py` enforces all driver data inputs are pinned. Unpinned = hard fail in offline mode.

4. **Optimizer determinacy**: `src/portfolio_opt.py` validates on constraints, not solver status. E050 exact active-set enumeration makes E041/E042 bit-reproducible.

## Next Session Guidance

- Run `make check` first to verify environment integrity
- Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
- All experiments are pre-registered; no goalpost moving
- Negative results (REJECTED/PARTIAL) are recorded honestly