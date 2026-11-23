# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T02:37:01Z
**Session ID**: Initial handoff created by Kilo
**Project**: Quantitative-Trading-Public-Research-Prompted

## Project Status

- **Research Phase**: Complete (E001–E043)
- **Surviving Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite**: Operational with three tiers (quick/extended/full)

## Quick Commands Reference

```bash
# Convention robustness check (~seconds, offline)
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

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical artifacts. Verification overwrites and restores them — never leave a run half-finished.
2. **Recovery**: If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline Pinning**: `ledger/golden_baseline.json` pins SHA-256 of canonical artifacts. Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update`
4. **Data Coverage**: `scripts/check_data_coverage.py` enforces all cache files exist and match pinned SHA-256 in `ledger/data_baseline.json`
5. **Offline Reproducibility**: Set `QUANT_RESEARCH_OFFLINE=1` to fail on missing cache instead of downloading

## Known Drift (Extended Verification)

- **E030**: 28 numeric diffs on near-zero quantities (reproduces with 0 diffs since 2026-10-20 after panel pinning)
- **E041**: 133 numeric diffs (1-ulp sensitivity of ill-conditioned QP), 0 structural diffs after optimizer fix (ledger E049)
- **Do NOT re-pin** E041/E042 grid artifacts to silence drift — see ledger open items

## Next Session Guidance

- Run `make check` first to validate conventions and golden baseline integrity
- Use `SEED=42` for all reproducibility
- Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
- All experiment drivers in `experiments/` have pre-registered JSON blocks with gates/falsification expectations