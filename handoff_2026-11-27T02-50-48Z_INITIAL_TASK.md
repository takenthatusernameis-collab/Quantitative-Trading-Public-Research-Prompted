# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-27T02:50:48Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact**: `handoff_2026-11-27T02-50-48Z_INITIAL_TASK.md` (repo root)
**Supersedes**: `handoff_2026-11-27T02-01-10Z_INITIAL_TASK.md` (E766 → E767)

## Initial Task (for the next agentic work session)

The research phase is **closed** (E001–E043). There is no new research to invent. Do the
following real work, then **stop** — do not manufacture another handoff refresh as a
substitute for work.

1. **Provision the environment** — `pip install -r requirements.txt`. `numpy` and `pandas`
   are NOT importable this session; the full suite cannot run without them.
2. **Reproduce (real work, not a handoff refresh)** —
   `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift
   precisely. **Do NOT re-pin artifacts to make a tolerance violation disappear** — the
   committed golden is the authoritative record (E049/E050 precedent).
3. **Confirm the tangency-QP drift stays closed** — E041/E042 must reproduce with 0
   differences under the E050 exact active-set solver. If a *deliberate* code change alters a
   published number, record it in the ledger first, then re-pin.
4. **Cleanup (propose only, do not execute)** — ~94% of git-tracked files are `handoff`-prefixed
   artifacts (2,245 handoff-named entries in the repo root alone). If that is a problem,
   *propose* a `.gitignore` + `git rm --cached` plan and let the user decide.
5. **Leave your own single handoff** (procedure below), then stop.

## Baseline Integrity Verification (2026-11-27T02:50:48Z)

- ✅ **No active verification run**: `.verify_snapshot/` and `.verify_reports/` do not exist.
- ✅ **Goldens match HEAD**: `scripts/check_goldens_clean.py` — ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD.
- ✅ **Goldens match pinned baseline**: `scripts/check_golden_baseline.py` — ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT.
- ✅ **Data coverage clean**: `scripts/check_data_coverage.py` — ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED.
- ⚠️ **Missing dependency**: `numpy` and `pandas` are not importable. Run `pip install -r requirements.txt` before the full suite.

## Git State

- Branch: `main`; HEAD `0de3cb76` == `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0 0`).
- `git diff HEAD -- experiments/` empty. Only untracked change is `src/__pycache__/cache_keys.cpython-312.pyc`.

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are documented in
`ledger/RESEARCH_LEDGER.md`. Golden artifacts in `experiments/*.json` are the authoritative
record; never re-pin or overwrite them as a side effect of running verification.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                          # fast convention + template validation (offline)
SEED=42 python3 run_all_verification.py                # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only # recover goldens if interrupted
```

## Recurring handoff procedure

1. `TS` = current UTC (`date -u +%Y-%m-%dT%H-%M-%SZ`).
2. Write `handoff_<TS>_INITIAL_TASK.md` at repo root.
3. Repoint the existing generic aliases only:
   `python3 scripts/repoint_handoff.py handoff_<TS>_INITIAL_TASK.md` (expect `bad=0`).
   **Do not create new mirror directories or new alias names**.
4. Append a short ledger entry (`## E<next> — Durable handoff refresh (<TS>)`).
5. Do not commit unless the user explicitly asks.

## Handoff Context

Created at the user's explicit request to leave a timestamped, clear initial task message for
the next agentic work session. Baseline re-verified clean at this timestamp (all three
pure-Python guards PASS); no snapshot recovery needed; no code changes made. The only
environment gap is the missing `numpy`/`pandas` dependencies.

**Warning — runaway handoff loop (E652–E766):** this repository carries a large number of
git-tracked files, ~94% of which are `handoff`-prefixed artifacts produced by repeated
refresh loops. Do NOT add to that by manufacturing another refresh as a substitute for the
real work above. This handoff is the deliverable; the ledger entry is bookkeeping.