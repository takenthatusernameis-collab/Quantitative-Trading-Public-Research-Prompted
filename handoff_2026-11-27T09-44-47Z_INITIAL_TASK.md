# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-27T15:30:20Z
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase:** Research complete (E001–E043) — surviving strategies in `ledger/RESEARCH_LEDGER.md`

## Current State

- All 43 experiments pre-registered with falsification expectations
- Verification suite operational: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`
- Golden artifacts in `experiments/*.json` are canonical baselines
- Data cache pinned at 2026-10-12 vintage (`data/vintages.json`); E026/E028/E029/E030/E034/E036/E037 also use 2026-10-11
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E050 exact KKT active-set solver landed (commit `72dc947`) — E041/E042 now bit-reproducible (0 differences)

## Key Commands

```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min; 8 drivers + batch + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended (~21 min; +18 drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full (~15 min; E042 n_sim=50 + 96-config sensitivity)
SEED=42 python3 run_all_verification.py --full
```

## Critical Guards (run before committing)

1. `scripts/check_goldens_clean.py` — working tree vs HEAD
2. `scripts/check_golden_baseline.py` — tracked artifacts vs `ledger/golden_baseline.json` SHA-256
3. `scripts/check_data_coverage.py` — every `data.download()` call resolves to committed, SHA-pinned cache
4. `tests/test_portfolio_opt.py` — optimizer validates on constraints, not solver exit status

## Open Items / Next Steps

- [ ] No active experiment drivers pending — research phase complete
- [ ] If promoting a strategy: pre-register confirmatory run with full placebo before promotion
- [ ] CI gate workflow (`.github/workflows/verification-gate.yml`) must be created manually via GitHub UI (template at `.github/workflow-templates/verification-gate.yml`)
- [ ] Any deliberate code change altering published numbers requires ledger entry + re-pin (`check_golden_baseline.py --update`)

## Recovery Notes

If verification interrupted:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

Stale snapshot marker: `.verify_snapshot/ACTIVE.json` (pid-owned). Suite self-recovers at startup.

---

*This handoff is durable — commit it if you want it persisted across sessions.*