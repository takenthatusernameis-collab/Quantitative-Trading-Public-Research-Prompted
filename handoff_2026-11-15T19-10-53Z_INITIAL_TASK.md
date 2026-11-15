# Handoff — 2026-11-15T19:10:53Z — Initial Task for Next Agentic Session

## Project Context
**Quantitative Trading Public Research** — Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Current State (as of this handoff)
- **Last verification**: `SEED=42 python3 run_all_verification.py` completed successfully
- **Golden artifacts**: All `experiments/*.json` are canonical baselines, restored and matching `ledger/golden_baseline.json` SHA-256 fingerprints
- **Data coverage**: Enforced invariant — all `data.download()` call sites resolve to committed, SHA-256-pinned parquet caches (`ledger/data_baseline.json`)
- **E029 fundamentals**: Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` — fully offline-reproducible
- **E030 panel**: 16-ETF input committed — offline-reproducible since 2026-10-20 (ledger E048)
- **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints (not solver exit status). Tangency QP remains ill-conditioned; 1-ulp drift expected in E041/E042 grid artifacts — **do not re-pin to silence** (ledger E049 open item)

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

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
#   or
make verify

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Guards (run before committing)
1. `scripts/check.sh` — fails if tracked artifacts under `experiments/` differ from HEAD or stale snapshot pending
2. `scripts/check_golden_baseline.py` — compares every tracked artifact with SHA-256 in `ledger/golden_baseline.json`
3. `scripts/check_data_coverage.py` — enforces cache coverage invariant
4. `tests/test_portfolio_opt.py` — pins optimizer determinism rule (constraint validation, not exit status)

## Open Items / Next Steps
- **E041 drift**: 133 numeric differences (1-ulp QP sensitivity) remain after optimizer fix — decision REJECTED 3/5 unchanged. Do not re-pin. See ledger E049.
- **E042 lead**: PARTIAL (3/5 gates). Min-var confirmatory run with n_sim=50 passes convention robustness but tangency grid drifts.
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` — maintainer must create via GitHub UI (automated agents cannot push workflows).
- **Promotion gates**: Any config clearing sensitivity grid requires dedicated pre-registered confirmatory run with full placebo before promotion.

## Quick Start for Next Agent
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Run `SEED=42 python3 run_all_verification.py` for quick verification
3. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
4. All experiments are pre-registered — never move goalposts post-hoc

---
*Generated at 2026-11-15T19:10:53Z for durable handoff to next agentic work session*