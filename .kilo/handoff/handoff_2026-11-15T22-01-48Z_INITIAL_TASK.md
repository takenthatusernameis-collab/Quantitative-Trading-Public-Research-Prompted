# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T22:01:48Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `bd95cb72926fc9e0620d7a38a95c80a32e267be3` (`chore(kilo): checkpoint agent session`) on `main`
**Sync:** `git rev-list --left-right --count origin/main...HEAD` → `0	0` (in sync with origin/main)

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase **complete (E001–E051)**; surviving validated strategies and dispositions are recorded in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered; never move goalposts post-hoc. Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.

## Current state (verified this session)

- **Working tree:** clean except pre-existing `__pycache__/*.pyc` churn (gitignored). No staged source/data/experiment changes. The only non-pycache changes vs the prior durable handoff (`handoff_2026-11-15T21-54-13Z_INITIAL_TASK.md`, HEAD `8be1c704` → `bd95cb72`) are generic canonical-pointer symlinks and handoff deliverable files — **no research content changed**.
- **No interrupted verification run:** `.verify_snapshot/` and `.verify_reports/` are absent; the canonical `experiments/*.json` goldens are intact.
- **Baseline integrity — all guards green (per-step isolation, no long verification run):**
  - `SEED=42 bash scripts/check.sh` → exit 0, `=== All checks passed ===` (includes `scripts/check_json_artifacts.py`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `scripts/validate_template.py`, `scripts/check_experiment_imports.py`, `verify_convention_robustness.py`).
  - `scripts/check_goldens_clean.py` → exit 0 (goldens match HEAD; no stale snapshot).
  - `scripts/check_golden_baseline.py` → exit 0 (all pinned goldens match SHA-256).
  - `scripts/check_data_coverage.py` → exit 0 (all pinned data inputs present/tracked/unchanged).
  - `verify_convention_robustness.py` → exit 0 (`ALL VERIFICATIONS PASSED`).
- **Dependencies:** unit tests are not runnable in this sandbox (missing `numpy`/`pandas`/`pytest`); unrelated to repo content. If needed: `pip3 install --break-system-packages -r requirements.txt`.

## Initial task for the next agent (do first)

1. **Confirm baseline integrity**
   - Run `SEED=42 bash scripts/check.sh` (or `make check`). Expect exit 0 and `=== All checks passed ===`.
   - If it fails only because deps are missing, install `requirements.txt` and retry — that is not a baseline failure.
2. **If checks reveal a real baseline issue**
   - Dirty goldens / stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned artifacts from `ledger/golden_baseline.json`). Never commit captured verification output.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Then proceed only with explicit user direction.**
   - Default: await instructions. Do **not** run long verification, invent experiments, or change gates/outcomes unprompted.
   - Do **not** modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without an explicit request and a justified diff.
   - Never leave a verification run half-finished; do not commit `__pycache__`.

## Quick reference

```bash
SEED=42 bash scripts/check.sh                       # fast convention + guard checks (seconds)
SEED=42 python3 run_all_verification.py             # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended  # +18 more committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full      # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 verify_convention_robustness.py     # convention robustness only (reads JSONs)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
```

## Open items (do not resolve silently)

- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity) remain after the optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin to silence.** See ledger E049.
- **E042 lead:** PARTIAL (3/5 gates). Min-var confirmatory run (n_sim=50) passes convention robustness but the tangency grid drifts. See ledger E049.
- **CI gate:** template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI (automated agents cannot push workflows).
- **Promotion gates:** any config clearing a sensitivity grid requires a dedicated pre-registered confirmatory run with full placebo before promotion.

## Handoff artifact

- Primary: `handoff_2026-11-15T22-01-48Z_INITIAL_TASK.md` (SHA-256 `e39864607549aac245950663a6740f402193e377fc870657980fead0be5aa28f`)
- Mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Generic canonical pointers repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-15T22-01-48Z_INITIAL_TASK.md`.

---

*Generated at 2026-11-15T22:01:48Z for durable handoff to the next agentic work session.*