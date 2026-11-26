# Agentic Work Session Handoff

**Timestamp:** 2026-11-26T02:22:55Z
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status

**Research Phase:** COMPLETE (E001–E043 executed)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Current Baseline:** Golden artifacts in `experiments/*.json` (canonical, committed)

---

## Key Commands for Next Session

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
```

---

## Critical Integrity Notes (Read Before Running)

1. **Golden artifacts** in `experiments/*.json` are the canonical baseline
2. **Verification overwrites then restores** - never leave a run half-finished
3. **Backup location:** `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker
4. **Recovery if interrupted:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
5. **Never commit verification output** - it replaces canonical baselines silently
6. **Baseline integrity check:** `scripts/check_golden_baseline.py` compares against SHA-256 in `ledger/golden_baseline.json`

---

## Reproducibility Requirements

- **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
- **Data cache:** Parquet in `data/` (pinned vintages 2026-10-11, 2026-10-12)
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Offline mode:** Verification runs with `QUANT_RESEARCH_OFFLINE=1`
- **Cache coverage enforced:** `scripts/check_data_coverage.py` validates all download call sites

---

## Optimizer Determinism (Ledger E049/E050)

- **Primary tangency solver:** Exact KKT active-set enumeration (bit-reproducible)
- **Validation rule:** Check against problem constraints, NOT solver exit status (SLSQP status 8 is build-dependent)
- **Test guard:** `tests/test_portfolio_opt.py` (step in `scripts/check.sh`)
- **Do NOT re-pin E041/E042** to silence tolerance violations - no remaining violations exist

---

## Next Session Suggested Starting Points

1. Run `make check` to verify baseline integrity before any work
2. Run `make verify-quick` to confirm reproducibility of core experiments
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and dispositions
4. Check `scripts/check_golden_baseline.py` output if any experiment artifacts appear modified

---

## Open/Closed Items

- ✅ Research phase complete (E001–E043)
- ✅ E042 min-var confirmatory: PARTIAL (ledger E042)
- ✅ E041 market-neutral portfolio: REJECTED (3/5 gates)
- ✅ E025 cointegration stat-arb: REJECTED
- ✅ Optimizer determinism fixed via E050 exact active-set enumeration
- ✅ E029 offline-reproducible (fundamentals pinned 2026-10-20)
- ✅ E030 offline-reproducible (16-ETF panel committed 2026-10-20)
- ✅ Cache coverage invariant enforced (ledger E048)
- ⏳ CI gate workflow template at `.github/workflow-templates/verification-gate.yml` (requires manual creation)

---

*This handoff is durable across sessions. Update before ending work.*