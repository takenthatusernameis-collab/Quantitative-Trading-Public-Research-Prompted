# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-26T23:47:30Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact**: `handoff_2026-11-26T23-47-30Z_INITIAL_TASK.md` (repo root)
**Supersedes**: `handoff_2026-11-26T23-46-38Z_INITIAL_TASK.md` (this session's start-of-session task)

## Initial Task (for the next agentic work session)

The research phase is **closed** (E001–E043). There is no new research to invent. Do the
following real work, then **stop** — do not manufacture another handoff refresh as a
substitute for work (see the runaway-loop warning below).

1. **Provision the environment** — `pip install -r requirements.txt`. `pandas` and `numpy`
   are NOT importable this session; the full suite cannot run without them.
2. **Reproduce (real work, not a handoff refresh)** —
   `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift
   precisely. **Do NOT re-pin artifacts to make a tolerance violation disappear** — the
   committed golden is the authoritative record (E049/E050 precedent).
3. **Confirm the tangency-QP drift stays closed** — E041/E042 must reproduce with 0
   differences under the E050 exact active-set solver. If a *deliberate* code change alters a
   published number, record it in the ledger first, then re-pin.
4. **Cleanup (propose only, do not execute)** — if the ~9,500-file handoff explosion is a
   problem, *propose* a `.gitignore` + `git rm --cached` plan and let the user decide.
5. **Leave your own single handoff** (procedure below), then stop.

## Baseline Integrity Verification (2026-11-26T23:47:30Z)

- ✅ **No active verification run**: `.verify_snapshot/` and `.verify_reports/` do not exist.
- ✅ **Goldens match HEAD**: `scripts/check_goldens_clean.py` — ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD.
- ✅ **Goldens match pinned baseline**: `scripts/check_golden_baseline.py` — ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT.
- ✅ **Data coverage clean**: `scripts/check_data_coverage.py` — ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED.
- ⚠️ **Missing dependency**: `pandas` and `numpy` are not importable. Run `pip install -r requirements.txt` before the full suite.

## Git State

- Branch: `main`; HEAD `e4214fbf` == `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0 0`).
- `git diff HEAD -- experiments/` empty. No tracked source changes from this session.
- Recent commits are `chore(kilo): checkpoint agent session` entries; no research substance changed.

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

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (E001–E043 + handoff refreshes through E751)
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- **Repoint script**: `scripts/repoint_handoff.py`

## Recurring handoff procedure (how this artifact was produced)

1. `TS` = current UTC (`date -u +%Y-%m-%dT%H-%M-%SZ`).
2. Write `handoff_<TS>_INITIAL_TASK.md` at repo root (this file).
3. Repoint the existing generic aliases only:
   `python3 scripts/repoint_handoff.py handoff_<TS>_INITIAL_TASK.md` (expect `bad=0`).
   **Do not create new mirror directories or new alias names** — E740–E751 deliberately broke
   the mirror/repoint explosion (~2,100 `handoff_`-prefixed tracked files already).
4. Append a short ledger entry (`## E<next> — Durable handoff refresh (<TS>)`).
5. Do not commit unless the user explicitly asks.

## Handoff Context

Created at the start of a new agentic work session at the user's explicit request to leave a
timestamped, clear initial task message. Baseline re-verified clean at this timestamp (goldens
match HEAD, all 107 pinned goldens match the baseline fingerprint, all 35 pinned data inputs
present/tracked/unchanged); no snapshot recovery needed; no code changes made. The only
environment gap is the missing `pandas`/`numpy` dependencies.

**Warning — runaway handoff loop (E652–E751):** this repository carries ~9,500 git-tracked
files, ~22% of which are `handoff_`-prefixed artifacts produced by repeated refresh loops.
Do NOT add to that by manufacturing an E752-style refresh as a substitute for the real work
above. This handoff is the deliverable; the ledger entry is bookkeeping.