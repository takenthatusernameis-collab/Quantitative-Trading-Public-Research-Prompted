# Agentic Work Session Handoff — Initial Task

**Timestamp (UTC)**: 2026-11-28T02:47:35Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch / HEAD**: `main` — `b59172887d9a09f427ce79193f785c307d577b99` (== `origin/main`)

> All state below was **verified live this session** (2026-11-28T02:47:35Z) against the current
> tree, not copied from older handoffs. HEAD has advanced since the previous detailed handoff
> (`625f8809` → `b5917288`); the facts here were re-checked at `b5917288`.

## TL;DR — the one real task

**HEAD carries a contaminated golden baseline.** 5 of the 107 pinned artifacts under
`experiments/` differ from `ledger/golden_baseline.json`. This is a verification-run capture
(last-digit floating-point drift only — no structural, string, or gate-flag changes), exactly the
checkpoint-capture pattern AGENTS.md warns about (precedents `d6042b0`/`9f20def`, `1623923`,
`701ed78`). **Recover the 5 files from commit `c5038332`; do NOT re-pin.**

## Verified state (2026-11-28T02:47:35Z)

- **HEAD** `b59172887d9a09f427ce79193f785c307d577b99` == `origin/main`; branch `main`.
- **Golden baseline: BROKEN at HEAD.** `SEED=42 python3 scripts/check_golden_baseline.py` → **FAIL (5 files)**:
  - `experiments/cointegration_large_liquid.json`
  - `experiments/dollar_neutral_lowbeta_large_liquid.json`
  - `experiments/e037_portfolio.json`
  - `experiments/e042_lead_config_confirmatory.json`
  - `experiments/pairs_large_liquid.json`
  The other 102 pinned artifacts match. The diff is pure floating-point drift
  (e.g. `e037_portfolio.json` `unlevered_lowvol/oos_sharpe 1.7279821897798262 → 1.7279821157955702`,
  `placebo_z 19.864325990635532 → 19.86431552051305`; 28 numeric diffs, **0 keys added/removed**,
  no gate flips — confirmed structurally this session).
- **`check_goldens_clean.py` → PASS** ("ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD") — i.e. the
  working tree equals HEAD; the contamination is *committed into HEAD*, not a dirty working tree.
- **Recovery source verified**: commit `c5038332` (`c5038332a6518a9b681646de8e89ad09e7060ee2`,
  2026-11-24 02:05:45 +0000, "chore(kilo): checkpoint agent session") is an **ancestor of HEAD**,
  and its blobs for all 5 drifted files hash to the **exact pinned SHA-256** in
  `ledger/golden_baseline.json` (verified file-by-file this session). Restoring from it is correct.
- **Data coverage: PASS.** `SEED=42 python3 scripts/check_data_coverage.py` → "ALL 35 PINNED DATA INPUTS
  ARE PRESENT, TRACKED AND UNCHANGED".
- **Environment gap**: `numpy` / `pandas` are **NOT importable** here
  (`ModuleNotFoundError: No module named 'numpy'`). Run `python3 -m pip install -r requirements.txt`
  before any driver, `scripts/check.sh`, or the verification suite. The guard scripts above are
  stdlib-only and run without deps.
- **No interrupted run**: `.verify_snapshot/` and `.verify_reports/` are absent; no live run owns the
  snapshot.
- Working tree clean of tracked source except the ignored `src/__pycache__/cache_keys.cpython-312.pyc`.

## Initial Task (do these in order, then stop)

Do **not** re-pin artifacts, run `check_golden_baseline.py --update`, overwrite goldens, or write
another handoff as a side effect. Do **not** commit unless the user explicitly asks.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist. If a live
   `ACTIVE.json` owner exists, recover with `SEED=42 python3 run_all_verification.py --restore-only`;
   do NOT delete a live snapshot.
2. **Provision environment** — `python3 -m pip install -r requirements.txt`; confirm
   `python3 -c "import numpy, pandas"`.
3. **Reproduce the baseline failure** — `SEED=42 python3 scripts/check_golden_baseline.py`
   (expect FAIL on the 5 files listed above).
4. **Recover the canonical baseline (surgical, 5 files)**:
   ```bash
   git checkout c5038332 -- \
     experiments/cointegration_large_liquid.json \
     experiments/dollar_neutral_lowbeta_large_liquid.json \
     experiments/e037_portfolio.json \
     experiments/e042_lead_config_confirmatory.json \
     experiments/pairs_large_liquid.json
   ```
   (Broad equivalent, safe because only these 5 differ: `git checkout c5038332 -- experiments/`.)
5. **Re-verify the baseline** — `SEED=42 python3 scripts/check_golden_baseline.py`
   → expect "ALL 107 PINNED GOLDEN ARTIFACTS MATCH".
6. **Surface the diff to the user and commit ONLY if asked.** After step 4 the working tree holds the
   clean baseline while HEAD still holds the capture, so `check_goldens_clean.py` will report a
   working-tree-vs-HEAD difference *until the recovery is committed*. That is expected. Commit the 5
   restored files (with a message noting it reverts a verification-run capture, per AGENTS.md) only
   on explicit user approval; then `check_goldens_clean.py` returns to PASS.
7. **Confirm data coverage** — `SEED=42 python3 scripts/check_data_coverage.py` (passes).
8. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

## Real-work task list (do these instead of refreshing the handoff)

1. **Fix the baseline (above) and commit the recovery** — restoring the 5 files from `c5038332`
   reverts a verification-run capture. Surface the diff; commit only if the user asks.
2. **Run real verification** — after deps are installed, `SEED=42 python3 run_all_verification.py
   --extended` (~21 min). Confirm E041/E042 tangency-QP drift stays closed (0 differences)
   **without re-pinning**.
3. **If the extended run is clean, the research is genuinely done** (E001–E043). Say so and stop; do
   not invent new experiments to look busy.
4. **Propose (do not execute) a handoff-file cleanup.** ~3,900+ root handoff files (plus `handoff/`,
   `HANDOFFS/`, `.kilo/handoff/` mirrors) dominate the tree and are actively harmful. Draft a removal
   plan and surface it for approval. Do **not** run the deletion unreviewed, and do not use
   `scripts/repoint_handoff.py` to regenerate aliases as a substitute for cleanup.
5. **Only if the user explicitly asks for new research**: open a new pre-registered experiment
   (E044+) per project conventions. Never re-pin a published number without a ledger entry first
   (E050 precedent).

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — the committed golden is the authoritative record, not
  the latest re-run. Never re-pin to silence drift; never commit verification output; never leave a
  run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`
  (107 artifacts); data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`
  (35 inputs).
- Optimizer: validate on the problem's constraints, not the solver exit status
  (`tests/test_portfolio_opt.py`, ledger E049/E050).
- Always `SEED=42`. Close-to-close is the v1.2.3 primary convention (overnight reported alongside).
- CI workflow cannot be created by automated agents; use local `make check` / `make verify*`.
- Closed items — do not re-open: E049/E050 optimizer determinism + exact KKT enumeration;
  E041/E042 ill-conditioned QP drift. All closed; artifacts reproduce 0 diffs.

## Quick Start Commands

```bash
python3 -m pip install -r requirements.txt                # deps missing here
SEED=42 python3 scripts/check_golden_baseline.py          # FAIL (5) now; MUST pass after recovery
SEED=42 python3 scripts/check_goldens_clean.py            # working tree == HEAD
SEED=42 python3 scripts/check_data_coverage.py            # PASS (35 inputs)
git checkout c5038332 -- experiments/                     # recover canonical baseline (5 files differ)
SEED=42 python3 run_all_verification.py --restore-only    # recover goldens if a run is interrupted
SEED=42 bash scripts/check.sh                             # fast offline sanity check
```

## Key Artifacts

- Golden files: `experiments/*.json` (107 pinned)
- Ledger: `ledger/RESEARCH_LEDGER.md`
- Pinned baselines: `ledger/golden_baseline.json` (107), `ledger/data_baseline.json` (35)
- Recovery commit: `c5038332` (last known clean baseline; ancestor of HEAD)

## Handoff Context

Created at the user's explicit request ("leave a timestamped clear initial task message for the next
agentic work session in a durable handoff"). Supersedes the generic
`handoff_2026-11-28T02-46-19Z_INITIAL_TASK.md` and the last detailed handoff
`handoff_2026-11-28T01-51-56Z_INITIAL_TASK.md`. Baseline state is **unchanged** since `01:51:56Z`
(still broken, same 5 files, same recovery source `c5038332`) and was re-verified at HEAD `b5917288`.
Generic aliases repointed via `scripts/repoint_handoff.py`; `.handoff.md` mirrored. No golden/data
baseline re-pinned, no verification suite run, no verification output committed, no new research
performed, no commit made (recovery left uncommitted pending explicit direction). It leads with the
broken baseline so the next session fixes real state instead of writing another handoff.

*This handoff was created for the next agentic work session.*