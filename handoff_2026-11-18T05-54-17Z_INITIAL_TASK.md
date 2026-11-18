# Agentic Work Session Handoff

**Timestamp:** 2026-11-18T05:58:04Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status Summary

**Research Phase:** COMPLETE (Experiments E001–E043 executed)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Baseline Artifacts:** Committed in `experiments/*.json` (canonical goldens)

---

## Verification Commands (Ready to Run)

```bash
# Fast convention-robustness check (~seconds, offline)
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
```

---

## Critical Integrity Notes (Read Before Running)

1. **Golden files in `experiments/*.json` are canonical** — verification overwrites them temporarily and restores after. Never leave a verification run half-finished.

2. **Recovery if interrupted:**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or
   git checkout -- experiments/
   ```

3. **Baseline protection:** `scripts/check_golden_baseline.py` compares tracked artifacts against SHA-256 fingerprints in `ledger/golden_baseline.json`. Re-pinning requires explicit `--update` flag.

4. **Cache coverage is enforced:** `scripts/check_data_coverage.py` requires every data download call site to have a committed, SHA-256-pinned cache file. Offline mode (`QUANT_RESEARCH_OFFLINE=1`) fails hard on missing cache.

5. **Optimizer determinism (ledger E049):** Portfolio optimizer validates on constraints, not solver exit status. Tangency QP remains ill-conditioned — E041/E042 grid artifacts drift by 29–133 differences (1-ulp sensitivity). Do NOT re-pin to silence.

---

## Key Files to Review

| File | Purpose |
|------|---------|
| `ledger/RESEARCH_LEDGER.md` | Surviving validated strategies & dispositions |
| `ledger/golden_baseline.json` | SHA-256 pins for all golden artifacts |
| `ledger/data_baseline.json` | SHA-256 pins for data cache files |
| `data/vintages.json` | Pinned data vintage (2026-10-12) |
| `data/fundamentals_vintages.json` | Pinned fundamentals for E029 |
| `experiments/*.json` | Canonical golden artifacts (8 quick + 18 extended drivers) |

---

## Suggested Next Steps for Next Session

1. **Run verification suite** to confirm reproducibility baseline:
   ```bash
   SEED=42 make verify-quick
   ```

2. **Review RESEARCH_LEDGER.md** for open items:
   - E041 optimizer drift (133 numeric diffs, ill-conditioned QP)
   - E030/E029 re-pinned to offline snapshots (now reproducible)
   - Confirmatory runs needed for any sensitivity-grid configs that cleared gates

3. **If verification passes:** Consider next research phase — new pre-registered experiments with falsification expectations.

4. **If verification fails:** Diagnose via `scripts/check.sh` output and `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`.

---

## Environment

- **Python:** 3.x with numpy, pandas, scipy, pyarrow, statsmodels, yfinance
- **Optional:** cvxpy/cvxopt (falls back to scipy.optimize)
- **Seed:** Always use `SEED=42` for walk-forward + placebo RNG
- **Convention:** Close-to-close primary (v1.2.3); overnight decomposition reported alongside

---

*This handoff is durable — commit or copy to persist across sessions.*