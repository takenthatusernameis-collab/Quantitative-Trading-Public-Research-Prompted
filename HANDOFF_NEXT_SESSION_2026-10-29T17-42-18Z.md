# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T17:42:18Z
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification baseline integrity guards in place.

## Initial Task (Start Here)

**Goal:** Establish a clean, verified baseline before making any changes.

### Steps

1. **Check repo state**
   ```bash
   git status --short && git log --oneline -3
   ```

2. **Run fast integrity checks**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Validates goldens vs HEAD, checks for stale snapshots, runs convention robustness, py_compile, etc.
   - If this fails due to golden/snapshot issues, follow the "Baseline Integrity" section in `AGENTS.md` before proceeding.

3. **Run quick verification (if checks pass)**
   ```bash
   SEED=42 python3 run_all_verification.py
   # or: make verify-quick
   ```
   - ~8 min; re-runs the 8-driver quick block and restores canonical baselines.
   - **Do not commit** verification output. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

4. **Report status**
   - Summarize `check.sh` and `verify-quick` results
   - Review `ledger/RESEARCH_LEDGER.md` for any open items (notably E049 optimizer determinism / drift notes)
   - Only proceed with new work after baseline is confirmed clean

## Prerequisites

- Dependencies installed: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- Working tree in a recoverable state (no stale verification snapshots)
- `SEED=42` set for all verification commands

## Success Criteria

- `scripts/check.sh` passes with no golden/snapshot mismatches
- `run_all_verification.py` (verify-quick) completes successfully and restores `experiments/*.json` to committed baselines
- No uncommitted modifications to tracked artifacts under `experiments/` resulting from verification
- Clear status summary documented before starting new work

## Important Notes

- **Baseline integrity:** The verification suite backs up and restores `experiments/*.json`. Leaving a run half-finished corrupts working tree state. Stale snapshots are tracked in `.verify_snapshot/ACTIVE.json`.
- **Do not re-pin goldens:** Numeric drift in ill-conditioned QPs is expected (see ledger E049). Only re-pin via `scripts/check_golden_baseline.py --update` with explicit justification.
- **Cache coverage:** Enforced by `scripts/check_data_coverage.py`. Missing/unpinned caches will fail under offline mode (`QUANT_RESEARCH_OFFLINE=1`).
- **CI:** GitHub workflow cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml` with instructions in `VERIFICATION_GATE_TEMPLATE.md`.
- **Golden safety:** If `check.sh` reports a golden mismatch, do **not** just `git checkout -- experiments/` blindly if HEAD was recently modified — restore from the commit matching `ledger/golden_baseline.json` instead.

## Key References

- `AGENTS.md` - Commands, conventions, baseline integrity rules
- `ledger/RESEARCH_LEDGER.md` - Experiment history and disposition (E001–E043 complete)
- `ledger/golden_baseline.json` - Pinned golden fingerprints
- `ledger/data_baseline.json` - Pinned data cache fingerprints
- `scripts/check.sh` - Fast integrity gate
- `run_all_verification.py` - Full verification orchestrator
