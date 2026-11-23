# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T03:56:52Z
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD**: 6d45343f9e7b814a2064ab12638a8b04ae4cb38f on `main` == `origin/main` (`0  0`)

---

## >>> INITIAL TASK MESSAGE FOR THE NEXT SESSION <<<

You are resuming a **reproducible quantitative-strategy research** repository whose
research phase (E001–E043) is **complete** and whose golden artifacts are the
**authoritative committed baseline**. Read this message top to bottom before doing
anything.

### Live-state warning (read first)

At the moment this handoff was written (2026-11-23T03:56:52Z) a verification run
was **in progress**:

- `.verify_snapshot/ACTIVE.json` existed with `pid=110848` running
  `python3 run_all_verification.py --extended`, ~1116 s (~18.6 min) elapsed.
- If that snapshot is still present and pid 110848 is still alive when you start,
  **do not start another verification run and do not touch `experiments/`** — wait
  for it to finish (it restores the goldens itself) or, if the pid is gone, run
  `SEED=42 python3 run_all_verification.py --restore-only` before doing anything
  else. Only after `.verify_snapshot/` is gone is the working tree trustworthy.
- This session did **not** start the suite (one was already running) and did
  **not** commit any verification output.

### Environment state confirmed this session

- **Dependencies are now provisioned** — `pandas 3.0.6`, `numpy 2.5.4`,
  `scipy 1.18.1`, `pyarrow 26.0.0`, `statsmodels` all import successfully. This
  removes the long-standing blocker that prevented prior sessions from running the
  real suite. There is no longer any excuse to skip `run_all_verification.py`.
- **Data coverage guard PASS**: `scripts/check_data_coverage.py` -> ALL 35 PINNED
  DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED (exit 0).
- **Golden guards report the live run**: `scripts/check_goldens_clean.py` and
  `scripts/check_golden_baseline.py` both returned "verification run in progress
  (pid 110848); golden artifacts temporarily modified by design" (exit 0) — the
  fingerprint comparison is skipped while the suite mutates `experiments/`.
  `git diff HEAD -- experiments/` was therefore **not** asserted empty.

### What is actually needed from you (do real work — do NOT manufacture another handoff)

The repository has accumulated a runaway **handoff-refresh loop** (ledger entries
E652 → E722; **thousands of git-tracked handoff files**). The single most valuable
thing you can do is **break that loop by doing substantive work**, not by writing
yet another `handoff_*_INITIAL_TASK.md`. In priority order:

1. **Confirm the verification run finished, then report its result precisely** —
   which drivers reproduce with 0 differences and which drift (numeric vs
   structural). Use the `--extended` drift report at
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`. Deps are installed, so
   just re-run if it died: `SEED=42 python3 run_all_verification.py --extended`.
   Do **not** re-pin any golden to silence drift. Expected per the ledger: 15/18
   extended drivers reproduce with 0 diffs; E030 and E041 are the known drifters
   (E030 fixed since E048; E041 still 133 numeric diffs from ill-conditioned QP).

2. **Address the E049 E041/E042 ill-conditioned-QP drift** (~133 numeric diffs on
   E041; ~1e-05 drift on 1-ulp perturbations of E042's tangency QP). The optimizer
   exit-status rule is already pinned by `tests/test_portfolio_opt.py`; the
   remaining drift is inherent ill-conditioning. Do **not** re-pin artifacts to
   hide it — document or fix the root cause instead.

3. **Only if explicitly requested by the user**: perform new pre-registered
   research (a new E-numbered driver with a `pre_registered` block, gates, and a
   falsification expectation). Goalposts are never moved post-hoc.

4. **If none of the above is possible in your environment**, *propose* (do not
   execute) a `.gitignore` + `git rm --cached` cleanup of the historical handoff
   clutter, and stop. Do not silently delete tracked history.

Do **not** end your turn having only refreshed the handoff — that is exactly the
behavior (E652–E722) that this file is warning you about.

---

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving validated
strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Baseline Integrity

`experiments/*.json` are canonical artifacts. Never re-pin as a side effect of
running the suite. Backups live in `.verify_snapshot/` (with `ACTIVE.json` holding
the owning pid). Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
The guards `scripts/check_goldens_clean.py` and
`scripts/check_golden_baseline.py` (both first-class `scripts/check.sh` steps)
fail loudly if the working tree or a commit ever diverges from the pinned
fingerprints in `ledger/golden_baseline.json`. Data inputs are pinned by
`ledger/data_baseline.json` and guarded by `scripts/check_data_coverage.py`.

## Handoff File Convention

This file is the canonical durable handoff. Generic alias symlinks
(`handoff_CURRENT.md`, `handoff_LATEST.md`, `next.md`, etc.) in the repo root and
the mirror dirs `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`
are repointed to it via `python3 scripts/repoint_handoff.py <this-filename>`.
Timestamped `HANDOFF_*` and `HANDOFF_NEXT_SESSION_*` files from history are left
untouched to preserve committed history.

## Lint / Format

Python 3 research repository; no separate linter. Run `python3 -m py_compile` on
changed files.