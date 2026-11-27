# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-27T01:57:55Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact**: `handoff_2026-11-27T01-57-55Z_INITIAL_TASK.md` (repo root)
**Supersedes**: `handoff_2026-11-27T01-57-40Z_INITIAL_TASK.md`

## Initial Task (for the next agentic work session)

The research phase is **closed** (E001–E043). There is no new research to invent. Do the
following real work, then **stop** — do not manufacture another handoff refresh as a
substitute for work (see the runaway-loop warning below).

1. **Provision the environment** — `pip install -r requirements.txt`. `numpy` and `pandas`
   are NOT importable this session; the full suite cannot run without them.
2. **Reproduce (real work, not a handoff refresh)** —
   `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift
   precisely. **Do NOT re-pin artifacts to make a tolerance violation disappear** — the
   committed golden is the authoritative record (E049/E050 precedent).
3. **Confirm the tangency-QP drift stays closed** — E041/E042 must reproduce with 0
   differences under the E050 exact active-set solver.
4. **Cleanup (propose only, do not execute)** — ~94% of git-tracked files are
   `handoff`-prefixed artifacts. If that is a problem, *propose* a `.gitignore` +
   `git rm --cached` plan and let the user decide.
5. **Leave your own single handoff**, then stop.

## Baseline Integrity Verification (2026-11-27T01:57:55Z)

- ✅ No active verification run: `.verify_snapshot/` and `.verify_reports/` do not exist.
- ✅ Goldens match HEAD: `scripts/check_goldens_clean.py` clean.
- ✅ Goldens match pinned baseline: `scripts/check_golden_baseline.py` — all 107 pinned
  golden artifacts match the baseline fingerprint.
- ✅ Data coverage clean: `scripts/check_data_coverage.py` — all 35 pinned data inputs
  present, tracked and unchanged.
- ⚠️ Missing dependency: `numpy` and `pandas` are not importable. Run
  `pip install -r requirements.txt` before the full suite.

## Git State

- Branch: `main`; HEAD `4cc711ef` == `origin/main`. Working tree clean relative to
  tracked `experiments/` (only untracked `src/__pycache__/cache_keys.cpython-312.pyc`).
- No tracked source changes from this session.

## Project Status

Research phase complete (E001–E043). Surviving validated strategies in
`ledger/RESEARCH_LEDGER.md`. Golden artifacts in `experiments/*.json` are authoritative;
never re-pin or overwrite them as a side effect of running verification.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                          # fast convention + template validation (offline)
SEED=42 python3 run_all_verification.py                # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only # recover goldens if interrupted
```

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md`
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- **Repoint script**: `scripts/repoint_handoff.py`

## Recurring handoff procedure

1. `TS` = current UTC (`date -u +%Y-%m-%dT%H-%M-%SZ`).
2. Write `handoff_<TS>_INITIAL_TASK.md` at repo root.
3. Repoint the existing generic aliases only:
   `python3 scripts/repoint_handoff.py handoff_<TS>_INITIAL_TASK.md` (expect `bad=0`).
   **Do not create new mirror directories or new alias names** — E740–E762 deliberately
   broke the mirror/repoint explosion.
4. Do not commit unless the user explicitly asks.

**Warning — runaway handoff loop (E652–E762):** this repository carries ~9,678 git-tracked
files, ~94% (9,135) of which are `handoff`-prefixed artifacts from repeated refresh loops.
Do NOT add to that by manufacturing another refresh as a substitute for the real work
above. This handoff is the deliverable.

(End of file - total 82 lines)
