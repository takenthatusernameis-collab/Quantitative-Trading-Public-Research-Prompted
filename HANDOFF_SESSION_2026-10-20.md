# Session Handoff 2026-10-20 (E047)

## What changed

No code, no golden, no gate, no decision changed. One documentation defect
found and corrected against direct artifact comparison (commit pending).

**`README.md`** — the reproducibility section carried a retracted caveat that
contradicted itself:

- Old (README:1024-1042, written in `510b7ef` before the 2026-10-12 cache
  vintage was pinned, never re-measured for E042): "E041/**E042** sensitivity
  grids are environment-sensitive ... `run_e041.py` and `run_e042.py --n-sim
  50` do **not** reproduce their committed goldens byte-for-byte".
- This directly contradicted README:943-955, which states `run_e042.py
  --n-sim 50` reproduces **both** E042 goldens **byte-for-byte (0 diffs)**.
  E044 (2026-10-19) had retracted the caveat for E042 in the *ledger* but
  never updated the README paragraph, leaving two self-contradictory statements
  in the published docs.

The paragraph was rewritten to describe **E041 only** with measured diff
counts, and to state explicitly that E042 is not in this class. The E041
sensitivity-grid paragraph was updated to quote the re-measured **7/96**
(with the 8 -> 7 drift noted) instead of the committed **8/96**.

**`ledger/RESEARCH_LEDGER.md`** — new **E047** entry recording the defect, the
re-measurement, and the fix.

## What was actually verified

Both drivers were re-run in **isolated copies** of the repository (so the
canonical goldens could not be captured mid-run) under `SEED=42` with the
pinned dependencies already present in this sandbox and the pinned
2026-10-12 cache vintage:

- **E042** (`run_e042.py --n-sim 50`, ~2 min): reproduces
  `experiments/e042_minvar_market_neutral.json` and
  `experiments/e042_sensitivity_grid.json` **byte-for-byte — 0 diffs on each
  artifact, including the full 96-config grid**. Confirms E044's retraction.
- **E041** (`run_e041.py`, ~5 min): does **not** reproduce —
  `e041_market_neutral_portfolio.json` **7602 numeric + 3 structural** diffs
  and `e041_sensitivity_grid.json` **151 numeric, 0 structural**. The 3
  structural diffs are exactly the ones the E041 extended-verification
  disposition already documents (`n_market_neutral_and_sharpe_gte_0.8` 8 -> 7,
  the "8 of 96" -> "7 of 96" note, `top_configs` length 8 -> 7). Gate decision
  (REJECTED 3/5, G3 fails) unchanged.

- `SEED=42 bash scripts/check.sh` -> ALL CHECKS PASSED (109 JSON artifacts,
  44 guard/report unit tests, 35 experiment imports), re-run after the edits.
- `git status --short` clean except `README.md` and `ledger/RESEARCH_LEDGER.md`
  (documentation only). The two goldens that an earlier E042 re-run in the
  *real* repo had overwritten were restored with `git checkout HEAD --`
  (restores the committed baseline, not a verification capture).

## What remains unresolved

- CI workflow `.github/workflows/verification-gate.yml` still requires
  maintainer creation via the GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`); outside agent scope
  per AGENTS.md.
- E030 (28 numeric diffs on near-zero quantities) and E041 (7602 numeric + 3
  structural at tolerance 0; 354 numeric + 3 structural at `numeric_tol=1e-4`)
  still drift between environments. Both are documented as reporting-only with
  unchanged decisions (E030 REJECTED, E041 REJECTED 3/5).
- The `dollar_neutral_longshort_weights` direction bug (confirmed by direct
  probe: it longs the *smallest* signal and shorts the *largest*, opposite to
  its docstring) is recorded as established context in E041
  `convention_findings`; the repo's standing disposition is to use it as-is
  (pre-registered component spec) and not re-litigate it.

## Failed approaches / dead ends

- Re-running `run_e042.py` / `run_e041.py` in the repository itself was
  avoided: the drivers overwrite `experiments/*.json`. An earlier accidental
  E042 run in the real repo did overwrite two goldens; they were restored with
  `git checkout HEAD --`, and all subsequent measurement was done in isolated
  copies that were deleted afterward.
- The `--restore-only` path reported "Nothing to restore: no pending
  verification snapshot found" because the accidental run was not wrapped by
  the suite's snapshot mechanism — `git checkout HEAD --` was the correct
  recovery.

## One precise next task

**None outstanding.** The research phase (E001–E046) is complete and the
repository is clean and fully verified. The only remaining durable action is
the maintainer-gated CI workflow creation, which is outside agent scope.

If a bounded in-session task is desired, the remaining environment-sensitive
drivers are E030 and E041 — both are documented as reporting-only with
unchanged decisions, and no further work is warranted unless a maintainer
re-pins them deliberately.

## Constraints (unchanged)

- `SEED=42`, pinned 2026-10-12 price-cache vintage + pinned 2026-10-12
  fundamentals snapshot.
- No committed-golden modification unless it is a deliberate re-pin
  (`python3 scripts/check_golden_baseline.py --update` puts the replacement
  in the diff); no tolerance/driver/skip change; no goalpost moved.
- Honor crash-safety snapshot/restore (`python3 run_all_verification.py
  --restore-only`).
- Follow repo policy: the golden is authoritative; re-pinning only
  deliberately with justification.