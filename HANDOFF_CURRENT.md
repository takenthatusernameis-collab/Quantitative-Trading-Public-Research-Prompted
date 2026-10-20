# Session Handoff

## What changed
- **Assigned task executed**: the quick verification suite was run and
  `scripts/check.sh` was confirmed green. The suite failed exactly one driver
  (`run_e042_lead.py`) with a *material* divergence, which exposed that the
  previously recorded diagnosis ("BLAS/numpy floating-point drift") was wrong:
  the divergences are **input-data-vintage** divergences, measured and
  reproduced this session (ledger **E045**).
- **`scripts/audit_data_vintage.py`** (new, fast, offline) — audits the data
  cache provenance: pinned vintage, panel inventory (committed vs session
  downloads), committed-panel label/content integrity, the panel each driver
  needs and whether it is committed, and the last observation date of every
  cached FRED series. `--strict` fails on an uncommitted driver input.
- **`run_all_verification.py`** — added `diff_records()`; the suite now reports
  `STRUCTURAL DIFF` and `NUMERIC DRIFT` separately with the magnitude and
  flags a `MATERIAL DIVERGENCE` at relative deviation >= 1e-2. The
  accept/reject rule is unchanged (`numeric_tol=1e-4`); the banner prints the
  resolved data vintage.
- **`tests/test_verify_diff_records.py`**, **`tests/test_audit_data_vintage.py`**
  (new, 13 unit tests); `scripts/check.sh` runs the new audit and both modules.
- **`ledger/RESEARCH_LEDGER.md`** — new entry **E045**. **`README.md`** and
  **`AGENTS.md`** — corrected the E042b reproducibility claim and documented
  the incomplete cache + the new divergence classes.

## What was actually verified (evidence)
- `SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED (exit 0).
- `SEED=42 python3 run_all_verification.py` (quick, ~13 min) → 13/14 steps
  PASS; only `run_e042_lead.py` FAILs (now correctly labelled as a material
  numeric divergence instead of "STRUCTURAL/STRING DIFF").
- Fresh-vs-fresh determinism: `run_e042_lead.py` and `run_e034.py` each run
  twice → bit-identical; `run_e034.py` vs its golden → 0 diffs. The code is
  deterministic.
- The E042b golden is reproduced to 1.1e-9 relative by a price panel ending
  2026-10-19, which the repo does **not** commit; under the committed
  2026-10-12 vintage the driver produces OOS 0.82187 / equity_beta +0.03524 /
  placebo z 1.64. No single data state reproduces the whole baseline.
- `scripts/audit_data_vintage.py` → E028, E029, E034, E036, E037 read panels
  that are not committed (network download at run time); E029 additionally
  reads live yfinance fundamentals (140 diffs vs its golden today).
- `experiments/` untouched (`check_goldens_clean.py`: ALL COMMITTED GOLDEN
  ARTIFACTS MATCH HEAD); no golden, tolerance, gate or decision changed.

## What remains unresolved
- The committed baseline is **not reproducible from the committed data**. The
  re-baseline decision (Option A/B/C in ledger E045) is a research decision and
  was deliberately not taken here — it moves recorded numbers.
- E029 has no reproducible input at all (live fundamentals) and needs an
  explicit disposition.
- CI workflow `.github/workflows/verification-gate.yml` still requires
  maintainer creation via the GitHub UI (unchanged repo constraint).

## Failed approaches
- Re-running `--extended` does not "randomise" the failing set: it is
  determined by which driver inputs are pinned (E028/E029/E034/E036/E037 are
  not) and by the session's gitignored `data/` downloads.
- Widening `numeric_tol` or calling the divergences float noise: rejected —
  the code is bit-deterministic and the divergence is ~5%.
- Chasing the exact panel mix behind the E042b placebo block: not worth more
  time; the actionable conclusion (one pinned vintage) is already established.

## One precise next task
Prepare the **Option-A re-baseline dry run** for the maintainer's decision
(do not commit regenerated artifacts yet): run `run_e042_lead.py` and
`run_e042.py --n-sim 50` on the committed 2026-10-12 vintage with `--out` /
in a sandbox, diff them against the current goldens with
`python3 scripts/diff_golden.py --golden <golden> --fresh <fresh> --tol 1e-4`,
and write a one-page decision memo listing, per artifact, the current vs
pinned-vintage values, the changed fields, and whether any gate decision or
recorded conclusion moves (known: none of the promotion conclusions move —
E042b REJECTED 4/5 and E042 PARTIAL 4/5 under both vintages; only the
reported-not-gated 96-config market-neutral count moves, 8/96 → 7/96). Then
obtain explicit maintainer sign-off before regenerating anything.

## Constraints
- `SEED=42`, pinned 2026-10-12 cache vintage (`data/vintages.json`).
- No committed-golden modification, no tolerance/driver/skip changes, no gate
  or recorded conclusion moved without maintainer sign-off + ledger amendment.
- Honor crash-safety snapshot/restore
  (`run_all_verification.py --restore-only`).
- Full detail: `HANDOFF_SESSION_2026-10-20_vintage_diagnosis.md`;
  evidence and reasoning: `ledger/RESEARCH_LEDGER.md` E045.
