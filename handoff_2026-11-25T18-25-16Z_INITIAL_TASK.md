# Handoff — 2026-11-26T05:09:06Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min + E042 n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Critical Integrity Notes
- **Never leave a verification run half-finished** — it overwrites `experiments/*.json` and restores after
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- Golden baseline pinned in `ledger/golden_baseline.json` — do not re-pin without ledger entry
- Cache coverage enforced: `scripts/check_data_coverage.py` validates all `data.download()` call sites

## Recent Key Fixes (Ledger)
- **E050** (2026-11-01): Exact KKT active-set enumeration for tangency portfolio → bit-reproducible E041/E042
- **E048** (2026-10-20): E029/E030 data pinned for offline reproducibility
- **E049**: Optimizer determinism — validate on constraints, not solver exit status

## Verification Status (2026-11-23T05:17Z)
- 18 extended drivers: **0 differences** (numeric_tol=1e-4)
- E041: 0 diffs after E050 fix (was 354 → 133 → 0)
- E029/E030: 0 diffs with pinned data

## Next Session Suggestions
1. Run `make check` to verify baseline integrity
2. Run `make verify-quick` for fast regression test
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Consider promoting any PARTIAL→CONFIRMED with dedicated pre-registered run