# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T08:51:26Z
**Session**: Initial handoff for the next agentic work session (durable artifact E677)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch / HEAD**: `main` @ `3a87e8c0bf1c43a81339d5dfe5d833624074a1e7` (== `origin/main`)

## TL;DR — what to do first

This is a **durable handoff refresh only** — no research was performed to produce it.
The research phase is **closed** (E001–E043 complete). Your first job is orientation,
not new experiments:

1. Read `ledger/RESEARCH_LEDGER.md` (tail) and `ledger/PRIORITIZATION.md` for current
   strategy dispositions and the procedure version in force (v1.2.7 active).
2. Run `SEED=42 bash scripts/check.sh` to confirm the environment and that no golden
   artifact has drifted from HEAD.
3. If you intend to run the full suite, use `SEED=42 python3 run_all_verification.py`
   (or `make verify-quick`) and **never leave it half-finished** — restore goldens with
   `SEED=42 python3 run_all_verification.py --restore-only` if interrupted.
4. Record any real new work as a new numbered entry in the ledger (next free slot is
   **E677**; see "Ledger numbering" below) and refresh this handoff at the end.

## Project Status

- **Research Phase**: Complete (E001–E043). All surviving validated strategies are
  documented in `ledger/RESEARCH_LEDGER.md`.
- **Validated components** (per PRIORITIZATION v1.2.6): equity TSM flagship (β-bearing),
  DN low-beta sort, futures TSM 18m, futures realized-roll-yield carry, macro momentum.
  The market-neutral *total-portfolio* line is **CLOSED** (E041 REJECTED 3/5;
  E042/E042b PARTIAL 4/5 — G2 placebo z below 3.0).
- **Current State**: Ready for verification / reproduction tasks only; the novelty
  search (E001–E039) and portfolio-construction phase are done.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; re-executes all 26 committed drivers)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Verified State at This Handoff

- HEAD `3a87e8c0bf1c43a81339d5dfe5d833624074a1e7` on `main` == `origin/main`
  (commit `chore(kilo): checkpoint agent session`, 2026-11-22 08:50:12 +0000).
- `git diff HEAD -- experiments/` is empty (no golden drift).
- `.verify_snapshot/` and `.verify_reports/` are absent (no interrupted run pending).
- Pre-existing working-tree modifications were 12 `__pycache__/*.pyc` bytecode files.
  This refresh adds the six new handoff copies and repoints the 512 tracked alias
  symlinks (both expected). No source, ledger, data, or `experiments/` file is
  modified.
- Golden guards (pure-stdlib, run this session): `scripts/check_goldens_clean.py` ->
  ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD; `scripts/check_golden_baseline.py` ->
  ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT.

## Key Notes

1. **Always use `SEED=42`** for reproducibility (walk-forward + placebo RNG).
2. **Golden files**: `experiments/*.json` are the canonical research artifacts. The
   verification suite overwrites them while re-running drivers and restores them
   afterwards — a run must never be left half-finished.
3. **Never commit verification output**. If a run is interrupted, restore before
   committing: `SEED=42 python3 run_all_verification.py --restore-only` (or
   `git checkout -- experiments/`). If HEAD already carries a captured run, restore
   the pinned artifact from the last commit whose SHA-256 matches
   `ledger/golden_baseline.json`.
4. **Data cache**: pinned vintages in `data/vintages.json`; E029 fundamentals pinned
   in `data/fundamentals/` per `data/fundamentals_vintages.json`. Cache coverage is
   an enforced invariant (`scripts/check_data_coverage.py`); an unpinned input is a
   live network download and yfinance is not bit-reproducible.
5. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow,
   statsmodels, yfinance). `cvxpy`/`cvxopt` are optional; the optimizer falls back to
   `scipy.optimize`.
6. **Optimizer determinism (E049)**: `src/portfolio_opt.py` validates a solver answer
   on the *problem constraints*, not on the solver exit status. The tangency QP is
   ill-conditioned; E041/E042 grid artifacts still drift by 29–133 differences at
   1e-4 tolerance. **Do NOT re-pin them to silence that** — see the open ledger item.

## Important Conventions

- **Pre-registration**: every experiment driver has a `pre_registered` JSON block and
  a docstring stating gates, falsification expectations, and sensitivity grid before
  execution. Goalposts are never moved post-hoc.
- **Multiple-testing discipline**: sensitivity grids are "reported, not gated." A grid
  config that clears gates requires a dedicated pre-registered confirmatory run with a
  full placebo before promotion.
- **Negative results** are recorded honestly (REJECTED / PARTIAL) with evidence.
- **Convention**: close-to-close is the v1.2.3 primary; overnight decomposition is
  reported alongside every strategy.
- **Premise verification (v1.2.1)**: verify every factual premise against recorded
  experiment JSONs/artifacts before pre-registering a follow-up.

## Ledger Numbering

The committed ledger's true last entry is **E676** (2026-11-22T08-47-45Z). The next
free slot is **E677**. Handoff *filenames* self-assign numbers that are not reliable
ledger references (see E673's numbering-drift note); append to the ledger yourself and
use the ledger's max as the source of truth.

## Next Steps for the New Session

1. Run `SEED=42 bash scripts/check.sh` to verify the environment and confirm no
   golden drift (expect: all guards PASS).
2. Read the tail of `ledger/RESEARCH_LEDGER.md` (from E660 onward) for open items:
   E041 optimizer drift, E049 tangency-QP ill-conditioning, E029/E030 re-pin notes.
3. Run `make verify-quick` (recommended first full run); escalate to `--extended` /
   `--full` only if you need the full driver re-execution.
4. If you do real work: append a new numbered ledger entry, regenerate this handoff
   with a fresh timestamp, mirror it to the five durable dirs, and repoint aliases via
   `python3 scripts/repoint_handoff.py <new-handoff-filename>`.
5. Leave the tree in the same clean state you found it (no verification output staged,
   goldens untouched, `__pycache__` is the only expected working-tree noise).

## Durable Artifact

This file: `handoff_2026-11-22T08-51-26Z_INITIAL_TASK.md` — mirrored byte-identically to
`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, and repointed as the
target of the generic stable aliases (`handoff_current`, `HANDOFF_LATEST`, `NEXT`,
`INITIAL_TASK`, `handoff.md`, etc.) via `scripts/repoint_handoff.py`.