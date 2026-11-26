# Handoff: Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T02:24:49Z
**Session:** Kilo agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status Summary

**Research Phase:** COMPLETE (E001–E043 executed)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

### Key Artifacts
- **Golden files:** `experiments/*.json` (canonical research artifacts, must not be modified by verification)
- **Data cache:** `data/` (gitignored parquet, pinned vintages 2026-10-11 and 2026-10-12)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (dispositions, gates, sensitivity grids)
- **Golden baseline:** `ledger/golden_baseline.json` (SHA-256 fingerprints of committed goldens)
- **Data baseline:** `ledger/data_baseline.json` (SHA-256 fingerprints of committed data cache)

### Git State (as of this handoff)
- **Branch:** `main`
- **HEAD:** `8b27e29d` (`8b27e29dacdcb5f85824ac5302d6d2e38a8a8a7e`) — `chore(kilo): checkpoint agent session`
- **Upstream:** up to date with `origin/main` (0 ahead / 0 behind)
- **Working tree:** clean apart from tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc`

---

## Verification Commands (use SEED=42)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or: make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or: make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or: make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Critical Baseline Integrity Rules

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If killed, recover with `--restore-only` or `git checkout -- experiments/`
2. **Golden files are committed artifacts** — `run_all_verification.py` backs up before re-running and restores after. Baseline never modified by verification.
3. **Do not commit verification output** — if interrupted, working tree holds driver output instead of goldens. Restore before committing.
4. **Golden baseline pinned in `ledger/golden_baseline.json`** — `scripts/check_golden_baseline.py` compares tracked artifacts to pinned SHA-256. Re-pinning requires `--update` and must be recorded in ledger.
5. **Data cache coverage enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site has a committed, SHA-256-pinned cache file. Unpinned input = live download (non-reproducible).

---

## Reproducibility Requirements

- **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Optional:** cvxpy/cvxopt (falls back to scipy.optimize)

---

## Optimizer Determinism (Ledger E049/E050)

- `src/portfolio_opt.py` validates solver answer on **problem constraints**, never on solver exit status
- SLSQP status 8 ("Positive directional derivative for linesearch") can occur at constrained optimum — gating on it made tangency portfolio environment-dependent
- **Rule pinned by `tests/test_portfolio_opt.py`** (first-class step in `scripts/check.sh`)
- **E050 fix (commit 72dc947):** Exact KKT active-set enumeration as primary tangency solver → bit-reproducible artifacts (0 differences at 2026-11-23T05:17Z measurement)
- **Do NOT re-pin E041/E042** to silence tolerance — no remaining violation; re-pin only for deliberate code changes recorded in ledger

---

## Key Files to Reference

| File | Purpose |
|------|---------|
| `ledger/RESEARCH_LEDGER.md` | Experiment dispositions, gates, sensitivity grids |
| `ledger/golden_baseline.json` | SHA-256 of committed `experiments/*.json` |
| `ledger/data_baseline.json` | SHA-256 of committed data cache files |
| `data/vintages.json` | Pinned data vintage (2026-10-12) |
| `data/fundamentals_vintages.json` | Pinned E029 fundamentals snapshot |
| `scripts/check_goldens_clean.py` | Detects working-tree vs HEAD drift in `experiments/` |
| `scripts/check_golden_baseline.py` | Detects committed baseline vs pinned SHA-256 drift |
| `scripts/check_data_coverage.py` | Validates all data.download() sites have pinned cache |
| `tests/test_portfolio_opt.py` | Optimizer determinism guard |

---

## Current State (as of this handoff)

- **Last verification:** Not run in this session
- **Working tree:** Clean (no uncommitted changes to tracked files)
- **Golden files:** At HEAD (assuming no interrupted verification)
- **Data cache:** Pinned vintages committed
- **Ledger:** Current through E043

---

## Next Session: Suggested First Actions

1. **Run fast check:** `SEED=42 bash scripts/check.sh` — validates conventions, golden cleanliness, golden baseline, data coverage, optimizer determinism
2. **If check passes:** Run `SEED=42 python3 run_all_verification.py` (quick verification)
3. **If check fails:** Address reported issues (golden mismatch, data coverage gap, optimizer drift) before any verification run

---

## Notes for Next Agent

- This project follows strict pre-registration and multiple-testing discipline. Sensitivity grids are "reported, not gated."
- Negative results (REJECTED / PARTIAL) are recorded honestly with evidence.
- The CI gate (`.github/workflows/verification-gate.yml`) cannot be created by automated agents — template at `.github/workflow-templates/verification-gate.yml`.
- Lint/format: `python3 -m py_compile` on changed files (no separate linter configured).

---

**End of Handoff**
