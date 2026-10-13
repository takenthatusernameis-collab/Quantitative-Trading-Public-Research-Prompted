# Handoff for Next Agent (v1.2.3 Release Baseline Restored + Golden Regeneration)

## Session Summary

**Date**: 2026-10-13
**Goal**: Execute the prior agent's assigned next task (HANDOFF.md
step 4: re-run `SEED=42 python3 run_all_verification.py --full`
after the v1.2.3 tag; completion = exit 0, all 4 checks PASS,
exact golden match).

**Bottom line**: The gate initially **FAILED**, exposing two real
defects in the release baseline. Both are now fixed, the goldens
were regenerated under the **committed** 2026-10-12 cache vintage,
and the gate now **PASSES** (exit 0, all 4 checks, exact golden
match, quick mode too). The research conclusions are unchanged:
E042 remains PARTIAL (4/5, G2 placebo-significance FAIL) and the
market-neutral-total-portfolio line remains CLOSED.

---

## What Was Found (evidence, not claims)

1. **Corrupted release golden (post-tag commit `3e33085`, empty
   message).** `experiments/e042_minvar_market_neutral.json` had
   been overwritten by a **quick-run artifact** (`n_sim=2`,
   placebo z=4.91, decision "VALIDATED" 5/5) — contradicting the
   recorded release result (n_sim=50, z=1.95, PARTIAL 4/5). The
   prior session's last action (a `--n-sim 2 --no-sensitivity`
   run at 07:11) had silently written its output into the canonical
   golden path, and it was committed with an empty message.
   * Root cause #1: `experiments/run_e042.py` wrote **every** run
     to the canonical golden path, including the documented
     quick-start command.
   * Root cause #2: `verify_convention_robustness.py::verify_e042`
     asserted **nothing** — it echoed whatever the JSON contained
     and printed a hardcoded "✓ PASS (REJECTED as expected)", so
     it silently "passed" while printing "Gates passed: True
     (5/5)".
2. **Vintage mismatch (the gate failure).** The v1.2.3 goldens
   were generated under the *original* pin (`default_end_date:
   2026-10-13`, a network-fetched parquet cache that is gitignored
   and therefore **not part of the committed archive**). The pin
   was later corrected to the **committed** cache vintage
   (`2026-10-12`, commit d2021bc). Fresh runs under the current
   pin are fully deterministic but differ from the goldens →
   `run_all_verification.py --full` failed on all 4 checks
   (batch_run: 13 JSON diffs; validate: 74 mismatches; e042:
   9712 + 360 mismatches; placebo z 1.72 vs golden 1.95).
   * Evidence: parquet inventory + mtimes — 2026-10-13 caches
     created 06:45 (network fetch, untracked); 2026-10-12 caches
     created 07:01–07:09 (after the pin fix); placebo seeding is
     deterministic (`np.random.default_rng(SEED=42)`), so the
     shift is entirely the one-day-shorter sample.

## What Changed This Session

1. **Restored** `experiments/e042_minvar_market_neutral.json`
   from the `v1.2.3` tag (intermediate step; superseded by the
   regeneration below).
2. **`experiments/run_e042.py`** — added `--out`; quick/non-primary
   runs (n_sim != 50 or `--no-sensitivity`) now default to
   `experiments/e042_minvar_market_neutral_quick.json` with a
   loud NOTE; the canonical golden path is reserved for the full
   pre-registered config. The release golden can no longer be
   silently corrupted by a quick run.
3. **`verify_convention_robustness.py`** — `verify_e042` now
   **asserts the recorded release invariants** (n_sim=50, OOS
   Sharpe 0.979, placebo z 1.72, beta +0.094, bear +1.967,
   turnover 0.0043, 4/5 gates with G2 FAIL, decision PARTIAL).
   Proven to reject the corrupted 2-sim artifact (n_sim != 50
   assertion fires).
4. **Regenerated all suite-gated goldens under the committed
   2026-10-12 vintage** (`SEED=42`, offline cache hits):
   `batch_run` (16 JSONs), `validation_summary.json`,
   `e042_minvar_market_neutral.json` + `e042_sensitivity_grid.json`
   (full n_sim=50 + 96-config grid), and
   `e042_lead_config_confirmatory.json` (E042b). Only the two G2
   placebo point estimates shifted at printed precision — primary
   z 1.95 → **1.72** (mean 0.748, std 0.134) and E042b lead
   z 1.50 → **1.96** (mean 0.572, std 0.150); both remain
   < 3.0. Every gate boolean, both decisions (PARTIAL 4/5 /
   REJECTED 4/5), FE1/FE2 results and all other printed numbers
   are unchanged.
5. **`run_all_verification.py`** — quick mode passes `--out`
   explicitly and compares the `_quick.json` output; the `finally`
   block now removes run-created JSON files so the tree is left
   exactly as found; stale vintage date (2026-10-13) in the
   docstring corrected to 2026-10-12.
6. **Docs** — README.md, RELEASE_NOTES.md and
   ledger/RESEARCH_LEDGER.md updated to the regenerated values;
   ledger §E042 gained **Erratum 2** documenting the vintage
   reconciliation; `experiments/run_e042_lead.py` docstring z
   corrected.

## What Was Actually Verified (evidence)

| Check | Command | Result |
|-------|---------|--------|
| Convention asserts | `SEED=42 python3 verify_convention_robustness.py` | exit 0; E042 z=1.72 vs target 1.72, PARTIAL 4/5 ✓ |
| Corruption detection | new asserts vs `git show 3e33085:...json` | "CORRUPTION DETECTED: placebo n_sim = 2" ✓ |
| Quick-run guard | `SEED=42 python3 experiments/run_e042.py --n-sim 2 --no-sensitivity` | wrote `_quick.json`; golden untouched ✓ |
| Lead reproducibility | `SEED=42 python3 experiments/run_e042_lead.py` (twice) | z=1.9578 identical; exit 1 = deliberate REJECTED code ✓ |
| **Full gate** | `SEED=42 python3 run_all_verification.py --full` | **ALL 4 CHECKS PASSED**, 16 batch_run JSONs + validation_summary + e042 minvar + sensitivity grid all **EXACT match** (excl timestamp), exit 0 ✓ |
| Quick gate | `SEED=42 python3 run_all_verification.py` | ALL 4 CHECKS PASSED; `_quick.json` created, compared, removed ✓ |

Logs: `/tmp/verify_full_final.log` (full), `/tmp/verify_quick_final.log`
(quick), `/tmp/verify_full_v123.log` (the initial failing run —
kept as evidence of the vintage mismatch).

## What Remains Unresolved

- **Clone-reproducibility gap (pre-existing, structural).** The
  parquet files the code actually requests (cache key with no
  suffix, `auto_adjust=True`) are **gitignored** working-tree
  files; the 14 parquet files committed in the release carry a
  `.adj0.act1` suffix (a different download config the code never
  requests) and are never read. A fresh clone therefore cannot run
  the verification suite offline without one network-populated
  cache build. This archive's convention is "cached data present
  in the working tree" (documented in RELEASE_NOTES); the gap is
  recorded here for the next agent (see next task).
- **Non-gated experiment JSONs (E016–E024, E041, etc.) remain
  recorded at the 2026-10-13 vintage.** They are not part of the
  automated gate and their quoted headline numbers are unchanged at
  printed precision (verified: only 4th-decimal shifts). If
  byte-exact vintage consistency across *all* artifacts is
  required, they need the same regeneration pass (~30–40 min) or
  `END_DATE=2026-10-13` with a re-download.
- **Commit `3e33085` (empty message, corrupted golden) remains in
  origin/main history.** It is pushed; history was not rewritten.
  The restoration is a new commit on top.

## Approaches Already Failed and Why

- **Trusting the tag's golden as the release baseline** (initial
  assumption): failed because the golden was generated under a
  transient, gitignored 2026-10-13 network cache, while the pin
  and committed cache are 2026-10-12. Evidence: the full suite
  failed with 9712+360 mismatches; parquet mtimes + gitignore
  analysis confirmed the vintage split.
- **Reverting the pin to 2026-10-13 instead of regenerating**:
  rejected — under a 2026-10-13 pin the futures-panel and
  macro caches (keyed 2026-10-12) would miss and force a network
  download, breaking offline reproduction. Regenerating the
  goldens under the committed vintage is strictly more robust.
- **Warning-only fix for the quick-run overwrite path**: rejected
  — a warning does not prevent `git add -A` from committing the
  corruption; the output-path separation does.

## One Precise Next Task (for the following agent)

**Decide and implement the archive's clone-reproducibility policy.**

The verification suite is offline-reproducible in *this* archive
working tree but not from a fresh clone, because the parquet
caches the code requests are gitignored (`data/*.parquet`) while
the committed `.adj0.act1` files are never requested. Two bounded
options:

- **(a) Commit the real caches** (~21 MB: the no-suffix
  2026-10-12 `large_liquid` combined file 17.6 MB, `SPY` 0.17 MB,
  futures panel 3.0 MB, `SPY_IEF_GLD`, `fred_*`): adjust
  `.gitignore` (e.g. negate `data/*.parquet` for the 2026-10-12
  vintage set or track them explicitly), `git add -f`, then
  re-run `SEED=42 python3 run_all_verification.py --full` on a
  clean checkout to prove clone-and-run works. Cost: ~21 MB in git.
- **(b) Document the one-time cache-population step** in
  RELEASE_NOTES.md (zero code change): state that a fresh clone
  must run once with network access (no `SEED`) to build the
  cache, after which `SEED=42` reproduction is offline.

Recommendation: **(a)** if the archive must be clone-and-run
(self-contained release artifact); **(b)** if the working-tree
archive convention is acceptable. Either way, also consider
regenerating the non-gated experiment JSONs (E016–E024, E041)
under the 2026-10-12 vintage for full-repo consistency, and
giving the restoration commit in this session a follow-up note if
any number here is re-derived.

**Prerequisite**: commit/tag permission per repo workflow rules.
Completion criterion for (a): `git clone` to a fresh dir,
`SEED=42 python3 run_all_verification.py --full` → exit 0, all 4
checks PASS, exact golden match, with no network access.

## Key Files

- `experiments/run_e042.py:733-748` — `--out` arg + full-config
  output-path guard.
- `verify_convention_robustness.py:107-140` — asserting E042
  release invariants.
- `run_all_verification.py:258-300` — quick-mode `--out`, compare
  path, run-created-file cleanup.
- `data/vintages.json` — pinned `default_end_date: 2026-10-12`
  (the committed cache vintage).
- `ledger/RESEARCH_LEDGER.md` §E042 Erratum 2 — vintage
  reconciliation record.
- Golden artifacts: `experiments/e042_minvar_market_neutral.json`
  (z=1.72, PARTIAL 4/5), `experiments/e042_sensitivity_grid.json`,
  `experiments/e042_lead_config_confirmatory.json` (z=1.96,
  REJECTED 4/5), `experiments/*_large_liquid.json`,
  `experiments/summary.json`, `experiments/validation_summary.json`.
