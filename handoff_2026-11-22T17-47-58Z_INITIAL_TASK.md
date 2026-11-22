# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T17:48:55Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts — verification overwrites and restores them
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker (pid-tracked)
- Run `SEED=42 python3 run_all_verification.py --restore-only` if interrupted
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard baseline integrity
- Never commit verification output; restore goldens before committing

## Data & Reproducibility
- Seed: Always `SEED=42`
- Data cached in `data/` (parquet, gitignored except pinned vintages)
- 2026-10-12 vintage pinned in `data/vintages.json`
- 2026-10-11 vintage committed (E026/E028/E029/E030/E034/E036/E037 explicit end date)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Cache coverage enforced: `scripts/check_data_coverage.py` validates all download call sites
- `QUANT_RESEARCH_OFFLINE=1` during verification — missing cache = hard fail

## Optimizer Determinism (Ledger E049)
- `src/portfolio_opt.py` validates on problem constraints, not solver exit status
- SLSQP status 8 ("Positive directional derivative for linesearch") is acceptable at constrained optimum
- Tangency QP ill-conditioned: 1-ulp perturbation moves min_var answers ~1e-05
- E041/E042 grid artifacts drift 29-133 differences — do NOT re-pin to silence

## Next Session Guidance
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current experiment dispositions
3. Use `make verify-quick` for fast validation before any changes
4. All experiments follow pre-registration discipline — no moving goalposts post-hoc