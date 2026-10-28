# HANDOFF_NEXT_SESSION_2026-10-28T12-27-48Z.md

**Timestamp:** 2026-10-28T12:27:48Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** Current working tree state at time of handoff
**Environment:** Linux, git repo

## Initial Task (For Next Agent)

**Objective:** Verify repository integrity and establish a clean baseline before proceeding with any new work.

### Steps (in order)
1. **Check for uncommitted changes**
   ```bash
   git status --short
   ```
   Ensure no unintended modifications exist, especially under `experiments/`. If verification artifacts were left behind from a previous run, restore them before committing.

2. **Run baseline integrity checks**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs golden-clean checks, baseline fingerprint validation, convention robustness, and py_compile. All must pass.

3. **Confirm ledger state**
   Read `ledger/RESEARCH_LEDGER.md` to confirm the current state (research phase is complete E001–E043; surviving strategies documented). Treat committed `experiments/*.json` and `ledger/golden_baseline.json` as the authoritative record.

4. **Only proceed if clean**
   If `scripts/check.sh` reports a golden mismatch or pending snapshot, restore first:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   Do not re-pin goldens as a side effect of verification runs. If a committed artifact appears modified, compare against HEAD and the ledger before taking action.

## Quick Reference
- **Fast check:** `SEED=42 bash scripts/check.sh`
- **Quick verify (~8 min):** `SEED=42 python3 run_all_verification.py`
- **Extended verify (~21 min):** `SEED=42 python3 run_all_verification.py --extended`
- **Full verify (~15 min):** `SEED=42 python3 run_all_verification.py --full`
- **Restore goldens:** `SEED=42 python3 run_all_verification.py --restore-only`

## Notes
- Always use `SEED=42` for reproducibility.
- `experiments/*.json` are canonical artifacts - never leave a verification run half-finished.
- Data caches: see `ledger/data_baseline.json` and `data/vintages.json` (some vintages are pinned).
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.
- Follow all conventions in `AGENTS.md` strictly.