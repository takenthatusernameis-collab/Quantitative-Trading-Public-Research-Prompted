# Handoff — Agentic Work Session

**Timestamp:** 2026-11-23T00:30:44Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status

**Research Phase:** COMPLETE (E001–E043 executed)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

## Verification Commands (SEED=42 required)

```bash
# Fast convention-robustness check (~seconds, offline)
make check

# Quick full verification (~8 min; 8 drivers + batch + validate + E042 n_sim=2)
make verify-quick

# Extended verification (~21 min; quick + 18 more drivers, structural match)
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
make verify-full
```

## Key Artifacts

- **Golden baselines:** `experiments/*.json` (canonical, committed)
- **Golden fingerprints:** `ledger/golden_baseline.json` (SHA-256 pinned)
- **Data baselines:** `ledger/data_baseline.json` (SHA-256 pinned cache files)
- **Fundamentals vintages:** `data/fundamentals_vintages.json` + `data/fundamentals/`
- **Vintage pins:** `data/vintages.json` (2026-10-12 primary, 2026-10-11 for E026/E028/E029/E030/E034/E036/E037)

## Critical Invariants

1. **Never leave verification half-finished** — it overwrites `experiments/` and restores after. If killed, recover with `make verify-quick --restore-only` or `git checkout -- experiments/`
2. **Cache coverage is enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site has a committed, SHA-256-pinned parquet file
3. **Golden baseline integrity** — `scripts/check_golden_baseline.py` compares `experiments/` to pinned SHA-256 in `ledger/golden_baseline.json`. Re-pin only via explicit `--update`, never as side effect of verification
4. **Optimizer determinism** — SLSQP status 8 is acceptable at constrained optimum (validated in `tests/test_portfolio_opt.py`). Do not re-pin E041/E042 grid artifacts to silence 1-ulp drift

## Known Drift (Extended Verification)

- **E030:** Was re-pinned 2026-10-20 (16-ETF panel committed), now reproduces with 0 differences
- **E041:** 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity). 3 structural diffs fixed. **Do not re-pin** — open ledger item
- **E029:** Offline-reproducible since 2026-10-20 (fundamentals pinned), 0 differences

## Next Steps for New Session

1. Run `make check` to verify working tree integrity
2. Run `make verify-quick` to confirm baseline reproducibility
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
4. Any new experiment requires pre-registration (gates, falsification, sensitivity grid) before execution

---

**Session ended cleanly.** No interrupted verification runs. Golden artifacts match HEAD.
