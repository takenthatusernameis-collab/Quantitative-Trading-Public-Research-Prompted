# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T10:31:13Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project Status
- **Research Phase:** Complete (E001–E043)
- **Surviving Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite:** Available via `run_all_verification.py` (quick/extended/full modes)

## Quick Commands
```bash
# Convention robustness check (seconds, offline)
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

# Restore golden artifacts after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Conventions
- **Seed:** Always use `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Golden Files:** `experiments/*.json` are canonical artifacts — never commit verification output
- **Data:** Cached parquet in `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages)
- **Cache Coverage:** Enforced invariant — `scripts/check_data_coverage.py` validates all downloads

## Critical Notes
1. **Verification runs must never be left half-finished** — they overwrite `experiments/*.json` and restore after. Use `--restore-only` if interrupted.
2. **Do not re-pin golden baselines** to silence drift — see ledger open items (E041/E042 ill-conditioned QP).
3. **CI workflow cannot be created by agents** — maintainer must create via GitHub UI from template at `.github/workflow-templates/verification-gate.yml`.

## Next Session Suggestions
- Run `make check` to validate conventions and golden baseline integrity
- Run `make verify-quick` for fast reproducibility check
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Check `scripts/check_golden_baseline.py` if any experiment artifacts need re-pinning (requires explicit `--update` flag)