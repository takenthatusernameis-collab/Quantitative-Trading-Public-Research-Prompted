# Agentic Work Session — Initial Task (durable handoff)

**Timestamp (UTC):** 2026-11-28T09:41:29Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch / HEAD:** `main` — `ed9f3fae99b042b8ad181a7a276f5bc10edb11c9` (== `origin/main`; a `chore(kilo): checkpoint agent session` commit on top of `d3e20c4b`, which itself sits on the contaminated baseline)

## TL;DR — the one real task

**HEAD carries a contaminated golden baseline.** 5 of the 107 pinned artifacts under
`experiments/` differ from `ledger/golden_baseline.json`. This is a verification-run capture
(last-digit float drift only — no structural, string, or gate-flag changes), exactly the
checkpoint-capture failure mode AGENTS.md warns about. **Recover the 5 files from commit
`337a0deb`; do NOT re-pin.**

This is the same defect flagged in the 2026-11-28T09:40:31Z handoff (and the 09:37:46Z,
09:35:41Z, 08:41:18Z ones before it). It is still unfixed: successive `chore(kilo): checkpoint
agent session` commits (`e80371fa` → `d3e20c4b` → `ed9f3fae`) re-committed the captured output
on top of the baseline. The recovery source and pinned SHAs are unchanged and re-verified below.

## Verified state (2026-11-28T09:41:29Z, re-checked this session)

- **HEAD** `ed9f3fae` == `origin/main`; branch `main`. Contamination is committed, not a
  working-tree change. `git status` is clean apart from an untracked
  `src/__pycache__/cache_keys.cpython-312.pyc` build artifact (ignore/remove).
- **Golden baseline: BROKEN at HEAD.** `SEED=42 python3 scripts/check_golden_baseline.py` → **FAIL (5 files)**:
  - `experiments/cointegration_large_liquid.json` (pinned `a4118252…`, actual `33a35b18…`)
  - `experiments/dollar_neutral_lowbeta_large_liquid.json` (pinned `c657c3af…`, actual `d946bdd6…`)
  - `experiments/e037_portfolio.json` (pinned `dcaeb797…`, actual `4eedc526…`)
  - `experiments/e042_lead_config_confirmatory.json` (pinned `fa06eeb8…`, actual `71c04548…`)
  - `experiments/pairs_large_liquid.json` (pinned `5ab39998…`, actual `07f258de…`)
  - The other 102 pinned artifacts match. Diff is pure floating-point drift.
- **Recovery source RE-VERIFIED this session**: `337a0deb` is an ancestor of HEAD
  (`git merge-base --is-ancestor 337a0deb HEAD` → yes); `git show 337a0deb:experiments/<f>.json | sha256sum`
  reproduces the exact pinned SHA-256 in `ledger/golden_baseline.json` for all 5 files. Restoring
  from it is correct.
- **No interrupted run**: `.verify_snapshot/` absent.
- **Data coverage: OK** (per prior session; pure SHA-256 check, no deps needed).
- **Environment gap**: `numpy` / `pandas` may not be importable here. Run
  `python3 -m pip install -r requirements.txt` before any driver or full suite
  (the baseline + data-coverage checks are pure SHA-256 and need no deps).

## Initial Task (do these in order, then stop)

Do not re-pin artifacts, run `check_golden_baseline.py --update`, overwrite goldens, or write
another handoff as a side effect. Do not commit unless the user explicitly asks.

1. Confirm no active verification run (`.verify_snapshot/` must not exist).
2. Provision environment — `python3 -m pip install -r requirements.txt`.
3. Reproduce the baseline failure — `SEED=42 python3 scripts/check_golden_baseline.py` (expect FAIL on 5).
4. Recover the canonical baseline (surgical, 5 files):
   ```bash
   git checkout 337a0deb -- \
     experiments/cointegration_large_liquid.json \
     experiments/dollar_neutral_lowbeta_large_liquid.json \
     experiments/e037_portfolio.json \
     experiments/e042_lead_config_confirmatory.json \
     experiments/pairs_large_liquid.json
   ```
5. Re-verify the baseline — `SEED=42 python3 scripts/check_golden_baseline.py` → expect
   "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT".
6. Surface the diff to the user; commit ONLY if asked.
7. Confirm data coverage — `SEED=42 python3 scripts/check_data_coverage.py`.
8. Fast sanity check — `SEED=42 bash scripts/check.sh`.

## Key Constraints

- `experiments/*.json` are committed goldens — never re-pin to silence drift; never commit verification output.
- Always `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents; use local `make check` / `make verify*`.
- Research phase is complete (E001–E043); do not introduce new strategies or move goalposts.
- If this session itself hands off, create its own timestamped durable handoff following the
  established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root) and repoint
  the `HANDOFF_CURRENT` / `HANDOFF_NEXT_SESSION` / `HANDOFF_NEXT_HANDOFF` symlinks.

## Handoff provenance

Supersedes previous INITIAL_TASK handoff `HANDOFF_2026-11-28T09-40-31Z_INITIAL_TASK.md`.
This file is the authoritative initial-task message for the next session.

*This handoff was created for the next agentic work session at 2026-11-28T09:41:29Z.*