# Handoff — Agentic Work Session

**Timestamp:** 2026-11-26T16:05:59Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

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

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes

- **Golden files:** `experiments/*.json` are canonical artifacts. Verification overwrites and restores them — never leave a run half-finished.
- **Snapshot recovery:** `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker. Use `--restore-only` or `git checkout -- experiments/` to recover.
- **Baseline pinning:** `ledger/golden_baseline.json` holds SHA-256 fingerprints. Never re-pin as side effect of verification — only deliberate code changes recorded in ledger.
- **Data coverage:** `scripts/check_data_coverage.py` enforces cache invariants. All downloads pinned in `ledger/data_baseline.json`.
- **Optimizer determinism:** E050 fix (exact KKT active-set enumeration) made E041/E042 bit-reproducible. Do not re-pin to silence tolerance — no violation remains.

## Recent Verification State (2026-11-23T05:17Z)

- **verify-extended:** All 18 extended drivers reproduce with 0 differences (numeric_tol=1e-4)
- **E029:** Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`)
- **E030:** Reproduces with 0 differences since 2026-10-20 (16-ETF panel committed)
- **E041/E042:** 0 differences post-E050 exact-solver fix (commit `72dc947`)

## Next Session Suggestions

1. Run `make check` to verify working tree integrity
2. Run `make verify-quick` for fast regression check
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation
4. Check `scripts/check_golden_baseline.py` if any golden drift suspected

---

*This handoff was created automatically at session start. Update as work progresses.*