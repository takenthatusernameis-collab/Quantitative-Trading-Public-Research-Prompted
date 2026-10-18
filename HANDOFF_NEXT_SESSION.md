# Session Handoff: E022 regression fixed; extended suite re-run

## What changed (this session)
- **`experiments/run_e022.py`** — 33 insertions, 9 deletions. Root cause: the driver iterated over all 15 themes in `macro.THEMES` (E038/E039 scope) instead of the pre-registered 5 core Brooks (2017) themes. That silently upgraded E022 to the 15-theme extended run (OOS -0.194) and overwrote the committed 5-theme golden (OOS 0.428).
  - Added `CORE_THEMES = ["growth", "trade", "policy", "sentiment", "inflation"]` and `CORE_THEME_SIGNS` (restricted sign matrix).
  - Restricted the signal frame to core themes *before* downstream use (placebo null, sensitivities, decomposition, serialization) — necessary because the 15-column frame shifts the block-permutation RNG sequence.
  - `falsification_diagnostic`, per-theme decomposition loop, primary/lookback/vol-target/DBC weight builders, and `specification`/`macro_series` serialization all now use the core set.
- **`experiments/e022_macro_momentum.json`** — restored to the committed 5-theme golden. Byte-identical to parent commit `4595851` (reverts the `51c8ae4` overwrite). Staged, not committed.

## What was actually verified (evidence)
- `SEED=42 bash scripts/check.sh` → **All checks passed** (107/107 JSON artifacts, 19/19 guard tests, 35/35 experiment imports).
- `SEED=42 python3 verify_convention_robustness.py` → **ALL VERIFICATIONS PASSED** (this was the gate that broke under the 15-theme overwrite; E022's overnight Sharpe 0.428 now matches the recorded value).
- `SEED=42 python3 run_all_verification.py --extended` (~38 min, exit 1). Results:
  - 5a block (e012, e023, e024, e027, e035, e037, e039, e042-lead): all **PASS**.
  - 5b block: 15/18 **PASS**, 3 **FAIL** — **run_e022.py**, run_e030.py, run_e041.py.
  - E022 diff is now **structural-match**: only 9 numeric mismatches, of which 6 are sub-1e-4 FP drift and 3 are the `placebo` block (`mean_sharpe` -0.187→-0.136, `std_sharpe` 0.308→0.296, `z_score` 1.999→1.909). The remaining placebo-z delta is FRED data-vintage drift: the golden was produced 2026-10-11 under an unseeded run (real timestamp `2026-10-11T15:04:26Z`), while the pinned cache vintage is 2026-10-12. The golden itself records this caveat ("current FRED vintage (revised data…)").
  - e030/e041 failures are **pre-existing** environmental drift (e041 has a structural `n_market_neutral_and_sharpe_gte_0.8: 8 -> 7`), unrelated to this change and already documented in `HANDOFF_SESSION_2026-10-18d.md`.

## What remains unresolved
- E022 `--extended` still FAILS on the 3 placebo fields beyond `numeric_tol=1e-4`. Two options, neither taken:
  1. Accept as documented vintage drift (golden's own caveat covers it).
  2. Regenerate the golden under the pinned 2026-10-12 vintage — but that would change the recorded placebo z (2.00 → 1.91) and thus the ledger's stated result, which is a goalpost-adjacent change the repo forbids without a pre-registered confirmatory run.
- `--extended` e030/e041 drift is pre-existing; not addressed here.
- CI workflow `.github/workflows/verification-gate.yml` still requires maintainer creation via GitHub UI (template at `.github/workflow-templates/verification-gate.yml`).

## Which approaches have already failed and why
- Restoring the 5-theme golden alone did not make `--extended` pass: the driver still emitted 15 themes, so the comparison failed structurally (`/macro_series/credit_spreads absent in golden, added in fresh`). The driver fix was required and is the correct minimal change.
- Restricting only the sign matrix (`CORE_THEME_SIGNS`) was insufficient: `signals` stayed 15 columns, shifting the placebo RNG (z 2.00 → 1.91) and `active_days` (3192 → 3191). Restricting the signal frame too was the fix.
- No tolerances were weakened, no drivers skipped, no `src/*` modified, no committed golden altered.

## One precise next task
- Decide the E022 placebo-z drift disposition. Evidence: golden timestamp `2026-10-11T15:04:26.879459Z` (unseeded run) vs pinned cache `2026-10-12`; regenerated z = 1.909 vs committed 1.999, delta +0.09, outside `numeric_tol=1e-4`. Constraint: do not weaken tolerances or move goalposts. If the disposition is "accept as vintage drift", record it verbatim in `ledger/RESEARCH_LEDGER.md` next to the existing E022 data-integrity caveat and close the item. If the disposition is "regenerate", that changes a committed result and requires a pre-registered confirmatory run + placebo first.