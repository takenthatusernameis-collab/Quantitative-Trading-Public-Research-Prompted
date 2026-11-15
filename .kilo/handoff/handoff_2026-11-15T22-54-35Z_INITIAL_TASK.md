# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T22:54:35Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `a9edad5ec93e52f7370c1d0d2a5f641703942c24` (`chore(kilo): checkpoint agent session`) on `main`
**Sync:** in sync with `origin/main` (`0 0`)

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase **complete (E001–E043/E051)**; surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered — never move goalposts post-hoc. Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.

## Current state (verified this session)

- **Working tree:** no research/source/data/experiment changes. Pre-existing modified tracked `__pycache__/*.pyc` files present (15 files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`) — do **not** commit them.
- **No interrupted verification:** `.verify_snapshot/` and `.verify_reports/` absent; canonical `experiments/*.json` goldens intact.
- **Baseline integrity guards (green):** `SEED=42 bash scripts/check.sh` → `=== All checks passed ===` (exit 0), including `check_json_artifacts.py`, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `validate_template.py`, `check_experiment_imports.py`, and `verify_convention_robustness.py` (`ALL VERIFICATIONS PASSED`).
- **Environment note:** `numpy`, `pandas`, `pytest` may be absent in this sandbox; unit tests are environment-limited, not a repo-content failure. If deps are missing, `pip3 install --break-system-packages -r requirements.txt` before long runs.

## Initial task for the next agent (do first)

1. **Confirm baseline:** `SEED=42 bash scripts/check.sh` (or `make check`). Expect exit 0 / `=== All checks passed ===`.
2. **If a real baseline issue appears:**
   - Dirty goldens / stale `.verify_snapshot/`: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json`). Never commit captured verification output.
   - Golden fingerprint mismatch: resolve deliberately against `ledger/golden_baseline.json`; do not re-pin as a side effect of verification.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Then await explicit user direction.** Do not run long verification, invent experiments, or change gates/outcomes unprompted. Do not modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without explicit request and justified diff. Never leave a verification run half-finished.

## Quick reference

```bash
SEED=42 bash scripts/check.sh                          # fast convention + guard checks
SEED=42 python3 run_all_verification.py                # quick verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 verify_convention_robustness.py        # convention robustness only
SEED=42 python3 run_all_verification.py --restore-only # recover after interrupted run
```

## Open items (do not resolve silently)

- **E041 drift:** 133 numeric diffs (1-ulp QP sensitivity) remain post optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin.** (ledger E049)
- **E042 lead:** PARTIAL (3/5 gates); min-var confirmatory (n_sim=50) passes convention robustness but tangency grid drifts. (ledger E049)
- **CI gate:** template `.github/workflow-templates/verification-gate.yml`; maintainer must create real workflow via GitHub UI.
- **Promotion:** any sensitivity-grid-clearing config needs a dedicated pre-registered confirmatory run with full placebo before promotion.

## Handoff artifact

- Primary: `handoff_2026-11-15T22-54-35Z_INITIAL_TASK.md`
- Mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Generic canonical pointers repointed to this file via `python3 scripts/repoint_handoff.py handoff_2026-11-15T22-54-35Z_INITIAL_TASK.md`.

---
*Generated 2026-11-15T22:54:35Z for durable handoff to the next agentic work session.*
