# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-27T03:53:10Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact**: `handoff_2026-11-27T03-53-10Z_INITIAL_TASK.md` (repo root)

## Initial Task (for the next agentic work session)

Research phase is closed (E001–E043). Do the real work below, then stop. Do NOT
manufacture another handoff refresh as a substitute for the work (see runaway-loop
warning at the bottom).

1. **Provision environment** — `pip install -r requirements.txt`.
   `numpy`/`pandas` are currently NOT importable, so nothing else can run yet.
2. **Reproduce** — `SEED=42 python3 run_all_verification.py --extended` (~21 min).
   Report per-driver drift precisely (numeric vs structural, worst drift as a
   multiple of the 1e-4 tolerance). Do NOT re-pin artifacts to silence drift.
3. **Confirm tangency-QP drift stays closed** — E041/E042 must reproduce with 0
   differences under the E050 exact active-set solver. If either drifts, root-cause
   it (optimizer, not data) before touching any golden.
4. **Cleanup (propose only, do not execute)** — ~2,223 of ~9,703 tracked files are
   handoff artifacts (`handoff_*.md`). Propose a `.gitignore` + `git rm --cached`
   plan and let the user decide. Do not delete or untrack anything unilaterally.
5. **Leave your own single handoff, then stop.**

## Baseline Integrity (verified 2026-11-27T03:53:10Z)

- No active verification run (`.verify_snapshot/` absent).
- `scripts/check_goldens_clean.py` → ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD.
- `scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE
  BASELINE FINGERPRINT.
- 35 pinned data inputs present/tracked/unchanged (per prior verification).
- Only known gap: `numpy`/`pandas` not installed.

## Git State

- Branch `main`, HEAD `19c3ce63` == origin/main (in sync).
- Working tree clean; no tracked source changes.

## Handoff Context

Created at user request to leave a timestamped, clear initial task message for the
next session. Baseline re-verified clean. No code changes made.

## Runaway-loop warning

This repo has accumulated thousands of near-identical handoff files. Writing yet
another handoff is NOT progress. The next session should execute steps 1–4 above
and only then write a single concise handoff summarizing real results.

(End of file)
