# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T15:09:23Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`. Working tree clean at HEAD 9792f78 except `__pycache__/*.pyc` (ignored). No live verification snapshot (`.verify_snapshot/` absent) — nothing to recover.

## INITIAL TASK FOR NEXT SESSION (START HERE)

> **CONFIRM BASELINE → ADDRESS E049**: Verify the clean baseline first. Only after it passes, tackle the standing tangency QP ill-conditioning issue. Do **not** re-pin goldens to silence drift.

### Step 1: Environment & Baseline Verification (REQUIRED)
```bash
# Ensure dependencies are present
pip install -r requirements.txt

# Run full convention + lint + reproducibility checks
SEED=42 bash scripts/check.sh
```
**Expected:** `EXIT 0` with `=== All checks passed ===`. This runs py_compile, golden-clean checks, golden-baseline fingerprint check, data coverage, portfolio-opt tests, and convention robustness.

```bash
# Confirm working tree state
git status --short
```
**Expected:** Only `__pycache__/*.pyc` modifications (ignored). Do **NOT** commit verification output.

### Step 2: Address Standing Open Item (E049) — Highest Value
**Issue:** Tangency QP ill-conditioning in `src/portfolio_opt.py` (`max_sharpe` branch). SLSQP at `ftol=1e-12` is chaotically ill-conditioned (1-ulp covariance perturbation can move OOS Sharpe by ~3e-02). E041/E042 artifacts still drift vs goldens (29–133 numeric diffs).

**Rules:**
- Do **NOT** re-pin goldens to silence drift
- Preserve solver-status independence (never gate on scipy exit status; validate on problem constraints)
- Do **NOT** change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions

**Planned Fix:**
1. Route `max_sharpe` through `exact_qp` / `exact_tangency_kkt` active-set enumeration (N ≤ 5 feasible; reference oracle from E049)
2. Fix the starting point at `src/portfolio_opt.py:253`: `y0 = w_feas / max(mu_s'w_feas, 1e-12)`
3. After fix, re-run affected drivers:
   ```bash
   SEED=42 python3 experiments/run_e041.py
   SEED=42 python3 experiments/run_e042.py
   SEED=42 python3 experiments/run_e042_lead.py
   ```
4. If artifacts change as expected from fixing the defect (not masking drift), re-pin deliberately with:
   ```bash
   python3 scripts/check_golden_baseline.py --update
   ```
5. Record the change in `ledger/RESEARCH_LEDGER.md` with rationale and before/after diff summary

### Step 3: Validation
```bash
# Quick verification of affected paths
SEED=42 python3 run_all_verification.py --skip-slow

# Or full extended check if time permits
SEED=42 bash scripts/check.sh
```

## Constraints (NON-NEGOTIABLE)
- **Never commit verification output.** If interrupted, restore goldens: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). If HEAD already captured a run, restore from the pinned commit per `ledger/golden_baseline.json`.
- **Never re-pin goldens to silence drift.** Only re-pin when fixing a documented defect.
- **Always use `SEED=42`.**
- **Honor pinned caches:** `data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`. E029/E030 are offline-reproducible due to pins.
- **Optimizer determinism:** Validate solutions on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`).
- **No scope creep:** Don't change gates, sensitivity grids, pre-registration, or validated constructions.
- **CI:** Workflow creation is maintainer-gated. Template at `.github/workflow-templates/verification-gate.yml`.
- **Lint:** Run `python3 -m py_compile` on changed files.

## Quick Reference
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (see E049 open item)
- **Baseline fingerprint:** `ledger/golden_baseline.json`
- **Data coverage:** `ledger/data_baseline.json`
- **Handoffs:** `.kilo/handoff/` (this file is the latest)
