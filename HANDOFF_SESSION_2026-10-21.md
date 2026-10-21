# Session Handoff 2026-10-21 (E048)

## What changed

The E047 handoff declared the research phase complete and left no outstanding
research task, so this session audited the repository's **verification layer**
instead of adding an experiment. It found two real defects and fixed both.

**1. `scripts/check_json_artifacts.py` could never fail (critical).** Its
`__main__` block called `main()` and discarded the return value, so the
process exit code was always 0. The guard printed
`JSON ARTIFACT CHECKS FAILED (n malformed)` and still exited 0 — so
`scripts/check.sh` could not abort on a malformed artifact and step 0.5 of
`run_all_verification.py` always recorded a PASS. Fixed with
`sys.exit(main())`; three new subprocess-level unit tests now cover the
command-line path (the old in-process tests could not see this bug).

**2. Three committed goldens were not valid JSON.** `e024_convention_audit.json`,
`e024_part_c.json` and `e029_fundamental_factors.json` carried bare `NaN`
literals (10 / 10 / 12 of them) for undefined statistics. Python's `json`
module accepts them, so they loaded locally and were rejected by `jq`, Go,
Rust, PostgreSQL and every browser `JSON.parse`. New `src/jsonio.py` maps a
non-finite float to `null` and writes with `allow_nan=False`; all artifact
writers (3 `src/` modules + 27 driver scripts) now route through it and the
guard enforces RFC 8259 strictly.

Supporting changes: `check_goldens_clean.py` now compares only the tracked
**JSON artifacts** under `experiments/` with HEAD (it previously reported the
29 driver sources as "golden artifact(s) differ" — same scope its sibling
guard documents); the four `data/` manifests are classified `NON_EXPERIMENT`
(they were false positives, invisible while the exit code was broken).

## What was actually verified

- `SEED=42 bash scripts/check.sh` -> **ALL CHECKS PASSED** (113 JSON
  artifacts, 47 guard/report unit tests, 35 experiment imports) after the
  commit `8c7c12f`.
- Pre-fix vs post-fix guard, measured in a throwaway repo: the pre-fix script
  reported a malformed artifact and **exited 0**; the fixed script exits 1.
- The three goldens were transformed `NaN` -> `null` and deliberately
  re-pinned (`python3 scripts/check_golden_baseline.py --update`; exactly 3
  fingerprints changed). The transform is not a hand edit: for each file,
  `jsonio.dump(json.loads(original))` was asserted to reproduce the
  transformed file **byte-for-byte**. `git diff -U0` on the three files shows
  only `"...": NaN` -> `"...": null` lines — no recorded number, gate,
  decision or string changed.
- Driver re-runs were executed in **isolated copies** under `/home/runner/work/_temp/kilo-tmp/`
  (never in the repo, so the canonical baseline could not be captured
  mid-run):
  - `run_e024.py --merge` -> fresh `e024_convention_audit.json` matches the
    transformed golden **exactly** (0 differences, timestamp excluded).
  - `run_e024.py --parts c` -> fresh `e024_part_c.json` matches within 29
    numeric values of relative size ~1e-8..1e-6 (live dividend data), i.e.
    inside the suite's `numeric_tol=1e-4`.
  - `run_e029.py` -> fresh artifact differs from the golden by 181 numeric
    values (relative ~1e-6, inside `numeric_tol=1e-4`; decision unchanged,
    DATA-INFEASIBLE). The **same 181-value drift** is produced by the
    pre-change driver (`HEAD:experiments/run_e029.py`, old `json.dump`) in
    the same sandbox and seed, so the drift is pre-existing and **not**
    caused by the writer change.
- `SEED=42 python3 run_all_verification.py` (quick mode) executed in an
  isolated copy of the committed tree -> see "Verification suite" below.

## Verification suite (quick mode, isolated copy)

Executed at commit `8c7c12f` in
`/home/runner/work/_temp/kilo-tmp/verify-e048b`; the copy's goldens were
restored by the suite's own snapshot/restore mechanism and its
`git status` showed no golden modification afterwards. The real repository
was never touched by the run.

```
  [PASS] check_json_artifacts.py (exit 0)      [PASS] test_json_guard.py (exit 0)
  [PASS] check_goldens_clean.py (exit 0)       [PASS] test_golden_baseline.py (exit 0)
  [PASS] check_golden_baseline.py (exit 0)     [PASS] verify_convention_robustness.py (exit 0)
  [PASS] batch_run --universe large_liquid      [PASS] validate --universe large_liquid
  [PASS] run_e012 / run_e023 / run_e024 / run_e027 / run_e035 / run_e037 / run_e039
  [PASS] run_e042 (quick n_sim=2)
  [FAIL] run_e042_lead.py (exit 1 + JSON match)
OVERALL: FAILURES DETECTED
```

**The single failing step is pre-existing and is not a regression** — proven
with a control run at the pre-change commit `9106a3b`:

| run | vs. committed golden |
|---|---|
| `run_e042_lead.py` at `8c7c12f` (new writer) | 23 numeric differences (`primary/oos_sharpe` 0.86594 -> 0.82187, `placebo_constrained/z_score` 1.9568 -> 1.6381, `primary/positive_folds` 27 -> 26, `bull/sharpe_pos` 18 -> 17) |
| `run_e042_lead.py` at `9106a3b` (**pre-change** code) | **the same 23 differences** |
| new-code output vs. pre-change-code output | **0 differences** (only `runtime_sec`) |
| two consecutive runs in this environment | **0 differences** (only `runtime_sec`) |

So the writer change is value-preserving, and the lead config is
deterministic *within* one environment but drifts *between* environments
(the walk-forward SLSQP optimization over the five component streams — the
same class as the documented E030 / E041 sensitivity). The **decision is
unchanged** (E042-lead REJECTED). No tolerance was raised, no driver was
skipped, and no golden was touched. The fast gate
(`SEED=42 bash scripts/check.sh`) passes in full.

## What remains unresolved

- **E029 is not offline-reproducible end to end** (new finding, ledger
  E048). E046 pinned the *fundamentals* panel, but E029's *price* panel is
  not in the committed cache: a seeded run still downloads it from yfinance,
  and two live downloads of the **same cache key one minute apart produce
  different files** (md5 `14b350ff5c3408ab8b6e7caac4d9c2a6` / 17,332,069
  bytes vs `aa5c1303f319d724a4bb60105529e2fa` / 17,332,357 bytes). Two E029
  runs one minute apart differ from *each other* by 179 numeric values, so
  the driver is not bit-reproducible in a fresh checkout. The AGENTS.md and
  README claims were corrected accordingly.
- E030 (28 numeric diffs on near-zero quantities) and E041 (354 numeric + 3
  structural at `numeric_tol=1e-4`) still drift between environments. Both
  remain reporting-only with unchanged decisions (E030 REJECTED, E041
  REJECTED 3/5).
- **E042-lead now also drifts between environments** (23 numeric differences
  against the committed golden in this sandbox, decision unchanged). The quick
  suite therefore reports `OVERALL: FAILURES DETECTED` here, with that one
  step as the cause; the fast gate `bash scripts/check.sh` passes. Measured
  and controlled above — it is not a regression from this session's change.
- CI workflow `.github/workflows/verification-gate.yml` still requires
  maintainer creation via the GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`); outside agent scope
  per AGENTS.md.
- `experiments/VERIFICATION_FINAL.json` is a stale verification report inside
  the golden directory (allowlisted/pinned). Left untouched.
- `experiments/_t.py` is a stray 11-byte scratch file (`print("hi")`) in the
  golden-artifact directory. Harmless (it is not a driver and not an
  artifact); left untouched to avoid an unrelated deletion.

## Failed approaches / dead ends

- **Re-running drivers in the repository itself** was avoided: the drivers
  overwrite `experiments/*.json`. All measurement was done in isolated copies
  that were deleted afterwards.
- **Testing the pre-fix guard from `/tmp`** failed first: the guard resolves
  its root from `__file__` and shells out to `git ls-files`, so it must run
  inside a git repository. Re-run with the script copied into a throwaway
  repo (`/tmp/oldguard`), which produced the exit-code evidence.
- **Hypothesis rejected: cvxpy/cvxopt.** The E041 drift was suspected to be
  an environment-dependent solver switch. `src/portfolio_opt.py` imports
  `scipy.optimize` only (`linprog`, `minimize`) — there is no cvxpy code
  path. The stale AGENTS.md sentence about it was corrected instead.
- **Hypothesis rejected: BLAS threading.** `OPENBLAS_NUM_THREADS=1
  OMP_NUM_THREADS=1` did not change the E029 drift (identical values to the
  multi-threaded run). The cause is the live price download, not the thread
  count.
- **Hypothesis rejected: the writer change caused the E042-lead suite
  failure.** A control run of the *pre-change* driver at commit `9106a3b`
  reproduced the identical 23-difference drift, and the old-code and
  new-code outputs of the same driver are byte-identical apart from
  `runtime_sec`. The failure is a between-environment difference, not a
  regression.

## One precise next task

**Make E029 offline-reproducible by pinning its price panel**, then re-measure
and re-pin the E029 golden if (and only if) the values change.

Evidence and constraints:

- The missing cache key is
  `data/AAPL_ABBV_ABT_ACN_ADBE_ADI_ADM_ADP_ADSK_AEP_AIG_ALL_AMAT_AMD_AMGN_AMT_AMZN_AVGO__30b385b8fada6ee9_2014-01-01_2026-10-11.parquet`
  (the committed twin has the `2026-10-12` end date). A fresh checkout
  therefore re-downloads it, and the download is not reproducible (see the two
  md5s above).
- Two candidate approaches, in order of preference:
  1. **Commit the missing price cache file** under the existing `data/`
     exemption in `.gitignore` (as the 2026-10-12 vintage files are), then
     re-run `SEED=42 python3 experiments/run_e029.py` twice and confirm the
     two outputs are byte-identical. This is the minimal change and needs no
     golden re-pin if the numbers happen to match.
  2. If the committed file's content still does not reproduce the committed
     golden, change E029's price request to the pinned `2026-10-12` vintage
     (or pin the price panel the same way the fundamentals panel was pinned
     in E046) and then deliberately re-pin
     `experiments/e029_fundamental_factors.json` with
     `python3 scripts/check_golden_baseline.py --update`. The decision
     (DATA-INFEASIBLE) must remain unchanged; record the new numbers in the
     ledger.
- Do **not** weaken tolerances, skip drivers, or re-pin as a side effect of
  running the verification suite. The committed golden stays the
  authoritative record until a deliberate, justified re-pin.

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
- Artifacts are written through `src/jsonio.py`; a bare `NaN` must never
  reach a committed file (`scripts/check_json_artifacts.py` enforces it and
  now exits non-zero when it fails).
