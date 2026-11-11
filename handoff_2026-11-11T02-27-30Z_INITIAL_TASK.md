# Agent Handoff — 2026-11-11T03:17:38Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043)
- **Surviving strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Baseline**: `experiments/*.json` are canonical golden artifacts (pinned in `ledger/golden_baseline.json`)

## Key Context
- **Verification suite**: `run_all_verification.py` with `--quick` / `--extended` / `--full` modes
- **Seed**: Always `SEED=42` for reproducibility
- **Data**: Cached parquet in `data/` (vintages pinned in `data/vintages.json` and `data/fundamentals_vintages.json`)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification
- **Critical**: Never leave verification half-finished — use `--restore-only` to recover goldens

## Open Items (from ledger)
- E041: 133 numeric differences remain (optimizer ill-conditioning) — do not re-pin
- E030: Now reproducible (pinned 16-ETF panel per E048)
- E029: Fully offline-reproducible since 2026-10-20 (pinned fundamentals)

## Quick Commands
```bash
# Convention check (fast, offline)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Restore goldens if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Next Session Priorities
1. Run `scripts/check.sh` to verify baseline integrity
2. Execute `make verify-quick` for fast validation
3. Review any drift in extended drivers (E041, E030)
4. Check `ledger/RESEARCH_LEDGER.md` for promotion gate status