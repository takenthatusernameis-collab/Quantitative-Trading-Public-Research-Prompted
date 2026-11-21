# Agentic Work Session Handoff

**Timestamp:** 2026-11-21T22:05:54Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase:** COMPLETE (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
```

## Critical Notes

1. **Baseline Integrity:** `experiments/*.json` are canonical research artifacts. Verification overwrites them temporarily and restores after. Never leave a verification run half-finished.
2. **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Golden Baseline:** Compare with `ledger/golden_baseline.json` SHA-256 fingerprints via `scripts/check_golden_baseline.py`
4. **Data Cache:** Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029). Cache coverage enforced by `scripts/check_data_coverage.py`.
5. **Reproducibility:** Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
6. **No CI Workflow Creation:** `.github/workflows/` managed by controller; maintainer must create via GitHub UI.

## Key Files

- `ledger/RESEARCH_LEDGER.md` — Surviving strategies & dispositions
- `ledger/golden_baseline.json` — Pinned SHA-256 fingerprints
- `ledger/data_baseline.json` — Pinned data cache fingerprints
- `experiments/*.json` — Canonical experiment artifacts (git-tracked)
- `scripts/check.sh` — Fast convention check (first-class gate)
- `run_all_verification.py` — Full verification orchestrator

---

**Next Session:** Resume from this context. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions before planning new work.