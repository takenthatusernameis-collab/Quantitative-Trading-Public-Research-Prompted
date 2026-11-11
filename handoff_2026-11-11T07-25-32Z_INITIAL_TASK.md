# Agentic Work Session Handoff

**Timestamp:** 2026-11-11T09:10:57Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

### Quick Verification (~8 min)
```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```

### Extended Verification (~21 min)
```bash
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended
```

### Full Verification (~15 min)
```bash
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

### Convention Robustness Only (fast, offline)
```bash
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

### Individual Experiment Drivers
```bash
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

---

## Critical Integrity Notes (from AGENTS.md)

1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up before re-running and restores afterward.
2. **Never commit verification output** — if interrupted, restore with `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline integrity**: `scripts/check_golden_baseline.py` compares artifacts with SHA-256 in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
4. **Cache coverage enforced**: `scripts/check_data_coverage.py` requires every `data.download()` call site to have a committed, SHA-256-pinned cache file.
5. **Offline mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache = hard failure.
6. **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status (ledger E049). E041/E042 grid artifacts drift by 29-133 differences — do NOT re-pin to silence.

---

## Reproducibility Requirements

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages)
- **E029 fundamentals**: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — fully offline-reproducible

---

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` (or `make check`) for fast convention-robustness check
2. If clean, proceed with desired verification level (quick/extended/full)
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
4. Check `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) for drift details if running extended

---

## Project Conventions Reminder

- Pre-registration: Every driver has `pre_registered` JSON block + docstring with gates/falsification expectations
- Multiple-testing discipline: Sensitivity grids "reported, not gated"
- Negative results recorded honestly (REJECTED / PARTIAL) with evidence
- No separate linter — use `python3 -m py_compile` on changed files

---

*This handoff was created automatically at session start. Update as work progresses.*