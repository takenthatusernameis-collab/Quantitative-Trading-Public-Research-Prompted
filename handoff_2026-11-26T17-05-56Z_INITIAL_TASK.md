# Handoff: Next Agentic Work Session

**Timestamp**: 2026-11-26T17:05:56Z
**Session**: Quantitative Trading Research — Verification & Reproducibility
**Branch / HEAD**: `main` @ `03b03c7194bc9b4af2a54227b9e89fb82aa7a210` ("chore(kilo): checkpoint agent session")
**Upstream**: `git rev-list --left-right --count origin/main...HEAD` = `0 0` (in sync)

---

## Read this first — the repo is in a handoff loop

This file is the deliverable you asked for. It is also, unavoidably, another entry in
the **E652–E750 runaway handoff-refresh loop** documented in
`ledger/RESEARCH_LEDGER.md`. Measured this session: ~9,578 git-tracked files, of which
~2,132 carry the `handoff_` prefix and ~87% match handoff/current/next/latest/initial_task
patterns. The research itself has been **closed since E043**; everything after that is
bookkeeping churn.

**Do NOT manufacture an E751-style refresh as a substitute for real work.** If you find
yourself writing another handoff file, stop: that is the loop, not progress. The single
most valuable thing you can do is one of the real-work items below, or propose (do not
execute) the cleanup that would end the loop.

To avoid feeding the explosion, this refresh **creates exactly one file and no new alias
symlinks and no mirror directories**. Existing `CURRENT.md` / `current.md` / `*_LATEST`
aliases are deliberately left pointing at their prior targets; this file supersedes them
by name and timestamp.

---

## Initial task message

You are resuming an independent, reproducible quantitative-strategy research repo
(2014–2026 US equities, futures, macro). **Research phase is COMPLETE (E001–E043)**;
surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. Your job is to
**preserve the verified baseline and only add pre-registered work** — never silently
mutate canonical artifacts.

Golden rule: `experiments/*.json` are the authoritative record. Re-pin a golden
(`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`)
**only** for a deliberate, ledger-recorded code/data change — never as a side effect of
running verification, and never to silence a tolerance violation.

---

## Verified state (this session, 2026-11-26T17:05:56Z)

- HEAD `03b03c71` == `origin/main`; working tree clean apart from
  `src/__pycache__/cache_keys.cpython-312.pyc` (expected build noise).
- `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and `.verify_reports/` absent.
- **Dependencies NOT importable** (`import numpy` -> `ModuleNotFoundError`);
  run `pip install -r requirements.txt` before any verification tier.
- **All three pure-Python guards PASS**:
  - `scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
  - `scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH BASELINE
  - `scripts/check_data_coverage.py` -> ALL 35 PINNED DATA INPUTS PRESENT, TRACKED, UNCHANGED
- Full verification suite **not run** this session (deps missing).

---

## Prioritized real-work task list (do one of these, not another handoff)

1. **Verify and stop.** `pip install -r requirements.txt`, then
   `SEED=42 python3 run_all_verification.py --extended`. Report drift precisely
   (per-driver numeric vs structural, worst drift as a multiple of the 1e-4 tolerance).
   Do not re-pin anything. If all 18 extended drivers reproduce with 0 differences,
   record the measurement and stop.
2. **Confirm the E049/E050 tangency-QP drift stays closed** without re-pinning E041/E042
   (exact active-set solver, commit `72dc947`). A re-pin here is only warranted for a
   deliberate, ledger-recorded code change.
3. **Propose (do not execute) the loop-ending cleanup**: a `.gitignore` entry for
   `handoff_*` / `*_LATEST*` / `*_CURRENT*` plus `git rm --cached` of the ~8,000 tracked
   handoff files, leaving the canonical `experiments/`, `ledger/`, `src/`, `scripts/`,
   `data/` pins. Present the plan and wait for explicit approval — do not run it unprompted.

## If instead you must add research (only after 1–2)

1. Read `ledger/RESEARCH_LEDGER.md` for surviving strategies and rejection rationale.
2. Pre-register: falsification expectations + sensitivity grid in the driver docstring and
   its `pre_registered` JSON block, before execution.
3. Add `experiments/run_eXXX.py` following existing driver patterns.
4. Run verification to establish a new golden; record the change in the ledger **before**
   re-pinning.

---

## Verification commands (SEED=42 always)

```bash
make check            # fast convention + integrity guards (~seconds)
make verify-quick     # ~8 min, 8 drivers + batch + validate + E042 n_sim=2
make verify-extended  # ~21 min, +18 committed drivers, structural match
make verify-full      # ~15 min, E042 n_sim=50 + 96-config sensitivity grid
# Recovery if a run is interrupted:
SEED=42 python3 run_all_verification.py --restore-only
```

## Environment
- Python 3; deps in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
- Optional cvxpy/cvxopt (optimizer falls back to scipy).
- Offline mode `QUANT_RESEARCH_OFFLINE=1` (used by the verification suite).

---

**Next agent**: `pip install -r requirements.txt`, then
`SEED=42 python3 run_all_verification.py --extended`, report drift, and stop. Do not
write another handoff. Do not commit until `make check` is green and `experiments/` is
unchanged.

(End of file - total 108 lines)
`