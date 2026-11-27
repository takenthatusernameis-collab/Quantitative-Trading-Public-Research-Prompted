# Agentic Work Session Handoff

**Timestamp:** 2026-11-27T00:59:46Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts

- **Golden files:** `experiments/*.json`
- **Research ledger:** `ledger/RESEARCH_LEDGER.md`
- **Data cache:** `data/`
- **Verification snapshot:** `.verify_snapshot/`

## Important Notes

- **Seed:** Always use `SEED=42`
- **Golden integrity:** `scripts/check_goldens_clean.py` / `scripts/check_golden_baseline.py`
- **Cache coverage:** `scripts/check_data_coverage.py`
- **Do not commit verification output** — restore with `--restore-only`

## Next Session Suggestions

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for fast verification
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Review any open issues in the ledger

---
*This handoff was created automatically at session start.*
