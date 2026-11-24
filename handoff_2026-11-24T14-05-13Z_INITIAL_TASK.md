# Agentic Work Session Handoff

**Timestamp:** 2026-11-24T14:13:30Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Critical Integrity Notes

- **Never leave verification half-finished**: The suite backs up `experiments/*.json` to `.verify_snapshot/` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Golden baseline protection**: `scripts/check_golden_baseline.py` compares tracked artifacts to SHA-256 fingerprints in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
- **Cache coverage enforced**: All `data.download()` call sites must have committed cache files matching `ledger/data_baseline.json`. Run `python3 scripts/check_data_coverage.py --update` to add new inputs.
- **Optimizer determinicity (E049/E050)**: `src/portfolio_opt.py` validates on constraints, not solver exit status. Exact KKT active-set enumeration (commit `72dc947`) makes E041/E042 bit-reproducible.

## Current State

No active verification run detected. Working tree clean for `experiments/` (golden artifacts intact).

## Next Steps for New Session

1. Run `make check` to validate conventions and golden baseline integrity
2. Choose verification tier (`verify-quick`, `verify-extended`, `verify-full`)
3. If adding new experiments: pre-register with falsification expectations, run driver, record honest result (REJECTED/PARTIAL/PROMOTED)
4. Any deliberate number changes require ledger entry first, then re-pin via `check_golden_baseline.py --update`

## Key Files

- `ledger/RESEARCH_LEDGER.md` — Experiment dispositions and decisions
- `ledger/golden_baseline.json` — SHA-256 pinned artifact fingerprints
- `ledger/data_baseline.json` — SHA-256 pinned data cache fingerprints
- `data/vintages.json` — Pinned data vintage (2026-10-12)
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot
- `scripts/check.sh` — Convention + golden + data coverage validation
- `run_all_verification.py` — Full verification orchestrator