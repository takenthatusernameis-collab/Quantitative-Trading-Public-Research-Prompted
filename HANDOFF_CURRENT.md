# Session Handoff

## What changed

1. **Restored the canonical E029 golden** (commit `34396a9`). The pinned
   fingerprint guard was failing at session start: commit `701ed78` (a
   checkpoint commit) had captured an interrupted E029 verification run over
   `experiments/e029_fundamental_factors.json`. Restored from `aa650fe`
   (the last commit whose SHA-256 matches `ledger/golden_baseline.json`);
   the digest now matches the pin. `git checkout -- experiments/` would not
   have fixed it — `HEAD` held the captured run.
2. **Added extended-verification drift reporting** (the task handed over by
   the previous agent): `run_all_verification.py` now writes a deterministic
   report to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored,
   outside `experiments/`). Per driver/artifact it records the number of
   differences, how many are numeric vs structural, the largest relative and
   absolute drift, the worst drift as a multiple of the accepted tolerance,
   and the five worst individual differences. The comparison logic, the
   tolerances and the gate outcomes are untouched.
3. **`tests/test_drift_report.py`** (22 tests) + registration in
   `scripts/check.sh`; `.gitignore` entry for `.verify_reports/`.
4. **Docs**: `README.md` (reproducibility section), `AGENTS.md` (driver
   coverage + baseline-integrity note), `ledger/RESEARCH_LEDGER.md` (new
   E045 entry with the full evidence).

## What was actually verified

- `SEED=42 bash scripts/check.sh` -> ALL CHECKS PASSED (109 JSON artifacts,
  44 unit tests, 35 experiment imports).
- `python3 scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS
  MATCH HEAD. `python3 scripts/check_golden_baseline.py` -> ALL 107 PINNED
  GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT.
- `SEED=42 python3 run_all_verification.py --extended` -> **23/26 PASS, 3 FAIL
  (e029/e030/e041)** — the documented baseline. The run was executed in an
  **isolated copy** of the repository (`/home/runner/work/_temp/kilo-tmp/
  verify-copy`) so the real working tree could not be captured mid-run; the
  copy's goldens were restored by the suite's backup/restore mechanism and
  its `git status` ended clean. The real repo was never modified by it.
- The new report was produced by that run (16 KB) and contains the measured
  drift table quoted below. Copies: the report is in the repository at
  `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) and the
  full run log + the repository copy used for the run are under
  `/home/runner/work/_temp/kilo-tmp/verify-copy/`.

### Measured extended drift (SEED=42, pinned 2026-10-12 vintage, 2026-10-20)

15 of the 18 extended drivers reproduce with **0** differences. The 3 that
drift:

| driver | artifact | diffs | numeric | structural | max rel | max abs | tol multiple |
|---|---|---|---|---|---|---|---|
| run_e029.py | e029_fundamental_factors.json | 140 | 140 | 0 | 3.03e-01 | 8.01e-01 | 3026x |
| run_e030.py | e030_multiasset_tsm.json | 28 | 28 | 0 | 2.89e-02 | 3.11e-04 | 289x |
| run_e041.py | e041_market_neutral_portfolio.json | 357 | 354 | **3** | 1.00e+00 | 1.00e+00 | 10000x |
| run_e041.py | e041_sensitivity_grid.json | 40 | 40 | 0 | 1.57e-01 | 1.92e-01 | 1565x |

- **E029 is not float drift.** E029 re-downloads yfinance quarterly
  fundamentals at run time (only the price cache is pinned), so the
  falsification diagnostics moved materially: blend FE1 frac_pos 0.390 ->
  0.475, GP FE1 frac_pos 0.299 -> 0.429, `/oos_short_tail[2]/sharpe` moved by
  0.80. The decision (DATA-INFEASIBLE) and the structure are unchanged; the
  ledger's E029 entry quotes the **canonical** numbers, which remain
  authoritative.
- **E030 is float-level**: the large relative deltas sit on near-zero
  quantities (total_return ~ -2.2e-05), absolute deltas <= 3.11e-04.
- **E041 fails on 3 structural differences**, not only numeric ones: the
  "8 of 96" -> "7 of 96" multiple-testing note,
  `sensitivity_market_neutral_summary/top_configs` 8 -> 7, and
  `top_configs[6]/method` "max_sharpe" -> "risk_parity" (one grid config's
  realized equity beta crosses the 0.10 bar between environments).

This **corrects** the previous session's handoff, which described E029 as
"float drift on order 1e-7-1e-8" and E041 as "all numeric within tolerance".
The E041 ledger disposition (2026-10-19) carries the same mis-characterisation
of E029's magnitude ("max absolute delta ~0.011"); the E045 ledger entry
records the correction with the measured numbers.

## What remains unresolved

- CI workflow `.github/workflows/verification-gate.yml` still requires
  maintainer creation via the GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`).
- `experiments/VERIFICATION_FINAL.json` is a stale verification report inside
  the golden directory (allowlisted/pinned). Left untouched.
- E029 is not reproducible offline: its numbers depend on a live yfinance
  fundamentals fetch. The committed golden remains the authoritative record,
  but the *ledger's* E029 result numbers (FE1 frac_pos etc.) cannot be
  re-derived from a fresh run.

## Failed approaches / dead ends

- Re-running `--extended` in the repository itself was avoided on purpose:
  the previous session lost an extended run and the next checkpoint commit
  captured its output. This session ran it in an isolated copy instead, and
  separately restored the artifact that a previous capture had already
  committed. Do not re-run `--extended` in-place right before a commit.
- `git checkout -- experiments/` does **not** repair a captured baseline
  (it restores `HEAD`, which may be the capture). Use the pinned digest:
  `git checkout <commit> -- experiments/<file>` where `<commit>` is the last
  one whose SHA-256 matches `ledger/golden_baseline.json`.
- The previous handoff suggested verifying the new reporting with
  `--extended --skip-slow`; that combination never reaches the extended
  block (`--skip-slow` returns before it). The reporting is instead covered
  by unit tests plus the real extended run.

## One precise next task

**Make E029 reproducible offline (or prove it is not), and align the ledger
with the outcome.**

Evidence and constraints:
- `experiments/run_e029.py` fetches yfinance quarterly fundamentals at run
  time; the price cache is pinned to 2026-10-12 but the fundamentals are
  not. A fresh run therefore lands on different falsification diagnostics
  (max relative delta 3.03e-01, max absolute 0.80) even though the
  DATA-INFEASIBLE decision and the whole structure are identical.
- Accepted options, in order of preference:
  1. **Cache and pin the fundamentals snapshot** the way `data/` is pinned
     (a `data/fundamentals_<hash>_<vintage>.parquet` artifact + an entry in
     `data/vintages.json`), so the driver is offline-reproducible; then the
     E029 artifact should reproduce and the extended block should show 16/18
     clean drivers.
  2. If pinning is judged out of scope, **document E029 as a
     network-dependent driver** in the ledger and in the extended-block
     reporting, so a future reader does not mistake its drift for float
     noise.
- Constraints: `SEED=42`, no committed golden altered unless the change is a
  deliberate re-pin (`python3 scripts/check_golden_baseline.py --update`
  puts the replacement in the diff), no tolerance weakened, no goalpost
  moved, and the E029 decision (DATA-INFEASIBLE) must not change on the
  strength of a new data snapshot. If the driver is made offline, the
  `--extended` run must be re-measured and the drift table in
  `README.md` / `AGENTS.md` / the ledger's E045 entry updated to match.

## Constraints (unchanged)

- `SEED=42`, pinned 2026-10-12 cache vintage.
- No committed-golden modification; no tolerance/driver/skip changes.
- Honor crash-safety snapshot/restore (`python3 run_all_verification.py
  --restore-only`).
- Follow repo policy: the golden is authoritative; re-pinning only
  deliberately with justification.
