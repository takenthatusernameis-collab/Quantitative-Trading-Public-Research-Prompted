# INITIAL TASK HANDOFF
**Timestamp (UTC):** 2026-11-04T09:57:06Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State
- **Research phase:** COMPLETE (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Portfolio construction:** E042 (confirmatory min-variance market-neutral blend) returned PARTIAL (4/5). G2 (β-constrained placebo z=2.11 < 3.0) failed → **market-neutral total portfolio line is CLOSED**. No blend of the 5 validated components is simultaneously market-neutral and placebo-significant on the free public data surface.
- **Validated components (surviving):** equity TSM flagship (β-bearing), DN low-beta sort, futures TSM 18m, futures realized-roll-yield carry, macro momentum.
- **Verification posture:** Baseline integrity is enforced (snapshot mechanism in `.verify_snapshot/` with `ACTIVE.json`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`). Convention is **close-to-close primary (v1.2.3)**. Always use `SEED=42`.

## Immediate Priorities (Do First)
1. **Verify cleanliness** - Ensure no interrupted verification run is pending.
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If it reports a golden mismatch or a stale snapshot, recover first (see #2). Do not commit while artifacts are out of sync with HEAD/ledger.

2. **Recover if interrupted** - If a previous verification run was killed mid-way:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   Or manually `git checkout -- experiments/`. Never leave a verification run half-finished.

3. **Respect guardrails** - Before any changes:
   - **Never re-pin goldens to silence numeric drift.** Known: E041 has ~133 numeric diffs due to ill-conditioned QP sensitivity (ledger E049) — do not re-pin. E029/E030 are offline-reproducible with pinned data; see ledger for details.
   - **Data coverage is enforced.** Any new data input requires committing the file and re-pinning via `python3 scripts/check_data_coverage.py --update`.
   - **Premise verification required.** If pre-registering any follow-up experiment, verify every factual premise in handoffs against recorded artifacts (v1.2.1). Record corrections in the new entry’s `pre_registered` block.
   - **Stochastic values must not be hard-asserted.** Assert gate pass/fail/outcome, not fixed point estimates (v1.2.7).

## Suggested Next Task
**Default task:** Audit repository state and confirm verification hygiene. Report:
- Output of `scripts/check.sh` (pass/fail + any warnings)
- Presence of `.verify_snapshot/ACTIVE.json` (should be absent)
- `git status --short` (should be clean or only intentional changes)
- Any open items from `ledger/RESEARCH_LEDGER.md` relevant to current state

**Do NOT** start a new novelty search — E001–E039 search is complete. Only proceed with new experimentation if explicitly requested by the user with a specific, pre-registrable hypothesis.

## Quick References
- `AGENTS.md` - Full commands, guardrails, and verification workflow
- `ledger/RESEARCH_LEDGER.md` - Experiment history, decisions, and open items
- `ledger/PRIORITIZATION.md` - Procedure (v1.2.7 active)
- `ledger/golden_baseline.json` & `ledger/data_baseline.json` - Pinned baselines
