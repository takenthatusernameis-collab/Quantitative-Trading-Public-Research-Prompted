# Handoff for Next Agent (v1.2.3 baseline stable + clone-reproducibility completed)

## Session Summary

**Date**: 2026-10-13
**Previous task (executed)**: Complete the v1.2.3 baseline's clone-reproducibility
policy (HANDOFF next task) — make `SEED=42 python3 run_all_verification.py --full`
pass from a **fresh clone with no network access**.

**Bottom line**: The archive is now clone-reproducible. `origin/main` at `ac0a116`
passes the full gate offline. This session also found and fixed a real,
regression-grade defect that the prior "commit caches" attempt (4ff660d /
4366b10 / cc6cf90) had introduced and **not caught** because no CI gate existed.

---

## What Changed This Session

1. **Reconciled a diverged remote** (per "reconcile remote changes" rule). A
   sibling commit `9330643` ("Fix Kilo checkpoint staging for ignored runtime
   caches", by the repo owner) added runtime-cache gitignores
   (`.venv/`, `.pytest_cache/`, `*.log`, …) on top of `4366b10` while this
   agent's two local commits (`cc6cf90` cache-tracking gitignores, `bcf377a`
   golden fix) also hung off `4366b10`. Rebased cleanly onto `9330643`
   (`.gitignore` regions are non-overlapping) → linear history
   `ac0a116 → c5416c6 → 9330643 → 4366b10`. Pushed.

2. **Fixed a corrupted gate golden** (`experiments/summary.json`, commit
   `ac0a116`). Commit `4366b10` committed an **internally inconsistent**
   `summary.json`: it reported **43** walk-forward folds per strategy, while
   the *same commit's* individual `*_large_liquid.json` goldens (and any fresh
   `SEED=42` run under the pinned 2026-10-12 cache) produce **42** folds
   (`train=504/test=63/step=63`). Because `summary.json` has no `timestamp`
   field, the gate's timestamp-strip did not mask it, so `batch_run` failed
   every fresh run (110 field mismatches, e.g. `quality` n_folds 43→42,
   is_sharpe 0.382→0.853).
   * Root cause: `4366b10` committed `summary.json` and the individual
     `*_large_liquid.json` from **different runs** (one used a larger/longer
     dataset yielding 43 folds; the committed cache yields 42).
   * Fix: regenerated `summary.json` from a cache-hit run so it is consistent
     with the committed individual goldens (`experiments/summary.json`).
   * Scope check: `e042` and non-batch summaries were already correct and were
     NOT touched; the v1.2.3 research conclusions (E042 PARTIAL 4/5, market-
     neutral portfolio line closed) are **unchanged**.

3. **Completed option (a)** from the prior handoff: the real no-suffix
   `2026-10-12` parquet caches that `src/data.py` actually requests
   (`auto_adjust=True`, cache key `*_2014-01-01_2026-10-12.parquet`) plus the
   14 `fred_*` series and `vintages.json` are **tracked** via the `.gitignore`
   negation patterns in `c5416c6`.

---

## What Was Actually Verified (evidence)

**Definitive test — fresh HTTPS clone of `origin/main` (`ac0a116`), no network:**

```
$ git clone https://github.com/.../Quantitative-Trading-Public-Research-Prompted /tmp/fclone_origin
$ cd /tmp/fclone_origin
$ SEED=42 python3 run_all_verification.py --full
```

Result (log: `/tmp/origin_final.log`) — `data/` git status **empty after the
run (no downloads)**, 26 tracked parquet, 0 "cache miss" warnings:

```
[data] large_liquid parquet cache present for vintage date: True
[PASS] verify_convention_robustness.py (exit 0)
[PASS] batch_run --universe large_liquid (exit 0 + JSON match)   # incl. summary.json EXACT
[PASS] validate --universe large_liquid (exit 0 + JSON match)
[PASS] run_e042 (full n_sim=50) (exit 0 + comparison)            # e042 + sensitivity EXACT
OVERALL: ALL CHECKS PASSED   (ORIGIN-CLONE FULL exit=0)
```

Before the fix, the same fresh-clone quick run failed exactly on
`summary.json` (43-fold stale golden vs 42-fold fresh), proving the defect
reproduces from a clean checkout.

---

## What Remains Unresolved

- **`.parquet.adj0.act1` legacy caches are NOT dead weight** (correcting the
  prior handoff's claim). `experiments/run_e026.py:43-44` calls
  `data.download(..., auto_adjust=False, actions=True, end="2026-10-11")`,
  which resolves to the `.adj0.act1` cache keys. They are consumed by the
  **non-gated** dividend/factor experiments (e024, e026) — which also run at a
  *different* hardcoded vintage (`2026-10-11`, bypassing the 2026-10-12 pin)
  — and are **never read by the verification suite**. ~21 MB of
  `auto_adjust=False` caches sit in `data/` tracked (they match `data/*.parquet`
  `.act1`), which evades the `data/*.parquet` ignore rule, so they are
  tracked). Cleaning or gitignoring them is safe for the gate but is a separate
  decision for the e024/e026 owner (see next-task option (b)).
- **Non-gated experiment JSONs (E016–E024, E041, etc.) remain at the
  2026-10-13 vintage.** Outside the automated gate; headline numbers unchanged
  at printed precision (4th-decimal shifts only). Regenerating them for full-repo
  byte consistency is optional (~30–40 min).
- **Commit `3e33085` (empty message, corrupted golden) remains in history.** Not
  rewritten (pushed). The `ac0a116` restoration supersedes it.
- **`cc6cf90` / `bcf377a` were rebased onto `9330643` during reconciliation**;
  original hashes changed but content is preserved on `origin/main`.

---

## Approaches Already Failed / Ruled Out

- **Reverting the pin to 2026-10-13** (prior handoff option): would force a
  network re-download of the futures-panel/macro caches (keyed 2026-10-12) and
  break offline reproduction. Regenerating under the committed vintage is
  strictly more robust (now proven by the offline clone).
- **Warning-only fix for quick-run golden overwrite**: rejected — a warning does
  not survive `git add -A`; the `--out` path separation in `run_e042.py` is
  required (unchanged).
- **Trusting the post-4366b10 `summary.json`**: the gate failed on it from a
  fresh clone; regenerated under the canonical cache.

---

## One Precise Next Task (for the following agent)

**Add a GitHub Actions reproducibility gate that runs the verification suite on
every push, so a stale/golden-drift commit like `4366b10`'s `summary.json` can
never land again.**

Concrete spec:
- Create `.github/workflows/verification-gate.yml` (and reuse the existing
  `kilo-workflow-audit.yml` path-filter pattern as a template).
- Triggers: `push` and `pull_request` on `main`, **paths**-filtered to changes
  that affect outputs: `src/**`, `experiments/**`, `data/**`,
  `data/vintages.json`, `run_all_verification.py`,
  `verify_convention_robustness.py`, `requirements.txt`, `.gitignore`.
- Job (`ubuntu-latest`, `timeout-minutes: 20`): checkout → setup-python →
  `pip install -r requirements.txt` → `SEED=42 python3 run_all_verification.py
  --full` (full mode is the real test; ~5 min and proven offline). On PRs,
  optionally run the faster quick mode (`--no-slow` not available; quick mode is
  the default, ~2 min).
- Fail the job on non-zero exit / on any `[FAIL]`.
- **Do not** commit regenerated experiment JSONs from CI; the job only *reads*
  the committed goldens and asserts the suite still reproduces them.

Completion criterion: open the workflow file (or a PR branch), run
`actionlint -color .github/workflows/verification-gate.yml` +
`bash -n` on any scripts → syntax OK; and the suite's own `--full` pass in a
fresh clone is the runtime guarantee (already demonstrated above).

**Secondary option (lower priority):** gitignore/remove the 14
`.adj0.act1` caches after confirming e024/e026 can rebuild them, to drop ~21 MB
of committed binary bloat — only if the e026 owner agrees (they rely on these
for `auto_adjust=False` dividend data at the `2026-10-11` vintage).

---

## Key Files

- `experiments/summary.json` — **regenerated** here (42 folds; 43-fold version
  in `4366b10` was the bug). `git show ac0a116:experiments/summary.json`.
- `.gitignore` — data-cache negations (`c5416c6`) + runtime ignores (`9330643`).
- `data/` — 26 tracked `*_2026-10-12.parquet` + 14 `fred_*.parquet` +
  `vintages.json` are the offline cache the suite needs.
- `run_all_verification.py`, `verify_convention_robustness.py`,
  `src/data.py`, `src/batch_run.py`, `src/validate.py`,
  `experiments/run_e042.py` — unchanged by this session.
- Prior baseline context: `HANDOFF.md` history (v1.2.3 restore, corrupted-golden
  fix) remains valid; this session supersedes only the clone-reproducibility
  and `summary.json` lines.
