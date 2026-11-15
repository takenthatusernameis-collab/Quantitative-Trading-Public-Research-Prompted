# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T19:46:32Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main` (in sync with `origin/main` at handoff creation)
**HEAD:** `e7ede52454ce1b9702674f7529bb93cb06e9ec6d` — `chore(kilo): checkpoint agent session`

## Project context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. **Research phase complete (E001–E051).** Surviving validated strategies and dispositions are recorded in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered; never move goalposts post-hoc. Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.

## Current state (verified at this handoff, 2026-11-15T19:46Z)
- **Baseline is intact.** All fast guard scripts pass with exit 0:
  - `scripts/check_json_artifacts.py` — 114 committed JSON artifacts parse OK.
  - `scripts/check_goldens_clean.py` — all committed golden artifacts match HEAD.
  - `scripts/check_golden_baseline.py` — all 107 pinned golden artifacts match `ledger/golden_baseline.json`.
  - `scripts/check_data_coverage.py` — all 35 pinned data inputs present, tracked and unchanged.
  - `verify_convention_robustness.py` — all convention verifications pass.
  - `scripts/validate_template.py` — OK.
  - `scripts/check_experiment_imports.py` — all experiment script imports OK.
- **No pending verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; `experiments/*.json` are the authoritative committed goldens.
- **`check.sh` exits 1 for ONE reason only — missing Python dependencies (environment, not a baseline defect):**
  - `tests.test_data_coverage` errors (3) on `ModuleNotFoundError: No module named 'pandas'`.
  - `tests.test_portfolio_opt` errors (1) on `ModuleNotFoundError: No module named 'numpy'`.
  - The other unittest modules pass: `test_json_guard` (8), `test_goldens_guard` (5), `test_golden_baseline` (9), `test_drift_report` (22).
  - Fix: `pip3 install --break-system-packages -r requirements.txt` and re-run `SEED=42 bash scripts/check.sh`.
- **Working tree note:** only `src/__pycache__/cache_keys.cpython-312.pyc` shows as modified (gitignored bytecode churn). **Do not commit `__pycache__`.** This is not a source/data/experiment change.

## Initial task for the next agent (do first)
1. **Establish a clean baseline**
   - Run: `SEED=42 bash scripts/check.sh` (or `make check`).
   - If it fails only on missing `numpy`/`pandas`, install `requirements.txt` and re-run. Expect exit 0 and `=== All checks passed ===`.
2. **If a real baseline issue appears**
   - Dirty goldens / stale verification snapshot: recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifacts per `ledger/golden_baseline.json`). **Never commit captured verification output.**
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Then stop and await explicit user direction**
   - Default action: report status and wait. Do **not** run long verification, invent experiments, or change gates/outcomes unprompted.
   - Do **not** modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/`, `src/`, `scripts/`, or `tests/` without an explicit request and a justified diff.
   - Never leave a verification run half-finished; never commit `__pycache__`.

## Open items (do not resolve silently)
- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity) remain after the optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin to silence.** (ledger E049)
- **E042 lead:** PARTIAL (3/5 gates). Min-var confirmatory (n_sim=50) passes convention robustness but the tangency grid drifts. (ledger E049)
- **CI gate:** template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI (agents cannot push workflows).
- **Promotion discipline:** any config clearing a sensitivity grid requires a dedicated pre-registered confirmatory run with full placebo before promotion.

## Quick reference
```bash
SEED=42 bash scripts/check.sh                        # fast guards + convention checks (seconds)
SEED=42 python3 run_all_verification.py              # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 more committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 verify_convention_robustness.py      # convention robustness only
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after interruption
```

## Handoff artifact
- **Primary:** `handoff_2026-11-15T19-46-32Z_INITIAL_TASK.md`
- Mirrored to the `handoff/` and `HANDOFFS/` directories; generic canonical pointers (`HANDOFF`, `HANDOFF_LATEST`, `LATEST.md`, `CURRENT`, `next_session.md`, etc.) repointed to this file.

---
*Generated at 2026-11-15T19:46:32Z for durable handoff to the next agentic work session.*