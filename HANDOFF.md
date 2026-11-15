# Agentic Work Session Handoff

**Timestamp**: 2026-11-15T14:53:58Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Current State

- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden artifacts in `experiments/*.json` are canonical baselines
- Verification suite: `run_all_verification.py` (quick/extended/full modes)

## Quick Commands

```bash
# Convention robustness check (fast, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min)
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
```

## Key Invariants

- **Seed**: Always use `SEED=42`
- **Golden files**: `experiments/*.json` — never modified by verification (backed up to `.verify_snapshot/`)
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`
- **Cache coverage**: Enforced by `scripts/check_data_coverage.py`
- **Optimizer determinicity**: Validated by `tests/test_portfolio_opt.py` (constraints-based, not solver status)

## Open Items (from Ledger)

- E041: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- E042 grid artifacts: 29-133 differences (same root cause) — do not re-pin
- See `ledger/RESEARCH_LEDGER.md` entries E045, E048, E049 for details

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current disposition of all experiments
3. Decide on next research direction (new experiment design, sensitivity analysis, promotion gates)
4. All experiments must be pre-registered with falsification expectations before execution

---

*This handoff was created automatically at session start. Update as work progresses.*