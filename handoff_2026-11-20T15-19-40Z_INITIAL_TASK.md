# Handoff — Agentic Work Session

**Timestamp:** 2026-11-20T15:21:49Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** Complete (E001–E043) — see `ledger/RESEARCH_LEDGER.md`

---

## Project State

- **Verification suite** operational: `SEED=42 python3 run_all_verification.py` (quick/extended/full)
- **Golden artifacts** in `experiments/*.json` — canonical baseline, restored after each verification run
- **Data cache** in `data/` (parquet, gitignored except pinned vintages)
- **Convention:** Close-to-close primary (v1.2.3), overnight decomposition reported alongside

---

## Key Commands

```bash
# Fast check (convention robustness + template validation)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min, 8 drivers + batch + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min, +18 drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min, E042 n_sim=50 + 96-config sensitivity)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Individual experiments
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

---

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores on completion. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

2. **Golden baseline pinned** in `ledger/golden_baseline.json` (SHA-256). `scripts/check_golden_baseline.py` enforces this — never re-pin as side effect of verification.

3. **Cache coverage invariant** (ledger E048): every `data.download()` call site must have a committed, SHA-256-pinned cache file. `scripts/check_data_coverage.py` enforces this.

4. **Optimizer determinism** (ledger E049): `src/portfolio_opt.py` validates on constraints, not solver exit status. Tangency QP remains ill-conditioned — E041/E042 grid artifacts drift by 29-133 differences (1-ulp sensitivity). **Do not re-pin to silence.**

5. **E029 offline-reproducible** since 2026-10-20 (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`)

6. **E030 offline-reproducible** since 2026-10-20 (16-ETF panel committed, golden re-pinned)

---

## Open Items (from Ledger)

- E041 drift: 133 numeric differences remain (ill-conditioned QP, not data) — decision REJECTED 3/5 unchanged
- E042 min-var confirmatory: PARTIAL (lead artifact reproduced, grid sensitivity noted)
- No surviving strategies promoted beyond research phase

---

## Next Session Suggestions

- Run `make verify-quick` to confirm baseline integrity
- Review `ledger/RESEARCH_LEDGER.md` for experiment dispositions
- Check `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` if any golden mismatch reported
- Consider extended/full verification if time permits