# Agentic Work Session Handoff — Initial Task

**Timestamp (UTC):** 2026-11-23T06:27:35Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Research phase:** CLOSED — E001–E043 complete; surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No new experiment is authorized.

## READ THIS FIRST — you are inside a runaway handoff loop

This repo is in a pathological state that every recent session has flagged and
then re-created. Do not repeat it.

- **8,211 of 8,736 git-tracked files (~94%) are handoff files.** Handoffs E652 →
  E722 are all "Durable handoff refresh" entries that accomplished nothing except
  adding another near-duplicate file and repointing symlinks.
- Each session has been asked to "leave a timestamped handoff for the next
  session," done exactly that, and produced handoff #N+1 — including this one.
- **The existing handoff from one minute ago
  (`handoff_2026-11-23T06-26-22Z_INITIAL_TASK.md`) was already accurate and
  current.** This file supersedes it only by timestamp, not by content.

The honest, high-value action for the next session is NOT to manufacture
E724-style refreshes. Pick a task from the prioritized list below.

## State at handoff time (verified this session, 2026-11-23T06:27:35Z)

- Branch `main`, HEAD `6d15fcebccd0b01848c54e3045ada76aecb64dc1`; `git rev-list
  --left-right --count origin/main...HEAD` = `0  0` (in sync).
- `git diff HEAD -- experiments/` empty; no `.verify_snapshot/` or
  `.verify_reports/` present.
- Working tree: only one benign tracked bytecode artifact
  (`src/__pycache__/cache_keys.cpython-312.pyc`) — a compile cache, not a source
  change. Do not commit it.
- All three pure-Python guards PASS this session (hashlib-only, no deps needed):
  - `scripts/check_goldens_clean.py` → ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
  - `scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH
    THE BASELINE FINGERPRINT
  - `scripts/check_data_coverage.py` → ALL 35 PINNED DATA INPUTS ARE PRESENT,
    TRACKED AND UNCHANGED
- Reproducibility baseline: all 18 extended drivers reproduced with 0
  differences at the 2026-11-23T05:17Z measurement (numpy 2.5.4, scipy 1.18.1).

## Prioritized task list for the next session (do real work, in this order)

1. **Verify-and-stop (lowest cost, highest value).** Re-run the three guards
   above, report PASS, and STOP. Do not write a new handoff. Do not add a ledger
   entry. This alone breaks the loop.

2. **Run the real verification suite.** The environment can provision deps
   (`pypi.org` reachable; `python3 -m pip` present); only `pip install -r
   requirements.txt` is missing. Then:
   ```bash
   pip install -r requirements.txt
   SEED=42 python3 run_all_verification.py --extended
   ```
   Report drift precisely (per-driver, numeric vs structural, worst as a
   multiple of tolerance). `--extended` writes a gitignored report to
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` and never touches
   `experiments/`. If a run is interrupted, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`.

3. **Address the E049 E041/E042 ill-conditioned-QP drift — WITHOUT re-pinning.**
   Per ledger E050 the tangency QP is now bit-reproducible via exact KKT
   active-set enumeration, so there is no remaining tolerance violation to
   silence. Do not re-pin E041/E042 to "fix" a violation; re-pinning is only
   warranted for a deliberate code change that alters a published number, and
   that change must be recorded in the ledger first (E050 precedent).

4. **Propose (do NOT execute) the handoff-clutter cleanup.** If you want to
   actually fix the loop rather than feed it, write up a concrete proposal: a
   `.gitignore` rule for future `handoff_*_INITIAL_TASK.md` files plus
   `git rm --cached` of the historical clutter. Present it for approval; do not
   run destructive git commands unprompted.

5. **Explicitly-requested pre-registered research only.** No new experiment is
   authorized. If the user asks for one, follow the full pre-registration
   discipline (gates, falsification expectations, sensitivity grid before
   execution; grids are "reported, not gated").

## If you truly must leave a handoff, leave ONE and stop

If (and only if) a future session explicitly requires a fresh timestamped
handoff, write a single file, repoint the generic aliases, add one ledger entry,
and STOP. Do not loop. The pattern that produced 8,211 files is the bug.

## Verification commands available

```bash
# Fast convention-robustness + template check (~seconds, offline)
SEED=42 bash scripts/check.sh        # or: make check

# Quick full verification (~8 min; 8 experiment drivers)
SEED=42 python3 run_all_verification.py            # or: make verify-quick

# Extended verification (~21 min; +18 committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full     # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py    # or: make verify

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Conventions to remember

- Always use `SEED=42`. Walk-forward + placebo RNG depend on it.
- `experiments/*.json` are committed golden artifacts; verification drivers
  overwrite them and restore afterwards. Never commit verification output.
- Reproducibility: run with `QUANT_RESEARCH_OFFLINE=1`; all data inputs must be
  pinned (tracked + SHA-256 in `ledger/data_baseline.json`). yfinance is not
  bit-reproducible, so an unpinned input is a live download and fails coverage.
- Do NOT re-pin E041/E042 goldens to silence a tolerance violation — there is no
  remaining violation. Re-pin only for a deliberate code change that alters a
  published number, and record it in the ledger first (see the E050 precedent).
- `src/portfolio_opt.py` validates solver answers on the problem's constraints,
  never on the solver's exit status (ledger E049). Do not gate on SLSQP exit
  status.
- Lint/typecheck: run `python3 -m py_compile` on changed Python files (no
  separate linter configured). The verification suite also py_compiles drivers.
- Pre-registration: never move goalposts post-hoc. Sensitivity grids are
  "reported, not gated." Negative results are recorded honestly.
- Commit messages should match repo style; only commit when explicitly asked.

## Board

Use `board_post`/`board_read` for peer coordination when multiple agents are
involved. Your own row is flagged self: true — do not post to yourself. Share
material findings (baseline mismatches, stale snapshots, blockers) rather than
routine progress.