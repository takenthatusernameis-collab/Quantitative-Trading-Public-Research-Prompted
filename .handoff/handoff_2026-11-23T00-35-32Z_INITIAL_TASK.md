# Agentic Work Session Handoff — Initial Task Message

**Timestamp**: 2026-11-23T00:35:32Z
**Session**: Durable handoff for the next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Initial task message (read first)

You are resuming an independent, reproducible quantitative-strategy research
repository. The research phase is **closed** (E001–E043); surviving validated
strategies and every disposition (including honest REJECTED / PARTIAL results)
are recorded in `ledger/RESEARCH_LEDGER.md`.

**Do not treat "refresh the handoff" as the task.** The ledger shows a runaway
loop (E652–E715) in which session after session only rewrote this handoff file
without doing real work, accumulating thousands of tracked handoff copies. If
you were invoked with no substantive instruction, do **not** add another
handoff-only refresh. Instead, in priority order:

1. **Do the real work the user actually asks for** (a pre-registered experiment,
   a code fix, an explicit research task). Pre-register before running; never
   move goalposts post-hoc.
2. If no substantive task is given, do something concretely useful and verifiable:
   provision deps and run the real verification suite (below), or address the
   open E049 item (E041/E042 ill-conditioned-QP drift).
3. Only if explicitly told to leave a handoff, leave **one** and stop. Do not
   loop.
4. If you want to reduce clutter, **propose** (do not execute) a `.gitignore` +
   `git rm --cached` cleanup of the historical handoff files.

---

## Start-here checklist (ordered, timestamped)

1. **Orient on HEAD.** `git status --short`, `git log --oneline -5`,
   `git rev-list --left-right --count origin/main...HEAD`.
2. **Recover any interrupted verification first.** If `.verify_snapshot/ACTIVE.json`
   exists with a dead pid, run `SEED=42 python3 run_all_verification.py --restore-only`.
   A live run is reported, not failed. Never leave a run half-finished.
3. **Confirm both golden guards pass** (pure-Python, offline):
   - `python3 scripts/check_goldens_clean.py`
   - `python3 scripts/check_golden_baseline.py`
   Both must report all artifacts matching HEAD / the pinned baseline fingerprint.
4. **Provision deps** (if running the suite): `pip install -r requirements.txt`
   (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).
5. **Run the real suite** as the task requires:
   - `SEED=42 bash scripts/check.sh` (fast, offline)
   - `SEED=42 python3 run_all_verification.py` (quick, ~8 min)
   - `--extended` (~21 min) / `--full` (~15 min)
6. **Do the user's task**, or stop if none was given (see the warning above).
7. **Leave your own single handoff** (if instructed) and stop.

---

## Verified state at handoff time (2026-11-23T00:35:32Z)

- HEAD `d3f48b9e4a609f851c4dcc61e08c9f442983532f` on `main`; equals `origin/main`
  (`git rev-list --left-right --count origin/main...HEAD` = `0  0`).
- `git status --short`: only `__pycache__/*.pyc` build noise (no tracked source change).
- `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and `.verify_reports/` absent.
- Both pure-Python golden guards were executed and **PASS** this session:
  `check_goldens_clean.py` and `check_golden_baseline.py` (107 pinned artifacts).
- Deps not provisioned (guards are hashlib-only); the full verification suite was
  **not** run this session.

---

## Verification scopes (SEED=42)

- `scripts/check.sh` — fast convention-robustness + template validation (seconds, offline).
- `run_all_verification.py` — 8 drivers (E012, E023, E024 --merge, E027, E035, E037, E039, E042-lead).
- `--extended` — adds the remaining 18 committed drivers; compares vs goldens (numeric_tol=1e-4).
- `--full` — E042 n_sim=50 + 96-config sensitivity grid.

## Integrity rules

- `experiments/*.json` are the canonical committed goldens. The suite backs them
  up to `.verify_snapshot/` and restores them. **Never commit verification output.**
- If a golden mismatch appears, fix before committing. Restore with
  `run_all_verification.py --restore-only` or `git checkout -- experiments/`.
  If HEAD itself carries a bad baseline, restore the pinned artifact with
  `git checkout <commit> -- experiments/<file>` where `<commit>` matches
  `ledger/golden_baseline.json`.
- Cache coverage is an enforced invariant: every `data.download()` input must be
  committed and SHA-256 pinned in `ledger/data_baseline.json`
  (`scripts/check_data_coverage.py`). Add data by committing + `--update`.
- Do not re-pin goldens/data to silence drift.

## Key references

- `ledger/RESEARCH_LEDGER.md` — full experiment record (E001–E715).
- `ledger/PRIORITIZATION.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- `scripts/repoint_handoff.py <file>` — repoints the 514 generic alias symlinks
  across repo root + `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md`
  (the live workflow cannot be created by agents; a maintainer must add it).

## Carried-forward open items

- **E049 (open):** `src/portfolio_opt.py` validates solver answers on the problem's
  constraints, not the solver exit status (fixed). The tangency QP remains
  ill-conditioned: a 1-ulp input perturbation moves `min_var` by ~1e-05, so the
  E041/E042 grid artifacts drift by ~29–133 numeric differences beyond the 1e-4
  tolerance. **Do not re-pin to silence this** — resolve the conditioning or
  document it as accepted drift.
- **E041 extended drift:** 133 numeric diffs remain (was 354; 3 structural diffs
  resolved). Expected; do not re-pin.
- **E030:** reproduces with 0 diffs since 2026-10-20 (pinned 16-ETF panel).
- **CI gate:** `.github/workflows/verification-gate.yml` cannot be created by
  agents; use the template via GitHub UI.

---

## Provenance / handoff procedure

This file was written at the user's explicit request to leave a timestamped,
durable initial task message for the next agentic work session. It is mirrored
into the five handoff directories and the generic alias symlinks are repointed
via `scripts/repoint_handoff.py`.

*This handoff is durable and survives session closure. Read this file first, then
`ledger/RESEARCH_LEDGER.md`, then run `SEED=42 bash scripts/check.sh`.*