# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T02:01:38Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State
- **Research phase**: Complete (E001–E043)
- **Validated strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts**: `experiments/*.json` (canonical baseline, pinned by `ledger/golden_baseline.json`)
- **Data cache**: Pinned vintages in `data/` (2026-10-12, 2026-10-11) and `data/fundamentals/`

## Quick Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full

# Restore golden artifacts if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Invariants
- **Never leave verification half-finished** — snapshots in `.verify_snapshot/` with `ACTIVE.json` marker
- **Never commit verification output** — restores goldens automatically; interrupted runs need `--restore-only`
- **Cache coverage enforced** — `scripts/check_data_coverage.py` validates all download sites against `ledger/data_baseline.json`
- **Optimizer determinism** — `src/portfolio_opt.py` validates on constraints, not solver status (ledger E049/E050)

## Recent Context
- E041/E042 ill-conditioned QP drift resolved by E050 exact KKT active-set enumeration (commit `72dc947`)
- E029/E030 offline-reproducible since 2026-10-20 (pinned fundamentals + ETF panel)
- All 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)

## Next Steps (if any)
- No pending tasks — research phase complete
- Ledger entries E001–E050 document all experiments and dispositions
- CI gate template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI)