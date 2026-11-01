# Handoff: Next Agentic Work Session

**Timestamp (UTC):** 2026-11-01T08:15:35Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Current State

- **Canonical artifacts:** `experiments/*.json` are committed goldens. The verification suite backs them up to `.verify_snapshot/` and restores them after runs. Never leave a verification run half-finished.
- **Integrity guards (active):** `scripts/check_goldens_clean.py` (working tree vs HEAD), `scripts/check_golden_baseline.py` (artifacts vs `ledger/golden_baseline.json` fingerprints), and `scripts/check_data_coverage.py` (all data inputs pinned and git-tracked).
- **Data coverage:** All driver inputs must be pinned. E029 fundamentals are pinned in `data/fundamentals/`, E029/E030 are offline-reproducible. The suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Known open items:** E041 still shows numeric drift (133 differences) due to ill-conditioned QP / solver sensitivity despite the optimizer determinism fix (E049). The three structural differences are resolved. **Do not re-pin baselines to silence this drift.** See `ledger/RESEARCH_LEDGER.md` for details.
- **CI:** The intended GitHub workflow cannot be created by agents (template in `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## Clear Initial Task (Priority Order)

1. **Verify baseline integrity (must do first)**
   - Run: `SEED=42 bash scripts/check.sh`
   - Expected: convention-robustness check, template validation, golden clean check, golden baseline fingerprint check, and data coverage all pass. If any guard reports a mismatch, follow recovery steps in `AGENTS.md` before making changes.

2. **Run quick verification**
   - Run: `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
   - Expected: re-runs the 8 quick drivers and compares to goldens. Ensure clean pass. If interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only`.

3. **Review open ledger items**
   - Read `ledger/RESEARCH_LEDGER.md` focusing on E041/E049 and any items marked open. Understand constraints before proposing changes. Do not re-pin `experiments/e041_*.json` or other drifted artifacts as a side effect of verification.

4. **Sanity check data coverage**
   - Run: `python3 scripts/check_data_coverage.py`
   - Expected: all resolved data files exist, are git-tracked, and match `ledger/data_baseline.json`. If adding new data inputs, commit the file and re-pin with `python3 scripts/check_data_coverage.py --update` (intentional only).

5. **Only proceed to new work if all of the above are green.** If integrity issues exist, fix them first. Do not commit verification output.

## Constraints & Reminders

- **Always use `SEED=42`** for all runs.
- **Never re-pin baselines** as a side effect of running the verification suite. Re-pinning requires explicit `--update` flags and a reviewed diff.
- **Recovery:** If working tree has modified `experiments/*.json` unexpectedly, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. If HEAD already contains a captured run, restore the pinned artifact from the commit that matches `ledger/golden_baseline.json`.
- **Offline mode:** Verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`. Do not introduce live network dependencies without pinning data.
- **Optimizer determinism:** Follow the rule in `AGENTS.md` — validate solver answers against problem constraints, not solver exit status.
- **No auto-created CI:** Do not attempt to create `.github/workflows/verification-gate.yml`; use local equivalents.

## Quick Command Reference

```bash
# Integrity + guards
SEED=42 bash scripts/check.sh

# Verification
SEED=42 python3 run_all_verification.py                # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended     # extended (~21 min)
SEED=42 python3 run_all_verification.py --full         # full (~15 min)
SEED=42 python3 run_all_verification.py --skip-slow    # convention only
SEED=42 python3 run_all_verification.py --restore-only # recover goldens

# Guards
python3 scripts/check_goldens_clean.py
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_golden_baseline.py --update      # only if intentionally re-pinning
python3 scripts/check_data_coverage.py --update        # only if intentionally adding data
```

## Files to Read First

- `AGENTS.md` — full project conventions, guards, and recovery procedures
- `ledger/RESEARCH_LEDGER.md` — experiment history, decisions, and open items
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` — pinned fingerprints

**End of handoff. Start at step 1.**