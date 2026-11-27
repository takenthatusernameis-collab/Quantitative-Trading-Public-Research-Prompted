# Durable Handoff — Initial Task Message

## Message Timestamp
Created: 2026-11-27T05:01:37Z

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. All experiments are pre-registered with falsification
expectations and promotion gates. **Research phase complete (E001–E043).**
Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Git State (verified this session, 2026-11-27T05:01Z)
- Branch: `main`; HEAD `1c38bd4d` ("chore(kilo): checkpoint agent session").
  `main...origin/main` is 0 ahead / 0 behind (up to date with origin).
- Working tree: **no source/data/ledger/artifact changes.** The only modified
  paths are 12 tracked bytecode caches under `scripts/__pycache__/`,
  `src/__pycache__/`, `tests/__pycache__/` (`*.cpython-312.pyc`). These are
  recompiled `__pycache__` artifacts, not real edits — the repo tracks 15 `.pyc`
  files in total. Do **not** commit these as if they were source changes; if a
  clean tree is required, `git checkout -- '*.pyc'` restores them.
- No `.verify_snapshot/` and no `.verify_reports/` — no verification run in progress.
- `scripts/check_goldens_clean.py`: ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0).
- `scripts/check_golden_baseline.py`: ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0).
- `scripts/check_data_coverage.py` (standalone): ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED (exit 0).

## Environment Gap — READ FIRST (blocks the verification suite)
This checkout still has **no Python scientific stack installed**. `python3 -c
"import pandas"` raises `ModuleNotFoundError: No module named 'pandas'`; numpy and
scipy are likewise absent, yet `requirements.txt` pins them (numpy==2.5.4,
pandas==3.0.6, scipy==1.18.1, pyarrow==26.0.0, statsmodels==0.15.0,
yfinance==1.7.0; Python 3.12.3).

Consequences:
- `SEED=42 bash scripts/check.sh` fails with `ModuleNotFoundError: No module named
  'pandas'` raised by `tests/test_data_coverage.py` (the missing-dep errors are
  NOT baseline corruption — the standalone coverage check above passes).
- `run_all_verification.py` and every `experiments/run_*.py` driver will fail to
  import until the stack is installed.

**First action for the next session:** `python3 -m pip install -r requirements.txt`
(ideally into a venv), then re-run `SEED=42 bash scripts/check.sh`; it should pass
with the deps present. Do not treat the missing-dep errors as baseline corruption.

## What Was Done This Session
None to code/data/ledger/artifacts. Baseline integrity was re-verified as the
first action (goldens clean, 107 pinned goldens match, 35 data inputs intact); the
only findings are (a) the still-missing Python dependency stack and (b) 12 tracked
`.pyc` caches showing as modified from recompilation. This file is the initial
handoff marker for the next agentic work session.

## Standing Commands (verbatim, always prefix `SEED=42`)
- `SEED=42 bash scripts/check.sh` — convention-robustness check + template validation (seconds, offline)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended verification (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full verification (~15 min)
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only (reads JSONs, no writes)
- `SEED=42 python3 run_all_verification.py --skip-slow` — skip slow batch/regression steps
- `SEED=42 python3 run_all_verification.py --restore-only` — recover golden artifacts after an interrupted run
- `python3 -m py_compile <file>` — syntax check on changed files (no separate linter configured)

## Critical Baseline Integrity Rules
1. `experiments/*.json` are canonical research artifacts. The verification suite
   overwrites them while re-running drivers and restores them afterwards —
   **never leave a verification run half-finished.**
2. Backup lives in the repo-local, gitignored `.verify_snapshot/` with an
   `ACTIVE.json` marker holding the owning pid. A killed run stays recoverable
   via `SEED=42 python3 run_all_verification.py --restore-only`.
3. `scripts/check_goldens_clean.py` fails when a tracked artifact under
   `experiments/` differs from HEAD or when a stale snapshot is pending.
4. `scripts/check_golden_baseline.py` compares every tracked artifact with the
   SHA-256 pinned in `ledger/golden_baseline.json`. Replacing an artifact
   requires re-pinning (`python3 scripts/check_golden_baseline.py --update`),
   which puts the replacement in the diff. **Never re-pin as a side effect of
   running verification** — the committed golden is the authoritative record.
5. **Do not commit verification output.** If a run is interrupted, restore the
   goldens before committing (`--restore-only`, or `git checkout <commit> --
   experiments/<file>` where `<commit>` is the last one matching
   `ledger/golden_baseline.json`).
6. Drivers re-execute with `QUANT_RESEARCH_OFFLINE=1`; a missing cache entry
   fails hard instead of silently downloading (yfinance is not bit-reproducible).
   To add a data input, commit the file and re-pin with
   `python3 scripts/check_data_coverage.py --update`.

## Optimizer Determinism (ledger E049 / E050)
- `src/portfolio_opt.py` validates a solver answer on the **problem's
  constraints**, never on the solver's exit status. SLSQP status 8 ("Positive
  directional derivative for linesearch") at a constrained optimum is acceptable;
  gating on it made the tangency portfolio environment-dependent. Pinned by
  `tests/test_portfolio_opt.py`.
- The E050 exact KKT active-set enumeration is the primary tangency solver; it
  has no iteration and no build-dependent branch, so the E041/E042 grid
  artifacts are bit-reproducible across environments (0 differences at the
  2026-11-23T05:17Z measurement). Do not re-pin E041/E042 to silence a
  tolerance violation — none remains.

## Next Steps for the Next Session
1. `python3 -m pip install -r requirements.txt` (the stack is currently absent).
2. Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` for standing dispositions and gate flags.
3. Run `SEED=42 bash scripts/check.sh` to confirm a clean baseline before starting work.
4. Do not commit verification output or re-pin goldens as a side effect of a run.
5. If modifying an experiment driver, update its `pre_registered` JSON block
   (goalposts are never moved post-hoc) and record any gate changes in the ledger first.
6. The intended CI gate (`.github/workflows/verification-gate.yml`) cannot be
   created by automated agents; a copyable template lives at
   `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

## Key Files
- `AGENTS.md` — project commands & conventions (read before running the suite)
- `requirements.txt` — pinned deps; install before running the suite
- `ledger/RESEARCH_LEDGER.md` — surviving strategies & gate dispositions
- `ledger/golden_baseline.json` — SHA-256 fingerprints of canonical artifacts (107 pinned)
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data inputs (35 pinned)
- `experiments/*.json` — committed experiment artifacts (canonical baseline)
- `src/batch_run.py`, `src/validate.py` — experiment drivers
- `src/portfolio_opt.py` — portfolio optimizer (SLSQP + exact active-set fallback)
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- `tests/test_portfolio_opt.py`