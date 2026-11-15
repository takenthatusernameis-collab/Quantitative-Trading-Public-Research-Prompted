# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-15T00:25:50Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Phase:** Research complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baseline)
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages)

## Key Commands

```bash
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

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or
make verify

# Restore golden artifacts after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores on completion. Use `--restore-only` if interrupted.
2. **Golden baseline integrity** — `scripts/check_golden_baseline.py` compares artifacts against SHA-256 fingerprints in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
3. **Cache coverage invariant** — Every `data.download()` call site must have a committed, SHA-256-pinned cache file (see `ledger/data_baseline.json`).
4. **E041 known drift** — 133 numeric differences (1-ulp QP sensitivity). Do not re-pin — see ledger open item.
5. **CI gate** — Template at `.github/workflow-templates/verification-gate.yml`; maintainer must create actual workflow via GitHub UI.

## Next Steps (if any)

- Run `make check` to verify convention robustness before any changes
- Consult `ledger/RESEARCH_LEDGER.md` for surviving strategy dispositions
- Check `ledger/golden_baseline.json` and `ledger/data_baseline.json` for pinned references

---

*This handoff was created automatically at session start.*