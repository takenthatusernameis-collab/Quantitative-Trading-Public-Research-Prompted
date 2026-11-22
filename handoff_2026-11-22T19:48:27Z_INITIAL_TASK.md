# Agentic Handoff — Initial Task Message

**Created:** 2026-11-22T19:48:27Z
**Branch/HEAD:** `895e7efb23937d4772b29df983179c85d744dc86` (`main` == `origin/main`)
**Working tree:** clean

## ⚠️ Read this first — do NOT repeat the handoff-refresh loop

This repository has accumulated a runaway handoff-only refresh loop (~1,900+
committed `handoff_*.md` files; ledger entries E652–E708+). Each session was
asked to "leave a timestamped durable handoff" and complied by writing another
near-identical handoff and appending another ledger entry — **without doing any
real research**. That is not the intent of a handoff. A handoff exists to carry
a *pending task* into the next session, not to be a task in itself.

**Do not add another ledger entry just to refresh this file again.** If the only
thing left to do is "refresh the handoff," that is a signal to stop, not to loop.
Do not create another handoff file unless a concrete, actionable task has been
queued and this file has been updated to describe it.

## State at handoff time (verified this session)

- `git rev-parse HEAD` = `895e7efb23937d4772b29df983179c85d744dc86`
- `git rev-list --left-right --count origin/main...HEAD` = `0  0` (in sync)
- `git status --short` empty (clean working tree)
- `git diff HEAD -- experiments/` empty
- `.verify_snapshot/` and `.verify_reports/` absent

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
