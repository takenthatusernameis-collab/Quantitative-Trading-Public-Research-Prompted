# Agentic Work Session — Initial Task Handoff

**Timestamp (UTC):** 2026-11-17T07:18:13Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** `b6d6e79c5c4b1d81e4f44240167db18a4482a28b` (`chore(kilo): checkpoint agent session`)
**Sync:** `origin/main` == HEAD (`git rev-list --left-right --count origin/main...HEAD` → `0	0`)
**Working tree:** clean (`git status --porcelain` empty; `experiments/` and `data/` untouched)
**Interrupted verification run:** none — `.verify_snapshot/` absent, `.verify_reports/` absent

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E051). Surviving validated
strategies and all rejections/partial results are recorded in
`ledger/RESEARCH_LEDGER.md` (with `ledger/PRIORITIZATION.md` and SHA-256 baselines
in `ledger/golden_baseline.json`, `ledger/data_baseline.json`).

## Clear Initial Task

**Leave a timestamped, clear initial task message for the next agentic work session
in a durable handoff** — i.e. refresh this handoff for the following session.

Concretely, the next session should:

1. Re-verify live state before writing (`date -u`, `git rev-parse HEAD`,
   `git rev-parse origin/main`, `git status --porcelain`, absence of
   `.verify_snapshot/`).
2. Write a new durable artifact `handoff_<UTC timestamp>_INITIAL_TASK.md` at the repo
   root using the established structure (timestamp, HEAD, sync status, project
   context, quick commands, guardrails, explicit initial task, provenance).
3. Mirror it identically to `handoff/`, `HANDOFFS/`, `.handoff/`, and `.kilo/`
   (all copies byte-identical).
4. Repoint canonical generic pointers:
   `python3 scripts/repoint_handoff.py handoff_<new timestamp>_INITIAL_TASK.md`
   and confirm `bad=0`.
5. Append a short ledger entry documenting the handoff refresh (prior entries:
   E444/E445) and leave the change uncommitted unless the user explicitly asks for a
   commit.

**Guardrails:** Do **not** run the verification suite, modify `experiments/*.json`,
re-pin golden/data baselines, or start new research without explicit user direction.
The baseline is clean and recoverable. If a run is ever interrupted, recover with
`SEED=42 python3 run_all_verification.py --restore-only` (or
`git checkout -- experiments/`), then re-check.

## Quick Commands

```bash
# Fast convention-robustness + guard/template validation (seconds, offline)
SEED=42 bash scripts/check.sh          # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py            # or: make verify-quick

# Extended verification (~21 min; 18 more committed drivers)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py   # or: make verify

# Recover a interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes & Constraints (from AGENTS.md)

- **Seed:** always `SEED=42` (walk-forward + placebo RNG).
- **Golden files:** `experiments/*.json` are canonical committed artifacts. The
  verification suite backs them up and restores them; never commit verification
  output and never leave a run half-finished.
- **Baseline integrity:** `scripts/check_goldens_clean.py` compares the working tree
  with HEAD; `scripts/check_golden_baseline.py` compares tracked artifacts with the
  SHA-256 fingerprints in `ledger/golden_baseline.json`. `scripts/check_data_coverage.py`
  enforces every data input against `ledger/data_baseline.json`. Never re-pin as a
  side effect of verification — the committed golden is the authoritative record.
- **Optimizer determinism (ledger E049):** `src/portfolio_opt.py` validates a solver
  answer on the problem's constraints, never on the solver exit status; the rule is
  pinned by `tests/test_portfolio_opt.py`. The E041/E042 tangency QP is
  ill-conditioned (1-ulp inputs move `min_var` by ~1e-05); do **not** re-pin to
  silence that drift.
- **Convention:** close-to-close is the v1.2.3 primary convention; overnight
  decomposition is reported alongside.
- **Data:** cached parquet in `data/` (gitignored except pinned 2026-10-12 and
  2026-10-11 vintages); E029 fundamentals pinned in `data/fundamentals/`.
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow,
  statsmodels, yfinance). `cvxpy`/`cvxopt` optional; optimizer falls back to scipy.
- **CI:** the GitHub Actions gate cannot be created by automated agents; use the local
  `make check` / `make verify*` equivalents.
- **Lint/format:** Python 3 research repo; no separate linter. Run
  `python3 -m py_compile` on changed files.

## Recommended First Steps (next session)

- Confirm HEAD == `origin/main` and the working tree is clean for `experiments/` and
  `data/` (and no `.verify_snapshot/` exists).
- Read `ledger/RESEARCH_LEDGER.md` (tail) for the surviving strategies and the most
  recent handoff-refresh entries.
- Run `SEED=42 bash scripts/check.sh` before any change to confirm goldens, data
  coverage, JSON guards, and templates are green.
- Wait for explicit user instructions before taking any research action.

## Provenance

Supersedes the previous durable handoff
`handoff_2026-11-17T06:23:03Z_INITIAL_TASK.md` (retained for history). This file is
the authoritative initial-task message for the next agentic work session. Written at
2026-11-17T07:18:13Z against HEAD `b6d6e79c5c4b1d81e4f44240167db18a4482a28b`.