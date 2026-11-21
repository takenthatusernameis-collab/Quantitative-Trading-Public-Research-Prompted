# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T05:04:17Z
**Session**: Initial handoff for next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status Summary

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Verification Suite**: Ready for execution via `make verify-quick`, `make verify-extended`, `make verify-full`
- **Baseline Integrity**: Golden artifacts in `experiments/*.json` are canonical; verification overwrites and restores them

## Key Commands for Next Session

```bash
# Fast convention check (offline, seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, n_sim=50)
SEED=42 python3 run_all_verification.py --full
```

## Critical Conventions to Maintain

1. **Never leave verification half-finished** — golden artifacts in `experiments/` are overwritten during verification and restored after; interrupted runs leave driver output instead of goldens
2. **Seed always 42** — walk-forward + placebo RNG
3. **Cache coverage invariant** — all data inputs must be pinned in `ledger/data_baseline.json` and committed; unpinned inputs cause live downloads (yfinance not bit-reproducible)
4. **Golden baseline pinned in `ledger/golden_baseline.json`** — do not re-pin as side effect of verification
5. **Convention**: Close-to-close primary (v1.2.3), overnight decomposition reported alongside

## Recovery Procedures

If verification was interrupted:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

If golden mismatch reported by `scripts/check.sh`:
- Fix before committing
- If HEAD already captured a run, restore pinned artifact: `git checkout <commit> -- experiments/<file>` where `<commit>` SHA-256 matches `ledger/golden_baseline.json`

## Open Items / Known Drift (per ledger)

- **E041**: 133 numeric differences (1-ulp QP ill-conditioning), 3 structural diffs resolved — do not re-pin
- **E042/E041 grid artifacts**: 29-133 differences from tangency QP ill-conditioning — do not re-pin
- **E030**: Now offline-reproducible (pinned panel), 0 diffs since 2026-10-20
- **E029**: Offline-reproducible (pinned fundamentals), 0 diffs

## Dependencies

```bash
pip install -r requirements.txt
# numpy, pandas, scipy, pyarrow, statsmodels, yfinance
# cvxpy/cvxopt optional (fallback to scipy.optimize)
```

---

*This handoff was created automatically at session start. Update as work progresses.*
