# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-27T20:44:50Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Read this first — two things are true at once

1. **The golden baseline is BROKEN at HEAD.** This is the real, urgent finding
   of this session and it is new (every prior handoff reported the baseline
   clean). `scripts/check_golden_baseline.py` now **FAILS**: 5 committed
   artifacts under `experiments/` differ from the SHA-256 pinned in
   `ledger/golden_baseline.json`, while `scripts/check_goldens_clean.py` still
   PASSES (working tree == HEAD). That combination means **a `chore(kilo):
   checkpoint agent session` commit captured verification-run output and
   replaced the canonical baseline** — the exact failure mode AGENTS.md warns
   about (precedents: `d6042b0`/`9f20def`, `1623923`, `701ed78`). HEAD
   `72a52c92` is contaminated; do **not** re-pin to "silence" it.

2. **You are also inside the ~777th handoff-refresh loop.** The research phase
   has been closed since E043; E652–E776 are the same "durable handoff refresh"
   re-run over and over (~9,343 git-tracked `handoff`-named files, ~94.5% of the
   tree). Do not manufacture an E777-style refresh as your deliverable.

**The deliverable of this session is #1 (fix the baseline) or an explicit
"nothing to do" report — NOT another handoff.**

## Initial Task (for the next agentic work session)

Do these in order and stop. Do **not** re-pin artifacts, overwrite goldens, or
write a new handoff as a side effect.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist.
   If a live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `numpy`/`pandas` are NOT importable here; the suite and most drivers need them.
3. **Reproduce the baseline failure** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (expect exit 1, 5 files).
4. **Recover the canonical baseline** (verified target, see below):
   `git checkout c5038332 -- experiments/`
   then re-run step 3 → expect `ALL 107 PINNED GOLDEN ARTIFACTS MATCH` (exit 0).
5. **Confirm goldens match HEAD + data coverage** —
   `SEED=42 python3 scripts/check_goldens_clean.py` and
   `SEED=42 python3 scripts/check_data_coverage.py` (both exit 0).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

If all pass after recovery, the baseline is clean again: report that and proceed
to the real-work list. Do not re-run the full suite or re-pin anything as a side
effect.

## Baseline recovery target (verified this session, 2026-11-27T20:44:50Z)

- **Newest clean commit**: `c5038332` (2026-11-24 02:05:45 +0000). Verified in a
  throwaway worktree: `check_golden_baseline.py` → `ALL 107 PINNED GOLDEN
  ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0).
- **Only these 5 files differ** between `c5038332` and HEAD `72a52c92`
  (`git diff --stat c5038332 HEAD -- experiments/`): the other 102 pinned
  artifacts are already identical, so `git checkout c5038332 -- experiments/`
  fully restores the baseline.
- The 5 drifted artifacts (pinned → actual at HEAD):
  - `experiments/cointegration_large_liquid.json`
    `a4118252…` → `33a35b18…`
  - `experiments/dollar_neutral_lowbeta_large_liquid.json`
    `c657c3af…` → `d946bdd6…`
  - `experiments/e037_portfolio.json`
    `dcaeb797…` → `4eedc526…`
  - `experiments/e042_lead_config_confirmatory.json`
    `fa06eeb8…` → `71c04548…`
  - `experiments/pairs_large_liquid.json`
    `5ab39998…` → `07f258de…`
- **Do NOT** run `check_golden_baseline.py --update` to re-pin. The committed
  golden is the authoritative record; re-pinning is only for a *deliberate*
  code change recorded in the ledger first (E050 precedent).

## Prioritized real-work task list (do these instead of refreshing the handoff)

1. **Fix the baseline (Section above) and commit the recovery** — restoring the
   5 files from `c5038332` is a legitimate, reviewable change (it reverts a
   verification-run capture). Surface the diff for the user; commit only if the
   user asks.
2. **Provision deps and run the real verification.** `pip install -r
   requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended`
   (~21 min). Report `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`;
   confirm E041/E042 tangency-QP drift stays closed (0 differences) **without
   re-pinning**.
3. **If the extended run is clean, the research is genuinely done.** Say so and
   stop. Do not invent new experiments to look busy.
4. **Propose (do not execute) a handoff-file cleanup.** ~9,343 tracked handoff
   files are ~94.5% of the tree and actively harmful (clone size, search noise,
   review burden). Draft a removal plan (e.g. `git rm` the `handoff_*` /
   `HANDOFF*` families, keep this one + the ledger) and surface it for the
   user's approval. **Do not run the deletion unreviewed**, and do not use
   `scripts/repoint_handoff.py` to regenerate aliases — that is loop machinery.
5. **Only if the user explicitly asks for new research**: open a new
   pre-registered experiment (E044+) per the project conventions. Do not re-pin
   any published number without a ledger entry first (E050 precedent).

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Git State (2026-11-27T20:44:50Z)

- Branch: `main`; HEAD `72a52c92` (checkpoint commit); `origin/main` identical
  (`git rev-list --left-right --count origin/main...HEAD` = `0 0`).
- Working tree clean of tracked source (only `src/__pycache__/*.pyc` modified).
- `.verify_snapshot/` and `.verify_reports/` absent (no live run owns the snapshot).
- ⚠️ **HEAD carries a contaminated baseline** (5 artifacts, see above). `HEAD`
  itself must not be treated as the recovery source — use `c5038332`.

## Baseline Integrity (verified 2026-11-27T20:44:50Z)

- ✅ No active verification run: `.verify_snapshot/` does not exist.
- ✅ Golden artifacts match HEAD (`git diff HEAD -- experiments/` empty).
- ❌ **Pinned baseline VIOLATED at HEAD**: `check_golden_baseline.py` → 5 of 107
  artifacts differ (checkpoint-commit capture). Recover from `c5038332`.
- ✅ Data coverage intact: `check_data_coverage.py` → all 35 pinned inputs
  present, tracked, unchanged.
- ⚠️ Missing dependencies: `numpy`/`pandas` not importable. Run
  `pip install -r requirements.txt` before the full verification suite.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                    # fast convention + template validation (offline)
SEED=42 python3 scripts/check_golden_baseline.py # MUST pass after recovery (107 artifacts)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
git checkout c5038332 -- experiments/            # recover canonical baseline (verified clean)
```

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md`
- **Pinned baselines**: `ledger/golden_baseline.json` (107), `ledger/data_baseline.json` (35)

## Handoff Context

Created at the start of a new agentic work session at the user's explicit
request ("leave a timestamped clear initial task message for the next agentic
work session in a durable handoff"). This handoff supersedes
`handoff_2026-11-27T20-40-46Z_INITIAL_TASK.md` (E776). The existing generic
aliases were repointed to this file via `scripts/repoint_handoff.py`
(edit-in-place of existing pointers only); **no new mirror directories or alias
names were created**. No golden/data baseline re-pinned, no verification suite
run, no verification output committed, no new research performed, no commit made
(left uncommitted pending explicit direction). It leads with the newly-broken
baseline so the next session fixes real state instead of writing handoff #778.

*This handoff was created for the next agentic work session.*