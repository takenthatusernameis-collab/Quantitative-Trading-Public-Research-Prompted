# Handoff — E042 lead root-caused, defect fixed, lead artifact re-pinned (2026-10-20)

## What changed

The previous handoff (`HANDOFF_SESSION_2026-10-20_cache_coverage.md`, ledger
E048) left exactly one task: *root-cause the `max_sharpe` optimizer path in
`src/portfolio_opt.py` and decide whether the E042 lead artifact or the
solver is authoritative.* It was the highest-value open item because it was
the single failure of the **primary** verification gate
(`run_all_verification.py` reported `OVERALL: FAILURES DETECTED`).

**The answer is neither, in the sense the question assumed.** The artifact
and the solver are *both* right about the mathematics; what was wrong was the
**interface between them**: the code judged a solver answer by scipy's
*exit status* instead of by the answer's own feasibility.

### Root cause

1. **The data is not the cause.** Recomputing the 96-config E042 sensitivity
   grid on the same pinned inputs, every row whose branch does not use the
   tangency QP reproduces **exactly** (`min_var` and `risk_parity`:
   Δ OOS Sharpe -0.000000, Δ equity beta +0.000000). Only the `max_sharpe`
   rows moved.
2. **The tangency QP is chaotically ill-conditioned.** A **1-ulp**
   (1e-16 relative) perturbation of the shrunk covariance moves the lead's
   OOS Sharpe between two branches (0.8219 vs 0.8659) and its equity beta
   between +0.0352 and -0.0009.
3. **The branch is chosen by SLSQP's exit status, which is build dependent.**
   At the lead's 2020-01-16 rebalance SLSQP returns the **exact global
   optimum** of the QP (objective 13.5743377390, identical to an independent
   active-set enumeration; constraint residuals -9.8e-12 and +6.0e-12) but
   exits with **status 8, "Positive directional derivative for linesearch"**.
   The shipped code discarded that optimal point on the strength of the flag
   and used the phase-1 LP vertex instead — hence `equity_beta +0.0352`
   instead of `-0.0009`.
4. Measured across scipy builds (unpatched driver): 1.14.1/1.15.3 →
   0.837 / -0.0030; 1.16.3/1.17.1/1.18.1 → 0.822 / +0.0352; the **committed
   golden → 0.866 / -0.0009**, a fourth branch that no tested build reaches
   from this machine. BLAS threading is not the cause (`OMP_NUM_THREADS=1`
   gives the identical 0.822 / +0.0352); the CPU here is an AMD EPYC
   (AVX2, no AVX-512), so the original artifact was most likely produced on a
   different CPU/BLAS build whose last bits differ.

### Fix

| File | Change |
|---|---|
| `src/portfolio_opt.py` | New `_tangency_feasible(y, mu_s, A_ub_y)`: a solver answer is validated against the **QP constraints** (finite, right dimension, `y >= 0`, `mu'y = 1`, the homogeneous beta caps; 1e-6 tolerance, consistent with `_feasible`). The `max_sharpe` branch now offers the SLSQP answer whenever it satisfies them, **regardless of `res.success`**; the existing candidate selection still keeps it only when its formation-window Sharpe beats the alternatives, so a worse point can never displace the LP fallback |
| `src/portfolio_opt.py` | `project_onto_beta_cap` (the placebo null's projection QP) gets the same treatment — a feasible projection is no longer discarded because of the exit status |
| `tests/test_portfolio_opt.py` (new) | 5 tests pinning the invariant: the answer must not depend on the exit status, an infeasible answer must be rejected, the result must always be feasible. **Fails against the pre-fix code** (2 failures) |
| `scripts/check.sh` | The new test is a first-class step |
| `experiments/e042_lead_config_confirmatory.json` | **Deliberately re-pinned** (see below) |
| `ledger/golden_baseline.json` | Re-pinned with `scripts/check_golden_baseline.py --update`, so the replacement is visible in the diff (E046 / E048 precedent) |
| `ledger/RESEARCH_LEDGER.md`, `AGENTS.md` | The E049 entry and the reproducibility notes |

### Deliberate re-pin

The lead artifact's `/primary` block now reproduces the **committed golden**
to 5e-9 (`equity_beta` -0.0009023437848591046 vs the golden's
-0.0009023438936704533) — the fix *restores* the committed numbers rather
than inventing new ones. Its `/placebo_constrained` block cannot: the
golden's placebo statistics (mean 0.5721, std 0.1502, min 0.2374, max
0.8731) come from the chaotic branch, and the two candidate rules land on
0.5958 (shipped gate) and 0.6254 (accept-if-feasible) — the golden is
*below* both, i.e. it encodes yet another SLSQP outcome pattern. That block
was therefore re-pinned deliberately.

**Impact of the re-pin, measured against the old golden: 5 numeric
differences, 0 structural** — the five `/placebo_constrained` statistics
(mean 0.5721 → 0.6254, std 0.1502 → 0.1327, min 0.2374 → 0.3228,
max 0.8731 → 0.9184, z 1.9568 → 1.8121). **No decision changed**:
`decision` REJECTED, 4/5 gates, `G2_placebo_z_gte_3.0` FAIL (z 1.8121, bar
3.0) — the pre-registered bar fails under the old and the new value alike.
Every other gate flag is identical.

## What was actually verified

- **The failure reproduces** in an isolated copy of the committed tree:
  `SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e042_lead.py`
  gave OOS 0.822 / beta +0.0352 / z 1.64 (20 mismatches at 1e-9).
- **After the fix**, the same command gives OOS 0.866 / beta -0.0009 /
  z 1.81, and `deep_compare` against the committed golden reports
  **6 differences at 1e-4 — 5 in `/placebo_constrained` and `runtime_sec`
  (which the suite excludes)**; at 1e-9 the 14 remaining differences are all
  ≤ 5e-9 relative in the `/primary` block.
- **Byte-reproducible**: two consecutive runs of the patched driver produce
  byte-identical artifacts (excl `timestamp` / `runtime_sec`).
- **The fix is what removes the chaos**: under 1-ulp input perturbations the
  lead's OOS Sharpe now moves by **9.7e-09** (was 5.8e-02) and the placebo
  statistics by **< 1e-06** (was up to 4e-02).
- **The regression test is real**: it fails against the pre-fix code
  (`exit status changed the answer: [0. 1.] != [0.81049172 0.18950828]`) and
  passes after it.
- **Drift reduction across the board** (diffs vs the committed goldens):
  E041 main 9273 → **133**, E041 grid 360 → **29**, E042 primary 6592 →
  **56**, E042 grid 210 → **42**, E042 lead 20 → **6**.
- **E041's three structural differences are gone**: the exploratory
  "8 of 96" market-neutral-and-Sharpe count is 8 before and after, and
  E041's decision (REJECTED, 3/5, G2 and G3 FAIL) and every gate flag are
  unchanged.
- `SEED=42 bash scripts/check.sh` → **ALL CHECKS PASSED** (including the new
  `tests.test_portfolio_opt` step).
- `SEED=42 python3 run_all_verification.py` (quick) → see *What was actually
  verified* in the ledger's E049 entry for the final numbers.

## What remains unresolved

- **The tangency QP is still ill-conditioned.** The fix removes the
  *dominant* environment dependence (the exit status); it does not make the
  QP well conditioned. The `min_var` branch never reports a failure status
  (measured: 101 solves, 0 failures) yet its answers still move by up to
  **2.6e-05** in the E042 primary's daily weights at the 1-ulp level, which
  is why **E041 (133 diffs), the E041 grid (29), the E042 primary (56) and
  the E042 grid (42) still differ from their goldens** — down from
  9273/360/6592/210, but not zero. A 1e-14 perturbation of the same
  covariance still moves the lead's OOS Sharpe by 3e-02.
  **Those artifacts were deliberately left alone**: re-pinning them would
  bake this machine's numbers over a defect that is not yet fixed.
- **E042's exploratory count moves 5 of 96 → 6 of 96** (one more grid
  configuration now clears the exploratory |beta| ≤ 0.1 and Sharpe ≥ 0.8
  bar). It is *reported, not gated*; the decision stays PARTIAL (4/5).
- **A second, smaller defect is known and deliberately not fixed**:
  `y0 = w_feas / max(mu_s'w_feas, 1e-12)` (`src/portfolio_opt.py:253`) masks
  a *negative* denominator, so at the 2019-10-16 rebalance the initial point
  has magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09. SLSQP returns
  garbage there (objective 3.7e+20), which the new feasibility check
  correctly rejects, so the shipped code falls back to the LP vertex exactly
  as the golden did. A feasible start (a max-`mu_s'w` LP on the feasible
  simplex) makes SLSQP converge to the exact optimum there — which would
  **change the published numbers**, so it belongs with the same deliberate
  re-pin decision.
- The CI workflow `.github/workflows/verification-gate.yml` still needs a
  maintainer to create it via the GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`). Outside agent scope.

## Approaches already tried and rejected

- **"It is the data"** — rejected: the `min_var` / `risk_parity` grid rows
  reproduce to 0.000000 on the same pinned inputs, and
  `scripts/check_data_coverage.py` passes (all 35 inputs tracked and
  unchanged).
- **"It is the BLAS thread count"** — rejected: `OMP_NUM_THREADS=1
  OPENBLAS_NUM_THREADS=1` gives the identical 0.822 / +0.0352.
- **"It is a scipy version"** — rejected as an *explanation* (not as a
  cause): the unpatched driver was run under scipy 1.14.1, 1.15.3, 1.16.3,
  1.17.1 and 1.18.1 and **none** of them reproduces the committed golden
  (two different branches, neither of them the golden's). The golden's
  branch is the "SLSQP reported success" one — which is exactly the branch
  the fix now selects *deterministically*.
- **"The tangency solution is a near-tie"** — rejected: with N = 3 the QP was
  solved to global optimality by enumerating every KKT point; SLSQP's answer
  is the global optimum (objective identical to 1e-10), and the objective
  gap over the 37 windows where SLSQP succeeded was ≤ 9.2e-16. There is no
  tie to break; the *branch* was being chosen by a status flag.
- **"Accept the solver's answer whenever it is feasible" (in the placebo
  projection)** — this *moved the placebo away from the golden* (0.5958 →
  0.6254 vs the golden's 0.5721) rather than towards it, which is how the
  placebo block was proven to be irreproducible from the golden by any
  environment-independent rule (and why it was re-pinned rather than
  "restored").
- **Fixing the `y0` start point in the same change** — rejected *for now*:
  it makes the 2019-10-16 rebalance converge to the exact optimum instead
  of the LP vertex, which changes the published numbers. Deferred to the
  deliberate re-pin decision.

## One precise next task

**Make the portfolio QPs well-conditioned and deterministic, then re-pin the
four artifacts that still drift.** Evidence and constraints:

- The remaining drift is *not* the exit status any more (E049). It is the
  **conditioning of the QPs themselves**: at the 1-ulp level the `min_var`
  answers move by 2.6e-05 and the `max_sharpe` answers by 3e-02 under a
  1e-14 perturbation. Affected artifacts and their current diff counts
  (numeric, 1e-4 tolerance):
  `e041_market_neutral_portfolio.json` 133, `e041_sensitivity_grid.json` 29,
  `e042_minvar_market_neutral.json` 56, `e042_sensitivity_grid.json` 42.
- The reference oracle already exists and was used in this session: for
  N ≤ 5 the tangency QP can be solved to **global optimality** by
  enumerating every active set (the KKT point of each subset; 848 subsets
  for N = 5) and taking the feasible one with the lowest objective. That
  enumeration confirmed SLSQP's answer at 2020-01-16 is the global optimum
  (objective 13.5743377390 vs the enumeration's 13.5743377395). A
  deterministic QP solver built on that idea would make the artifacts
  reproducible across CPU/BLAS builds — but it **changes the published
  numbers**, so it is a research decision, not a mechanical repair.
- Bounded deliverables: (a) implement the deterministic solver behind the
  existing `optimize_portfolio_weights` / `project_onto_beta_cap`
  interface, with a unit test that it returns the same weights on repeated
  runs and under 1-ulp input perturbations; (b) re-measure the four
  artifacts' diffs; (c) re-pin **deliberately** (one `--update` call, one
  ledger entry) and confirm that **every gate flag and every decision
  (E041 REJECTED 3/5, E042 PARTIAL 4/5) is unchanged** — the E042
  exploratory "N of 96" count must be re-derived and recorded.
- Also in scope for the same change: the `y0` defect at
  `src/portfolio_opt.py:253` (the `max(..., 1e-12)` clamp turns a negative
  denominator into a 1e11-magnitude infeasible start). Fixing it moves the
  2019-10-16 rebalance from the LP vertex to the exact optimum, so it must
  land in the same deliberate re-pin.
- Constraints: `SEED=42`; do **not** weaken the 1e-4 comparison tolerance;
  do **not** silently replace a golden (use
  `python3 scripts/check_golden_baseline.py --update` and record it in the
  ledger); run the work in an isolated copy so the canonical goldens cannot
  be captured mid-run; do not move any pre-registered gate; keep
  `QUANT_RESEARCH_OFFLINE=1` enabled when re-running the suite (all inputs
  are pinned, so a green run proves no network use).

### Constraints for the next session

- `SEED=42` for every driver.
- `python3 scripts/check_golden_baseline.py` must pass before committing; a
  changed artifact needs an explicit `--update` **and** a ledger entry.
- Never commit the output of a verification run: the suite's
  `.verify_snapshot/` restore step is the only thing that keeps the
  canonical artifacts intact.
- If a run is interrupted: `SEED=42 python3 run_all_verification.py
  --restore-only`.
- Keep `ledger/RESEARCH_LEDGER.md` and `AGENTS.md` in step with any change
  to a driver, a golden or a guard.
