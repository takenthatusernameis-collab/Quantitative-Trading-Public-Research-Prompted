# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T19:43:39Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main` (in sync with `origin/main` at handoff creation)
**HEAD:** `7b35f7a7332cd78b5b9063fc4034845600d8ee49` — `chore: capture completed workflow run diagnostics`

## Project context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. **Research phase complete (E001–E051).** Surviving validated strategies and dispositions are recorded in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered; never move goalposts post-hoc. Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.

## Current state (baseline at this handoff)
- **Canonical baseline artifacts intact:** no `.verify_snapshot/` or `.verify_reports/` present; `experiments/*.json` goldens are the authoritative committed baseline (per `ledger/golden_baseline.json` / project invariants).
- **Baseline guards last verified green (2026-11-15T19:42Z, per-step isolation):** `scripts/check_json_artifacts.py`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `scripts/validate_template.py`, `scripts/check_experiment_imports.py`, and `verify_convention_robustness.py` all exit 0.
- **Working tree note:** pre-existing gitignored `__pycache__/*.pyc` churn may appear; do not commit it. Do not treat it as a source/data/experiment change.
- **Environment note:** this sandbox may lack `numpy`/`pandas`/`pytest`; install `pip3 install --break-system-packages -r requirements.txt` if needed for unit tests or longer verification (dependency absence is not a baseline defect).

## Initial task for the next agent (do first)
1. **Confirm baseline integrity before making changes**
   - Run: `SEED=42 bash scripts/check.sh` (or `make check`). Expect exit 0 and `=== All checks passed ===`.
   - If it fails only due to missing dependencies, install `requirements.txt` and retry.
2. **If a real baseline issue is found**
   - Dirty goldens / stale verification snapshot: recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json`). **Never commit captured verification output.**
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Then stop and await explicit user direction**
   - Default action: report status and wait. Do **not** run long verification, invent experiments, or change gates/outcomes unprompted.
   - Do **not** modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/`, `src/`, `scripts/`, or `tests/` without an explicit request and a justified diff.
   - Never leave a verification run half-finished; never commit `__pycache__`.

## Open items (do not resolve silently)
- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity) remain after the optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin to silence.** (ledger E049)
- **E042 lead:** PARTIAL (3/5 gates). Min-var confirmatory (n_sim=50) passes convention robustness but the tangency grid drifts. (ledger E049)
- **CI gate:** template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via GitHub UI (agents cannot push workflows).
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
- **Primary:** `handoff_2026-11-15T19-43-39Z_INITIAL_TASK.md`
- Mirrored to available handoff directories and generic canonical pointers repointed to this file.

---
*Generated at 2026-11-15T19:43:39Z for durable handoff to the next agentic work session.*
