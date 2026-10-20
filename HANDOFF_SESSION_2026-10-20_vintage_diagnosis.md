# Session Handoff — 2026-10-20 — Baseline reproducibility diagnosis (data-vintage provenance)

## What changed

**Assigned task (from the previous handoff):** run the quick verification suite
and confirm `scripts/check.sh` passes. Done — the suite ran, `scripts/check.sh`
passes, and the single suite failure was diagnosed to its root cause (below).
The prior handoff's diagnosis ("BLAS/numpy floating-point drift") was **wrong**
and has been replaced with a measured one.

**Code / tooling (this session):**

- `scripts/audit_data_vintage.py` (**new**, fast, offline) — data-cache
  provenance audit: pinned vintage, panel inventory by end date (committed vs
  session downloads), committed-panel label/content integrity check, the panel
  each driver needs and whether it is committed, and the last observation date
  of every cached FRED series. `--strict` fails on an uncommitted driver input.
- `run_all_verification.py` — added `diff_records()` (structured counterpart of
  `deep_compare()`): classifies each difference as `numeric` or `structural`
  and carries the absolute/relative deviation. The accept/reject rule is
  **unchanged** (unit-tested equivalent to `deep_compare` on 23 cases at two
  tolerances). Reporting now prints `STRUCTURAL DIFF` and `NUMERIC DRIFT`
  separately with the magnitude, and flags a **MATERIAL DIVERGENCE** at
  relative deviation >= 1e-2. The banner prints the resolved data vintage.
- `tests/test_verify_diff_records.py`, `tests/test_audit_data_vintage.py`
  (**new**, 13 unit tests).
- `scripts/check.sh` — runs the new audit and the two new test modules.

**Documentation:**

- `ledger/RESEARCH_LEDGER.md` — new entry **E045** (full evidence, tooling,
  open decision).
- `README.md` — E042b "provenance correction" bullet + Reproducibility-section
  corrections (the "byte-for-byte" claim was true only against an unpinned
  2026-10-19 session cache).
- `AGENTS.md` — documents that the committed cache is incomplete for five
  drivers and that the suite now separates divergence classes.

## What was actually verified (evidence)

- `SEED=42 bash scripts/check.sh` → **ALL CHECKS PASSED** (exit 0).
- `SEED=42 python3 run_all_verification.py` (quick, ~13 min) → 13/14 steps PASS.
  Only `run_e042_lead.py` FAILS, now reported as `NUMERIC DRIFT ... max abs dev
  4.3e-04, max rel dev 5.3e-02` + `MATERIAL DIVERGENCE` (it used to be
  mislabelled `STRUCTURAL/STRING DIFF ... 20 mismatches`).
- **Fresh-vs-fresh determinism** (same code, same data, `SEED=42`):
  `run_e042_lead.py` twice → bit-identical; `run_e034.py` twice → bit-identical;
  `run_e034.py` vs its golden → **0 diffs**. The code is deterministic.
- **The E042b golden needs a price panel the repo does not commit** (yfinance
  `end` is exclusive, so `end=2026-10-12` = data through 2026-10-09):

  | input price vintage | primary OOS Sharpe | equity_beta | bear_sharpe |
  |---|---|---|---|
  | committed cache (through 2026-10-09) | 0.8218658734663784 | +0.03523997365008045 | 1.9929639142154165 |
  | fresh panel (through 2026-10-16) | 0.8266652094190708 | +0.034975251148301655 | 1.9929626564924945 |
  | fresh panel (through 2026-10-19) | **0.8659385360140676** | −0.0009508228303314658 | 2.2418921986152336 |
  | **committed golden** | **0.8659374781071205** | −0.0009023438936704533 | 2.241896251463706 |

  The golden is reproduced to **1.1e-9 relative** by the 2026-10-19 vintage and
  by no other state tested; `data/` commits only 2026-10-11 and 2026-10-12 panels.
- **No single data state reproduces the baseline**: E042b needs the 2026-10-19
  panel, while `e042_minvar_market_neutral.json` and its 96-config grid are
  closest to the pinned 2026-10-12 vintage (75 and 47 diffs) and move *further*
  away under 2026-10-19 (161 and 218 diffs).
- **Five drivers read uncommitted panels** (`scripts/audit_data_vintage.py`):
  E028, E029, E034, E036, E037 → they download at run time and are not
  offline-reproducible. E029 is worse: `src/fundamentals.py::fetch_fundamentals`
  reads **live** yfinance fundamentals (no cache, no pin) → 140 diffs vs its
  golden today (`fe1_frac_positive` 0.38983 → 0.47458).
- `experiments/` untouched: `scripts/check_goldens_clean.py` → ALL COMMITTED
  GOLDEN ARTIFACTS MATCH HEAD.

## What remains unresolved

- **The committed baseline is not reproducible from the committed data.** The
  re-baseline decision (below) is a research/process decision and was *not*
  taken here: it moves recorded numbers.
- **E029 has no reproducible input** (live fundamentals). It needs an explicit
  disposition (E022-style vintage exception, or a committed fundamentals
  snapshot).
- CI workflow `.github/workflows/verification-gate.yml` still requires
  maintainer creation via the GitHub UI (unchanged, repo/process constraint).

## Failed approaches (do not repeat)

- **Do not re-run `--extended` expecting a different result.** The failing set
  is not random: it is exactly the drivers whose inputs are not pinned
  (E029, E034, and the E042 family) plus whatever the current session's
  gitignored `data/` downloads contain. Re-running only re-samples the
  network downloads.
- **Do not treat the divergences as BLAS/float noise** and do not widen
  `numeric_tol` — the E042b divergence is ~5% in `oos_sharpe` and 5.3e-2
  relative in `equity_beta`; that is a different computation (different input
  vintage), and the code is proven bit-deterministic.
- **Do not "fix" the failure by regenerating goldens** without the maintainer's
  Option-A decision (below): that is exactly the goalpost move the repo
  forbids, and it must be pre-registered as a re-baseline.
- Chasing the exact panel mix behind the E042b placebo block
  (mean_sharpe 0.5721 → 0.5796, z 1.9568 → 1.8964 under the closest
  reconstructable state) is **not worth more time**: the actionable conclusion
  (re-baseline under one pinned vintage) is already established.

## One precise next task

**Prepare the Option-A re-baseline dry run for the maintainer's decision** —
do not commit the regenerated artifacts yet:

1. `SEED=42 python3 experiments/run_e042_lead.py` and
   `SEED=42 python3 experiments/run_e042.py --n-sim 50` on the **committed
   2026-10-12 vintage**, each with `--out`/a sandbox so the committed goldens
   are not touched, and diff them against the current goldens with
   `python3 scripts/diff_golden.py --golden <golden> --fresh <fresh> --tol 1e-4`.
2. Write a one-page **decision memo** (ledger E045 follow-up) listing, per
   affected artifact: the current golden values, the pinned-vintage values,
   the changed fields, and whether any **gate decision or recorded research
   conclusion** changes. Known so far: the E042b decision is REJECTED (4/5)
   under both vintages (G2 fails at z 1.64 and at z 1.96, bar 3.0) and the
   E042 decision is PARTIAL (4/5) under both (z 1.601 → 2.11, bar 3.0), so
   **no promotion conclusion moves**; the reported-not-gated 96-config
   "market-neutral count" does move (8/96 → 7/96).
3. Get the maintainer's explicit sign-off, then regenerate the artifacts under
   the pinned vintage in one commit with a ledger amendment.

Decision options for the maintainer (ledger E045):
- **Option A (recommended)** — re-baseline under the pinned 2026-10-12 vintage:
  regenerate the affected artifacts on the committed cache, amend the ledger.
  Fully offline, no new data committed, one vintage for every artifact.
- **Option B** — re-pin to 2026-10-19 and commit that cache (~150 MB): fixes
  E042b but not the E042 main artifact; the 2026-10-12 artifacts still need
  regeneration.
- **Option C** — keep the baseline, formalise the divergence classes (status
  quo + this session's tooling): the suite stays red on the E042 family and
  E029 with an explicit cause.

Option A additionally needs a decision for E029 (vintage-unstable disposition
like E022's, or a committed fundamentals snapshot).

## Constraints

- `SEED=42`, pinned 2026-10-12 cache vintage (`data/vintages.json`).
- No committed-golden modification, no tolerance/driver/skip changes, no gate or
  recorded conclusion moved without maintainer sign-off and a ledger amendment.
- Honor crash-safety snapshot/restore; never leave a verification run
  half-finished (`run_all_verification.py --restore-only`).
- Keep `data/` clean of committed junk: this session added gitignored session
  downloads under `data/` (two `…_2026-10-11.parquet` panels). They are
  ignored by git, but they change what a later run downloads — delete them if
  a clean-cache measurement is wanted.
