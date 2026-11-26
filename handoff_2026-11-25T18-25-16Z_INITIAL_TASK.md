# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T03:26:32Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates.

**Research Phase**: Complete (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`

---

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

---

## Critical Baseline Integrity Notes

1. **`experiments/*.json`** are canonical research artifacts
2. Verification suite overwrites them during re-runs and restores afterward
3. **Never leave a verification run half-finished** - it corrupts the baseline
4. Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker (pid-tracked)
5. Recovery: `SEED=42 python3 run_all_verification.py --restore-only`

---

## Reproducibility Requirements

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
- **Cache coverage**: Enforced invariant via `scripts/check_data_coverage.py`
- **Dependencies**: `pip install -r requirements.txt`

---

## Project Conventions

- **Pre-registration**: Every driver has `pre_registered` JSON block + docstring
- **Multiple-testing discipline**: Sensitivity grids "reported, not gated"
- **Negative results**: Recorded honestly (REJECTED / PARTIAL) with evidence
- **Golden files**: `experiments/*.json` are committed artifacts
- **Do not commit verification output** - restore before committing

---

## CI / Automation

- CI gate template at `.github/workflow-templates/verification-gate.yml`
- Controller restores `.github/workflows/` at checkpoints
- Maintainer must create actual workflow via GitHub UI
- Local equivalents: `make check`, `make verify`, `make verify-full`

---

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current research status
3. Review any open issues or planned experiments
4. Consider running `verify-quick` if baseline verification needed

---

## Files to Reference

- `AGENTS.md` - Full project commands & conventions
- `ledger/RESEARCH_LEDGER.md` - Validated strategies documentation
- `ledger/golden_baseline.json` - SHA-256 fingerprints of golden artifacts
- `ledger/data_baseline.json` - SHA-256 fingerprints of data cache
- `scripts/check.sh` - Fast convention-robustness check
- `run_all_verification.py` - Main verification suite