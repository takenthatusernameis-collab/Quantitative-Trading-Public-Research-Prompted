# Agentic Work Session Handoff

**Timestamp:** 2026-11-24T21:12:22Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

---

## Project Status

**Research Phase:** Complete (E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

## Quick Start Commands

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

## Key Conventions

- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close is v1.2.3 primary; overnight decomposition reported alongside
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages)
- **Golden Files:** `experiments/*.json` are canonical artifacts — verification overwrites and restores them
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

## Verification Suite Notes

- `verify-quick` re-executes 8 drivers in 5a block (E012, E023, E024 --merge, E027, E035, E037, E039, E042-lead)
- `verify-extended` adds 18 more committed drivers with structural match (numeric_tol=1e-4)
- All 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (offline-reproducible)
- E030 16-ETF panel committed (reproducible since 2026-10-20)
- E041/E042 optimizer determinism fixed via E050 exact active-set enumeration (bit-reproducible)

## Important Guardrails

1. **Never leave verification half-finished** — baseline in `.verify_snapshot/` with `ACTIVE.json` marker
2. **Run `scripts/check.sh` before committing** — catches golden mismatches and stale snapshots
3. **Do not re-pin goldens to silence tolerance violations** — only re-pin for deliberate code changes (recorded in ledger)
4. **Cache coverage enforced** — `scripts/check_data_coverage.py` validates all download call sites
5. **CI gate cannot be created by agents** — maintainer must create via GitHub UI

## Next Steps / Open Items

- [ ] Review `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation
- [ ] Consider running `make verify` for convention robustness check
- [ ] Any new experiments should follow pre-registration protocol with falsification expectations

---

*This handoff was created automatically at session end. Update as needed for next session.*