# Agentic Work Session Handoff

**Timestamp:** 2026-11-14T23:23:21Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status

**Research Phase:** COMPLETE (E001–E043 executed)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Canonical Artifacts:** `experiments/*.json` (committed golden baselines)

---

## Quick Reference Commands

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

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Key Integrity Rules (from AGENTS.md)

1. **Golden files** in `experiments/*.json` are canonical — verification overwrites then restores them
2. **Never leave verification half-finished** — use `--restore-only` or `git checkout -- experiments/` to recover
3. **Seed:** Always `SEED=42` for reproducibility
4. **Cache coverage enforced:** `scripts/check_data_coverage.py` validates all data inputs are pinned
5. **Optimizer determinism:** `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049)
6. **Do not re-pin drifting artifacts** to silence tolerance failures — see open items in ledger

---

## Current Baseline State

- `ledger/golden_baseline.json` — SHA-256 fingerprints of all `experiments/*.json` artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of all pinned data cache files
- `data/vintages.json` — 2026-10-12 vintage pinned
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot pinned (offline-reproducible since 2026-10-20)
- `data/fundamentals/` — Committed fundamentals for E029

---

## Known Drift (Extended Verification)

| Driver | Status | Notes |
|--------|--------|-------|
| E030 | 0 diffs (since 2026-10-20) | 16-ETF panel now committed |
| E041 | 133 numeric diffs | Ill-conditioned QP, 1-ulp sensitivity; REJECTED 3/5 unchanged |
| E029 | 0 diffs | Offline-reproducible with pinned fundamentals |
| 15/18 extended | 0 diffs | Fully reproducible |

---

## Next Session Suggestions

- Run `SEED=42 bash scripts/check.sh` to verify working tree integrity
- Run `SEED=42 python3 run_all_verification.py --extended` for full driver coverage
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Review `src/portfolio_opt.py` optimizer determinism fix (ledger E049)

---

## Git State

```bash
# Check for uncommitted changes or verification artifacts
git status

# Verify experiments/ matches HEAD
git diff experiments/

# Check golden baseline alignment
python3 scripts/check_golden_baseline.py
```

---

*End of handoff — ready for next agentic session*