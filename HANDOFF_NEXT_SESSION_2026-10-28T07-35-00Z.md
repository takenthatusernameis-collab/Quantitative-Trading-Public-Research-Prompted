# HANDOFF: Next Agentic Work Session

**Timestamp:** 2026-10-28T07:35:00Z
**From:** Session checkpoint `6f98068`
**To:** Next agentic work session
**Repo:** Quantitative-Trading-Public-Research-Prompted

## INITIAL TASK (Clear & Actionable)

**PRIMARY OBJECTIVE:** Verify the repository is in a clean, reproducible state and identify the highest-priority next work from the research ledger.

### Immediate Actions (Do First)

1. **Check baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Must pass all guards (goldens clean, golden baseline pinned, data coverage, JSON artifacts, portfolio optimizer tests)
   - If `check_goldens_clean.py` reports a live verification run, do **not** fail - recover first

2. **Recover if needed**
   If interrupted verification left the working tree modified:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   Or if needed: `git checkout -- experiments/` (but prefer the restore-only script)

3. **Review open items**
   Read `ledger/RESEARCH_LEDGER.md` to understand current state:
   - Research phase complete (E001–E043)
   - E041 has remaining numeric drift (133 diffs) due to ill-conditioned QP - **do not re-pin**
   - E029/E030 are now offline-reproducible
   - Check for any new open items or TODOs

### Context

- **Convention:** Close-to-close is v1.2.3 primary; overnight decomposition reported
- **Seeds:** Always use `SEED=42`
- **Golden files:** `experiments/*.json` are canonical - never modify via verification runs
- **Data:** Pinned vintages in `data/vintages.json`, fundamentals in `data/fundamentals_vintages.json`
- **Cache coverage:** Enforced invariant - all inputs must be pinned or tracked
- **Optimizer:** SLSQP status 8 is acceptable if feasible/optimal (validated on constraints)

### Success Criteria

- [ ] `scripts/check.sh` passes completely
- [ ] No stale snapshots in `.verify_snapshot/`
- [ ] Working tree clean relative to HEAD for tracked artifacts
- [ ] Clear understanding of next actionable item from ledger
- [ ] Ready to proceed with identified work

## Notes

- **Do not commit** verification outputs or modified goldens
- **Do not re-pin** artifacts to silence known numeric drift (E041) - follow ledger guidance
- If `check_golden_baseline.py` would require re-pinning, stop and understand why first
- Extended verification exists but is slow (~21-40 min) - only run if specifically needed

**Next agent:** Start with step 1 above. Report findings before taking further action.