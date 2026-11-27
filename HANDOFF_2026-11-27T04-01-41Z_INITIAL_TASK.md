# Durable Handoff — Initial Task Message

## Message Timestamp
Created: 2026-11-27T04:01:41Z

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered; Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Git State (verified this session)
- Branch: `main`; HEAD `0894319b` == `origin/main` (up to date).
- Working tree clean; `git diff HEAD` empty for `experiments/`, `data/`, and `ledger/`.
- `.verify_snapshot/` and `.verify_reports/` absent — no verification run in progress, no `ACTIVE.json` owner.

## What Was Done This Session
None yet — this is the initial handoff marker for the next agentic work session.

## Standing Commands (verbatim)
Always prefix with `SEED=42`:

- `SEED=42 bash scripts/check.sh` — convention-robustness check + template validation (seconds, offline)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended verification (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full verification (~15 min)
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only
- `SEED=42 python3 run_all_verification.py --skip-slow` — skip slow batch/regression steps
- `SEED=42 python3 run_all_verification.py --restore-only` — recover golden artifacts after interrupted run
- `python3 -m py_compile <file>` — syntax check on changed files

## Critical Baseline Integrity Rules
1. `experiments/*.json` are canonical research artifacts. Verification suite overwrites them while re-running drivers and restores them afterwards — **never leave a verification run half-finished**.
2. Backup lives in repo-local, gitignored `.verify_snapshot/` with `ACTIVE.json` marker holding the owning pid. A killed run stays recoverable via `--restore-only`.
3. `scripts/check_goldens_clean.py` fails when a tracked artifact under `experiments/` differs from HEAD or a stale snapshot is pending.
4. `scripts/check_golden_baseline.py` compares every tracked artifact with the SHA-256 pinned in `ledger/golden_baseline.json`. Replacing an artifact requires re-pinning (`python3 scripts/check_golden_baseline.py --update`). Never re-pin as a side effect of running verification.
5. **Do not commit verification output.** If interrupted, restore before committing.
6. Drivers re-execute with `QUANT_RESEARCH_OFFLINE=1`; missing cache entries fail hard. To add a data input, commit the file and re-pin with `python3 scripts/check_data_coverage.py --update`.

## Optimizer Determinism (ledger E049/E050)
- `src/portfolio_opt.py` validates a solver answer on the **problem's constraints**, never on the solver's exit status. SLSQP status 8 at a constrained optimum is acceptable; gating on it made artifacts environment-dependent. Pinned by `tests/test_portfolio_opt.py`.
- E050 exact KKT active-set enumeration is the primary tangency solver; artifacts are bit-reproducible across environments (0 differences at 2026-11-23T05:17Z measurement).

## Next Steps for the Next Session
1. Review `ledger/RESEARCH_LEDGER.md` for standing dispositions and gate flags.
2. Run `SEED=42 bash scripts/check.sh` to confirm a clean baseline before starting work.
3. Do not commit verification output or re-pin goldens as a side effect.
4. If modifying an experiment driver, update its `pre_registered` JSON block (goalposts never moved post-hoc) and record any gate changes in the ledger.

## Key Files
- `AGENTS.md` — project commands & conventions (read before running the suite)
- `ledger/RESEARCH_LEDGER.md` — surviving strategies & gate dispositions
- `ledger/golden_baseline.json` — SHA-256 fingerprints of canonical artifacts
- `experiments/*.json` — committed experiment artifacts (canonical baseline)
- `src/batch_run.py`, `src/validate.py` — experiment drivers
- `src/portfolio_opt.py` — portfolio optimizer (SLSQP + exact active-set fallback)
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- `tests/test_portfolio_opt.py`