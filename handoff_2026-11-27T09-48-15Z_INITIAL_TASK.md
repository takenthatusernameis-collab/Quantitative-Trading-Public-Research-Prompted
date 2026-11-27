# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-27T09:48:15Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Read this first — you are inside a runaway handoff-refresh loop

This file is the ~773rd "durable handoff" written at a user request to "leave a
timestamped initial task message for the next session." The research phase has
been **closed since E043**. Everything after that (E652–E772, plus this entry)
is the *same* handoff refresh, re-run over and over. The ledger says so itself:
each entry warns against the loop and then commits the loop. **Do not repeat it.**

Concrete evidence of the loop, measured this session (2026-11-27T09:48:15Z):

- **9,244 git-tracked files** have `handoff` in their name; **5,706** sit in the
  repo root alone. ~94% of the tracked tree is handoff noise.
- The last ~120 ledger entries (E652–E772) are all "Durable handoff refresh."
- No research artifact has changed in any of them.

**The deliverable of this session is NOT another handoff.** It is real work
(§"Prioritized real-work task list") or an explicit "nothing to do, baseline
clean" report. If you catch yourself writing `handoff_..._INITIAL_TASK.md` or a
`## E7xx — Durable handoff refresh` ledger entry as the *output*, stop: that is
the loop, not progress.

## Initial Task (for the next agentic work session)

Start from the verified-clean baseline below, do the real work in priority
order, and stop. Do **not** manufacture a handoff refresh, re-pin artifacts, or
overwrite goldens unless a deliberate code change is requested and recorded in
the ledger first.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist.
   If a live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `numpy`/`pandas` are NOT importable in this environment; the full suite and
   most drivers need them.
3. **Confirm goldens match HEAD** — `SEED=42 python3 scripts/check_goldens_clean.py`.
4. **Confirm goldens match pinned baseline** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (all 107 pinned artifacts).
5. **Confirm data coverage** —
   `SEED=42 python3 scripts/check_data_coverage.py` (all 35 pinned inputs).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

If all six pass, the baseline is clean: report that and proceed to the real-work
list. Do not re-run the full suite or re-pin anything as a side effect.

## Prioritized real-work task list (do these instead of refreshing the handoff)

1. **Provision deps and run the real verification.** `pip install -r
   requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended`
   (~21 min). This is the only thing that has not been executed for ~120
   sessions because deps were missing. Report the extended drift summary
   (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`); confirm E041/E042
   tangency-QP drift stays closed (0 differences) **without re-pinning**.
2. **If the extended run is clean, the research is genuinely done.** Say so and
   stop. Do not invent new experiments to look busy.
3. **Propose (do not execute) a handoff-file cleanup.** 9,244 tracked handoff
   files are ~94% of the tree and actively harmful (clone size, search noise,
   review burden). Draft a removal plan (e.g. `git rm` the `handoff_*` /
   `HANDOFF*` families, keep this one + the ledger) and surface it for the
   user's approval. **Do not run the deletion unreviewed**, and do not use
   `scripts/repoint_handoff.py` to regenerate aliases — that is loop machinery.
4. **Only if the user explicitly asks for new research**: open a new
   pre-registered experiment (E044+) per the project conventions. Do not
   re-pin any published number without a ledger entry first (E050 precedent).

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Git State (2026-11-27T09:48:15Z)

- Branch: `main`; HEAD `4fde6011` (checkpoint commit); `origin/main` identical
  (`git rev-list --left-right --count origin/main...HEAD` = `0 0`).
- Working tree clean of tracked source (only `__pycache__/*.pyc` modified).
- `.verify_snapshot/` and `.verify_reports/` absent (no live run owns the snapshot).

## Baseline Integrity (verified 2026-11-27T09:48:15Z)

- ✅ No active verification run: `.verify_snapshot/` does not exist.
- ✅ Golden artifacts match HEAD (`check_goldens_clean.py`: ALL MATCH).
- ✅ All 107 pinned golden artifacts match the baseline fingerprint
  (`check_golden_baseline.py`).
- ✅ All 35 pinned data inputs present, tracked, and unchanged
  (`check_data_coverage.py`).
- ⚠️ Missing dependencies: `numpy`/`pandas` not importable. Run
  `pip install -r requirements.txt` before the full verification suite.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                    # fast convention + template validation (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md`
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Handoff Context

Created at the start of a new agentic work session at the user's explicit
request. No snapshot recovery needed; no code changes made; no commit made
(left uncommitted pending explicit direction). This handoff deliberately does
**not** create mirror directories or repoint aliases, and it leads with the
runaway-loop diagnosis so the next session does real work instead of writing
handoff #774.

*This handoff was created for the next agentic work session.*