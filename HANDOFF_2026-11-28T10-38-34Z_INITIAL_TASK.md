# INITIAL TASK — Handoff for Next Agentic Work Session

**Timestamp (UTC): 2026-11-28T10:38:34Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `d9770a21b5f46c142a75226470c1078a3691f32e` (== `origin/main`)
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Working Tree:** clean (0 changes vs HEAD). `.verify_snapshot/` absent (no interrupted run).

> All state below was **verified live this session** at 2026-11-28T10:38:34Z — not copied
> from older handoffs. HEAD has advanced since the previous handoff (`213ab5e9` →
> `d9770a21`, checkpoint commits) but the canonical state is unchanged.

## ⚠️ Read this first — the golden baseline is BROKEN at HEAD

`SEED=42 python3 scripts/check_golden_baseline.py` → **FAIL (5 of 107 pinned artifacts
differ from `ledger/golden_baseline.json`)**. `check_goldens_clean.py` → PASS only because
the working tree == HEAD; **HEAD itself carries the contaminated baseline** (a prior
verification-run capture was committed). Do **not** re-pin to silence it — AGENTS.md
precedent: `d6042b0`/`9f20def`, `1623923`, `701ed78` (all reverted).

The 5 drifted artifacts (pinned → actual SHA-256):

| File | pinned | actual (at HEAD) |
|---|---|---|
| `experiments/cointegration_large_liquid.json` | `a4118252…c4120e2` | `33a35b18…ccd402a6` |
| `experiments/dollar_neutral_lowbeta_large_liquid.json` | `c657c3af…d38b2aa3` | `d946bdd6…4a67b6` |
| `experiments/e037_portfolio.json` | `dcaeb797…d7adde7` | `4eedc526…d6834` |
| `experiments/e042_lead_config_confirmatory.json` | `fa06eeb8…c901921` | `71c04548…c79f951` |
| `experiments/pairs_large_liquid.json` | `5ab39998…64ac95d` | `07f258de…3b51b850b` |

**Recovery source (verified this session):** commit `c5038332` — `git show
c5038332:experiments/<file> | sha256sum` matches the pinned SHA-256 for **all 5** files.
`git checkout c5038332 -- experiments/` restores the canonical baseline.

Other checks (verified live):
- `check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (HEAD is the problem).
- `check_data_coverage.py` → `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED`.
- `pandas`/`numpy` are **not importable** — run `pip install -r requirements.txt` before any
  full verification run.
- `.verify_snapshot/` absent; working tree fully clean.

## CLEAR INITIAL TASK (do these in order, then stop)

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist. If a live
   `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
3. **Reproduce the baseline failure** — `SEED=42 python3 scripts/check_golden_baseline.py`
   (expect the 5 files above).
4. **Recover the canonical baseline** — `git checkout c5038332 -- experiments/`, then re-run
   step 3 → expect `ALL 107 PINNED GOLDEN ARTIFACTS MATCH`.
5. **Confirm goldens + data coverage** —
   `SEED=42 python3 scripts/check_goldens_clean.py` and
   `SEED=42 python3 scripts/check_data_coverage.py` (both pass).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

Do **not** re-pin artifacts, run `check_golden_baseline.py --update`, overwrite goldens, or
write another handoff as a side effect. If all pass after recovery, report that and proceed to
real work.

## Real-work task list (do these instead of refreshing the handoff)

1. **Fix + commit the baseline recovery** — restoring the 5 files from `c5038332` reverts a
   verification-run capture. Surface the diff for the user; commit only if the user asks.
2. **Run real verification** — `SEED=42 python3 run_all_verification.py --extended` (~21 min).
   Confirm E041/E042 tangency-QP drift stays closed (0 differences) **without re-pinning**.
3. **If the extended run is clean, the research is genuinely done** (E001–E043). Say so and
   stop. Do not invent new experiments to look busy.
4. **Propose (do not execute) a handoff-file cleanup.** The tree carries **thousands of
   tracked handoff files** (most of the tree, actively harmful). ⚠️ Do **not** run
   `scripts/repoint_handoff.py` casually — with no args/`--help` it rewrites 587+ alias/mirror
   files across `.handoff/`, `.kilo/`, repo root and `src/` as a side effect. Draft a removal
   plan and surface it for the user's approval; do not delete unreviewed.
5. **Only if the user explicitly asks for new research**: open a new pre-registered experiment
   (E044+) per project conventions. Never re-pin a published number without a ledger entry
   first (E050 precedent).

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them;
  never commit verification output or leave a run half-finished (recover with `--restore-only`).
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`;
  data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (`tests/test_portfolio_opt.py`,
  ledger E049/E050). The committed golden is the authoritative record.
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 scripts/check_golden_baseline.py      # MUST pass after recovery (107 artifacts)
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 python3 scripts/check_data_coverage.py
SEED=42 python3 run_all_verification.py --restore-only # recover goldens if interrupted
git checkout c5038332 -- experiments/                 # recover canonical baseline (verified)
```

## Key Artifacts

- Golden files: `experiments/*.json` · Ledger: `ledger/RESEARCH_LEDGER.md`
- Pinned baselines: `ledger/golden_baseline.json` (107), `ledger/data_baseline.json` (35)

## Handoff provenance

Created at the user's explicit request ("leave a timestamped clear initial task message for the
next agentic work session in a durable handoff"). Supersedes
`handoff_2026-11-28T10-38-07Z_INITIAL_TASK.md` and all earlier INITIAL_TASK handoffs. Baseline
state is **unchanged** since 10-38-07Z: still broken, same 5 files, same recovery source
`c5038332`; only HEAD advanced (`213ab5e9` → `d9770a21`). No golden/data baseline re-pinned, no
verification suite run, no verification output committed, no new research performed, **no commit
made** (this file is left uncommitted pending explicit direction). It leads with the broken
baseline so the next session fixes real state instead of writing another handoff.

*This handoff was created for the next agentic work session.*