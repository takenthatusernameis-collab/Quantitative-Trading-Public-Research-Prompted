# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-27T23:42:48Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `9334a210a5e7ad8dd563b11bba46b50ab862bc7d` (2026-11-27 23:42:07 +0000) == origin/main
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean. No `.verify_snapshot/`. `experiments/`, `data/`, `ledger/` match HEAD.

Written at the explicit request of the user: *"Leave a timestamped clear initial task
message for the next agentic work session in a durable handoff !"* This file is the
authoritative initial-task message and supersedes `HANDOFF_2026-11-27T19-44-31Z_INITIAL_TASK.md`
and the `CURRENT.md` / `current.md` pointers dated 2026-11-27T20:44:50Z.

---

## Read this first — the real, verified state (checked 2026-11-27T23:42:48Z)

1. **The golden baseline is BROKEN at HEAD. This is the real, urgent finding.**
   `SEED=42 python3 scripts/check_golden_baseline.py` **FAILS**: 5 committed artifacts
   under `experiments/` differ from the SHA-256 pinned in `ledger/golden_baseline.json`,
   while `scripts/check_goldens_clean.py` still **PASSES** (working tree == HEAD). That
   combination means a `chore(kilo): checkpoint agent session` commit captured
   verification-run output and replaced the canonical baseline — the exact failure mode
   AGENTS.md warns about (precedents: `d6042b0`/`9f20def`, `1623923`, `701ed78`). HEAD
   `9334a210` is contaminated; do **not** re-pin to "silence" it.

   The 5 differing artifacts (pinned → actual):
   - `experiments/cointegration_large_liquid.json`
   - `experiments/dollar_neutral_lowbeta_large_liquid.json`
   - `experiments/e037_portfolio.json`
   - `experiments/e042_lead_config_confirmatory.json`
   - `experiments/pairs_large_liquid.json`

2. **You are also inside the ~777th handoff-refresh loop.** The research phase has been
   closed since E043; E652–E776 are the same "durable handoff refresh" re-run over and
   over (~9,351 git-tracked `handoff`-named files, ~94% of the tree). Do **not**
   manufacture an E777-style refresh as your deliverable.

**The deliverable of this session is #1 (fix the baseline) or an explicit
"nothing to do" report — NOT another handoff.**

---

## CLEAR INITIAL TASK (do these in order, then stop)

Do **not** re-pin artifacts, overwrite goldens, or write a new handoff as a side effect.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist. If a
   live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`. `numpy`/`pandas` are
   NOT importable here (verified: `ModuleNotFoundError: No module named 'numpy'`); the
   suite and most drivers need them.
3. **Reproduce the baseline failure** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (expect the 5-file FAIL above).
4. **Recover the canonical baseline** (verified target, see below):
   `git checkout c5038332 -- experiments/`
   then re-run step 3 → expect `ALL 107 PINNED GOLDEN ARTIFACTS MATCH` (exit 0).
5. **Confirm goldens match HEAD + data coverage** —
   `SEED=42 python3 scripts/check_goldens_clean.py` and
   `SEED=42 python3 scripts/check_data_coverage.py` (both already exit 0; re-confirm).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

If all pass after recovery, the baseline is clean again: report that and proceed to the
real-work list. Do not re-run the full suite or re-pin anything as a side effect.

---

## Baseline recovery target (verified this session, 2026-11-27T23:42:48Z)

- **Newest clean commit**: `c5038332` (2026-11-24 02:05:45 +0000). Verified by hashing
  the 5 files at each candidate commit against `ledger/golden_baseline.json`:
  `c5038332` is the only CLEAN one; `72a52c92`, `8cd55e5e`, and HEAD `9334a210` are all
  dirty on exactly those 5 files. The other 102 pinned artifacts are already identical,
  so `git checkout c5038332 -- experiments/` fully restores the baseline.
- Do **not** use `git checkout -- experiments/` as the recovery — HEAD already carries
  the captured run, so that would restore the contaminated files. Restore from
  `c5038332` (or re-pin deliberately via `python3 scripts/check_golden_baseline.py
  --update` **only** if a deliberate code change is the cause and is recorded in the
  ledger first — that is not the case here).

## Verified state snapshot (2026-11-27T23:42:48Z)

- HEAD `9334a210` == origin/main; working tree clean; no `.verify_snapshot/`.
- `check_goldens_clean.py`: PASS (working tree == HEAD).
- `check_data_coverage.py`: PASS (35 pinned data inputs present, tracked, unchanged).
- `check_golden_baseline.py`: FAIL (5 artifacts, listed above).
- `numpy`/`pandas`: not importable (run `pip install -r requirements.txt` first).
- Git-tracked handoff-named files: 9,351 (the refresh loop — do not add to it
  unnecessarily).

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores
  them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs
  `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs
  `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see
  `tests/test_portfolio_opt.py`, ledger E049/E050 — closed; E041/E042 ill-conditioned-QP
  drift closed, artifacts reproduce 0 diffs).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the
  committed golden is the authoritative record.

## Handoff provenance

Supersedes `HANDOFF_2026-11-27T19-44-31Z_INITIAL_TASK.md` and the `CURRENT.md` /
`current.md` pointers dated 2026-11-27T20:44:50Z. This file is the authoritative
initial-task message for the next session. Written by agent at 2026-11-27T23:42:48Z.