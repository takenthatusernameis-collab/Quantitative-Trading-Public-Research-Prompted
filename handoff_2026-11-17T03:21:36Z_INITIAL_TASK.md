# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T03:21:36Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates

## Verification Commands (from AGENTS.md)
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

## Key Notes for Next Session
- Golden files in `experiments/*.json` are canonical research artifacts
- Verification suite backs them up before re-running and restores afterward
- **Never leave a verification run half-finished** - use `--restore-only` to recover if interrupted
- Seed is always `SEED=42` for reproducibility
- Data cached in `data/` (gitignored except pinned vintages)
- Cache coverage is enforced invariant - all inputs must be pinned

## Open Items (from ledger)
- E041 drift: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP) - do not re-pin
- E030: Now reproduces with 0 differences since 2026-10-20 (panel committed)
- E029: Fully offline-reproducible since 2026-10-20 (fundamentals pinned)

## Next Steps
- Run `SEED=42 python3 run_all_verification.py --skip-slow` for fast convention-only check
- Or run full verification suite to validate all experiments
- Check `ledger/RESEARCH_LEDGER.md` for current experiment dispositions

(End of file)
