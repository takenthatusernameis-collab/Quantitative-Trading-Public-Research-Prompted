# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T10:54:30Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes
- `experiments/*.json` are canonical research artifacts — verification overwrites and restores them
- Backup lives in `.verify_snapshot/` with `ACTIVE.json` marker (pid-tracked)
- `scripts/check_goldens_clean.py` fails on tracked artifact drift from HEAD
- `scripts/check_golden_baseline.py` compares against SHA-256 in `ledger/golden_baseline.json`
- Never re-pin to silence tolerance violations — only deliberate code changes with ledger entry
- Cache coverage enforced: `scripts/check_data_coverage.py` validates all download call sites
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- E030 16-ETF panel committed for offline reproducibility

## Optimizer Determinism (ledger E049/E050)
- `src/portfolio_opt.py` validates on problem constraints, not solver exit status
- Exact KKT active-set enumeration (E050 fix, commit `72dc947`) makes E041/E042 bit-reproducible
- SLSQP status 8 is scipy-build dependent — gating on it was the bug

## Recent State
- All 18 extended drivers reproduce with 0 differences (measured 2026-11-23T05:17Z)
- E041/E042 tangency QP ill-conditioned in principle but exact solver removes iteration/branch variance
- CI workflow template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI)
- No separate linter; use `python3 -m py_compile` on changed files

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity
2. Run `SEED=42 python3 run_all_verification.py --extended` for full structural match
3. Check `ledger/RESEARCH_LEDGER.md` for current disposition of all experiments
4. Any new experiment requires pre-registration with falsification expectations