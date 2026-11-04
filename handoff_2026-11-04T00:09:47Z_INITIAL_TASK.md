# Durable Handoff

**Timestamp:** 2026-11-04T01:09:23Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Workspace:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task for Next Agentic Session

**Objective:** Verify baseline integrity and ensure reproducibility of committed research artifacts.

### Steps
1. **Quick sanity check (baseline integrity):**
   `SEED=42 bash scripts/check.sh`
   - Must pass `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, and tests.
2. **Run verification (choose level):**
   - If time-limited: `SEED=42 python3 run_all_verification.py --quick`
   - If full confidence needed: `SEED=42 python3 run_all_verification.py --full`
3. **Review results:** Check for drift vs committed goldens. Note known issues (e.g., E041 optimizer drift per ledger).
4. **Commit policy:** Do **NOT** commit verification outputs. If interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only`.

### Context
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification overwrites/restores `experiments/*.json` via `.verify_snapshot/` (pid-tracked, recoverable).
- Data coverage enforced; suite runs drivers in offline mode.
- Golden baseline pinned in `ledger/golden_baseline.json`.

### Success Criteria
- `scripts/check.sh` passes cleanly.
- Verification completes without baseline contamination.
- Any material anomalies documented in `ledger/` with evidence.

## Notes from This Session
- Created this durable handoff at 2026-11-04T01:09:23Z.
