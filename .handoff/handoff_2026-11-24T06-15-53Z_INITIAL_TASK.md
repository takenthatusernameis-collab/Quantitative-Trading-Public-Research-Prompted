# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T06-15-53Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments (E001–E043) are pre-registered with falsification expectations and promotion gates. Research phase is complete.

**Key surviving validated strategies** are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Important Integrity Notes

- **Never leave a verification run half-finished** — it overwrites `experiments/*.json` (canonical artifacts) and restores them after. Use `--restore-only` if interrupted.
- **Golden baseline protection**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`. Never re-pin as a side effect of verification.
- **Cache coverage is enforced**: `scripts/check_data_coverage.py` requires all data inputs to be pinned. Unpinned inputs fail hard under `QUANT_RESEARCH_OFFLINE=1`.
- **Optimizer determinism**: Tangency QP uses exact KKT active-set enumeration (E050 fix, commit `72dc947`) for bit-reproducibility across environments.

## Current State

- Research phase complete (E001–E043)
- All experiment drivers committed
- Golden artifacts in `experiments/` are the canonical baseline
- Verification suite is the primary CI gate (local equivalents: `make check`, `make verify`, `make verify-full`)

## Next Session Suggestions

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Run `SEED=42 python3 run_all_verification.py --skip-slow` for quick convention check
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation
4. Check `.verify_reports/` for any extended drift reports from prior runs

---

*This handoff was created automatically at session start. Update as needed for the next session.*