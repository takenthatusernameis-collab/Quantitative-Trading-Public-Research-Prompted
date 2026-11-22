# Agentic Work Session Handoff

**Timestamp**: 2026-11-22T17:44:03Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Files & Structure

- **Experiments**: `experiments/*.json` - Canonical research artifacts (golden baselines)
- **Drivers**: `experiments/run_e*.py` - Individual experiment drivers
- **Core Library**: `src/` - Shared research infrastructure
- **Verification**: `run_all_verification.py`, `scripts/check.sh`, `verify_convention_robustness.py`
- **Ledger**: `ledger/RESEARCH_LEDGER.md` - Experiment outcomes and dispositions
- **Data**: `data/` - Cached parquet (gitignored except pinned vintages)

## Quick Commands

```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Integrity Notes

1. **Golden artifacts**: `experiments/*.json` are backed up to `.verify_snapshot/` during verification and restored after. Never leave a verification run half-finished.
2. **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline pinning**: `ledger/golden_baseline.json` contains SHA-256 fingerprints. Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update`
4. **Data coverage**: `scripts/check_data_coverage.py` enforces all cache files exist and match pinned SHA-256 in `ledger/data_baseline.json`
5. **Offline mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1` - missing cache entries fail hard

## Current State

- Research phase complete (E001–E043)
- Verification suite operational
- Golden baselines committed and pinned
- Data vintages pinned (2026-10-11, 2026-10-12)
- E029 fundamentals snapshot pinned for offline reproducibility
- E030 ETF panel committed for offline reproducibility

## Next Session Guidance

Start with `SEED=42 bash scripts/check.sh` to verify environment integrity before any experimental work. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items.
