# Agent Handoff — 2026-11-19T13:03:18Z

## Project State
Quantitative Trading Public Research (2014–2026 US equities, futures, macro). Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands (SEED=42)
```bash
make check                    # Fast convention-robustness (~seconds)
make verify-quick             # 8 min: 8 drivers + batch + validate + E042 n_sim=2
make verify-extended          # 21 min: quick + 18 more drivers, structural match
make verify-full              # 15 min: E042 n_sim=50 + 96-config sensitivity grid
```

## Key Constraints
- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
- **Golden baseline integrity**: `ledger/golden_baseline.json` pins SHA-256 of every artifact in `experiments/`. Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update` (shows in diff).
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates all `data.download()` call sites resolve to committed parquet matching `ledger/data_baseline.json`.
- **Optimizer determinism** (ledger E049): `src/portfolio_opt.py` validates solver answers on problem constraints, not exit status. Tangency QP ill-conditioned — 1-ulp drift moves min_var ~1e-05. Do not re-pin E041/E042 to silence drift.

## Current Drift Status (as of 2026-10-20)
- 15/18 extended drivers reproduce with 0 differences
- E030: 0 diffs (panel now committed, golden re-pinned per ledger E048)
- E029: 0 diffs (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`)
- E041: 133 numeric diffs (1-ulp QP sensitivity), 0 structural diffs — decision REJECTED 3/5 unchanged. Open item in ledger.

## Next Session Suggestions
1. Run `make check` to verify baseline cleanliness before any work
2. If continuing verification: choose `verify-quick` / `verify-extended` / `verify-full` per time budget
3. If adding experiments: pre-register with falsification gates, add driver to `experiments/`, update `ledger/RESEARCH_LEDGER.md`
4. If modifying optimizer: run `python3 -m pytest tests/test_portfolio_opt.py` (part of `scripts/check.sh`)

## Critical Files
- `ledger/RESEARCH_LEDGER.md` — canonical experiment log with dispositions
- `ledger/golden_baseline.json` — SHA-256 pins for `experiments/*.json`
- `ledger/data_baseline.json` — SHA-256 pins for data cache files
- `data/vintages.json` — primary data vintage (2026-10-12)
- `data/fundamentals_vintages.json` — E029 fundamentals vintage
- `scripts/check.sh` — pre-commit gate (run before any commit)