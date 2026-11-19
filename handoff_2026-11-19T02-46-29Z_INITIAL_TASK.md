# Agentic Work Session Handoff

**Timestamp:** 2026-11-19T02:51:30Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands Available

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

## Key Artifacts

- **Golden files:** `experiments/*.json` (canonical research artifacts)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data cache:** `data/` (gitignored except pinned vintages)
- **Baseline integrity:** `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Important Notes

1. **Never leave verification half-finished** - it overwrites golden files and restores them after. Use `--restore-only` if interrupted.
2. **Seed must be 42** for reproducibility (walk-forward + placebo RNG).
3. **Convention:** Close-to-close is v1.2.3 primary; overnight decomposition reported alongside.
4. **Cache coverage is enforced invariant** - all data inputs must be pinned per `ledger/data_baseline.json`.

## Open Items (from Ledger)

- E041 optimizer determinism: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP) - do not re-pin
- E042 grid artifacts drift by 29-133 differences - do not re-pin
- E030 now offline-reproducible since 2026-10-20 (pinned panel committed)
- E029 offline-reproducible since 2026-10-20 (fundamentals snapshot pinned)

## Next Session Suggestions

- Run `make verify-quick` to confirm baseline integrity
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies
- Consider running extended/full verification if time permits
- Review any new experiment ideas against pre-registration requirements

---
*This handoff was created automatically at session start for durability across agentic sessions.*