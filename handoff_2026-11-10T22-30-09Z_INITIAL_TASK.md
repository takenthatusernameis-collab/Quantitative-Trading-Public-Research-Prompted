# Agent Handoff — 2026-11-10T22:37:42Z

## Project State
- **Research phase**: Complete (E001–E043)
- **Surviving strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current verification status**: Not run in this session

## Key Artifacts
- Golden baselines: `experiments/*.json` (canonical, committed)
- Ledger: `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- Data vintages: `data/vintages.json`, `data/fundamentals_vintages.json`
- Pinned fundamentals: `data/fundamentals/` (E029 offline-reproducible since 2026-10-20)
- Pinned ETF panel: `data/` (E030 offline-reproducible since 2026-10-20)

## Open Items (from Ledger)
- **E041**: Optimizer QP ill-conditioned — 133 numeric diffs remain in extended verification (1-ulp sensitivity). Do not re-pin.
- **E042/E041 grid artifacts**: Drift 29–133 diffs due to same ill-conditioning. Do not re-pin.
- **E029/E030**: Now offline-reproducible (pinned vintages committed).

## Verification Commands (SEED=42)
```bash
# Fast convention check (~seconds)
make check

# Quick verification (~8 min, 8 drivers)
make verify-quick

# Extended (~21 min, 26 drivers + structural match)
make verify-extended

# Full (~15 min, E042 n_sim=50 + 96-config grid)
make verify-full
```

## Critical Guards
- `scripts/check_goldens_clean.py` — fails if `experiments/` differs from HEAD or stale snapshot pending
- `scripts/check_golden_baseline.py` — compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json`
- `scripts/check_data_coverage.py` — enforces every `data.download()` call site has committed, pinned cache
- `tests/test_portfolio_opt.py` — optimizer validates on problem constraints, not solver exit status

## Recovery
If verification interrupted:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

## Next Session Suggestions
1. Run `make check` to validate conventions and baseline integrity
2. Run `make verify-quick` for fast regression check
3. Review any extended drift reports in `.verify_reports/` (gitignored)
4. Address open ledger items if pursuing optimizer improvements