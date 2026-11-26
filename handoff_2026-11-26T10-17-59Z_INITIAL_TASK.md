# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T10:21:43Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Workspace Root**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed artifacts, never modified by verification)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data cache**: `data/` (gitignored except pinned vintages)
- **Verification reports**: `.verify_reports/` (gitignored)

## Baseline Integrity Rules
- Verification suite backs up goldens to `.verify_snapshot/` before re-running, restores after
- Never leave a verification run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 in `ledger/golden_baseline.json`
- Never re-pin to silence tolerance violations — only for deliberate code changes recorded in ledger

## Reproducibility
- Seed: Always `SEED=42` (walk-forward + placebo RNG)
- Convention: Close-to-close primary (v1.2.3), overnight decomposition reported alongside
- Data: Pinned 2026-10-12 vintage in `data/vintages.json`, 2026-10-11 vintage committed
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Cache coverage enforced via `scripts/check_data_coverage.py`

## Next Session Starting Point
No active task. Ready for new research, verification runs, or maintenance work.