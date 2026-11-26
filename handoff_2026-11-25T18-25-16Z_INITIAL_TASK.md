# Agentic Work Session Handoff

**Timestamp:** 2026-11-26T00:24:02Z
**Session ID:** [auto-generated]
**Project:** Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Current Verification Status:** Ready for verification runs

---

## Key Artifacts & Baselines

| Artifact | Location | Status |
|----------|----------|--------|
| Golden experiment outputs | `experiments/*.json` | Canonical baseline (pinned to `ledger/golden_baseline.json`) |
| Data vintages | `data/vintages.json`, `data/fundamentals_vintages.json` | Pinned 2026-10-12 / 2026-10-11 |
| Verification snapshot | `.verify_snapshot/` | Gitignored, auto-managed by `run_all_verification.py` |

---

## Quick Start Commands (Next Session)

```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full

# Recovery if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Critical Integrity Notes (Read Before Running)

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If killed, use `--restore-only` or `git checkout -- experiments/`.

2. **Golden baseline protection** — `scripts/check_golden_baseline.py` compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires deliberate action (`--update`) and ledger entry.

3. **Cache coverage invariant** — `scripts/check_data_coverage.py` enforces all `data.download()` call sites resolve to committed, SHA-256-pinned parquet files. Unpinned = hard fail under `QUANT_RESEARCH_OFFLINE=1`.

4. **Optimizer determinism** — `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049). E050 exact active-set enumeration (commit `72dc947`) made E041/E042 bit-reproducible.

---

## Recent Ledger Entries (Context)

- **E049** (2026-10-20): Root-caused E041/E042 optimizer drift — SLSQP status-gating defect fixed
- **E050** (2026-11-01): Exact KKT active-set enumeration as primary tangency solver — 0 differences confirmed 2026-11-23
- **E029/E030** (2026-10-20): Offline-reproducible via pinned fundamentals & ETF panel
- **E045**: Convention robustness documented

---

## Suggested Next Steps

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Run `SEED=42 python3 run_all_verification.py` (quick) to confirm baseline
3. If quick passes, consider `--extended` for structural match across all 26 drivers
4. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion gates

---

## Environment

- **Python:** 3.x (see `requirements.txt`: numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Optional:** cvxpy/cvxopt (fallback to scipy.optimize)
- **Seed:** Always `SEED=42` for walk-forward + placebo RNG
- **Convention:** Close-to-close primary (v1.2.3), overnight decomposition reported alongside

---

*This handoff was created automatically at session start. Update with session findings before exit.*