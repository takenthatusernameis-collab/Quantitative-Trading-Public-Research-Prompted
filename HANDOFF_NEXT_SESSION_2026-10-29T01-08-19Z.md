# HANDOFF_NEXT_SESSION — 2026-10-29T01:07:38Z

## Repository State
- **Project:** Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014–2026)
- **Phase:** Research complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Canonical baselines:** `experiments/*.json` are pinned. `ledger/golden_baseline.json` and `ledger/data_baseline.json` enforce integrity
- **Environment:** Linux, git repo, Python 3 research environment. Use `SEED=42` for all runs.

## Initial Task For Next Session (Clear & Actionable)
**Goal:** Verify baseline integrity and ensure the repo is in a clean, reproducible state before making any changes.

### Step 1: Baseline Integrity (MUST pass first)
```bash
SEED=42 bash scripts/check.sh
```
This runs py_compile, golden cleanliness checks, data coverage, optimizer tests, and convention robustness.

**If it fails:**
- If it reports a stale verification snapshot → recover: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
- If it reports `experiments/` differs from HEAD due to a captured run → restore to HEAD. If HEAD itself was incorrectly re-pinned, restore from the commit matching `ledger/golden_baseline.json`.
- If data coverage fails → do **not** download. Check `ledger/data_baseline.json` and commit missing pinned data before proceeding.

### Step 2: Quick Verification (Confirm reproducibility)
```bash
SEED=42 python3 run_all_verification.py
# or: make verify-quick
```
This re-runs the 8 quick drivers (E012, E023, E024, E027, E035, E037, E039, E042-lead) and restores goldens on success.

### Step 3: Triage & Report
- **If clean:** Review `ledger/RESEARCH_LEDGER.md` for any open items (notably E041 numeric drift / optimizer determinism noted in E049) and propose next concrete work.
- **If drift:** Do **NOT** re-pin goldens to silence it. Investigate per AGENTS.md (extended drift report goes to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`, gitignored). Numeric drift can be due to ill-conditioned QPs (SLSQP) — treat as environment-sensitive, not a reason to overwrite baselines.

## Guardrails (Do Not Violate)
- **Goldens are authoritative:** Never let verification overwrite committed `experiments/*.json`. The suite backs up and restores them. A half-finished run must be recovered.
- **Pre-registration first:** Any new experiment must have a pre-registered JSON block, gates, falsification expectations, and sensitivity grid before execution. Goalposts cannot be moved post-hoc.
- **MHT:** Sensitivity grids are "reported, not gated". Promotion requires a dedicated pre-registered confirmatory run with full placebo.
- **Offline discipline:** Prefer pinned data/vintages. The suite runs with `QUANT_RESEARCH_OFFLINE=1`. Unpinned inputs are not allowed.
- **Optimizer rule:** Solver exit status is not a gating criterion. Validate on problem constraints (enforced by `tests/test_portfolio_opt.py`).
- **CI:** Do not create `.github/workflows/`. Use the template in `.github/workflow-templates/` if needed.
- **Commits:** Only commit when explicitly requested. Never commit verification output or corrupted goldens.

## Quick References
- **Full commands:** `AGENTS.md` (Quick Start, Reproducibility, Baseline Integrity)
- **Ledger:** `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- **Extended verification:** `SEED=42 python3 run_all_verification.py --extended` (~21 min)
- **Full verification:** `SEED=42 python3 run_all_verification.py --full` (~15 min)
- **Convention check only:** `SEED=42 python3 verify_convention_robustness.py`

## Handoff Metadata
- **Created:** 2026-10-29T01:07:38Z
- **Created by:** Current agentic session
- **Purpose:** Durable handoff with clear initial task for next session
