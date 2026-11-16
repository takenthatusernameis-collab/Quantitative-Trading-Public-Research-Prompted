# Agent Handoff — 2026-11-16T04:42:34Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git Repo**: Yes (clean state expected)

## Key Commands (from AGENTS.md)
```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --skip-slow

# Extended verification (~21 min; structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Restore golden artifacts after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Notes
1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites then restores them. Never commit verification output.
2. **Recovery**: If verification interrupted, run `--restore-only` or `git checkout -- experiments/`
3. **Baseline integrity**: `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against baseline drift (run via `scripts/check.sh`)
4. **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`. Offline mode enforced via `QUANT_RESEARCH_OFFLINE=1`
5. **Seed**: Always `SEED=42` for reproducibility

## Individual Experiment Drivers (committed)
- E011, E012, E013, E015, E016, E017, E018, E019, E020, E021, E022, E023, E024, E025, E026, E027, E028, E029, E030, E034, E035, E036, E037, E039, E041, E042

## Open Items (from ledger)
- E041: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- E042: Grid artifacts drift by 29-133 differences — do not re-pin
- E029/E030: Now offline-reproducible (pinned data), reproduce with 0 diffs

## Next Session Suggested Actions
- Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
- If clean, run `SEED=42 python3 run_all_verification.py --skip-slow` for quick verification
- Check `ledger/RESEARCH_LEDGER.md` for latest dispositions