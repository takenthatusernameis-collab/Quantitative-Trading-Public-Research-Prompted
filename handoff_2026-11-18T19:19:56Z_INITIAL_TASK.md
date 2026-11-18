# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T19:20:23Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Session Type**: Quantitative Trading Research Repository

## Project Context

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Key Verification Commands

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

## Critical Notes for Next Session

1. **Golden artifacts**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them during re-run and restores them afterwards. **Never leave a verification run half-finished.**

2. **Baseline integrity**:
   - Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker
   - `scripts/check_goldens_clean.py` compares working tree with HEAD
   - `scripts/check_golden_baseline.py` compares with SHA-256 in `ledger/golden_baseline.json`
   - Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`

3. **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention. Data cached in `data/` (gitignored except pinned vintages).

4. **CI gate**: Cannot be created by automated agents. Template at `.github/workflow-templates/verification-gate.yml`.

5. **Known drift issues** (documented in ledger):
   - E041: 133 numeric differences from ill-conditioned QP (optimizer determinism, ledger E049)
   - E030: Was drifting, now 0 diffs since 2026-10-20 (ledger E048)
   - E029: Offline-reproducible since 2026-10-20 (fundamentals pinned, ledger E045)

6. **Cache coverage invariant**: `scripts/check_data_coverage.py` enforces all download call sites have pinned cache files matching `ledger/data_baseline.json`.

## Next Steps / Open Items

- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Consider running `make verify` or `make check` to validate current state
- Do not re-pin drifting artifacts (E041, E042 grid) to silence differences — see ledger open items

## File Structure Reference

```
├── experiments/           # Golden artifacts (committed JSONs)
├── ledger/               # Research ledger + golden baselines
├── src/                  # Core research code
├── scripts/              # Verification/check scripts
├── data/                 # Cached parquet (gitignored, pinned vintages committed)
├── tests/                # Unit tests (e.g., test_portfolio_opt.py)
└── .verify_snapshot/     # Backup during verification (gitignored)
```