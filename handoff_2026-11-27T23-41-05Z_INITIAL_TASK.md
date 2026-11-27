# Handoff: Next Agentic Work Session

**Timestamp:** 2026-11-27T23:41:05Z
**Session Type:** Initial Task Handoff
**Project:** Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Current Verification Baseline:** Committed golden artifacts in `experiments/*.json`

---

## Quick Start Commands (SEED=42)

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
```

---

## Critical Baseline Integrity Notes

**⚠️ NEVER leave a verification run half-finished.** The suite overwrites `experiments/*.json` during execution and restores them afterward. If interrupted:

- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker (pid-tracked)
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- `scripts/check_goldens_clean.py` (in `scripts/check.sh`) detects working-tree vs HEAD mismatches
- `scripts/check_golden_baseline.py` compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json` — **never re-pin as side effect of verification**

**Key pins:**
- Data vintage: 2026-10-12 (pinned in `data/vintages.json`); 2026-10-11 also committed for E026/E028/E029/E030/E034/E036/E037
- E029 fundamentals: pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Cache coverage enforced: `scripts/check_data_coverage.py` requires every `data.download()` call site to have committed, SHA-256-pinned cache file

---

## Reproducibility Status (measured 2026-11-23T05:17Z, numpy 2.5.4, scipy 1.18.1)

| Block | Drivers | Status |
|-------|---------|--------|
| Quick (5a) | E012, E023, E024--merge, E027, E035, E037, E039, E042-lead | ✅ 0 diffs |
| Extended | E011, E013, E015, E016, E017, E018, E019, E020, E021, E022, E025, E026, E028, E029, E030, E034, E036, E041 | ✅ 0 diffs (all 18) |
| E042 min-var grid | 96 configs | ✅ bit-reproducible |

**Resolved drift history:**
- E029: offline-reproducible since 2026-10-20 (fundamentals pinned)
- E030: 0 diffs since 2026-10-20 (16-ETF panel committed)
- E041/E042: ill-conditioned QP drift closed by E050 fix (exact KKT active-set enumeration, commit `72dc947`) — now bit-reproducible
- **Do NOT re-pin E041/E042** — no tolerance violation remains; re-pin only for deliberate code changes recorded in ledger

---

## Optimizer Determinism (ledger E049/E050)

- `src/portfolio_opt.py` validates solver answer on **problem constraints**, never solver exit status
- SLSQP status 8 ("Positive directional derivative for linesearch") can occur at constrained optimum — gating on it made tangency portfolio environment-dependent
- Rule pinned by `tests/test_portfolio_opt.py` (first-class step in `scripts/check.sh`)
- E050 exact active-set enumeration: no iteration, no build-dependent branch → bit-reproducible across environments

---

## Next Session Suggested Actions

1. **Run `make check`** to verify baseline integrity before any work
2. **If continuing research:** Design new pre-registered experiment (E044+) with falsification expectations
3. **If promoting a strategy:** Follow ledger promotion gates — dedicated confirmatory run + full placebo required
4. **If modifying code:** Run `make verify-quick` after changes; extended/full for structural changes
5. **If adding data inputs:** Commit cache file + re-pin with `python3 scripts/check_data_coverage.py --update`

---

## Key Files to Reference

- `ledger/RESEARCH_LEDGER.md` — surviving strategies, dispositions, drift resolutions
- `ledger/golden_baseline.json` — SHA-256 pins for all `experiments/*.json`
- `ledger/data_baseline.json` — SHA-256 pins for all committed data cache files
- `data/vintages.json` — primary data vintage pin (2026-10-12)
- `data/fundamentals_vintages.json` — E029 fundamentals pin
- `scripts/check.sh` — canonical baseline integrity check (run before committing)
- `AGENTS.md` — this project's commands & conventions

---

**End of Handoff** — Next session should start with `make check` to verify working tree matches committed baseline.