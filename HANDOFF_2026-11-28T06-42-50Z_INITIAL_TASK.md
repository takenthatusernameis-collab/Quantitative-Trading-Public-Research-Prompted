# Handoff for Next Agentic Work Session

**Timestamp:** 2026-11-28T09:35:05Z
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase:** Research complete (E001–E043) — surviving strategies in `ledger/RESEARCH_LEDGER.md`

## Current State

- All 43 experiments completed and documented
- Verification suite operational with three tiers:
  - `make check` / `SEED=42 bash scripts/check.sh` — fast convention-robustness (~seconds)
  - `make verify-quick` / `SEED=42 python3 run_all_verification.py` — 8 drivers, ~8 min
  - `make verify-extended` / `SEED=42 python3 run_all_verification.py --extended` — 26 drivers, ~21 min
  - `make verify-full` / `SEED=42 python3 run_all_verification.py --full` — full sensitivity grid, ~15 min
- Golden artifacts in `experiments/*.json` are canonical baselines (protected by snapshot/restore mechanism)
- Data cache in `data/` (gitignored except pinned vintages 2026-10-11/2026-10-12)

## Key Commands for Next Session

```bash
# Quick health check (run first)
SEED=42 bash scripts/check.sh

# Full verification pipeline
SEED=42 python3 run_all_verification.py --extended

# Individual experiment drivers (if needed)
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
```

## Critical Conventions (from AGENTS.md)

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores on completion. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
2. **Seed is always 42** for reproducibility
3. **Do not re-pin goldens** to silence tolerance violations — only deliberate code changes with ledger entry
4. **Cache coverage is enforced** — `scripts/check_data_coverage.py` validates all download call sites
5. **Optimizer determinism** — `src/portfolio_opt.py` validates on constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`)

## Ledger Status

Validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Key entries:
- E042: Min-var confirmatory (PARTIAL)
- E041: Market-neutral portfolio (REJECTED)
- E025: Cointegration stat-arb (REJECTED)
- E050: Exact KKT active-set fix (closed E041/E042 drift)

## Next Steps (Suggested)

- Run `make check` to verify baseline integrity
- Run `make verify-extended` for full structural match verification
- Review `ledger/RESEARCH_LEDGER.md` for promotion candidates requiring confirmatory runs
- Any new experiment requires pre-registration with falsification expectations before execution