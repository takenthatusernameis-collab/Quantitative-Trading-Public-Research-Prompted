# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-27T20:43:37Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Supersedes**: handoff_2026-11-27T20-42-51Z_INITIAL_TASK.md

## Read this first

Research phase is complete (E001–E043). The deliverable of this session is real
work or an explicit "baseline clean" report — NOT another handoff refresh. Do
not re-pin artifacts, overwrite goldens, or regenerate alias symlinks unless a
deliberate code change is requested and recorded in the ledger first.

## Initial Task (for the next agentic work session)

Start from the verified-clean baseline below, do the real work in priority order,
and stop.

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist
   (confirmed absent at 2026-11-27T20:43:37Z). If a live `ACTIVE.json` owner
   exists, recover with `SEED=42 python3 run_all_verification.py --restore-only`;
   do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `numpy`/`pandas` are NOT importable (confirmed this session); most drivers
   need them.
3. **Confirm goldens match HEAD** — `SEED=42 python3 scripts/check_goldens_clean.py`.
4. **Confirm goldens match pinned baseline** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (107 pinned artifacts).
5. **Confirm data coverage** —
   `SEED=42 python3 scripts/check_data_coverage.py` (35 pinned inputs).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

If all six pass, the baseline is clean: report that and proceed to the real-work
list. Do not re-run the full suite or re-pin anything as a side effect.

## Prioritized real-work task list (do these instead of refreshing the handoff)

1. **Provision deps and run the real verification.** `pip install -r
   requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended`
   (~21 min). Report the extended drift summary
   (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`); confirm E041/E042
   tangency-QP drift stays closed (0 differences) **without re-pinning**.
2. **If the extended run is clean, the research is genuinely done.** Say so and
   stop. Do not invent new experiments to look busy.
3. **Propose (do not execute) a handoff-file cleanup.** Thousands of tracked
   `handoff_*` / `HANDOFF*` files are ~94.5% of the tree and actively harmful.
   Draft a removal plan (keep the current one + the ledger) and surface it for
   the user's approval. **Do not run the deletion unreviewed.**
4. **Only if the user explicitly asks for new research**: open a new
   pre-registered experiment (E044+) per the project conventions. Do not re-pin
   any published number without a ledger entry first (E050 precedent).

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Git State (2026-11-27T20:43:37Z)

- Branch: `main`; HEAD `7f69b553` (checkpoint commit).
- Working tree clean of tracked source (only `src/__pycache__/*.pyc` modified).
- `.verify_snapshot/` and `.verify_reports/` absent (no live run owns the snapshot).

## Baseline Integrity (to be confirmed this session)

- No active verification run: `.verify_snapshot/` does not exist (confirmed).
- Golden artifacts match HEAD (`git diff HEAD -- experiments/` empty).
- Pinned baselines present: `ledger/golden_baseline.json` (107 artifacts),
  `ledger/data_baseline.json` (35 inputs).
- Missing dependencies: `numpy`/`pandas` not importable (confirmed). Run
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
(left uncommitted pending explicit direction). Deliberately does not create
mirror directories or new alias names beyond the single `handoff_CURRENT`
pointer; leads with the real-work list so the next session does real work
instead of writing another handoff refresh.

*This handoff was created for the next agentic work session.*