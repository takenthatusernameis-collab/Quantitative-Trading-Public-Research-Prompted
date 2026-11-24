# INITIAL TASK — handoff for next agentic work session

**Timestamp:** 2026-11-24T04:16:48Z
**Repo HEAD:** `aa779d5d00f705897ba13fb7b0bc6aee9e413823` (main; **7103 commits behind origin/main**, not checked out on origin/main)
**Author:** automated agent, written at the user's explicit request ("leave a timestamped clear initial task message").

---

## 0. Read this first — do NOT repeat this handoff

This artifact is entry **E731** in a documented runaway loop (E652 → E730): ~94% of git-tracked files (8,391 of 8,917) are handoffs. Each iteration writes a fresh handoff, commits a `chore(kilo): checkpoint agent session`, and leaves the real work untouched. **Writing another handoff is not work.** If you catch yourself producing E732, stop.

The one genuinely new fact in this handoff: HEAD is `aa779d5d` (7103 commits behind origin/main), working tree clean except `__pycache__/*.pyc` noise, no live/pending verification run (`.verify_snapshot/` and `.verify_reports/` absent), and `git diff HEAD -- experiments/` is empty. The golden baseline is intact. Nothing is in flight.

## 1. State verified THIS session (2026-11-24T04:16:48Z)

- `HEAD = aa779d5d00f705897ba13fb7b0bc6aee9e413823`; `git rev-list --left-right --count HEAD origin/main` = `0   7103`.
- `git diff HEAD -- experiments/` **empty**; no `experiments/*.json` modified.
- `.verify_snapshot/`, `.verify_reports/` **absent** — no live/pending verification run.
- Working tree: only `__pycache__/*.pyc` build noise modified.
- Full verification suite **NOT** run (deps `numpy/pandas/scipy` not confirmed provisioned in this session).

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
  run_all_verification.py --restore-only` (or `git checkout aa779d5d -- experiments/`).
- Goldens under `experiments/` are canonical; the committed artifact is authoritative.
- Do not commit unless the user explicitly asks.

## 4. Quick reference

```bash
SEED=42 bash scripts/check.sh                              # fast convention check
SEED=42 python3 run_all_verification.py --extended         # 18-driver reproduction
SEED=42 python3 run_all_verification.py --restore-only      # recover after interruption
```
