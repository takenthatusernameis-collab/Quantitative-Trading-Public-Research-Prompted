# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T01:23:41Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** Complete (E001–E043)
**Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`

## Current State

- **Verification Suite:** Ready to run (`make check`, `make verify-quick`, `make verify-extended`, `make verify-full`)
- **Golden Artifacts:** Committed in `experiments/*.json` (canonical baseline)
- **Data Cache:** Pinned vintages in `data/` (2026-10-12, 2026-10-11) and `data/fundamentals/`
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)

## Quick Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Rules (from AGENTS.md)

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. A killed run stays recoverable via `.verify_snapshot/`.
2. **Run `scripts/check.sh` before committing** — it validates goldens against HEAD and `ledger/golden_baseline.json`.
3. **Do not re-pin goldens to silence tolerance violations** — only re-pin after a deliberate code change recorded in the ledger (E050 precedent).
4. **Cache coverage is invariant** — `scripts/check_data_coverage.py` enforces every download call site has a committed, SHA-256-pinned cache file.
5. **Optimizer determinism** — `src/portfolio_opt.py` validates on problem constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`).

## Next Steps / Open Items

- [ ] Run verification suite to confirm reproducibility
- [ ] Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
- [ ] Consider next research phase or production hardening of validated strategies
- [ ] CI workflow template available at `.github/workflow-templates/verification-gate.yml` (requires manual GitHub UI creation)

## Notes for Next Session

- Seed is always `SEED=42` for reproducibility
- Close-to-close is v1.2.3 primary convention; overnight decomposition reported alongside
- Negative results (REJECTED/PARTIAL) are recorded honestly with evidence
- `run_all_verification.py` backs up goldens before re-running and restores after — baseline never modified by verification

---
*Generated automatically at session start. Update this file before ending your session.*