# Handoff - Agentic Work Session

**Timestamp:** 2026-11-17T10:53:51Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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
- **Baseline integrity:** `experiments/*.json` are canonical artifacts. The verification suite overwrites and restores them; never leave a verification run half-finished.
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`; if HEAD already carries a captured run, restore pinned artifacts via `git checkout <commit> -- experiments/<file>` per `ledger/golden_baseline.json`).
- **Golden baseline:** SHA-256 fingerprints pinned in `ledger/golden_baseline.json`. Do not re-pin as a side effect of verification.
- **Data coverage:** Enforced via `scripts/check_data_coverage.py` against `ledger/data_baseline.json`. Unpinned inputs imply live network downloads.
- **Reproducibility:** Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
- **Known open items:** E041/E042 optimizer ill-conditioning (~1e-05 drift) and E049 — do not re-pin artifacts to silence drift (see `ledger/RESEARCH_LEDGER.md`).

## Initial Task for Next Session
- [ ] Run `SEED=42 bash scripts/check.sh` and confirm a clean baseline (no golden mismatch, no stale snapshot) before making changes.
- [ ] Review `ledger/RESEARCH_LEDGER.md` open items (E041 optimizer drift, E049) and determine whether any further pre-registered confirmatory work is warranted.
- [ ] If verification is needed, run the chosen suite to completion and ensure goldens are restored (`--restore-only` if interrupted) before any commit; never commit verification output.
- [ ] Do not commit or re-pin baselines unless explicitly requested by the user.
