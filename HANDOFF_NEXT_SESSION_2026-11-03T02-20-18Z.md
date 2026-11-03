# HANDOFF - Next Agentic Session
Timestamp: 2026-11-03T02-20-18Z
Repository: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 752acf2 "chore(kilo): checkpoint agent session"
Working tree: 1 changes

## Research State
- Phase: COMPLETE (E001-E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Golden artifacts: `experiments/*.json` are committed and authoritative (pinned in `ledger/golden_baseline.json`)
- Data coverage: Enforced via `scripts/check_data_coverage.py` against `ledger/data_baseline.json`
- Baseline guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` active

## Known Issues
- Optimizer determinism (E049): 1-ULP sensitivity in ill-conditioned QP causes numeric drift in E041/E042 beyond 1e-4 tolerance. Do NOT re-pin to silence - decision unchanged.
- E029, E030 reproduce with 0 differences (pinned data). E041 drifts numerically but structural diffs resolved.

## Immediate Actions
1. Run `SEED=42 bash scripts/check.sh` - verify all guards pass. Fix any failures before committing.
2. If verification left artifacts modified, recover: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. Review `ledger/RESEARCH_LEDGER.md` and `AGENTS.md` before making changes.
4. Always use `SEED=42`. Never overwrite `experiments/*.json` without explicit re-pinning per AGENTS.md.

## Verification Commands
- Quick check: `make check` or `SEED=42 bash scripts/check.sh`
- Quick verify: `make verify-quick` (~8 min)
- Extended: `make verify-extended` (~21 min)
- Full: `make verify-full` (~15 min)

## Key Constraints
- Pre-registration discipline - no goalpost moving post-hoc
- Sensitivity grids reported, not gated (dedicated confirmatory run needed for promotion)
- Negative results recorded honestly (REJECTED/PARTIAL)
- Never commit verification output
- CI gate template only - cannot be created by agents
