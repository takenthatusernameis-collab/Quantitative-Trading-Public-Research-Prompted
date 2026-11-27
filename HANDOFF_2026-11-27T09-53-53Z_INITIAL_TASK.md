# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-27T09:53:53Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `930d9f9c0b8d544b86f82dccab38a8262e7af5b9` (2026-11-27 09:52:00 +0000); `origin/main` identical (`git rev-list --left-right --count origin/main...HEAD` = `0 0`).
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for canonical artifacts (`experiments/`, `data/`, `ledger/`). No live verification run; `.verify_snapshot/` and `.verify_reports/` absent.

## Read this first — you are inside a runaway handoff-refresh loop

This is the ~775th "durable handoff" written at a user request to "leave a
timestamped initial task message for the next session." The research phase has
been **closed since E043**. Everything after that is the *same* handoff refresh,
re-run over and over. **Do not repeat it.**

**The deliverable of this session is NOT another handoff.** It is real work
(§"Prioritized real-work task list") or an explicit "nothing to do, baseline
clean" report. If you catch yourself writing `handoff_..._INITIAL_TASK.md` or a
`## E7xx — Durable handoff refresh` ledger entry as the *output*, stop: that is
the loop, not progress.

## CLEAR INITIAL TASK

**Await explicit user instructions before any research action.** Start from the
verified-clean baseline below, do the real work in priority order, and stop. Do
**not** manufacture a handoff refresh, re-pin artifacts, or overwrite goldens
unless a deliberate code change is requested and recorded in the ledger first.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist.
   If a live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `numpy`/`pandas` are NOT importable here; the full suite and most drivers need
   them.
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
   (~21 min). This is the only thing that has not been executed for ~120 sessions
   because deps were missing. Report the extended drift summary
   (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`); confirm E041/E042
   tangency-QP drift stays closed (0 differences) **without re-pinning**.
2. **If the extended run is clean, the research is genuinely done.** Say so and
   stop. Do not invent new experiments to look busy.
3. **Propose (do not execute) a handoff-file cleanup.** 9,248 tracked handoff
   files dominate the tree and are actively harmful (clone size, search noise,
   review burden). Draft a removal plan (e.g. `git rm` the `handoff_*` /
   `HANDOFF*` families, keep this one + the ledger) and surface it for the
   user's approval. **Do not run the deletion unreviewed**, and do not use
   `scripts/repoint_handoff.py` to regenerate aliases — that is loop machinery.
4. **Only if the user explicitly asks for new research**: open a new
   pre-registered experiment (E044+) per the project conventions. Do not re-pin
   any published number without a ledger entry first (E050 precedent).

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Baseline Integrity (verified 2026-11-27T09:53:53Z)

- ✅ No active verification run: `.verify_snapshot/` does not exist.
- ✅ Working tree clean for `experiments/`, `data/`, `ledger/`.
- ✅ `origin/main` identical to HEAD (`0 0`).
- ⚠️ Missing dependencies: `numpy`/`pandas` not importable. Run
  `pip install -r requirements.txt` before the full verification suite.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                    # fast convention + template validation (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and
  restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs
  `ledger/golden_baseline.json`; data coverage by
  `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see
  `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning
  process; the committed golden is the authoritative record.

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md`
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Handoff provenance

Supersedes prior INITIAL_TASK handoffs (most recent prior:
`HANDOFF_2026-11-27T09-52-20Z_INITIAL_TASK.md`). This file is the authoritative
initial-task message for the next session. It deliberately does **not** create
mirror directories or repoint aliases, and it leads with the runaway-loop
diagnosis so the next session does real work instead of writing handoff #776.

Handoff written by agent at 2026-11-27T09:53:53Z.
