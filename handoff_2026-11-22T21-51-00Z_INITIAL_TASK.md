# Agentic Work Session Handoff — INITIAL TASK

**Created:** 2026-11-22T21:51:00Z
**Status:** Durable initial task message — for the next agentic work session
**Repo HEAD at creation:** `27d3164685c3db4c7096f65ff90f51824194873b` on `main` (== `origin/main`, clean tree)

---

## Initial Task Message (read this FIRST)

The quantitative-strategy research phase is **COMPLETE**: experiments E001–E043 are
finalized and the surviving validated strategies are recorded in
`ledger/RESEARCH_LEDGER.md`. There is **no open research task** awaiting execution.

**Do NOT default to writing another handoff file as your deliverable.**
Between roughly E652 and E712 the only "work" performed in this repository was a
runaway loop of timestamped handoff refreshes — thousands of near-identical
`handoff_*_INITIAL_TASK.md` files, each re-asserting that the research phase was
closed and then closing again. That is not progress; it is a no-op loop and it is
explicitly called out as such in the ledger. Producing yet another refresh is the
single most likely (and least useful) way to spend this session. If your only
instruction is "leave a handoff", write one file, run the guards below, repoint the
generic aliases, and stop.

### What to actually do

Pick ONE of the following and state which you chose in your first reply:

1. **Verify the baseline and stop.** The cleanest correct action. Run the
   read-only guards, confirm the tree is healthy, and report back — no new files,
   no new commits:
   ```bash
   SEED=42 python3 scripts/check_goldens_clean.py      # expect: ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
   SEED=42 python3 scripts/check_golden_baseline.py    # expect: ALL 107 PINNED GOLDEN ARTIFACTS MATCH
   git status --short                                  # expect: empty
   ```
   If all pass, the repository is sound. Report and end the session.

2. **Run the real verification suite** if you need end-to-end proof:
   ```bash
   SEED=42 python3 run_all_verification.py --full       # ~15 min
   ```
   Restore goldens with `--restore-only` if interrupted. Do NOT commit verification
   output.

3. **Do genuinely new research** only if the user has explicitly asked for a new
   experiment. Pre-register it first (docstring with gates + falsification
   expectations), pin any new data input (cache-coverage invariant), and use
   `SEED=42`.

---

## Project Context

- Repository: `Quantitative-Trading-Public-Research-Prompted`
- Root: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Research phase complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts: `experiments/*.json` (committed goldens; never modified by verification runs).
- Verification suite: `run_all_verification.py` backs up and restores `experiments/` goldens.

## Quick Start Commands

- Convention-robustness check (~seconds, offline): `SEED=42 bash scripts/check.sh` or `make check`
- Convention-only verify: `SEED=42 python3 run_all_verification.py --skip-slow`
- Quick full verify (~8 min): `SEED=42 python3 run_all_verification.py`
- Full verify (~15 min): `SEED=42 python3 run_all_verification.py --full`
- Individual driver: `SEED=42 python3 experiments/run_e042.py --n-sim 50`

## Rules (hard constraints)

- Always use `SEED=42` for reproducibility.
- Never commit verification output. If a run is interrupted, restore goldens with
  `SEED=42 python3 run_all_verification.py --restore-only` (or
  `git checkout <commit> -- experiments/<file>` for a pinned artifact).
- Do NOT re-pin goldens or data baselines to silence drift; see the ledger open items.
- Data inputs must be committed and SHA-256 pinned (cache-coverage invariant) before any
  offline run; the suite runs with `QUANT_RESEARCH_OFFLINE=1`.
- Research is pre-registered: gates and falsification expectations are declared before
  execution and never moved post-hoc.

## State at Creation (verified 2026-11-22T21:51:00Z)

- HEAD `27d3164685c3db4c7096f65ff90f51824194873b` on `main` == `origin/main` (`0  0`).
- `git status --short` empty (clean tree); `git diff HEAD -- experiments/` empty.
- `.verify_snapshot/` and `.verify_reports/` absent.
- **Both pure-Python golden guards executed and PASS**: `check_goldens_clean.py` ->
  `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (exit 0); `check_golden_baseline.py` ->
  `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0).
- Full verification suite NOT run (deps not provisioned this session).

## Notes for the Next Session

- Check `git status` and `git log --oneline -10` before starting.
- Confirm no live verification run owns `.verify_snapshot/ACTIVE.json` (a stale snapshot
  means a previous run was killed; recover with `--restore-only`).
- Read the tail of `ledger/RESEARCH_LEDGER.md` before acting — it records the full
  history, including the handoff-refresh runaway loop this message warns against.

(End of file.)
