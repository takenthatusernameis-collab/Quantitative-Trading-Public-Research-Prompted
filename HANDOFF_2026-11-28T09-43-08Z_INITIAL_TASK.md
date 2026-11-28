# Agent Handoff — Initial Task — 2026-11-28T09:43:08Z

> Durable handoff for the next agentic work session. Read this file first.
> Timestamp (UTC): **2026-11-28T09:43:08Z**. If a newer
> `HANDOFF_*_INITIAL_TASK.md` exists, prefer it; this file is the record for
> this checkpoint.

## TL;DR — Do this first
1. **BLOCKER: the golden baseline is out of sync with `HEAD`.** `scripts/check_golden_baseline.py`
   FAILS on 5 artifacts (details + exact recovery commits below). The working
   tree is clean, so `HEAD` itself carries a captured verification run that
   silently replaced the canonical baseline — the exact failure mode AGENTS.md
   warns about (prior incidents `d6042b0`/`9f20def`, `1623923`, `701ed78`).
   **Do not commit anything until this is reconciled.**
2. Reconcile per the runbook below, then run `SEED=42 bash scripts/check.sh`
   and `SEED=42 python3 run_all_verification.py --extended`.
3. Only after green: resume the open research/verification items at the bottom.

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro).
- **Phase**: Research complete (E001–E043). Surviving validated strategies in
  `ledger/RESEARCH_LEDGER.md`. Procedure/ranking in `ledger/PRIORITIZATION.md`.
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git**: branch `main`, up to date with `origin/main`. Only uncommitted change
  is a recompiled bytecode file `src/__pycache__/cache_keys.cpython-312.pyc`
  (harmless; `git checkout -- src/__pycache__/cache_keys.cpython-312.pyc` to clean).

## BLOCKER DETAIL — golden baseline divergence (measured 2026-11-28T09:43Z)
`SEED=42 python3 scripts/check_golden_baseline.py` → **FAIL, 5 pinned artifacts differ**:

| Artifact | Pinned SHA-256 (in `ledger/golden_baseline.json`) | Recovery commit (ancestor of HEAD) |
|---|---|---|
| `experiments/cointegration_large_liquid.json` | `a411825…4120e2` | `da00bd0d6524357a1830b6ed85e674d73d02bb3c` |
| `experiments/pairs_large_liquid.json` | `5ab3999…4ac95d` | `da00bd0d6524357a1830b6ed85e674d73d02bb3c` |
| `experiments/dollar_neutral_lowbeta_large_liquid.json` | `c657c3a…4d38b2aa3` | `bf42916931e92f763abc3f415279d30108c9d274` |
| `experiments/e037_portfolio.json` | `dcaeb79…ddef3d7adde7` | `c5038332a6518a9b681646de8e89ad09e7060ee2` |
| `experiments/e042_lead_config_confirmatory.json` | `fa06eeb…f3c901921` | `c5038332a6518a9b681646de8e89ad09e7060ee2` |

Key facts established this session:
- Working tree == HEAD for `experiments/` (only the `.pyc` differs), so the
  divergence lives in `HEAD`, not in uncommitted edits.
- **No single commit matches all 5 pinned SHAs.** The pinned artifacts come from
  three different commits (table above). All three are ancestors of `HEAD`.
- `HEAD` matches **0/5** pinned artifacts.

### Recovery runbook (choose ONE, deliberately)
- **Option A — restore the pinned artifacts (preferred if the published numbers
  are authoritative).** Per AGENTS.md, restore each from the last commit whose
  SHA-256 matches the pin (do NOT use plain `git checkout -- experiments/`,
  which would restore the captured run that `HEAD` already holds):
  ```bash
  git checkout da00bd0d6524357a1830b6ed85e674d73d02bb3c -- experiments/cointegration_large_liquid.json experiments/pairs_large_liquid.json
  git checkout bf42916931e92f763abc3f415279d30108c9d274 -- experiments/dollar_neutral_lowbeta_large_liquid.json
  git checkout c5038332a6518a9b681646de8e89ad09e7060ee2 -- experiments/e037_portfolio.json experiments/e042_lead_config_confirmatory.json
  SEED=42 python3 scripts/check_golden_baseline.py   # must now PASS
  ```
  Then re-run `scripts/check.sh` and the extended suite to confirm the restored
  goldens reproduce under committed code. Record the reconciliation in the ledger.
- **Option B — re-pin (only if a *deliberate* code change is intended to alter
  these published numbers).** First record the change in the ledger, then
  `python3 scripts/check_golden_baseline.py --update`, and make the re-pin
  visible in the diff. **Never re-pin as a side effect of running verification.**
- Do NOT "silence" this by re-pinning to whatever a re-run produced — that is the
  documented anti-pattern that caused the prior baseline captures.

## Key Commands
```bash
# Fast convention-robustness check + template validation + golden guards (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended (~21 min; +18 drivers, structural match) / Full (~15 min; E042 n_sim=50 + grid)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Individual Experiment Drivers
```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Critical Invariants (must not break)
1. **Golden files**: `experiments/*.json` are canonical. Verification backs up,
   re-runs, restores. Never commit verification output; `--restore-only` if interrupted.
2. **Seed**: always `SEED=42` (walk-forward + placebo RNG).
3. **Cache coverage**: every `data.download()` input must be committed and pinned
   in `ledger/data_baseline.json` (`scripts/check_data_coverage.py`); suite runs
   with `QUANT_RESEARCH_OFFLINE=1`. Unpinned input = live download = not reproducible.
4. **Optimizer determinism**: tangency QP uses exact active-set enumeration (E050).
   Do **not** re-pin E041/E042 to silence tolerance — there is no remaining
   tolerance violation; re-pin only for a deliberate, ledger-recorded change.
5. **Pre-registration**: never move goalposts post-hoc; grids are "reported, not
   gated"; grid winners need a dedicated confirmatory run before promotion.

## Ledger References
- E049 optimizer determinism (SLSQP status-gating removed); E050 exact KKT
  active-set enumeration (bit-reproducible tangency).
- E045 E029 offline reproducibility (fundamentals pinned, `data/fundamentals/`).
- E048 E030 16-ETF panel pinned; cache coverage enforced.
- E042/E042b market-neutral blend line CLOSED (PARTIAL 4/5, G2 placebo fail).
- Standing rule v1.2.7: artifact-vs-code reconciliation; assert pre-registered
  *outcomes* (gate pass/fail, decision), not stochastic point values.

## Open Items (after the blocker is cleared)
- [ ] Reconcile the golden baseline divergence (see runbook) and re-run `check.sh`.
- [ ] `SEED=42 python3 run_all_verification.py --extended` → confirm all 26 drivers
      reproduce (expect 0 differences per 2026-11-23T05:17Z measurement).
- [ ] Confirm CI gate template `.github/workflow-templates/verification-gate.yml`
      is current (actual workflow cannot be created by agents — see AGENTS.md).
- [ ] `scripts/check_golden_baseline.py` green against `ledger/golden_baseline.json`.

## Environment
- Python 3 with numpy, pandas, scipy, pyarrow, statsmodels, yfinance.
  `cvxpy`/`cvxopt` optional (fallback to `scipy.optimize`).
- Data cache in `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12;
  fundamentals pinned separately in `data/fundamentals/`).