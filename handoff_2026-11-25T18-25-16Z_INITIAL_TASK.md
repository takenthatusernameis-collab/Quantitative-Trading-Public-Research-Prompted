# Agentic Work Session Handoff

**Timestamp:** 2026-11-26T00:43:07Z
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Workspace:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase:** Complete (E001–E043 executed)
**Surviving Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite:** Operational with three tiers:
- `make check` / `SEED=42 bash scripts/check.sh` — convention robustness (~seconds)
- `make verify-quick` — 8 drivers + batch + validate + E042 n_sim=2 (~8 min)
- `make verify-extended` — +18 committed drivers, structural match (~21 min)
- `make verify-full` — E042 n_sim=50 + 96-config sensitivity grid (~15 min)

---

## Key Artifacts (Canonical Baselines)

- `experiments/*.json` — committed golden outputs (never modified by verification)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of every golden
- `ledger/data_baseline.json` — SHA-256 of all pinned data caches
- `data/vintages.json` — 2026-10-12 vintage (primary)
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot (2026-10-20)

---

## Critical Invariants (Must Preserve)

1. **Golden integrity:** Verification backs up `experiments/` to `.verify_snapshot/`, restores after. Never leave a run half-finished.
2. **Offline reproducibility:** `QUANT_RESEARCH_OFFLINE=1` enforced; all data inputs must be pinned in `ledger/data_baseline.json`.
3. **Optimizer determinism:** `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049). E050 exact active-set enumeration makes tangency QP bit-reproducible.
4. **No silent re-pins:** Re-pinning goldens or data requires ledger entry first (see E050 precedent).

---

## Quick Commands for Next Session

```bash
# Verify environment & conventions (fast, offline)
SEED=42 bash scripts/check.sh

# Quick verification (recommended starting point)
SEED=42 python3 run_all_verification.py

# Full verification if time permits
SEED=42 python3 run_all_verification.py --full

# Recover goldens if previous run was interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Open Items / Next Steps

- [ ] Run full verification suite to confirm current baseline integrity
- [ ] Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion candidates
- [ ] Consider confirmatory runs for any sensitivity-grid configs that cleared gates (requires dedicated pre-registration + placebo)
- [ ] Update documentation if any new experiments are designed

---

## Environment Notes

- Python 3, deps in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`
- Data cached in `data/` (gitignored except pinned vintages)
- SEED=42 for all reproducibility (walk-forward + placebo RNG)

---

*This handoff is durable across sessions. Update it when material state changes.*