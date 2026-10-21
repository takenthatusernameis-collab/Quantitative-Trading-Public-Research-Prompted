# Handoff — E048 data-cache coverage gap closed (2026-10-20)

## What changed

The previous handoff (`HANDOFF_SESSION_2026-10-20.md`, ledger E047) left no
outstanding research task, so this session audited the repository's
reproducibility machinery. It found a real, unclosed defect and closed it.

**Root cause.** 7 of the 19 cached price files the committed drivers read were
**absent from the repository**. A driver whose `data.download()` request does
not resolve to a committed cache file silently falls through to a live
`yf.download`, and **yfinance is not bit-reproducible**: two consecutive
downloads of the same request differ by up to **3.2e-06** in the resulting
correlations (measured 2026-10-20). That is why **E030** drifted (28 numeric
differences beyond the 1e-4 relative tolerance): its 16-ETF panel had never
been pinned, so the artifact was derived from a price file that no longer
existed anywhere. The 4-decimal-rounded correlation matrix and the
near-zero fold metrics (`folds[3]/total_return = -2.19e-05`) amplified the
1e-6 jitter into visible differences.

**Changes (all in commit `37f0af0`):**

| Area | Change |
|---|---|
| `data/` | The 7 missing panels are now committed (~41 MB) plus E024's raw OHLCV panel; the `2026-10-11` vintage is exempted in `.gitignore` next to the `2026-10-12` one |
| `experiments/run_e024.py` | The raw download was **unbounded** (`yf.download` with no `end`), so E024's ex-dividend sample grew with the calendar. It is now bounded by `data.pinned_end_date()` and the end date is part of the cache key. No number changes |
| `src/cache_keys.py` (new) | Single source of truth for cache file names; `src/data.py` now calls it instead of computing the name inline |
| `src/offline.py` (new) | Offline gate. `src/data.download`, `src/macro.fetch_fred`, `src/fundamentals.fetch_fundamentals` and E024's raw download raise `OfflineDataUnavailable` instead of reaching the network |
| `scripts/check_data_coverage.py` (new) | Statically resolves **every** `data.download()` / `data.get_benchmark()` call site in the 28 driver sources and requires each cache file to be **present**, **git-tracked** and **unchanged** vs the SHA-256 pinned in the new `ledger/data_baseline.json` (35 inputs) |
| `run_all_verification.py` | Re-executes every driver with `QUANT_RESEARCH_OFFLINE=1`, so a passing run also proves no network use |
| `scripts/check_json_artifacts.py` | **Its CLI discarded `main()`'s return value**, so it printed `FAIL …` and always exited 0 — `check.sh` could never abort on a malformed artifact. Now `sys.exit(main())`. Its schema check is also scoped to `experiments/` (the pinned data manifests added by E046 are not experiment artifacts) |
| `experiments/e030_multiasset_tsm.json` | **Deliberately re-pinned** to its now-pinned input (E046 precedent). Structure identical, decision `REJECT` 2/5 unchanged, all five gate `pass` flags unchanged, 0 structural diffs, max absolute delta 1.0e-04 |
| `tests/test_data_coverage.py` (new) | 13 tests: cache-key parity with `src/data.py`, 0 unresolved call sites repo-wide, and the guard's failure modes (missing / modified / untracked) |
| `README.md`, `AGENTS.md`, `ledger/RESEARCH_LEDGER.md` | The "full offline re-run" claim is now an *enforced* invariant, not prose |

## What was actually verified

- `SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e030.py` **twice**
  -> **byte-identical** output (offline reproducible). Previously the same
  driver drifted on every run.
- E030 re-pin impact, measured against the old golden: 1490 numeric
  differences, **0 structural**; 33 beyond rel_tol 1e-4; **max absolute
  delta 1.0e-04** (a 4-dp correlation entry); `n_gates_passed` 2 -> 2; all
  five gate `pass` flags identical; decision `REJECT` -> `REJECT`.
- `python3 scripts/check_data_coverage.py` -> `ALL 35 PINNED DATA INPUTS ARE
  PRESENT, TRACKED AND UNCHANGED`.
- `python3 scripts/check_json_artifacts.py` -> exit 0 on the clean tree; exit
  **1** on a deliberately malformed artifact in a scratch repository (the
  failure mode that was previously impossible).
- `python3 -m unittest tests.test_data_coverage` -> 13 tests, OK.
- `SEED=42 bash scripts/check.sh` -> **ALL CHECKS PASSED**.
- **Full quick verification suite in a fresh isolated copy of the committed
  tree, with the new `QUANT_RESEARCH_OFFLINE=1` gate** (i.e. the whole
  suite ran with no network access):
  `check_json_artifacts` PASS, `test_json_guard` PASS, `check_goldens_clean`
  PASS, `check_golden_baseline` PASS, `test_golden_baseline` PASS,
  `verify_convention_robustness` PASS, `batch_run` PASS, `validate` PASS,
  and the 5a drivers E012 / E023 / **E024** / E027 / E035 / **E037** / E039
  / E042(quick) all PASS; `run_e042_lead.py` FAIL (20 mismatches — see
  *What remains unresolved*; this failure is **pre-existing** and reproduces
  byte-identically in a copy of the repository as it was before this
  session's changes). E024 and E037 are the two drivers that consume the
  newly pinned inputs (E024 the bounded raw panel, E037 the 2026-10-11
  large_liquid and SPY panels), and both reproduce their committed goldens.
- E024 re-run with the bounded raw download -> `match (excl ('timestamp',),
  numeric_tol=1e-04)`, confirming the bounding changes no number.
- The static resolver currently resolves **100 %** of the drivers' data call
  sites (0 unresolved), including universe-selected requests,
  comprehension-built ticker lists and `UNIVERSES[...]` dispatch. This is
  asserted by a test, so a future driver that adds a request without pinning
  it fails the check rather than silently downloading.

## What remains unresolved

- **The E042 *lead* artifact does not reproduce — pre-existing, and it breaks
  the primary (quick) verification gate.** `run_all_verification.py` reports
  `OVERALL: FAILURES DETECTED`; the only failure is
  `run_e042_lead.py` -> `e042_lead_config_confirmatory.json` (20
  mismatches, e.g. `/placebo_constrained/z_score` 1.9568 -> 1.6381 and
  `/primary/equity_beta` -0.0009 -> 0.0352). **This is not a regression
  from E048**: an isolated copy of the repository exactly as it was at the
  start of this session (original code, original data) produces the
  byte-identical mismatch list. The sharpest evidence that this is a
  *computation* drift and not a data problem: the committed E042
  sensitivity grid records the lead configuration with
  `equity_beta = -0.0009023438936704533` — the identical value the lead
  golden records in `/primary/equity_beta`. The grid and the lead artifact
  were mutually consistent when they were produced; today the same config
  on the same pinned inputs yields `+0.0352`. The suspect is the
  `max_sharpe` branch of `src/portfolio_opt.py` (the tangency QP
  `min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y` solved with SLSQP at
  `ftol=1e-12`, a flat and often near-degenerate feasible set).
  **Not fixed here** — see the next task.
- **E041 is not explained by the cache-coverage defect and is still open.**
  Its input (`data/AAPL_ABBV_…_5549a49c92b76287_2014-01-01_2026-10-12.parquet`)
  was **already committed and unchanged**, so its 7602 numeric + 3 structural
  differences cannot be a cache-coverage problem. The 3 structural
  differences are the documented `8 of 96` -> `7 of 96` multiple-testing
  count, the `top_configs` count, and one config's `method`. It is very
  likely the *same* `max_sharpe`/SLSQP mechanism as the E042 lead finding
  (E041 is the 96-config market-neutral grid whose `8 of 96` count the lead
  driver consumes).
- The CI workflow `.github/workflows/verification-gate.yml` still needs a
  maintainer to create it via the GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`). Outside agent scope.
- The `2026-10-11` panels now committed are the snapshots yfinance served on
  2026-10-20. They are *not* the panels that produced the pre-E048 goldens
  for E028/E029/E034/E036/E037 (those were downloaded on 2026-10-12/13). The
  difference is ~1e-6 and those drivers still reproduce within the 1e-4
  tolerance (E037 re-verified below), but it is the reason the drift report
  must be re-measured rather than assumed.
- The E047 handoff states that the quick suite reported "OVERALL: ALL CHECKS
  PASSED". That is not what the suite reports now, and the difference is the
  E042-lead failure above, which is present in a pristine copy of the
  repository. The claim should be treated as unverified rather than as
  evidence that the suite is green.

## Approaches already tried and rejected

- **Re-pinning the E030 golden without pinning the input.** Rejected: it
  would replace an unreproducible artifact with a *different* unreproducible
  one (the next run would download a third panel). The input had to be
  pinned first.
- **Aligning the drivers' `end="2026-10-11"` to the pinned vintage
  (`2026-10-12`) so the already-committed panels would be reused.** Rejected
  on scope: it touches 7 driver sources and would have changed 6 panels'
  provenance, for ~35 MB. The two cache keys resolve to the same trading
  days, so the alternative is numerically inert, but editing pre-registered
  driver code is a larger blast radius than adding data files.
- **Letting the guard read the cache-key rule from a copy of the logic in
  `src/data.py`.** Rejected: the rule is now in `src/cache_keys.py` and
  imported by `src/data.py`, so the audit cannot drift from the
  implementation. A unit test pins the parity.
- **A full static dataflow resolver for the driver call sites.** Rejected as
  over-engineering: a bounded AST evaluator (literals, module constants,
  `UNIVERSES[...]`, comprehensions, function-parameter binding, loop
  expansion) resolves 100 % of the call sites today, and anything it cannot
  resolve is reported as "not statically audited" rather than guessed.

## One precise next task

**Root-cause the `max_sharpe` optimizer path in `src/portfolio_opt.py` and
decide whether the E042 lead artifact or the solver is authoritative.** This
breaks the *primary* verification gate, so it outranks E041 (which only
affects the extended block). Evidence and constraints:

- Reproduce in isolation (never in the canonical tree):
  `SEED=42 python3 experiments/run_e042_lead.py` in a scratch copy; compare
  `experiments/e042_lead_config_confirmatory.json` against the committed
  golden. Expected: the same 20 mismatches, with
  `/primary/equity_beta` = 0.0352 instead of the committed
  -0.0009023438936704533.
- Cross-check the grid: `experiments/e042_sensitivity_grid.json` still records
  the lead config with `equity_beta = -0.0009023438936704533` and
  `oos_sharpe = 0.8659374781071205`. Re-evaluating *that one config* with
  today's code should reproduce the grid's value if the grid is authoritative,
  or give 0.0352 if the solver is. This is the decisive experiment and it
  costs one config, not 96.
- The mechanism to test: `optimize_portfolio_weights(..., method="max_sharpe")`
  solves the tangency QP `min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y`
  with SLSQP (`ftol=1e-12`, `maxiter=500`). The equality constraint plus
  `y >= 0` leaves a flat, often near-degenerate feasible set, so a different
  local optimum gives a materially different equity beta. Compare the
  objective value and the constraint residuals of the solver's answer against
  the grid's recorded answer: if the objectives are equal to solver
  tolerance, the portfolio is a *near-tie* and the artifact is
  ill-conditioned rather than wrong; if the fresh solution has a strictly
  better objective, the solver used to be finding a worse local optimum and
  the code changed.
- Also check `src/portfolio_opt.py`'s git-visible history for changes to the
  `max_sharpe` branch after the E042 grid and lead artifacts were produced
  (the repository is a single squashed commit, so the history may have to be
  inferred from the ledger's E041/E042/E044 entries).
- Bounded, verifiable deliverables: (a) a one-line ledger note stating
  whether the lead/grid inconsistency is a near-tie (ill-conditioning) or a
  solver regression; (b) if it is a near-tie, leave the goldens alone and
  document it; (c) if it is a solver regression, decide deliberately whether
  to re-pin the affected artifacts (E042 grid + lead, and possibly E041) or
  to restore the previous solver behaviour — and record that decision in the
  ledger, because it changes published numbers.
- Constraints: `SEED=42`; do **not** weaken the 1e-4 comparison tolerance;
  do **not** silently replace a golden (use
  `python3 scripts/check_golden_baseline.py --update` and record it in the
  ledger); run the work in an isolated copy so the canonical goldens cannot
  be captured mid-run; do not move any pre-registered gate; keep the
  `QUANT_RESEARCH_OFFLINE=1` gate enabled when re-running the suite (all
  inputs are now pinned, so a green run proves no network use).

### Constraints for the next session

- `SEED=42`, pinned `2026-10-12` **and** `2026-10-11` cache vintages.
- The committed golden is the authoritative record; re-pinning is deliberate
  and must appear in the diff (`scripts/check_golden_baseline.py --update`).
- Honor the crash-safety snapshot/restore: never leave a verification run
  half-finished; recover with `python3 run_all_verification.py --restore-only`.
- Every cached input a driver reads must stay committed, git-tracked and
  fingerprinted; add new inputs with
  `python3 scripts/check_data_coverage.py --update` and commit the file.
- The verification suite now runs with `QUANT_RESEARCH_OFFLINE=1`: a driver
  that needs an unpinned input fails with `OfflineDataUnavailable` instead
  of downloading. Do not "fix" that by disabling the gate.
