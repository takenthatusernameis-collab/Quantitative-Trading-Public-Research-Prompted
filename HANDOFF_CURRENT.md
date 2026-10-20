# Session Handoff

## What changed

**1. Restored the canonical golden baseline (commit `026d109`).**
The empty-message checkpoint commit `1623923` had replaced five committed
artifacts with the output of a verification re-run — the same anti-pattern the
repository already reverted once (`d6042b0` / `9f20def` → `05b5353`).
Evidence that it was a capture and not a research update:
- `experiments/e042_lead_config_confirmatory.json` differed from the published
  artifact **only** in the timing field `runtime_sec` (11.5 → 9.8); every
  recorded research value was unchanged.
- The other four differed only in float noise: ≤3.3e-6 relative on E037's
  SLSQP-optimized fields, 5e-16 on the `batch_run` `in_sample.corr_spy`
  fields — the optimizer-environment sensitivity already recorded in the
  ledger (E042 artifact reconciliation, 2026-10-13/17).
Restored to the published baseline (`510b7ef`). No gate, decision, or quoted
number changes.

**2. Added a pinned-baseline fingerprint guard (this commit).**
`scripts/check_golden_baseline.py` + `ledger/golden_baseline.json`
(SHA-256 per tracked artifact under `experiments/`, 107 files) close the gap
that let the incident happen: `check_goldens_clean.py` compares the working
tree with `HEAD`, so it cannot see a *commit* that replaced the baseline.
The guard is step 0.5d of the verification suite, a first-class step of
`scripts/check.sh`, and is backed by `tests/test_golden_baseline.py` (9
negative tests, run as suite step 0.5e). Re-pinning is a deliberate act
(`--update`) that puts the replacement in the diff.

Docs updated: `AGENTS.md` (Baseline Integrity), `README.md` (verification
guards), `ledger/RESEARCH_LEDGER.md` (E042 artifact-reconciliation note).

## What was actually verified

- `SEED=42 python3 run_all_verification.py` (quick, full suite) →
  **OVERALL: ALL CHECKS PASSED** (17/17 steps, incl. the two new ones);
  working tree clean afterwards, no snapshot pending. This is the end-to-end
  proof that the *restored* baseline still reproduces: `batch_run` output
  matches the restored goldens inside the suite's 1e-9 tolerance and E037
  inside the 1e-4 tolerance.
- `SEED=42 bash scripts/check.sh` → exit 0 (incl. 108 JSON artifacts parse,
  107 pinned artifacts match, 22 guard unit tests).
- Live demonstration of the new guard: writing the drifted E037 Sharpe into
  `experiments/e037_portfolio.json` → guard exits 1 with the pinned/actual
  digests; `git checkout -- experiments/` → exits 0 again.
- Reproduction evidence gathered in this environment: `batch_run` reproduces
  the *post-`1623923`* values bit-for-bit and is stable across
  `PYTHONHASHSEED` 1/12345/999; `run_e037.py` reproduces the post-`1623923`
  values bit-for-bit; `run_e042_lead.py` reproduces the *published* values
  bit-for-bit except `runtime_sec` (11.5 published / 9.8 captured / 11.1
  fresh) — i.e. the two artifact sets come from two different environments
  and neither is "the" re-run output of this one.

## What remains unresolved

- CI workflow `.github/workflows/verification-gate.yml` still requires
  maintainer creation via the GitHub UI (outside agent scope; template at
  `.github/workflow-templates/verification-gate.yml`).
- Extended verification (`--extended`) remains environment-nondeterministic
  (SLSQP/BLAS drift on E011/E029/E030/E041); accepted per ledger disposition.
  The pre-existing 23/26 expectation in the previous handoff is unchanged by
  this session — the restored artifacts are within tolerance of a fresh run.
- `experiments/VERIFICATION_FINAL.json` is a stale verification *report*
  living in the golden directory (it records `git_commit: 510b7ef`). It is
  allowlisted in `check_json_artifacts.py` and pinned by the new manifest.
  Left untouched (deleting/moving committed artifacts is not this session's
  scope) — a candidate cleanup for a future session.

## Failed approaches / dead ends

- Restoring the published baseline was checked against the suite's tolerances
  before committing: the worst deviation is 3.3e-6 relative (E037), far inside
  the 1e-4 driver tolerance, and the `batch_run` files deviate by 5e-16,
  inside the 1e-9 batch tolerance. No re-run of the drivers is required to
  justify the restore.
- Considered but rejected: blessing the `1623923` values because they are
  what this environment reproduces. The ledger's standing disposition is
  that *the committed golden is the authoritative record, not the latest
  re-run*; blessing them would have contradicted the documented policy and
  left the provenance of the artifacts unexplained.
- Considered but rejected: pinning the driver sources (`experiments/*.py`)
  as well. They are code (reviewed by the ordinary diff), and pinning them
  would turn every comment edit into a manifest update.



## Extended verification results (this session)

Ran:
```bash
SEED=42 python3 run_all_verification.py --extended
```

Outcome (from suite summary): **OVERALL: FAILURES DETECTED** — 23/26 driver comparisons passed (exit codes ok where appropriate; e.g. e042_lead failed gates but matched). The expected environment-nondeterministic failures were reproduced:
- `[FAIL] run_e029.py (exit 0 + structural match (numeric_tol=1e-4))` — 140 mismatches (fundamentals/data availability issues noted in driver output)
- `[FAIL] run_e030.py (exit 0 + structural match (numeric_tol=1e-4))` — 28 mismatches
- `[FAIL] run_e041.py (exit 0 + structural match (numeric_tol=1e-4))` — 357 mismatches across artifacts (optimization/grid sensitive to environment)

All other extended drivers matched within tolerance; quick/full blocks all passed. Snapshot recovered after the background process; working tree clean at end of suite run. **Goldens and tolerances unchanged** (no re-pinning). This matches the pre-existing 23/26 expectation documented in the prior handoff.

## One precise next task

The extended verification has been run and recorded above. No further action required on this specific task. If continuing work, consider either (1) investigating the environment causes of E029/E030/E041 drift to see if tolerances can be tightened safely without weakening policy, or (2) moving to another high-value bounded task from the ledger. Any changes to goldens/tolerances must follow the documented policy (deliberate re-pinning with justification in diff).

## Constraints (unchanged)

- `SEED=42`, pinned 2026-10-12 cache vintage.
- No committed-golden modification; no tolerance/driver/skip changes.
- Honor the crash-safety snapshot/restore
  (`python3 run_all_verification.py --restore-only`).
