# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T13:51:54Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
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

## Key Artifacts

- **Golden files**: `experiments/*.json` - canonical research artifacts (never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` - surviving validated strategies
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Baseline integrity**: `ledger/golden_baseline.json` - SHA-256 fingerprints

## Critical Notes

1. **Never leave verification half-finished** - it overwrites golden files and restores them after. If interrupted, run `--restore-only` to recover.
2. **Golden baseline is authoritative** - do not re-pin artifacts to silence drift (see AGENTS.md for E041/E042 open items).
3. **Offline reproducibility** - E029 and E030 are now fully offline-reproducible with pinned data.
4. **SEED=42** - Always use this for walk-forward + placebo RNG.

## Next Session Guidance

Check `ledger/RESEARCH_LEDGER.md` for current status of experiments. The research phase is complete; focus areas could include:
- Production deployment of validated strategies
- Extended sensitivity analysis
- New pre-registered experiments (E044+)
- Documentation and reporting