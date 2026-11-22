# Handoff — 2026-11-22T09:54:40Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Timestamp**: 2026-11-22T09:54:40Z

## Quick Start Commands
```bash
# Convention robustness check (seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min; 8 drivers + batch + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Individual drivers
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Critical Integrity Notes
- **Never leave a verification run half-finished** — it overwrites `experiments/*.json` goldens and restores them after. Use `--restore-only` to recover if interrupted.
- **Golden baseline** pinned in `ledger/golden_baseline.json` (SHA-256). Do not re-pin as side effect of verification.
- **Data cache coverage enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site against `ledger/data_baseline.json`.
- **Optimizer determinism** (ledger E049): `src/portfolio_opt.py` validates on constraints, not solver exit status. Tangency QP remains ill-conditioned; E041/E042 grid artifacts drift ~1e-5. Do not re-pin to silence.

## Key Files
- `AGENTS.md` — project commands, conventions, CI, reproducibility
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions (E001–E043, E045, E048, E049)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of canonical artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data caches
- `data/vintages.json` — 2026-10-12 vintage pinned
- `data/fundamentals_vintages.json` — E029 fundamentals snapshot pinned
- `experiments/*.json` — canonical golden artifacts (git-tracked)
- `scripts/check.sh` — fast convention-robustness + golden baseline guard
- `scripts/check_goldens_clean.py` — working tree vs HEAD check
- `scripts/check_golden_baseline.py` — working tree vs pinned SHA-256 check
- `scripts/check_data_coverage.py` — data cache coverage invariant

## Current State
- No active verification run (checked: no `.verify_snapshot/ACTIVE.json`)
- All goldens match HEAD (last `scripts/check.sh` clean)
- Research phase complete; surviving strategies documented

## Next Steps (if any)
- No pending tasks. Session ready for new work or verification run.