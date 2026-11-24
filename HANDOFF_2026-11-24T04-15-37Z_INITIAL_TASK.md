# INITIAL TASK — handoff for next agentic work session

**Timestamp:** 2026-11-24T04:15:37Z
**Repo HEAD:** `f60572486e1f2b2f2364576c146d20f665336290` (main, == origin/main, `0 0`)
**Author:** automated agent, written at the user's explicit request ("leave a timestamped clear initial task message").

---

## 0. Read this first — do NOT repeat this handoff

This artifact is entry **E730** in a documented runaway loop (E652 → E729): ~94% of
git-tracked files (8,391 of 8,917) are handoffs. Each iteration writes a fresh handoff,
commits a `chore(kilo): checkpoint agent session`, and leaves the real work untouched.
**Writing another handoff is not work.** If you catch yourself producing E731, stop.

The one genuinely new fact in this handoff: the last session (E729) had a **live
`run_all_verification.py --extended` run** in progress. That run is now **gone** —
`.verify_snapshot/` and `.verify_reports/` are absent, and `git diff HEAD -- experiments/`
is empty. The run either completed and self-restored, or was terminated cleanly. Either
way the golden baseline is intact (verified below). Nothing is in flight.

## 1. State verified THIS session (2026-11-24T04:15:37Z)

- `HEAD == origin/main == f6057248` (`git rev-list --left-right --count` = `0  0`).
- `git diff HEAD -- experiments/` **empty**; no `experiments/*.json` modified.
- `.verify_snapshot/`, `.verify_reports/` **absent** — no live/pending verification run.
- Working tree: only `__pycache__/*.pyc` build noise tracked.
- All three pure-Python guards **PASS** (hashlib-only, ran this session):
  - `scripts/check_goldens_clean.py` → ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0)
  - `scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0)
  - `scripts/check_data_coverage.py` → ALL 35 PINNED DATA INPUTS PRESENT, TRACKED, UNCHANGED (exit 0)
- Full verification suite **NOT** run (deps `numpy/pandas/scipy` not confirmed provisioned).

## 2. Prioritized REAL work (do these; none require inventing new research)

1. **Verify, then stop.** After `pip install -r requirements.txt`, run
   `SEED=42 python3 run_all_verification.py --extended` and report drift **precisely**
   (per-driver numeric vs structural, worst multiple of tol from
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`). Do not commit verification output.
   AGENTS.md records the last full measurement (2026-11-23T05:17Z): all 18 extended
   drivers reproduce with **0 differences** at numeric_tol=1e-4.
2. **E049 ill-conditioned tangency QP (E041/E042).** Per AGENTS.md the drift was closed by
   the E050 exact active-set enumeration (commit `72dc947`) and artifacts are bit-reproducible.
   Confirm this still holds under the current environment; **do not re-pin goldens to silence
   a tolerance violation** — there is none to silence.
3. **Repo hygiene (PROPOSE, do not execute without user sign-off).** 8,391 of 8,917 tracked
   files are handoffs. Draft a `.gitignore` + `git rm --cached` plan that untracks the mirror
   dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/`) and the ~643 generic aliases.
   Present the plan; let the user approve before any `git rm`.

## 3. Hard constraints (from AGENTS.md — do not violate)

- Research phase is **CLOSED** (E001–E043). Do not run new experiments or move goalposts.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect
  of running verification. Re-pin only for a *deliberate* code change, ledger-recorded first.
- Never commit verification output. If a run is interrupted: `SEED=42 python3
  run_all_verification.py --restore-only` (or `git checkout f6057248 -- experiments/`).
- Goldens under `experiments/` are canonical; the committed artifact is authoritative.
- Do not commit unless the user explicitly asks.

## 4. Quick reference

```bash
SEED=42 bash scripts/check.sh                              # fast convention check
SEED=42 python3 run_all_verification.py --extended         # 18-driver reproduction
SEED=42 python3 run_all_verification.py --restore-only      # recover after interruption
```