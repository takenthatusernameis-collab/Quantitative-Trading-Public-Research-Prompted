# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T19:38:16Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Artifacts
- **Golden files**: `experiments/*.json` (committed canonical baselines)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data cache**: `data/` (gitignored, pinned vintages in `data/vintages.json`)
- **Fundamentals**: `data/fundamentals/` (pinned for E029)

## Integrity Notes
- Verification suite overwrites `experiments/*.json` during runs and restores after — never leave a run half-finished
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Cache coverage enforced: `scripts/check_data_coverage.py` must pass

## Next Session Priorities
- [ ] Run verification suite to confirm baseline integrity
- [ ] Review any new experiment drivers or modifications
- [ ] Check ledger for pending dispositions