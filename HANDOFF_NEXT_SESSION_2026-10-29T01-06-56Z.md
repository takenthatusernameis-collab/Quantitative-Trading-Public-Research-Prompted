# Handoff: Next Agentic Work Session
**Timestamp (UTC):** 2026-10-29T01:06:56Z
**Handoff ID:** handoff-20261029T010656Z
**From:** current session (baseline verification only — no new work performed)
**To:** next agentic work session

## Initial Task (Clear & Actionable)

Resume work from a clean, verified baseline. Do **not** guess or start new
experiments without first establishing state.

### Step 1: Verify Repository State (Required)
```bash
git status
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

- If `scripts/check.sh` fails due to golden/baseline issues, **stop and resolve
  before making changes** (see AGENTS.md "Baseline Integrity").
- If `.verify_snapshot/ACTIVE.json` exists, a verification run may be pending;
  recover with `SEED=42 python3 run_all_verification.py --restore-only`.

### Step 2: Load Project Context (Required)
- Read `ledger/RESEARCH_LEDGER.md` (E001–E049; the last entry E049 is the
  optimizer-determinism fix).
- Read `AGENTS.md` (conventions, seeds, golden files, reproducibility,
  baseline integrity).
- Inspect `experiments/` and `data/` state.

### Step 3: Determine Next Action
- Pick the highest-priority open ledger item and confirm scope before editing.
- If clean with no explicit direction, summarize state and ask for direction
  (no large refactors).
- Never modify committed goldens (`experiments/*.json`) as a side effect of
  verification; re-pin only via
  `python3 scripts/check_golden_baseline.py --update` with explicit
  justification.

## Verified Baseline (measured this session, 2026-10-29T01:06Z)

| Check | Result |
|---|---|
| `git status` | clean working tree, branch `main` |
| HEAD | `19f75f5` chore(kilo): checkpoint agent session |
| `.verify_snapshot/` | absent — no live run, nothing to recover |
| `SEED=42 bash scripts/check.sh` | **ALL CHECKS PASSED** (exit 0) |

`scripts/check.sh` coverage confirmed this run: golden-baseline guard,
data-coverage guard, JSON-artifact guard, `tests/test_portfolio_opt.py`,
convention robustness, template validation, and all 28 experiment-script
imports (run_e011 … run_e042_lead).

## Open Items (from `ledger/RESEARCH_LEDGER.md`)

1. **E049 residual — the tangency QP is still ill-conditioned.** The fix in
   E049 removed the *dominant* environment dependence (the solver's exit status
   is no longer an input to the result), but a 1-ulp input perturbation still
   moves the `min_var` answers by ~2.6e-05 and the lead's OOS Sharpe by up to
   3e-02 at 1e-14. The E041/E042 grid artifacts therefore still drift by
   29–133 differences beyond the 1e-4 tolerance. **Do not re-pin them to
   silence that** — see the open item in the ledger. The remaining work is a
   research-engineering decision: replace the SLSQP QP solves with a
   well-conditioned, deterministic solver (for N <= 5 an exact active-set
   enumeration of all KKT points is feasible and was used as the reference
   oracle), then re-pin the affected artifacts deliberately.
2. **E049 secondary defect (deliberately not fixed):** `y0 = w_feas /
   max(mu_s'w_feas, 1e-12)` masks a *negative* denominator at the 2019-10-16
   rebalance, so the start point has magnitude 8.1e+11 and SLSQP returns
   garbage (objective 3.7e+20), which the feasibility check correctly rejects.
   Fixing the start point (a max-`mu_s'w` LP on the feasible simplex) would
   **change the published numbers**, so it is left for the same deliberate
   re-pin decision.
3. **Known reporting-only drift (do not re-pin):** E030 (near-zero quantities,
   input now pinned), E041 (133 numeric diffs, 3 structural differences
   resolved). Both decisions and gate flags are unchanged.

## Constraints & Reminders

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`,
  `data/fundamentals_vintages.json`, `ledger/data_baseline.json`).
- Follow pre-registration, multiple-testing discipline, falsification
  expectations.
- Do not commit verification outputs; restore goldens if interrupted
  (`SEED=42 python3 run_all_verification.py --restore-only`).
- Cache coverage is enforced; a missing pinned data input fails hard in
  offline mode (`QUANT_RESEARCH_OFFLINE=1`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or
  validated constructions (`src/backtest.py`, `src/strategies.py`,
  `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at
  `.github/workflow-templates/verification-gate.yml`, instructions in
  `VERIFICATION_GATE_TEMPLATE.md`).

## Suggested First Action

Run Step 1 above, report baseline status, then propose next steps from the
ledger state (E049 residual is the highest-value open item).

(End of file)