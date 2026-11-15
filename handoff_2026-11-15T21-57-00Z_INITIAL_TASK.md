# Handoff - Agentic Work Session

**Timestamp:** 2026-11-15T21:59:36Z
**Workspace:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or
make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes

- `experiments/*.json` are canonical research artifacts — verification overwrites and restores them
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker (pid-tracked)
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are first-class checks in `scripts/check.sh`
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Never commit verification output** — restore before committing

## Current State

- All 43 experiments (E001–E043) completed
- Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden baselines pinned in `ledger/golden_baseline.json`
- Data cache coverage enforced via `ledger/data_baseline.json`
- CI workflow template at `.github/workflow-templates/verification-gate.yml` (requires manual creation)

## Recommended Next Steps

1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for fast verification
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategy status
4. Consider extending research with new pre-registered experiments (E044+)

---

*This handoff was created automatically at session start. Update as work progresses.*