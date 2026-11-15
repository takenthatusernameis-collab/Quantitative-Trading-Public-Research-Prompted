# Agentic Work Session Handoff

**Timestamp:** 2026-11-15T04:17:46Z
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase:** Research complete (E001–E043) — surviving strategies documented in `ledger/RESEARCH_LEDGER.md`

## Current State

- **Verification suite** operational with three tiers:
  - `make check` / `SEED=42 bash scripts/check.sh` — convention robustness (~seconds)
  - `make verify-quick` / `SEED=42 python3 run_all_verification.py` — 8 drivers + batch + validate + E042 n_sim=2 (~8 min)
  - `make verify-extended` — +18 committed drivers, structural match (~21 min)
  - `make verify-full` — E042 n_sim=50 + 96-config sensitivity grid (~15 min)

- **Golden artifacts** in `experiments/*.json` are canonical baselines. Verification backs up, re-runs, restores.
- **Data cache** in `data/` (gitignored except pinned 2026-10-12 / 2026-10-11 vintages). Fundamentals for E029 pinned in `data/fundamentals/`.
- **Cache coverage enforced** by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`.

## Key Conventions (from AGENTS.md)

1. **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
2. **Pre-registration:** Every driver has `pre_registered` JSON block + docstring with gates/falsification/sensitivity
3. **Multiple-testing:** Sensitivity grids reported, not gated; confirmatory run required for promotion
4. **Negative results:** Recorded honestly (REJECTED/PARTIAL) with evidence
5. **Never commit verification output** — restore with `run_all_verification.py --restore-only` if interrupted

## Known Drift Items (ledger E045, E048, E049)

- **E029, E030:** Now offline-reproducible (pinned inputs), reproduce with 0 diffs
- **E041:** 133 numeric diffs (1-ulp ill-conditioned QP), 0 structural — **do not re-pin**
- **E042/E041 grid:** 29–133 numeric diffs from same optimizer sensitivity — **do not re-pin**
- **Optimizer rule:** `src/portfolio_opt.py` validates on constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`)

## Next Session Suggestions

- Run `make check` to verify working tree integrity before any changes
- If modifying drivers/data: update cache coverage via `python3 scripts/check_data_coverage.py --update`
- If modifying optimizer: run `python3 -m pytest tests/test_portfolio_opt.py -v`
- Full verification: `make verify-extended` (recommended before committing)

## Commands Reference

```bash
SEED=42 bash scripts/check.sh              # Fast check
SEED=42 python3 run_all_verification.py    # Quick verify
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only  # Recover goldens
SEED=42 python3 verify_convention_robustness.py         # Convention only
```