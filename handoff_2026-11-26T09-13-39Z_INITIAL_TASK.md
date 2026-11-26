# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T09:13:39Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

---

## Quick Reference Commands

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

---

## Key Files to Review

- `AGENTS.md` - Project commands, conventions, and verification procedures
- `ledger/RESEARCH_LEDGER.md` - Documented surviving validated strategies
- `experiments/*.json` - Canonical research artifacts (golden files)
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Main verification suite

---

## Critical Integrity Notes

1. **Golden files**: `experiments/*.json` are committed artifacts. The verification suite backs them up before re-running and restores them afterward.
2. **Never commit verification output**: If a run is interrupted, restore with `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline integrity**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`
4. **Data coverage**: `scripts/check_data_coverage.py` enforces cache coverage - every `data.download()` call site must have a pinned cache file

---

## Next Session Suggested Starting Points

- Run `SEED=42 bash scripts/check.sh` to verify current state
- Review `ledger/RESEARCH_LEDGER.md` for latest strategy dispositions
- Check if any experiments need re-running or if new experiments are planned
- Verify CI workflow template at `.github/workflow-templates/verification-gate.yml`

---

*This handoff was created automatically at session initialization.*