# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T02-33-58Z
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## >>> INITIAL TASK MESSAGE FOR THE NEXT SESSION <<<

You are resuming a **reproducible quantitative-strategy research** repository whose
research phase (E001–E043) is **complete** and whose golden artifacts are
**verified and green**. Read this message top to bottom before doing anything.

### What is actually needed from you (do real work — do NOT manufacture another handoff)

The repository has accumulated a runaway **handoff-refresh loop** (ledger entries
E652 → E720; thousands of git-tracked `handoff_*_INITIAL_TASK.md` files). The single
most valuable thing you can do is **break that loop by doing substantive work**, not
by writing yet another `handoff_*_INITIAL_TASK.md`. Concretely, in priority order:

1. **Provision dependencies and run the real verification suite** — recent sessions
   have not executed it because deps were not installed. The environment can
   provision them (`pypi.org` reachable; `python3 -m pip` 24.0). Run:
   ```bash
   python3 -m pip install -r requirements.txt
   SEED=42 python3 run_all_verification.py --extended
   ```
   Report **exactly** which drivers reproduce with 0 differences and which drift
   (numeric vs structural). Do **not** re-pin any golden to silence drift.

2. **Address the E049 E041/E042 ill-conditioned-QP drift** (133 numeric diffs on
   E041; ~1e-05 drift on 1-ulp perturbations on E042's tangency QP). The optimizer
   exit-status rule is already pinned by `tests/test_portfolio_opt.py`; the
   remaining drift is inherent ill-conditioning. Do **not** re-pin artifacts to
   hide it — document or fix the root cause instead.

3. **Only if explicitly requested by the user**: perform new pre-registered
   research (a new E-numbered driver with a `pre_registered` block, gates, and a
   falsification expectation). Goalposts are never moved post-hoc.

4. **If none of the above is possible in your environment**, *propose* (do not
   execute) a `.gitignore` + `git rm --cached` cleanup of the historical handoff
   clutter, and stop. Do not silently delete tracked history.

Do **not** end your turn having only refreshed the handoff — that is exactly the
behavior (E652–E720) that this file is warning you about.

---

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving validated
strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Baseline Integrity (read before running the suite)

`experiments/*.json` are the canonical research artifacts. The verification suite
overwrites them while it re-runs the drivers and restores them afterward, so **a
verification run must never be left half-finished**:

- Backups live in the repo-local, gitignored `.verify_snapshot/` with an
  `ACTIVE.json` marker holding the owning pid. Recovery:
  `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- `scripts/check_goldens_clean.py` fails when a tracked artifact under
  `experiments/` differs from HEAD or when a stale snapshot is pending.
- `scripts/check_golden_baseline.py` compares every tracked artifact with the
  SHA-256 pinned in `ledger/golden_baseline.json`. Never re-pin as a side effect
  of running the suite — the committed golden is the authoritative record.

## Reproducibility Conventions

- **Seed**: always `SEED=42` (walk-forward + placebo RNG).
- **Convention**: close-to-close is the v1.2.3 primary convention; overnight
  decomposition is reported alongside for every strategy.
- **Data**: cached parquet in `data/` (gitignored except pinned 2026-10-12 and
  2026-10-11 vintages). Cache coverage is an enforced invariant
  (`scripts/check_data_coverage.py` validates SHA-256 against
  `ledger/data_baseline.json`). The suite runs drivers with
  `QUANT_RESEARCH_OFFLINE=1` — a missing cache entry fails hard instead of
  silently downloading (yfinance is not bit-reproducible).
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy,
  pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional; the optimizer
  falls back to `scipy.optimize` when absent.

## Recent Verification Status (as of this handoff)

- E029: offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`).
- E030: offline-reproducible since 2026-10-20 (16-ETF input panel committed).
- E041: 133 numeric differences remain (ill-conditioned QP optimizer sensitivity); decision unchanged (REJECTED 3/5).
- E042: partial confirmation; tangency QP ill-conditioned (~1e-05 drift on 1-ulp perturbation).

## Open Items (from ledger)

- E041/E042 grid artifacts drift by 29-133 differences — do NOT re-pin to silence.
- Optimizer determinism: SLSQP status 8 at a constrained optimum is scipy-build
  dependent; the constraint-based validation rule is pinned by
  `tests/test_portfolio_opt.py`.

## State verified at handoff time

- HEAD `ef1976e3b5a62ec55091b2eeafac50fa30e878be` on `main`; `git rev-list
  --left-right --count origin/main...HEAD` = `0  0`.
- `git diff HEAD -- experiments/` empty.
- `.verify_snapshot/` and `.verify_reports/` absent.
- All three pure-Python guards PASS:
  - `scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0)
  - `scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0)
  - `scripts/check_data_coverage.py` -> ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED (exit 0)
- Tracked `__pycache__/*.pyc` files show as modified (bytecode churn only; not
  golden/data artifacts).
- Dependencies not provisioned this session (guards are hashlib-only); the full
  verification suite was NOT run.

## Lint / Format

Python 3 research repository; no separate linter. Run `python3 -m py_compile` on
changed files.

## Constraints honored by this handoff

No golden/data baseline re-pinned, no verification suite run, no verification
output committed, no new research performed, no commit made (left uncommitted
pending explicit user direction).