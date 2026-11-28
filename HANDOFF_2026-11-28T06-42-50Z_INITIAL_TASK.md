# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-28T09:34:32Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** Complete (E001–E043) — surviving validated strategies in `ledger/RESEARCH_LEDGER.md`

## Quick Start Commands
```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Context
- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files:** `experiments/*.json` are canonical artifacts; verification backs up & restores them
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages 2026-10-12 / 2026-10-11)
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (offline-reproducible)
- **Cache coverage:** Enforced invariant — `scripts/check_data_coverage.py` validates all `data.download()` calls
- **Optimizer determinacy:** `src/portfolio_opt.py` validates on problem constraints, not solver exit status (ledger E049)
- **E050 fix:** Exact KKT active-set enumeration makes E041/E042 bit-reproducible across environments

## Verification Suite Notes
- `scripts/check.sh` runs: `check_goldens_clean.py` → `check_golden_baseline.py` → py_compile → convention robustness
- A verification run must never be left half-finished (snapshot in `.verify_snapshot/`)
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Never re-pin goldens** to silence tolerance violations — only deliberate code changes recorded in ledger warrant re-pin

## Individual Experiment Drivers
```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Project Conventions
- Pre-registration: every driver has `pre_registered` JSON block + docstring with gates/falsification/sensitivity grid
- Multiple-testing: sensitivity grids are "reported, not gated"
- Negative results: recorded honestly (REJECTED / PARTIAL) with evidence
- Golden files: committed artifacts, never modified by verification

## CI / Automation
- CI gate template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI)
- Controller restores `.github/workflows/` at checkpoints; repo `GITHUB_TOKEN` lacks workflows push permission

## Lint / Format
- Python 3 research repo; checked by verification suite (py_compile + reproducibility)
- No separate linter configured; run `python3 -m py_compile` on changed files

---

**Next Steps / Open Items:** None specified — session started fresh. Check `ledger/RESEARCH_LEDGER.md` for current disposition of all experiments.