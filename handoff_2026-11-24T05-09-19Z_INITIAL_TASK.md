# INITIAL TASK — handoff for next agentic work session

**Timestamp:** 2026-11-24T05:09:19Z
**Repo HEAD:** `acfd67c35bc9afc3fde305499423a0c9ef4641bb` (main; **7108 commits behind origin/main**, not checked out on origin/main)
**Author:** automated agent, written at the user's explicit request ("leave a timestamped clear initial task message").

---

## 0. Read this first — do NOT repeat this handoff

This repo is dominated by handoff artifacts (~94% of git-tracked files). **Writing another handoff is not work.** If you catch yourself producing yet another handoff file instead of doing real work, stop.

## 1. State verified THIS session (2026-11-24T05:09:19Z)

- `HEAD = acfd67c35bc9afc3fde305499423a0c9ef4641bb`; `git rev-list --left-right --count HEAD origin/main` = `0   7108`.
- `git diff HEAD -- experiments/` **empty**; no `experiments/*.json` modified.
- `.verify_snapshot/`, `.verify_reports/` **absent** — no live/pending verification run.
- Working tree: only `src/__pycache__/cache_keys.cpython-312.pyc` build noise modified.
- Full verification suite **NOT** yet run in this session.

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
3. **Repo hygiene (PROPOSE, do not execute without user sign-off).** ~8,391 of ~8,917 tracked
   files are handoffs. Draft a `.gitignore` + `git rm --cached` plan that untracks the mirror
   dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/`) and the ~643 generic aliases.
   Present the plan; let the user approve before any `git rm`.

## 3. Hard constraints (from AGENTS.md — do not violate)

- Research phase is **CLOSED** (E001–E043). Do not run new experiments or move goalposts.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect
  of running verification. Re-pin only for a *deliberate* code change, ledger-recorded first.
- Never commit verification output. If a run is interrupted: `SEED=42 python3
  run_all_verification.py --restore-only` (or `git checkout acfd67c -- experiments/`).
- Goldens under `experiments/` are canonical; the committed artifact is authoritative.
- Do not commit unless the user explicitly asks.

## 4. Quick reference

```bash
SEED=42 bash scripts/check.sh                              # fast convention check
SEED=42 python3 run_all_verification.py --extended         # 18-driver reproduction
SEED=42 python3 run_all_verification.py --restore-only      # recover after interruption
```

---
*Durable handoff for continuity between agentic work sessions. Timestamp: 2026-11-24T05:09:19Z.*
