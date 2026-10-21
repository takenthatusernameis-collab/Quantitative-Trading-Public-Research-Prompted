# Session Handoff

## What changed

E029 is now **offline-reproducible** (the task handed over by the previous
agent). Commit `482a62d` ("E046: make E029 offline-reproducible by pinning the
yfinance fundamentals snapshot").

1. **`src/fundamentals.fetch_fundamentals()`** now caches the three panels
   (revenue / cogs / total assets) as parquet under `data/fundamentals/` (with a
   `.meta.json` SHA-256 fingerprint per panel) and, when `SEED` is set, reads the
   vintage named in the new `data/fundamentals_vintages.json` (`2026-10-12`)
   instead of the live yfinance feed. E029 was the only driver that
   re-downloaded fundamentals at run time, so its numbers were not reproducible
   offline and drifted between runs (max relative delta 3.03e-01 at
   `/falsification/blend/fe1_frac_positive`, max absolute 8.01e-01 at
   `/oos_short_tail[2]/sharpe`).
2. **`data/fundamentals/` + `data/fundamentals_vintages.json`** committed
   (gitignored by default; exempted in `.gitignore`). The price cache in
   `data/` is untouched.
3. **Deliberate re-pin** of `experiments/e029_fundamental_factors.json` via
   `python3 scripts/check_golden_baseline.py --update` (shows
   `~ changed experiments/e029_fundamental_factors.json`). The DATA-INFEASIBLE
   decision is unchanged and snapshot-robust (FE1 frac_pos 0.429/0.421/0.475 vs
   the canonical 0.299/0.421/0.390; no OOS Sharpe gate evaluated). No goalpost
   moved.
4. **Docs**: ledger E029 result table updated to the pinned snapshot with a
   provenance note; new **E046** entry. README and AGENTS drift tables updated —
   E029 now reproduces with **0** differences and is removed from the drift
   list.

## What was actually verified

- `SEED=42 python3 experiments/run_e029.py` twice -> **byte-identical**
  output (offline reproducible).
- `SEED=42 bash scripts/check.sh` -> ALL CHECKS PASSED (109 JSON artifacts,
   44 guard/report unit tests, 35 experiment imports).
- `python3 scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS
   MATCH HEAD. `python3 scripts/check_golden_baseline.py` -> ALL 107 PINNED
   GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT.
- `SEED=42 python3 run_all_verification.py --extended` (~28 min, executed in an
   isolated copy at `/home/runner/work/_temp/kilo-tmp/verify-e046`) ->
   **24/26 PASS, 2 FAIL (e030/e041)** — the documented baseline, now with
   **E029 passing** (was failing). The copy's goldens were restored by the
   suite's backup/restore mechanism; its `git status` shows only untracked
   caches and the gitignored `.verify_reports/` — no golden modification. The
   real repo was never modified by it (`git status` clean, pin intact).
- The real repo is clean at HEAD `482a62d`; the E029 working-tree digest matches
  the re-pinned fingerprint.

## What remains unresolved

- CI workflow `.github/workflows/verification-gate.yml` still requires
  maintainer creation via the GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`).
- `experiments/VERIFICATION_FINAL.json` is a stale verification report inside
  the golden directory (allowlisted/pinned). Left untouched.
- E030 (28 numeric diffs on near-zero quantities) and E041 (354 numeric + 3
  structural) still drift between environments. Both are documented as
  environment-sensitive, reporting-only, with unchanged decisions (E030
  REJECTED, E041 REJECTED 3/5).
- E029's fundamentals snapshot must be regenerated deliberately if the live
  yfinance feed is ever re-fetched: `SEED=42 python3 experiments/run_e029.py`
  (first seeded run fetches live and caches; subsequent seeded runs are
  offline), then `python3 scripts/check_golden_baseline.py --update`.

## Failed approaches / dead ends

- Re-running `--extended` in the repository itself was avoided on purpose: a
  checkpoint commit that captures verification output silently replaces the
  canonical baseline (this happened three times: `d6042b0`/`9f20def`,
  `1623923`, `701ed78`). The extended run was executed in an isolated copy
  instead.
- `git checkout -- experiments/` does **not** repair a captured baseline (it
  restores `HEAD`, which may be the capture). Use the pinned digest:
  `git checkout <commit> -- experiments/<file>` where `<commit>` is the last
  one whose SHA-256 matches `ledger/golden_baseline.json`.
- The previous handoff's option 2 (document E029 as network-dependent) was not
  needed: pinning was feasible and was done.

## One precise next task

**None outstanding from this session's mandate.** The handoff task (make E029
reproducible offline and align the ledger) is complete and verified. If a new
task is desired, the remaining environment-sensitive drivers are E030 and
E041 — both are documented as reporting-only with unchanged decisions, and no
further work is warranted unless a maintainer re-pins them deliberately.

## Constraints (unchanged)

- `SEED=42`, pinned 2026-10-12 price-cache vintage + pinned 2026-10-12
  fundamentals snapshot.
- No committed-golden modification unless it is a deliberate re-pin
  (`python3 scripts/check_golden_baseline.py --update` puts the replacement in
  the diff); no tolerance/driver/skip change; no goalpost moved.
- Honor crash-safety snapshot/restore (`python3 run_all_verification.py
  --restore-only`).
- Follow repo policy: the golden is authoritative; re-pinning only
  deliberately with justification.