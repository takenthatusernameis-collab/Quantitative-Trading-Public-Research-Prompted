# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-28T00:42:42Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Read this first

The durable handoff convention lives here. This file is `handoff_2026-11-28T00-42-42Z_INITIAL_TASK.md`; generic aliases (`handoff_CURRENT`, `handoff_LATEST`, `handoff_INITIAL_TASK`, `handoff_NEXT_SESSION`, etc.) are repointed via `scripts/repoint_handoff.py`. No new alias names or mirror directories were created.

No execution happened this session; the prior handoff's initial task (recover the broken golden baseline) was carried forward, not performed.

## Carried-forward known state (inherited, not re-verified this session)

- **The golden baseline is BROKEN at HEAD.** HEAD `afc3feee33094a6f18f189efa50b062a7c2c7260` (2026-11-28 00:42:35 +0000, checkpoint commit) differs from the clean recovery target in exactly 5 pinned artifacts under `experiments/`. `scripts/check_golden_baseline.py` is expected to FAIL while `scripts/check_goldens_clean.py` still PASSES (working tree == HEAD). Do **not** re-pin to "silence" it (AGENTS.md precedent: `d6042b0`/`9f20def`, `1623923`, `701ed78`).
- **Recovery target**: commit `c5038332` (2026-11-24 02:05:45 +0000) — verified clean (`ALL 107 PINNED GOLDEN ARTIFACTS MATCH`). `git checkout c5038332 -- experiments/` restores the 5 drifted files.
- The 5 drifted artifacts: `cointegration_large_liquid.json`, `dollar_neutral_lowbeta_large_liquid.json`, `e037_portfolio.json`, `e042_lead_config_confirmatory.json`, `pairs_large_liquid.json`.
- Missing dependencies: `numpy`/`pandas` may not be importable — run `pip install -r requirements.txt` before the verification suite.
- `.verify_snapshot/` absent (no live run owns the snapshot). Do not delete a live snapshot if one appears.

## Initial Task (for the next agentic work session)

Do these in order and stop. Do **not** re-pin artifacts, overwrite goldens, run `check_golden_baseline.py --update`, or write a new handoff as a side effect.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist. If a live `ACTIVE.json` owner exists, recover with `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
3. **Reproduce the baseline failure** — `SEED=42 python3 scripts/check_golden_baseline.py` (expect exit 1, 5 files).
4. **Recover the canonical baseline** — `git checkout c5038332 -- experiments/` then re-run step 3 → expect `ALL 107 PINNED GOLDEN ARTIFACTS MATCH` (exit 0).
5. **Confirm goldens match HEAD + data coverage** — `SEED=42 python3 scripts/check_goldens_clean.py` and `SEED=42 python3 scripts/check_data_coverage.py` (both exit 0).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

If all pass after recovery, report that and proceed to real work. Do not re-run the full suite or re-pin anything as a side effect.

## Real-work task list (do these instead of refreshing the handoff)

1. **Fix the baseline (Section above) and commit the recovery** — restoring the 5 files from `c5038332` reverts a verification-run capture. Surface the diff for the user; commit only if the user asks.
2. **Provision deps and run real verification** — `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Confirm E041/E042 tangency-QP drift stays closed (0 differences) **without re-pinning**.
3. **If the extended run is clean, the research is genuinely done.** Say so and stop. Do not invent new experiments to look busy.
4. **Propose (do not execute) a handoff-file cleanup.** Thousands of tracked handoff files dominate the tree and are actively harmful. Draft a removal plan and surface it for the user's approval. **Do not run the deletion unreviewed**, and do not use `scripts/repoint_handoff.py` to regenerate aliases — that is loop machinery.
5. **Only if the user explicitly asks for new research**: open a new pre-registered experiment (E044+) per project conventions. Do not re-pin any published number without a ledger entry first (E050 precedent).

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in `experiments/*.json` are the authoritative record; never re-pin or overwrite them as a side effect of running verification.

## Git State (2026-11-28T00:42:42Z)

- Branch: `main`; HEAD `afc3feee33094a6f18f189efa50b062a7c2c7260` (checkpoint commit); `origin/main` identical.
- Working tree clean of tracked source (only `src/__pycache__/*.pyc` modified).
- `.verify_snapshot/` and `.verify_reports/` absent.
- ⚠️ **HEAD carries a contaminated baseline** (5 artifacts). Recovery source is `c5038332`, not HEAD.

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

Created at the user's explicit request ("leave a timestamped clear initial task message for the next agentic work session in a durable handoff"). This handoff supersedes `handoff_2026-11-27T23-44-29Z_INITIAL_TASK.md`. Generic aliases repointed via `scripts/repoint_handoff.py`; no golden/data baseline re-pinned, no verification suite run, no verification output committed, no new research performed, no commit made (left uncommitted pending explicit direction). It leads with the broken baseline so the next session fixes real state instead of writing another handoff.

*This handoff was created for the next agentic work session.*
