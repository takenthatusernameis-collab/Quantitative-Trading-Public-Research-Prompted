# Agentic Work Session Handoff

**Timestamp:** 2026-11-11T10:24:42Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase: COMPLETE** (Experiments E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates
- Negative results recorded honestly (REJECTED / PARTIAL) with evidence

---

## Key Verification Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or
make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Critical Baseline Integrity Notes

1. **Golden files** (`experiments/*.json`) are canonical research artifacts
2. Verification suite backs them up to `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker before re-running
3. **Never leave a verification run half-finished** — it overwrites goldens during execution
4. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
5. `scripts/check_goldens_clean.py` compares working tree with HEAD (step in `scripts/check.sh`)
6. `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 in `ledger/golden_baseline.json` (step in `scripts/check.sh`)
7. **Cache coverage is enforced** — `scripts/check_data_coverage.py` requires every `data.download()` call site to have a committed, SHA-256-pinned cache file

---

## Reproducibility Requirements

- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Data:** Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- **E029 fundamentals:** Pinned separately in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **cvxpy/cvxopt:** Optional; portfolio optimizer falls back to `scipy.optimize`

---

## Known Drift Items (from extended verification)

| Driver | Status | Notes |
|--------|--------|-------|
| E030 | 0 diffs since 2026-10-20 (ledger E048) | 16-ETF panel now committed |
| E041 | 133 numeric diffs (1-ulp QP ill-conditioning) | 3 structural diffs fixed (ledger E049); **do not re-pin** |
| E042 grid | 29-133 diffs | Ill-conditioned tangency QP; **do not re-pin** |

---

## Project Conventions

- **Pre-registration:** Every driver has `pre_registered` JSON block + docstring with gates/falsification/sensitivity grid
- **Multiple-testing discipline:** Sensitivity grids are "reported, not gated"
- **Golden files:** Committed artifacts; verification backs up/restores — baseline never modified by verification
- **Do not commit verification output** — restore before committing (`--restore-only`)

---

## CI / Automation

- Intended CI gate: `.github/workflows/verification-gate.yml` (cannot be created by automated agents)
- Template at `.github/workflow-templates/verification-gate.yml` with instructions in `VERIFICATION_GATE_TEMPLATE.md`
- Maintainer must create actual workflow via GitHub UI
- Local equivalents: `make check`, `make verify`, `make verify-full`

---

## Lint / Format

- Python 3 research repository
- Core scripts checked by verification suite (py_compile + reproducibility)
- No separate linter configured; run `python3 -m py_compile` on changed files

---

## Next Steps / Open Items

1. Monitor ledger for resolution of E041/E042 ill-conditioned QP drift (open item)
2. Ensure any new data inputs are committed and pinned via `scripts/check_data_coverage.py --update`
3. Verify CI gate workflow is created by maintainer if needed

---

*This handoff was generated automatically at session start. Update as needed during work.*