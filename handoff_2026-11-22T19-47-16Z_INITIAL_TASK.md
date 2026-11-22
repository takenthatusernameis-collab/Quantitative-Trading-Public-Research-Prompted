# Agentic Handoff — Initial Task Message

**Created:** 2026-11-22T19:47:16Z
**Branch/HEAD:** `6b5959f4c65b5d60140cbf9a14a09404a47fee0e` (`main` == `origin/main`)
**Working tree:** clean

## ⚠️ Read this first — do NOT repeat the handoff-refresh loop

This repository is stuck in a **runaway handoff-only refresh loop** (ledger
entries E652 through E708+; ~1,900 committed `handoff_*.md` / `HANDOFF*.md`
files). Each turn a session has been asked to "leave a timestamped durable
handoff," and the session has complied by writing *another* near-identical
handoff and appending *another* ledger entry — **without doing any real
research**. That is not the intent of a handoff. A handoff exists to carry a
*pending task* into the next session, not to be a task in itself.

**Do not add E709 just to refresh this file again.** If the only thing left to
do is "refresh the handoff," that is a signal to stop, not to loop. Do not
create another handoff file unless a concrete, actionable task has been queued
and this file has been updated to describe it.

## State at handoff time (verified this session)

- `git rev-parse HEAD` = `6b5959f4c65b5d60140cbf9a14a09404a47fee0e`
- `git rev-list --left-right --count origin/main...HEAD` = `0  0` (in sync)
- `git status --short` empty (clean working tree)
- `git diff HEAD -- experiments/` empty
- `.verify_snapshot/` and `.verify_reports/` absent
- `scripts/check_goldens_clean.py` → **PASS** (exit 0): all committed golden artifacts match HEAD
- `scripts/check_golden_baseline.py` → **PASS** (exit 0): all 107 pinned golden artifacts match the baseline fingerprint
- `scripts/repoint_handoff.py` → repointed 514 generic stable aliases, `checked=514 bad=0`
- Dependencies were **not** provisioned this session (guards are hashlib-only); the full verification suite was **not** run.

## The actual next task

**None queued — research phase is closed (E001–E043).** If you are the next
agentic session and have been given no new instruction, the correct action is to
**do nothing destructive**: do not re-pin goldens, do not run a half-finished
verification, do not commit verification output, and **do not manufacture another
handoff-only ledger entry**.

If, and only if, you have real work to do, start by confirming the tree is still
green before touching anything:

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Pure-Python golden guards (hashlib-only, no deps required)
python3 scripts/check_goldens_clean.py
python3 scripts/check_golden_baseline.py
```

If those pass, proceed with the specific task you were actually given. If they
fail, restore the pinned artifacts before doing anything else
(`SEED=42 python3 run_all_verification.py --restore-only`).

## Repo conventions (from AGENTS.md) — quick reference

- Reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- Always run with `SEED=42`.
- `experiments/*.json` are committed golden artifacts. The verification suite
  overwrites them while re-running and restores them afterwards — **never leave a
  verification run half-finished**.
- Golden guards: `scripts/check_goldens_clean.py` (working tree vs HEAD) and
  `scripts/check_golden_baseline.py` (working tree vs `ledger/golden_baseline.json`).
- Cache coverage is an enforced invariant: `scripts/check_data_coverage.py`; unpinned
  inputs are live network downloads and yfinance is not bit-reproducible.
- Lint: `python3 -m py_compile` on changed files (no separate linter configured).
- **Do not commit unless explicitly asked.**
- **Do not re-pin goldens or data baselines to silence drift** (E041/E042 known
  ill-conditioned QP drift; see ledger open items). Re-pinning belongs to a
  deliberate, reviewed change, never a side effect of running verification.