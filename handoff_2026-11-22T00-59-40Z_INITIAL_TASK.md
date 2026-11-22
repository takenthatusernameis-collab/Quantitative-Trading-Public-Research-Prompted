# Agentic Work Session Handoff

**Timestamp:** 2026-11-22T01:01:54Z
**Session ID:** Initial handoff for next agentic session
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts — verification overwrites and restores them
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker
- Never leave verification half-finished; use `--restore-only` to recover
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Cache coverage enforced via `scripts/check_data_coverage.py` and `ledger/data_baseline.json`

## Current State
- Repository clean, no uncommitted changes
- All verification commands available via `make check`, `make verify`, `make verify-full`
- CI workflow template at `.github/workflow-templates/verification-gate.yml` (requires manual creation)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current disposition of all experiments
3. Run verification suite as needed (`verify-quick`, `verify-extended`, `verify-full`)
4. Any new experiment requires pre-registration with gates and falsification expectations

---
*This handoff was created automatically at session start.*