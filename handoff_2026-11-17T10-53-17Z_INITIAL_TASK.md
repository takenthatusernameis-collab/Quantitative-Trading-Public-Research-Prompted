# Handoff - Agentic Work Session

**Timestamp:** 2026-11-17T10:53:17Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. All experiments are pre-registered with falsification
expectations and promotion gates. Research phase complete (E001–E043). Surviving
validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Notes for Next Session
- **Baseline Integrity**: `experiments/*.json` are canonical artifacts. The
  verification suite overwrites and restores them. Never leave a verification
  run half-finished.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only`
  (or `git checkout -- experiments/`; if HEAD already carries a captured run,
  restore the pinned artifact with `git checkout <commit> -- experiments/<file>`).
- **Golden Baseline**: SHA-256 fingerprints pinned in `ledger/golden_baseline.json`.
  Never re-pin as a side effect of verification.
- **Data Coverage**: Cache coverage enforced via `scripts/check_data_coverage.py`
  against `ledger/data_baseline.json`. Unpinned inputs are live network downloads.
- **Reproducibility**: Always use `SEED=42`. Close-to-close is the v1.2.3 primary
  convention; overnight decomposition reported alongside.
- **E041/E042 Drift**: Known optimizer ill-conditioning causes ~1e-05 drift.
  Do not re-pin to silence. See ledger open items (E041 optimizer drift, E049).

## Initial Task for Next Session
- [ ] Run `SEED=42 bash scripts/check.sh` first and confirm no golden mismatch
      before touching anything (baseline integrity gate).
- [ ] Review `ledger/RESEARCH_LEDGER.md` for open items (E041 optimizer drift,
      E049) and decide whether any further confirmatory work is warranted.
- [ ] If verification is required, run the suite to completion and restore goldens
      (`--restore-only`) before any commit; never commit verification output.
- [ ] Do not commit unless explicitly asked.