# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T16:12:15Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact:** `handoff_2026-11-26T16-12-15Z_INITIAL_TASK.md` (repo root)
**Supersedes:** `handoff_2026-11-26T16-11-04Z_INITIAL_TASK.md`.
**HEAD:** `742cc96f` (`main`), in sync with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0 0`).

---

## READ THIS FIRST — you are inside a documented loop

This repository has been stuck in a **runaway handoff-refresh loop** since ~E652
(see `ledger/RESEARCH_LEDGER.md`). Each session is asked to "leave a timestamped
durable handoff," complies, and produces yet another near-identical refresh — which
the ledger then records as *itself an instance of the loop it warns against*.

Measured this session:
- The only commits since the previous durable artifact (`f1731e20` → `742cc96f`) are
  `28e7790c` and `742cc96f`, both `chore(kilo): checkpoint agent session`, and the only
  files they touch are **two more handoff `.md` files** (114 insertions, 0 deletions).
  No code, golden, or data input changed.
- By the repo's own standing rule ("do not refresh this handoff unless verified state
  materially changes"), another refresh is **not** warranted as work. This file exists
  only because the current session was explicitly instructed to leave one.

**Do NOT manufacture an E750-style refresh as a substitute for real work.** If you feel
the pull to write another handoff, that is the loop talking. The deliverable below is the
real work; the handoff is only a pointer to it.

## Real work backlog (prioritized — pick the top one you can actually complete)

1. **Verify-and-stop (highest value).** `pip install -r requirements.txt`, then
   `SEED=42 bash scripts/check.sh`, then `SEED=42 python3 run_all_verification.py --extended`.
   Report drift precisely (per-driver, numeric vs structural, worst drift as a multiple of
   `numeric_tol=1e-4`). **Do NOT re-pin goldens** — none is violated. Then **stop** and report.
2. **Confirm the E049/E050 tangency-QP drift stays closed** without re-pinning (exact KKT
   active-set solver, commit `72dc947`; E041/E042 bit-reproducible, 0 differences).
3. **Propose (do not execute) a cleanup** of the handoff-alias explosion: a `.gitignore` +
   `git rm --cached` plan for the thousands of alias/symlink files, plus a single canonical
   `HANDOFF.md`. Present the plan; await explicit approval before deleting anything.
4. **Default if no instruction:** await explicit user direction. Do not invent work.

## Verified state (this session, 2026-11-26T16:12:15Z)

- Branch `main`; HEAD `742cc96fa614f4160a9f409afdd7c3dcfee07439` == `origin/main` (`0 0`).
- Working tree clean apart from tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc`
  (safe to `git restore`). `git diff HEAD -- experiments/` empty.
- `.verify_snapshot/` and `.verify_reports/` absent; no live verification in progress.
- **Dependencies NOT importable** (`import numpy` -> `ModuleNotFoundError`); run
  `pip install -r requirements.txt` first.
- **All three pure-Python guards PASS** (offline, no deps):
  - `scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0)
  - `scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0)
  - `scripts/check_data_coverage.py` -> ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED (exit 0)
- Full verification suite **not run** (deps missing).

## Quick commands

```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh                    # fast convention-robustness + template validation (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 more drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
```

## Integrity rules (do not violate)

- Never leave verification half-finished; it overwrites `experiments/*.json` and restores afterward.
- Never re-pin goldens as a side effect of verification — re-pin only for a deliberate code change recorded in the ledger first.
- Never commit verification output; it silently replaces the canonical baseline.
- Always `SEED=42`.
- Do NOT create new alias/mirror symlinks for this handoff.

---

**Next session:** install deps -> run the verify-and-stop backlog item -> report drift -> **stop**.
Do not refresh this handoff unless verified state materially changes. This handoff is a
pointer, not the deliverable. The research phase is closed; there is no new research to do.