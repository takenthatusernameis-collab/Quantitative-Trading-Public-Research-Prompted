# Agentic Work Session Handoff

**Timestamp:** 2026-11-27T00:59:19Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

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

## Key Artifacts

- **Golden files:** `experiments/*.json` — committed artifacts, never modified by verification
- **Research ledger:** `ledger/RESEARCH_LEDGER.md` — surviving validated strategies
- **Data cache:** `data/` (gitignored except pinned vintages)
- **Verification snapshot:** `.verify_snapshot/` (gitignored, recovery mechanism)

## Important Notes

- **Seed:** Always use `SEED=42` for reproducibility
- **Golden integrity:** `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against baseline corruption
- **Cache coverage:** Enforced invariant — `scripts/check_data_coverage.py` validates all cache entries
- **Optimizer determinism:** E050 fix (exact KKT active-set enumeration) makes E041/E042 bit-reproducible
- **Do not commit verification output** — restore with `--restore-only` if interrupted

## Next Session Suggestions

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for fast verification
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Review any open issues in the ledger

---
*This handoff was created automatically at session start.*