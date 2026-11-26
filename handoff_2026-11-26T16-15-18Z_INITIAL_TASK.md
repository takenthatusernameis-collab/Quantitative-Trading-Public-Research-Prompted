# Handoff: Next Agentic Work Session

**Timestamp**: 2026-11-26T16:15:18Z
**Session**: Quantitative Trading Research — Verification & Reproducibility

---

## Project State Summary

**Research Phase**: COMPLETE (E001–E043 executed)
**Surviving Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite**: All tiers operational (`check`, `verify-quick`, `verify-extended`, `verify-full`)

### Key Artifacts (Canonical Baselines)
- `experiments/*.json` — Committed golden outputs (never modified by verification)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of all golden artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data caches
- `data/vintages.json` — 2026-10-12 vintage (primary)
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot (2026-10-20)

### Verification Commands (SEED=42 always)
```bash
# Fast convention check (~seconds)
make check

# Quick full verification (~8 min, 8 drivers + batch + validate + E042 n_sim=2)
make verify-quick

# Extended (~21 min, +18 committed drivers, structural match)
make verify-extended

# Full (~15 min, E042 n_sim=50 + 96-config sensitivity grid)
make verify-full
```

---

## Current Status (as of this handoff)

### Last Verified
- `make check` — PASS (convention robustness + template validation)
- `make verify-quick` — PASS (8 drivers reproduce)
- `make verify-extended` — PASS (26 drivers reproduce, 0 differences at 2026-11-23T05:17Z measurement)
- `make verify-full` — PASS (E042 n_sim=50 + 96-config grid)

### Critical Invariants (Enforced)
1. **Golden integrity**: `scripts/check_goldens_clean.py` + `scripts/check_golden_baseline.py` in `check.sh`
2. **Cache coverage**: `scripts/check_data_coverage.py` — every `data.download()` call site must have pinned cache
3. **Optimizer determinism**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049)
4. **Exact tangency solver**: E050 fix (commit `72dc947`) — active-set enumeration, bit-reproducible

### Known Drift (Closed)
- E041/E042 ill-conditioned QP drift → **RESOLVED** by E050 exact solver (0 differences since 2026-11-23)
- E029 offline-reproducible since 2026-10-20 (fundamentals pinned)
- E030 offline-reproducible since 2026-10-20 (16-ETF panel committed)

---

## Next Session: Suggested Entry Points

### If Continuing Verification
```bash
# Quick sanity check
SEED=42 make check

# Full regression (if time permits)
SEED=42 make verify-full
```

### If Investigating New Strategy
1. Read `ledger/RESEARCH_LEDGER.md` for surviving strategies and rejection rationale
2. Pre-register new experiment with falsification expectations + sensitivity grid
3. Add driver in `experiments/run_eXXX.py` following existing patterns
4. Run verification to establish new golden

### If Debugging Reproducibility
- Check `scripts/check_goldens_clean.py` for working-tree vs HEAD diffs
- Check `scripts/check_golden_baseline.py` for committed baseline vs pinned SHA-256 diffs
- Check `scripts/check_data_coverage.py` for missing cache entries
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`

---

## Environment
- Python 3, deps in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- Optional: cvxpy/cvxopt (optimizer falls back to scipy)
- Offline mode: `QUANT_RESEARCH_OFFLINE=1` (used by verification suite)

---

**Next agent**: Start with `make check` to confirm baseline integrity, then proceed per objective.