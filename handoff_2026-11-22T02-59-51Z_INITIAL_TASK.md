# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-22T03:01:27Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase:** Complete (E001–E043)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

## Quick Commands Reference

```bash
# Fast convention-robustness check + template validation
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

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Critical Notes

1. **Golden files** in `experiments/*.json` are canonical artifacts — verification suite backs them up and restores after re-running
2. **Never leave verification half-finished** — use `--restore-only` to recover if interrupted
3. **Data cache coverage is enforced** — `scripts/check_data_coverage.py` validates all download call sites
4. **Seed must be 42** for reproducibility (walk-forward + placebo RNG)
5. **E041/E042 optimizer drift** is known (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin to silence

## Key Files to Review

- `AGENTS.md` — Project commands & conventions
- `ledger/RESEARCH_LEDGER.md` — Surviving validated strategies
- `ledger/golden_baseline.json` — SHA-256 fingerprints of golden artifacts
- `data/vintages.json` — Pinned data vintages
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot

## Next Steps (if any)

[No specific task assigned — this is a clean handoff for the next session]

---

*Generated automatically at session start*