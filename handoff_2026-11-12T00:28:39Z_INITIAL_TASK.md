# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T10:32:26Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden Artifacts**: `experiments/*.json` (canonical baseline, pinned by SHA-256 in `ledger/golden_baseline.json`)

## Verification Commands

```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
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

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores them after; interrupted runs are recoverable via `run_all_verification.py --restore-only` or `git checkout -- experiments/`
2. **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
3. **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage enforced by `scripts/check_data_coverage.py`
4. **Convention**: Close-to-close primary (v1.2.3); overnight decomposition reported alongside
5. **Golden baseline integrity**: `scripts/check_golden_baseline.py` compares tracked artifacts against SHA-256 in `ledger/golden_baseline.json` — never re-pin as side effect of verification

## Current Open Items (from Ledger)

- **E041**: 133 numeric differences (1-ulp sensitivity of ill-conditioned QP) — do not re-pin
- **E042**: Grid artifacts drift by 29-133 differences — do not re-pin
- **Optimizer determinism**: Pinned by `tests/test_portfolio_opt.py` (validates on constraints, not solver exit status)

## Next Session Suggestions

- Run `SEED=42 bash scripts/check.sh` to verify baseline integrity before any work
- Consider running `verify-quick` if making changes to drivers or core modules
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Any new experiment must follow pre-registration protocol with falsification expectations

## Files to Know

- `AGENTS.md` — Project commands & conventions (this file's source)
- `ledger/RESEARCH_LEDGER.md` — Surviving strategies & dispositions
- `ledger/golden_baseline.json` — SHA-256 fingerprints of canonical artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data inputs
- `scripts/check.sh` — Fast convention-robustness + golden integrity check
- `run_all_verification.py` — Full verification suite with backup/restore