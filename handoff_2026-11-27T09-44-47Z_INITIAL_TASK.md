# Handoff — 2026-11-27T15:38:59Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Current commit**: Check `git log --oneline -1` for latest

## Quick Commands
```bash
# Convention robustness check (fast, offline)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, includes E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts
- **Golden baselines**: `experiments/*.json` (canonical, never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (surviving strategies + dispositions)
- **Golden fingerprints**: `ledger/golden_baseline.json` (SHA-256 pins)
- **Data baselines**: `ledger/data_baseline.json` (cache SHA-256 pins)

## Critical Invariants
1. **Never commit verification output** — `run_all_verification.py` backs up/restores goldens; interrupted runs leave driver output in `experiments/`. Restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
2. **Seed always 42** — walk-forward + placebo RNG
3. **Offline reproducibility** — `QUANT_RESEARCH_OFFLINE=1` enforced in verification; all cache files must exist and match pinned SHA-256
4. **No goalpost moving** — pre-registration in every driver output; sensitivity grids reported not gated

## Recent Context
- E050 fix (exact KKT active-set enumeration) landed — E041/E042 now bit-reproducible (0 differences at 2026-11-23T05:17Z)
- E029 fundamentals pinned offline-reproducible since 2026-10-20
- E030 16-ETF panel committed and pinned
- Optimizer validates on problem constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`)

## Next Session Suggestions
- Run `make check` to verify convention robustness
- If extending research: pre-register new experiment with falsification expectations before coding
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion gates