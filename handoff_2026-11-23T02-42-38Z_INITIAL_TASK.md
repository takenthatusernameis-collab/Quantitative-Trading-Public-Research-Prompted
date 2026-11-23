# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T03:35:46Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Workspace Root**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Notes for Next Session
- Baseline integrity: `experiments/*.json` are canonical artifacts. Verification suite backs up and restores them.
- Reproducibility: Always use `SEED=42`. Data cached in `data/` (gitignored except pinned vintages).
- Convention: Close-to-close is v1.2.3 primary. Overnight decomposition reported alongside.
- No separate linter; use `python3 -m py_compile` on changed files.
- CI gate template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI).

## Current State
No active tasks. Ready for next research/verification work.