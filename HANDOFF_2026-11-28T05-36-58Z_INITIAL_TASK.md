# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-28T05-36-58Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Read this first

This file is `HANDOFF_2026-11-28T05-36-58Z_INITIAL_TASK.md`. The generic aliases
(`handoff_CURRENT`, `handoff_LATEST`, `handoff_INITIAL_TASK`, `handoff_NEXT_SESSION`, etc.)
are repointed to it via `scripts/repoint_handoff.py`. No new alias names or mirror
directories were created.

All state below was **verified live this session** (2026-11-28T05-36-58Z), not copied from
older handoffs:

- **The golden baseline is BROKEN at HEAD.** HEAD `a8164d92`
  (`chore(kilo): checkpoint agent session`, == `origin/main`, 0 ahead / 0 behind) carries a
  contaminated baseline: 5 of the 107 pinned artifacts under `experiments/` differ from
  `ledger/golden_baseline.json`. `scripts/check_golden_baseline.py` → **FAIL (5 files)** while
  `scripts/check_goldens_clean.py` → **PASS** (working tree == HEAD). Do **not** re-pin to
  "silence" it (AGENTS.md precedent: `d6042b0`/`9f20def`, `1623923`, `701ed78`).
- **Recovery target**: commit `c5038332` (2026-11-24 02:05:45 +0000) — the last known clean
  baseline. Verified this session: `git show c5038332:experiments/<file>` SHA-256 matches the
  pinned hash for all 5 drifted files. `git checkout c5038332 -- experiments/` restores them.
- The 5 drifted artifacts (pinned → actual):
  - `cointegration_large_liquid.json` — pinned `a4118252…` → actual `33a35b18…`
  - `dollar_neutral_lowbeta_large_liquid.json` — pinned `c657c3af…` → actual `d946bdd6…`
  - `e037_portfolio.json` — pinned `dcaeb797…` → actual `4eedc526…`
  - `e042_lead_config_confirmatory.json` — pinned `fa06eeb8…` → actual `71c04548…`
  - `pairs_large_liquid.json` — pinned `5ab39998…` → actual `07f258de…`
- **Data coverage PASSES**: `check_data_coverage.py` → `ALL 35 PINNED DATA INPUTS ARE PRESENT,
  TRACKED AND UNCHANGED`.
- **Missing dependency**: `pandas`/`numpy` not importable — run `pip install -r requirements.txt`
  before the full verification suite.
- `.verify_snapshot/` and `.verify_reports/` absent (no live run owns the snapshot; nothing to
  recover).
- Working tree clean of tracked source (only `src/__pycache__/*.pyc` modified, ignored).

> Note: the immediately-prior handoff `HANDOFF_2026-11-28T05-36-11Z_INITIAL_TASK.md` was
> written at HEAD `a8164d92` and this file supersedes it with the same verified state,
> updated timestamp.

## Initial Task (for the next agentic work session)

Do these in order and stop. Do **not** re-pin artifacts, overwrite goldens, run
`check_golden_baseline.py --update`, or write a new handoff as a side effect.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist. If a live
   `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
3. **Reproduce the baseline failure** — `SEED=42 python3 scripts/check_golden_baseline.py`
   (expect the 5 files listed above).
4. **Recover the canonical baseline** — `git checkout c5038332 -- experiments/` then re-run
   step 3 → expect `ALL 107 PINNED GOLDEN ARTIFACTS MATCH`.
5. **Confirm goldens match HEAD + data coverage** —
   `SEED=42 python3 scripts/check_goldens_clean.py` and
   `SEED=42 python3 scripts/check_data_coverage.py` (both pass).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

If all pass after recovery, report that and proceed to real work. Do not re-run the full
suite or re-pin anything as a side effect.

## Real-work task list (do these instead of refreshing the handoff)

1. **Fix the baseline (Section above) and commit the recovery** — restoring the 5 files from
   `c5038332` reverts a verification-run capture. Surface the diff for the user; commit only
   if the user asks.
2. **Provision deps and run real verification** — `pip install -r requirements.txt`, then
   `SEED=42 python3 run_all_verification.py --extended` (~21 min). Confirm E041/E042
   tangency-QP drift stays closed (0 differences) **without re-pinning**.
3. **If the extended run is clean, the research is genuinely done.** Say so and stop. Do not
   invent new experiments to look busy.
4. **Propose (do not execute) a handoff-file cleanup.** ~9,300+ tracked handoff files are the
   overwhelming majority of the tree and actively harmful. Draft a removal plan and surface it
   for the user's approval. **Do not run the deletion unreviewed**, and do not use
   `scripts/repoint_handoff.py` to regenerate aliases as a substitute for cleanup.
5. **Only if the user explicitly asks for new research**: open a new pre-registered experiment
   (E044+) per project conventions. Do not re-pin any published number without a ledger entry
   first (E050 precedent).

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in
`ledger/RESEARCH_LEDGER.md`. Golden artifacts in `experiments/*.json` are the authoritative
record; never re-pin or overwrite them as a side effect of running verification.

## Git State (2026-11-28T05-36-58Z)

- Branch: `main`; HEAD `a8164d92` (checkpoint agent session); `origin/main` identical
  (0 ahead / 0 behind).
- Working tree clean of tracked source (only `src/__pycache__/*.pyc` modified, ignored).
- `.verify_snapshot/` and `.verify_reports/` absent.
- ⚠️ **HEAD carries a contaminated baseline** (5 artifacts). Recovery source is `c5038332`,
  not HEAD.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 scripts/check_golden_baseline.py      # MUST pass after recovery (107 artifacts)
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 python3 scripts/check_data_coverage.py
SEED=42 python3 run_all_verification.py --restore-only # recover goldens if interrupted
git checkout c5038332 -- experiments/                 # recover canonical baseline
```

## Key Artifacts

- Golden files: `experiments/*.json`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- Pinned baselines: `ledger/golden_baseline.json` (107), `ledger/data_baseline.json` (35)

## Handoff Context

Created at the user's explicit request ("leave a timestamped clear initial task message for
the next agentic work session in a durable handoff"). Supersedes
`HANDOFF_2026-11-28T05-36-11Z_INITIAL_TASK.md` (same verified state, updated timestamp).
Generic aliases will be repointed via `scripts/repoint_handoff.py`; no golden/data baseline
re-pinned, no verification suite run, no verification output committed, no new research
performed, no commit made (left uncommitted pending explicit direction). It leads with the
broken baseline so the next session fixes real state instead of writing another handoff.

*This handoff was created for the next agentic work session.*