# Handoff — 2026-11-12T04:08:18Z

## Session Context
- **Project**: Quantitative-Trading-Public-Research-Prompted (independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data)
- **Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands (from AGENTS.md)
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Critical Baseline Integrity Notes
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up before re-running and restores afterward.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Never commit verification output** — restore goldens before committing.
- **Cache coverage enforced**: `scripts/check_data_coverage.py` requires every `data.download()` call site to have a pinned cache file matching SHA-256 in `ledger/data_baseline.json`.

## Reproducibility
- **Seed**: Always `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 / 2026-10-11 vintages)
- **E029**: Fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — fully offline-reproducible
- **E030**: 16-ETF input panel now committed; reproduces with 0 differences

## Known Drift (Extended Verification)
- **E041**: 133 numeric differences (1-ulp sensitivity of ill-conditioned QP), 0 structural — optimizer determinism issue (ledger E049), do NOT re-pin
- **E030**: 0 differences since 2026-10-20 (ledger E048)
- **E029**: 0 differences since 2026-10-20 (ledger E045)

## Open Items (from Ledger)
- E041/E042 grid artifacts drift due to ill-conditioned QP — open item in ledger, do not re-pin to silence
- Optimizer validates on problem constraints, not solver exit status (pinned by `tests/test_portfolio_opt.py`)

## Next Session Suggestions
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. If continuing verification: `SEED=42 python3 run_all_verification.py --extended`
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
4. Review any new experiment ideas against pre-registration requirements