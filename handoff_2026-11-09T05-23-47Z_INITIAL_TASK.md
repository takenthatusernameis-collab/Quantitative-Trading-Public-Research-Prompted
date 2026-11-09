# Handoff — 2026-11-09T06:22:15Z

## Context
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Working directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Key Invariants
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification backs them up to `.verify_snapshot/` and restores after.
- **Never leave verification half-finished** — interrupted runs are recoverable via `--restore-only`.
- **Seed**: Always `SEED=42` for reproducibility.
- **Data**: Cached parquet in `data/` (gitignored). Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`.
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates all download call sites.

## Open Items (from ledger)
- E041 optimizer determinism: 133 numeric diffs remain (1-ulp sensitivity of ill-conditioned QP). Do not re-pin.
- E042 min-var confirmatory: PARTIAL — see ledger E045.
- CI workflow template at `.github/workflow-templates/verification-gate.yml` — maintainer must create via GitHub UI.

## Next Steps
- Run `make check` to validate conventions before any changes.
- Use `make verify-quick` for rapid feedback during development.
- Consult `ledger/RESEARCH_LEDGER.md` for experiment dispositions and open items.