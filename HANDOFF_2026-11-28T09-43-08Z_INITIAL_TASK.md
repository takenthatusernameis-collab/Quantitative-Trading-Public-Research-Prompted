# Agent Handoff — 2026-11-28T10:37:07Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git Status**: Clean repo, verification suite available

## Key Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min + 50 sims)
SEED=42 python3 run_all_verification.py --full
# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```

## Critical Integrity Notes
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification backs up → re-runs → restores.
- **Never leave verification half-finished** — use `--restore-only` to recover if interrupted.
- **Baseline pinned in** `ledger/golden_baseline.json` (SHA-256). Re-pinning requires ledger entry first.
- **Data cache**: Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`. Coverage enforced by `scripts/check_data_coverage.py`.
- **Optimizer determinacy**: Exact active-set enumeration (E050 fix) makes E041/E042 bit-reproducible. Do not re-pin to silence tolerance.

## Current State
- All 8 quick drivers + 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)
- E029/E030 fundamentals/ETF panels pinned for offline reproducibility
- No pending tasks or blockers

## Next Session Guidance
Run `SEED=42 bash scripts/check.sh` first to verify integrity. Then proceed with any planned experiments or verification runs per AGENTS.md.