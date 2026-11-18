# Agentic Work Session Handoff

**Timestamp:** 2026-11-18T13:35:06Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** 63897932b4197e3733b4a9fe16c2537db6f16fad (2 commits ahead of prior durable handoff target `233b9bd4`, both `chore(kilo): checkpoint agent session`; working tree clean of research/code changes at handoff creation except this handoff's uncommitted artifacts)

---

## Initial Task (for the next agentic work session)

This is the durable starting point for the next automated work session. Read this
file first, then confirm the environment is intact before making any changes.

**This session's only action:** created this timestamped durable handoff and
repointed the generic handoff aliases to it. No code, experiments, data,
goldens, or ledger substance were modified.

**Next session should:**

1. **Orient.** Skim `AGENTS.md` (commands, conventions, invariants) and
   `ledger/RESEARCH_LEDGER.md` (experiment ledger, surviving strategies, open
   items). The research phase is COMPLETE for E001–E051; subsequent E052+ entries
   are durable-handoff refreshes. Do not re-run the whole research program
   unless a ledger open item explicitly calls for it.
2. **Verify integrity before touching anything.** Run the fast offline check:
   ```bash
   SEED=42 bash scripts/check.sh      # or: make check
   ```
   This confirms goldens are clean, the golden baseline matches
   `ledger/golden_baseline.json`, and the data-cache coverage invariant holds.
   If it reports a golden mismatch or stale verification snapshot, recover
   before committing:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or, if HEAD is known-good: git checkout -- experiments/
   ```
3. **Pick up the highest-priority open item** from the ledger, if any. The
   long-standing optimizer-determinism note (E049/E050) is CLOSED; the remaining
   E030/E041 numeric drift is documented and must **NOT** be silenced by
   re-pinning goldens. No actionable OPEN/PENDING/BLOCKED/TODO markers are
   recorded in recent ledger entries.
4. **Work on a branch, keep the baseline authoritative.** Never commit
   verification output; never re-pin goldens as a side effect of a verification
   run.

---

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or
make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Critical Integrity Notes

1. **Golden Files:** `experiments/*.json` are canonical research artifacts. The
   verification suite backs them up to the gitignored `.verify_snapshot/` (with an
   `ACTIVE.json` pid marker) before re-running and restores them afterward — the
   committed baseline is never modified by verification.
2. **Baseline Integrity:**
   - `scripts/check_goldens_clean.py` fails if a tracked artifact under
     `experiments/` differs from HEAD or if a stale snapshot is pending.
   - `scripts/check_golden_baseline.py` compares every artifact against the
     SHA-256 pinned in `ledger/golden_baseline.json`. Replacing an artifact
     requires re-pinning (which shows up in the diff) — **never re-pin as a side
     effect of running the suite.**
3. **Cache Coverage:** Enforced invariant — `scripts/check_data_coverage.py`
   requires every `data.download()` call site to resolve to a committed,
   SHA-256-pinned cache file in `ledger/data_baseline.json`. Unpinned input =
   live network download = non-reproducible. To add a data input, commit the file
   and re-pin with `python3 scripts/check_data_coverage.py --update`.
4. **Optimizer Determinism (ledger E049/E050, closed):** `src/portfolio_opt.py`
   validates a solver answer on the problem's constraints, never on the solver's
   exit status (SLSQP status 8 can be a constrained optimum). E050 added exact KKT
   enumeration for the tangency QP. The E041/E042 grid artifacts still drift by a
   bounded number of 1-ulp differences and are documented — do **not** re-pin them
   to silence the drift.

---

## Reproducibility Requirements

- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG).
- **Convention:** Close-to-close is the v1.2.3 primary convention; overnight
  decomposition reported alongside every strategy.
- **Data:** Cached parquet in `data/` (gitignored except the pinned
  2026-10-12 / 2026-10-11 vintages). E029 fundamentals are separately pinned in
  `data/fundamentals/`; with `SEED` set the driver is fully offline-reproducible.
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy,
  pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional — the optimizer
  falls back to `scipy.optimize` when absent.

---

## Environment Caveat (this runner)

Recent sessions observed that the bare system interpreter `/usr/bin/python3`
(Python 3.12.3) on this runner may not have the core deps importable (e.g.
`pandas`/`numpy`/`scipy`/`pyarrow`/`statsmodels`/`yfinance` missing). If
`scripts/check.sh` or verification steps fail with `ModuleNotFoundError`, fix it
with:

```bash
python3 -m pip install -r requirements.txt
```

This is an environment gap, not a code defect. Re-check imports before assuming
deps are unavailable.

---

## Delta vs Prior Durable Handoff

- **Prior handoff:** `handoff_2026-11-18T13-33-22Z_INITIAL_TASK.md` at HEAD
  `233b9bd4f831f788ef599c6182dbd07d940f0799`.
- **This handoff:** HEAD advanced `233b9bd4` → `63897932` (2 checkpoint commits:
  `233b9bd4 chore(kilo): checkpoint agent session`,
  `63897932 chore(kilo): checkpoint agent session`). No `experiments/`, `data/`,
  `src/`, `tests/`, `scripts/`, or research substance changed in this range.
- Prior closed/conformance state adopted: E001–E051 research complete (E051 last
  research entry, 2026-11-02); E052+ are durable-handoff refreshes only.
  Optimizer-determinism E049/E050 closed; remaining E030/E041 numeric drift is
  documented and must not be re-pinned away.

---

## Handoff Durability

This file is the timestamped durable handoff for this session. Generic aliases
(CURRENT, LATEST, next_session, initial_task, etc. in the repo root, `handoff/`,
`HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`) are repointed to it with:

```bash
python3 scripts/repoint_handoff.py handoff_2026-11-18T13-35-06Z_INITIAL_TASK.md
```

Mirrors are written byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`,
`.kilo/`, and `.kilo/handoff/`.

---

*Created 2026-11-18T13:35:06Z for durable continuity across agentic work sessions.*
