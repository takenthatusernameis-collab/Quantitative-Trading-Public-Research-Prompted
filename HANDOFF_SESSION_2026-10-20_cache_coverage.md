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
- E024 re-run with the bounded raw download -> `match (excl ('timestamp',),
  numeric_tol=1e-04)`, confirming the bounding changes no number.
- The static resolver currently resolves **100 %** of the drivers' data call
  sites (0 unresolved), including universe-selected requests,
  comprehension-built ticker lists and `UNIVERSES[...]` dispatch. This is
  asserted by a test, so a future driver that adds a request without pinning
  it fails the check rather than silently downloading.

## What remains unresolved

- **E041 is not explained by this defect and is still open.** Its input
  (`data/AAPL_ABBV_…_5549a49c92b76287_2014-01-01_2026-10-12.parquet`) was
  **already committed and unchanged**, so its 7602 numeric + 3 structural
  differences cannot be a cache-coverage problem. The 3 structural
  differences are the documented `8 of 96` -> `7 of 96` multiple-testing
  count, the `top_configs` count, and one config's `method`.
- The CI workflow `.github/workflows/verification-gate.yml` still needs a
  maintainer to create it via the GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`). Outside agent scope.
- The `2026-10-11` panels now committed are the snapshots yfinance served on
  2026-10-20. They are *not* the panels that produced the pre-E048 goldens
  for E028/E029/E034/E036/E037 (those were downloaded on 2026-10-12/13). The
  difference is ~1e-6 and those drivers still reproduce within the 1e-4
  tolerance, but it is the reason the drift report must be re-measured
  rather than assumed.

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

**Root-cause E041's drift, now that the cache is no longer a candidate
explanation.** Evidence and constraints:

- E041's input is already pinned and byte-unchanged
  (`ledger/data_baseline.json` lists it; `scripts/check_data_coverage.py`
  passes), so the cause is in the *computation*.
- The 3 structural differences are localized:
  `/sensitivity_grid/...` count `8 -> 7`, the `top_configs` list length
  `8 -> 7`, and one config's `method` string. The "8 of 96" -> "7 of 96"
  multiple-testing note is the downstream consequence.
- The 7602 numeric differences are concentrated in the 96-config grid,
  whose walk-forward optimization runs through `src/portfolio_opt.py`
  (SLSQP). The hypothesis to test: the optimizer's solution is
  ill-conditioned, so a sub-1e-6 perturbation of the *optimizer's* inputs
  (or a different scipy/BLAS path) flips which of the 96 configs clears the
  gate, and the flip cascades into the portfolio weights.
- Bounded, verifiable deliverables: (a) show whether the grid's objective
  values differ by more than the gate margin between two runs of the *same*
  pinned input (i.e. is it bit-level non-determinism inside SLSQP, or a
  genuine near-tie?); (b) if it is a near-tie, say so in the ledger and
  leave the golden alone; (c) if it is solver non-determinism, pin the
  solver path (e.g. a fixed method/`tol`) so the grid is stable — and treat
  that as a *driver change* requiring a deliberate re-pin, not a quiet fix.
- Constraints: `SEED=42`; do **not** weaken the 1e-4 comparison tolerance;
  do **not** silently replace a golden (use
  `python3 scripts/check_golden_baseline.py --update` and record it in the
  ledger); run the work in an isolated copy so the canonical goldens cannot
  be captured mid-run; do not move any pre-registered gate.

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
