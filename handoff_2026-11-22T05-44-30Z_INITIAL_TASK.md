# Agent Handoff — 2026-11-22T05:44:50Z

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git Status**: Clean (verify with `git status`)

## Key Artifacts
- **Golden baseline**: `experiments/*.json` (canonical, pinned in `ledger/golden_baseline.json`)
- **Data cache**: `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12)
- **Fundamentals**: `data/fundamentals/` pinned per `data/fundamentals_vintages.json`
- **Verification snapshot**: `.verify_snapshot/` (gitignored, `ACTIVE.json` tracks live run)

## Quick Commands
```bash
# Convention robustness only (~seconds)
SEED=42 make check
# or
SEED=42 python3 verify_convention_robustness.py

# Quick verification (~8 min, 8 drivers)
SEED=42 make verify-quick
# or
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min, 26 drivers + drift report)
SEED=42 make verify-extended
# or
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 make verify-full
# or
SEED=42 python3 run_all_verification.py --full

# Recovery if interrupted
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

## Integrity Guards (run before committing)
- `scripts/check.sh` → `make check` (convention + golden diff + baseline SHA-256 + optimizer test)
- Never commit verification output; golden files must match `ledger/golden_baseline.json`
- If `check_goldens_clean.py` or `check_golden_baseline.py` fails, fix before commit

## Open Items (from ledger)
- **E041/E042 grid artifacts**: 29–133 numeric diffs from ill-conditioned tangency QP (1-ulp sensitivity). Do not re-pin.
- **E049**: Optimizer determinism fixed (validate on constraints, not solver status); residual drift remains.
- **E048**: Cache coverage enforced — all `data.download()` calls must have pinned SHA-256 in `ledger/data_baseline.json`.

## Next Session Suggestions
1. Run `SEED=42 make check` to verify baseline integrity
2. If clean, choose verification tier (`verify-quick` / `verify-extended` / `verify-full`)
3. Review any drift in `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored)
4. Update ledger if new experiments or dispositions are needed

---
*Generated automatically at session start. Update this file before ending work.*