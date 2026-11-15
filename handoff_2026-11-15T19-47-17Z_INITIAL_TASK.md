# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T19:47:17Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main` (in sync with `origin/main` at handoff creation)
**HEAD:** `a78c36900c37f1e752937d5c2f3a2b8c4e6a0b01` — `chore(kilo): checkpoint agent session`

## Project context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. **Research phase complete (E001–E051).** Surviving validated strategies and dispositions are recorded in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered; never move goalposts post-hoc. Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.

## Current state (verified at this handoff, 2026-11-15T19:47Z)
- **Baseline is intact.** All fast guard scripts pass with exit 0:
  - `scripts/check_json_artifacts.py` — committed JSON artifacts parse OK.
  - `scripts/check_goldens_clean.py` — all committed golden artifacts match HEAD.
  - `scripts/check_golden_baseline.py` — pinned golden artifacts match `ledger/golden_baseline.json`.
  - `scripts/check_data_coverage.py` — pinned data inputs present, tracked and unchanged.
  - `verify_convention_robustness.py` — all convention verifications pass.
- **No pending verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; `experiments/*.json` are the authoritative committed goldens.
- **Working tree note:** only `__pycache__/*.pyc` bytecode files show as modified (gitignored bytecode churn). **Do not commit `__pycache__`.** This is not a source/data/experiment change.
- **Environment:** `numpy`/`pandas` are required for `check.sh`; install via `pip3 install --break-system-packages -r requirements.txt` if missing, then re-run `SEED=42 bash scripts/check.sh`.

## Initial task for the next agent (do first)
1. **Establish a clean baseline**
   - Run: `SEED=42 bash scripts/check.sh` (or `make check`). Expect exit 0 and `=== All checks passed ===`.
   - If it fails only on missing `numpy`/`pandas`, install `requirements.txt` and re-run.
2. **If a real baseline issue appears**
   - Dirty goldens / stale verification snapshot: recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json`). **Never commit captured verification output.**
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
SEED=42 python3 run_all_verification.py --restore-only # recover goldens after interruption
```

## Handoff artifact
- **Primary:** `handoff_2026-11-15T19-47-17Z_INITIAL_TASK.md`
- Durable repo-root artifact for handoff to the next agentic work session.

---
*Generated at 2026-11-15T19:47:17Z for durable handoff to the next agentic work session.*
