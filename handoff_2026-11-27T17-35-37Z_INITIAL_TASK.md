# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T19:35:47Z
**Session ID**: Initial handoff for next session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

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

- **Golden files**: `experiments/*.json` - canonical research artifacts (never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` - surviving validated strategies
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Verification**: Uses `.verify_snapshot/` for backup/restore (gitignored)

## Important Conventions

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention**: Close-to-close is the v1.2.3 primary convention
- **Pre-registration**: Every experiment driver has a `pre_registered` JSON block
- **Negative results**: Recorded honestly (REJECTED / PARTIAL) with evidence
- **Do not commit verification output**: Restore with `run_all_verification.py --restore-only` if interrupted

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification suite as needed (`verify-quick`, `verify-extended`, or `verify-full`)
4. Any new experiments must follow pre-registration protocol

---

*This handoff was created automatically at session start. Update as work progresses.*