# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T10:22:07Z
**Session ID:** New session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

- **Research Phase:** Complete (E001–E043)
- **Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite:** Ready for execution (see AGENTS.md for commands)

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Key Notes for Next Session

1. **Baseline Integrity:** `experiments/*.json` are canonical artifacts. Verification suite backs up and restores them. Never leave a verification run half-finished.

2. **Reproducibility:** Always use `SEED=42`. Cache coverage is enforced invariant - all data inputs must be pinned.

3. **Current State:** No active verification run. Golden artifacts are at HEAD.

4. **Open Items (from ledger):**
   - E041 optimizer determinism (133 numeric diffs remain, 1-ulp sensitivity)
   - E029 now offline-reproducible (fundamentals pinned)
   - E030 now offline-reproducible (16-ETF panel committed)

5. **CI Gate:** Template at `.github/workflow-templates/verification-gate.yml` - maintainer must create via GitHub UI.

## Next Steps (if continuing)

- Run `make check` to verify baseline integrity
- Run `make verify-quick` for quick verification
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Check `scripts/check_golden_baseline.py` if golden artifacts need re-pinning