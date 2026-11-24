# INITIAL TASK — durable handoff for the next agentic work session

**Timestamp:** 2026-11-24T05:10:21Z
**Repo HEAD:** `23f5536fd636eabe69161dd8a5aff88f9a6446d0` (main; **7109 commits behind origin/main**, not checked out on origin/main)
**Author:** automated agent, written at the user's explicit request ("leave a timestamped clear initial task message").
**Supersedes:** `handoff_2026-11-24T05-09-19Z_INITIAL_TASK.md` (prior session; its findings are re-verified below and still hold).

---

## 0. Read this first — do NOT repeat this handoff

This repo is dominated by handoff artifacts (~94% of git-tracked files; ~8,391 of ~8,917 tracked files). **Writing another handoff is not work.** If you catch yourself producing yet another handoff file instead of doing real work, stop and do item 1 in §2 instead.

## 1. State verified THIS session (2026-11-24T05:10:21Z)

- `HEAD = 23f5536fd636eabe69161dd8a5aff88f9a6446d0`; `git rev-list --left-right --count HEAD origin/main` = `0   7109`. HEAD is one checkpoint commit ahead of the prior handoff's HEAD (`acfd67c`), no research content change.
- `git diff --stat HEAD -- experiments/` **empty**; no `experiments/*.json` modified. Golden baseline is clean relative to HEAD.
- `.verify_snapshot/` and `.verify_reports/` **absent** — no live or pending verification run; no stale snapshot to recover.
- Working tree: only `src/__pycache__/cache_keys.cpython-312.pyc` build noise is modified.
- Full verification suite **NOT** yet run in this session.

## 2. Prioritized REAL work (do these; none require inventing new research)

1. **Verify, then stop.** After `pip install -r requirements.txt`, run
   `SEED=42 python3 run_all_verification.py --extended` and report drift **precisely**
   (per-driver numeric vs structural, worst multiple of tol from
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`). Do **not** commit verification output.
   AGENTS.md records the last full measurement (2026-11-23T05:17Z, numpy 2.5.4 / scipy 1.18.1):
   all 18 extended drivers reproduce with **0 differences** at numeric_tol=1e-4. This session's
   job is to re-confirm that under the *current* environment and report, not to change anything.
2. **E049 ill-conditioned tangency QP (E041/E042).** Per AGENTS.md the drift was closed by
   the E050 exact active-set enumeration (commit `72dc947`); artifacts are bit-reproducible.
   Confirm this still holds under the current environment; **do not re-pin goldens to silence
   a tolerance violation** — there is none to silence.
3. **Repo hygiene (PROPOSE, do not execute without user sign-off).** ~8,391 of ~8,917 tracked
   files are handoffs. Draft a `.gitignore` + `git rm --cached` plan that untracks the mirror
   dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/`) and the ~643 generic aliases
   (`latest.md`, `next.md`, `handoff_CURRENT`, `initial_task`, …). Present the plan; let the
   user approve before any `git rm`.

## 3. Hard constraints (from AGENTS.md — do not violate)

- Research phase is **CLOSED** (E001–E043). Do not run new experiments or move goalposts.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect
  of running verification. Re-pin only for a *deliberate* code change, ledger-recorded first
  (see the E050 precedent).
- Never commit verification output. If a run is interrupted: `SEED=42 python3
  run_all_verification.py --restore-only` (or `git checkout 23f5536 -- experiments/`).
- Goldens under `experiments/` are canonical; the committed artifact is authoritative, not the latest re-run.
- Cache coverage is an enforced invariant (`scripts/check_data_coverage.py`); an unpinned input is a
  live network download and yfinance is not bit-reproducible. Do not add unpinned data inputs.
- Do not commit unless the user explicitly asks.

## 4. Quick reference

```bash
SEED=42 bash scripts/check.sh                              # fast convention + template check
SEED=42 python3 run_all_verification.py --extended         # 18-driver reproduction (~21 min)
SEED=42 python3 run_all_verification.py --restore-only      # recover after an interrupted run
cat .verify_reports/VERIFICATION_EXTENDED_SUMMARY.json     # per-driver drift report (after --extended)
```

---
*Durable handoff for continuity between agentic work sessions. Timestamp: 2026-11-24T05:10:21Z.*