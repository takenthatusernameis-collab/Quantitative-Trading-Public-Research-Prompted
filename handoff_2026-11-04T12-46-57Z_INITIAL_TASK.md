# INITIAL TASK HANDOFF — 2026-11-04T12:46:12Z

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted (research phase complete E001–E043; surviving validated strategies in ledger/RESEARCH_LEDGER.md)
- Working tree clean at checkpoint commits (last: 7be6bb0 chore(kilo): checkpoint agent session)
- Golden baselines enforced (ledger/golden_baseline.json) — do not re-pin as side effect of verification
- Data coverage enforced (ledger/data_baseline.json); offline verification uses QUANT_RESEARCH_OFFLINE=1
- Optimizer determinism fixed (E049) but some artifacts still show small numerical drift (tolerance 1e-4)

## Immediate Priorities
1. **Verify repo integrity** before new work
   - `SEED=42 python3 scripts/check_golden_baseline.py` (must pass)
   - `SEED=42 python3 scripts/check_data_coverage.py` (must pass)
   - `SEED=42 python3 scripts/check_goldens_clean.py` (no stale snapshot / no working tree drift vs HEAD)

2. **Quick verification** to confirm baseline
   - `SEED=42 python3 run_all_verification.py` (or `make verify-quick`) — ~8 min
   - If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`

## Open Issues / Watchlist
- **E041 numerical drift** (133 numeric diffs, 1-ulp QP sensitivity) — do NOT re-pin; documented in ledger E049
- **E042/E041 grid artifacts** may show bounded numeric drift due to ill-conditioned tangency QP
- **Extended verification** reports drift for some drivers (E030 now fixed/pinned, E029 pinned) — see `AGENTS.md` reproducibility section
- **CI workflow** cannot be created by agents (controller restores .github/workflows/); template at `.github/workflow-templates/verification-gate.yml`

## Suggested Starting Point
- Read `AGENTS.md` for full commands/conventions
- Read `ledger/RESEARCH_LEDGER.md` for strategy status and promotion gates
- Check `.verify_snapshot/` for stale ACTIVE.json (should be absent if clean)
- If starting new research: follow pre-registration rules, falsification expectations, multiple-testing discipline

## Notes
- Always use `SEED=42`
- Never commit verification outputs as golden replacements without updating ledger pins via the check scripts
- Close-to-close is primary convention (v1.2.3); overnight decomposition reported
