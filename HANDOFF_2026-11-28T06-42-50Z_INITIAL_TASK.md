# Agent Handoff — 2026-11-28T09:39:08Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Context
- All experiments pre-registered with falsification expectations and promotion gates
- Golden artifacts in `experiments/*.json` are canonical baselines
- Verification suite overwrites and restores goldens; never leave a run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`

## Quick Commands
```bash
# Fast check (convention robustness + template validation)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Guards
1. `scripts/check_goldens_clean.py` — fails if `experiments/` differs from HEAD or stale snapshot pending
2. `scripts/check_golden_baseline.py` — compares artifacts to SHA-256 in `ledger/golden_baseline.json`
3. `scripts/check_data_coverage.py` — enforces cache coverage (pinned vintages in `data/vintages.json`, `data/fundamentals_vintages.json`)

## Reproducibility
- **Seed**: Always `SEED=42`
- **Convention**: Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 / 2026-10-11 vintages)
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification

## Recent Ledger Entries
- **E049**: Optimizer determinism fix (SLSQP status-gating removed, validate on constraints)
- **E050**: Exact KKT active-set enumeration as primary tangency solver → bit-reproducible E041/E042
- **E048**: Cache coverage invariant enforced; E029/E030 fundamentals/ETF panels pinned

## Next Session Priorities
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. If clean, proceed with `SEED=42 python3 run_all_verification.py --extended` for structural match
3. Any golden mismatch must be fixed before committing (restore with `--restore-only` if needed)
4. Do not re-pin artifacts to silence tolerance violations — only deliberate code changes with ledger entry

## Files to Reference
- `AGENTS.md` — full project commands & conventions
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions
- `ledger/golden_baseline.json` — pinned SHA-256 fingerprints
- `ledger/data_baseline.json` — pinned data cache fingerprints
- `scripts/check.sh` — first-class validation pipeline