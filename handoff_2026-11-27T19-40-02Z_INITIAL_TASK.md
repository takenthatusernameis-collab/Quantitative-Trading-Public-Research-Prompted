# Durable Handoff — Initial Task Message for the Next Agentic Work Session

**Created:** 2026-11-27T19:40:02Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** 33cb39a1 (== origin/main; `git rev-list --left-right --count HEAD...origin/main` = `0 0`)
**Supersedes:** handoff_2026-11-27T19-38-40Z_INITIAL_TASK.md

## Read this first — there is a REAL problem, not just a handoff refresh

This handoff was requested by the user ("leave a timestamped clear initial task
message for the next agentic work session in a durable handoff"). Unlike the
E652–E775 runaway refresh loop this repo is famous for, this file reports a
**genuine, verified integrity regression** discovered while writing it. Do not
dismiss it as bookkeeping.

**The canonical golden baseline has been overwritten by checkpoint commits.**
`python3 scripts/check_golden_baseline.py` FAILS: 5 pinned artifacts under
`experiments/` no longer match the SHA-256 pinned in `ledger/golden_baseline.json`.
`scripts/check_goldens_clean.py` PASSES only because it compares the working tree
to HEAD — it is blind to a *commit* that replaced the baseline (exactly the
failure mode AGENTS.md documents for commits d6042b0 / 9f20def / 1623923 / 701ed78).

Drifted artifacts (pinned -> actual, abbreviated):

| file | pinned | last good commit (matches pin) |
|------|--------|-------------------------------|
| experiments/cointegration_large_liquid.json | a41182528234 | da00bd0d |
| experiments/dollar_neutral_lowbeta_large_liquid.json | c657c3afc38a | bf429169 |
| experiments/e037_portfolio.json | dcaeb797e112 | c5038332 |
| experiments/e042_lead_config_confirmatory.json | fa06eeb8403d | c5038332 |
| experiments/pairs_large_liquid.json | 5ab39998fc4b | da00bd0d |

- The drift was introduced by checkpoint commit **8cd55e5e** ("chore(kilo):
  checkpoint agent session"), which is an ancestor of HEAD. All "last good"
  commits above are ancestors of 8cd55e5e, so a clean restore is possible.
- `git diff --name-only HEAD -- experiments/` is empty (working tree == HEAD);
  the corruption is *in the committed history*, not the working tree.
- No `.verify_snapshot/` or `.verify_reports/` present; no interrupted run.

## Initial task for the next session (CLEAR, prioritized)

1. **Do NOT re-pin to silence this.** Re-pin only after a *deliberate* code
   change that is recorded in the ledger first (E050 precedent). This drift is
   an accidental checkpoint capture, so the fix is restore, not re-pin.
2. **Restore the 5 pinned artifacts** from their last-good commits, e.g.:
   `git checkout da00bd0d -- experiments/cointegration_large_liquid.json experiments/pairs_large_liquid.json`
   `git checkout bf429169 -- experiments/dollar_neutral_lowbeta_large_liquid.json`
   `git checkout c5038332 -- experiments/e037_portfolio.json experiments/e042_lead_config_confirmatory.json`
   Then confirm `python3 scripts/check_golden_baseline.py` PASSES and
   `python3 scripts/check_goldens_clean.py` still PASSES.
3. **Get explicit user approval before committing** the restore. Do not commit
   verification output. Do not let a checkpoint commit recapture the baseline.
4. **Provision deps and reproduce (real work):** `pip install -r requirements.txt`
   (numpy/pandas currently NOT importable), then
   `SEED=42 python3 run_all_verification.py --extended` (~21 min). Confirm all 18
   extended drivers reproduce with 0 differences; do NOT re-pin to hide drift.
5. **Propose (do not execute) a handoff-file cleanup.** ~9,324 git-tracked files
   are handoff-prefixed (~94% of the tree). Draft an archive/delete plan; get
   explicit user approval before removing anything.

## State verified this session (2026-11-27T19:40Z)

- HEAD `33cb39a1` == origin/main; working tree clean (only `__pycache__/*.pyc` noise).
- `check_goldens_clean.py` PASS; `check_data_coverage.py` PASS (35 pinned inputs);
  `check_golden_baseline.py` **FAIL (5 artifacts — see above)**.
- Dependencies NOT importable (numpy/pandas `ModuleNotFoundError`).

## Constraints honored by this handoff

- No baseline re-pinned; no verification suite run (deps missing); no
  verification output committed; no new research performed.
- **No ledger entry appended** and **no mirror dirs / alias repointing** created,
  deliberately, to avoid feeding the E652–E775 loop. This single root file is the
  deliverable.
- No source, experiment, ledger, or pinned-data file was modified.

## Key conventions (from AGENTS.md)

- Always run with `SEED=42`.
- `experiments/*.json` are canonical goldens — never commit verification output over them.
- Cache coverage is enforced: every `data.download()` call site must have a pinned,
  git-tracked cache entry (`ledger/data_baseline.json`).
- Run `python3 -m py_compile` on any changed Python file.
- `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.