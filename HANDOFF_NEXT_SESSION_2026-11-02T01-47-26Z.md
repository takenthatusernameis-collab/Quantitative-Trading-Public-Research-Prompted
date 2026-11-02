# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-11-02T01:56:15Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** (check `git branch --show-current`)
**Status:** Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

---

## Current State (what to know)

- **Canonical artifacts:** `experiments/*.json` are the committed goldens. The verification suite backs them up/restores them; never leave a verification run half-finished.
- **Baselines pinned:** `ledger/golden_baseline.json` (SHA-256 of all tracked `experiments/*.json`) and `ledger/data_baseline.json` (cache coverage).
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). `data/vintages.json` has 2026-10-12 pinned; 2026-10-11 is committed for E026/E028/E029/E030/E034/E036/E037. E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.
- **Known drift notes (important):** E041/E042 grid can show numeric drift due to ill-conditioned QP / optimizer determinism (ledger E049). Do **not** re-pin them to silence drift. E030/E029 offline-reproducible as pinned.
- **Safety guards:** `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (working tree vs pinned SHAs) are first-class in `scripts/check.sh`.

---

## Immediate Task (start here)

1. **Verify baseline integrity (must be clean before any changes):**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - If it reports a golden mismatch: do **not** commit. Restore with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) and re-run check. If HEAD already captured a bad baseline, restore the last commit whose SHA matches `ledger/golden_baseline.json` for affected files.
   - If a stale snapshot is pending, recover it (check `.verify_snapshot/ACTIVE.json`).

2. **Understand scope before editing:** Read `AGENTS.md` (especially "Baseline Integrity" and "Reproducibility") and `ledger/RESEARCH_LEDGER.md` for context on what’s validated vs rejected.

3. **Only proceed with user-directed changes.** Do not re-run the full verification suite as a side effect to "update" goldens. If a legitimate change requires updating a golden, use `python3 scripts/check_golden_baseline.py --update` and document it in the ledger.

---

## Quick Commands

```bash
# Fast integrity check
SEED=42 bash scripts/check.sh

# Recover goldens if interrupted
SEED=42 python3 run_all_verification.py --restore-only

# Quick verification (8 drivers + batch/validate + E042 n_sim=2) - ~8 min
SEED=42 python3 run_all_verification.py

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

---

## Notes for next session
- **Do not commit verification output.** If you run verification, goldens must be restored before committing.
- **Offline by default in verification:** suite sets `QUANT_RESEARCH_OFFLINE=1`; missing pinned caches will fail hard.
- **Optimizer:** Tangency QP validation is on constraints (not solver exit status) per tests; ill-conditioning remains (see E049).
- **CI:** GitHub workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.

**Next agent:** Start with step 1 (integrity check). Only take action based on the user's actual request after confirming a clean baseline.