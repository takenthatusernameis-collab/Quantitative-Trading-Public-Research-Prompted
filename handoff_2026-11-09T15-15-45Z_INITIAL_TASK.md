# Agentic Work Session Handoff

**Timestamp:** 2026-11-09T15:30:50Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

- **Research Phase:** Complete (E001–E043)
- **Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Baseline:** Committed golden artifacts in `experiments/*.json` (pinned to SHA-256 in `ledger/golden_baseline.json`)

## Quick Start Commands

```bash
# Fast convention-robustness check (~seconds, offline)
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

## Key Constraints

1. **Never leave verification half-finished** - it overwrites `experiments/*.json` and restores them after. Use `--restore-only` to recover if interrupted.
2. **Golden baseline integrity** - `scripts/check_golden_baseline.py` compares tracked artifacts to SHA-256 in `ledger/golden_baseline.json`. Never re-pin as side effect of verification.
3. **Cache coverage enforced** - `scripts/check_data_coverage.py` requires all driver cache files exist, are git-tracked, and match SHA-256 in `ledger/data_baseline.json`.
4. **Reproducibility** - Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.

## Recent Important Notes (from AGENTS.md)

- **E029:** Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`)
- **E030:** Reproduces with 0 differences since 2026-10-20 (16-ETF input panel now committed)
- **E041:** Drift root-caused 2026-10-20 (optimizer defect fixed, 354→133 numeric diffs, 3 structural diffs gone). Still exceeds 1e-4 tolerance — **do not re-pin**.
- **Optimizer determinism:** `src/portfolio_opt.py` validates on problem constraints, not solver exit status. Tangency QP remains ill-conditioned (1-ulp perturbation → ~1e-05 drift in min_var answers).

## Verification Suite Behavior

- Backs up `experiments/*.json` to `.verify_snapshot/` with `ACTIVE.json` marker (pid)
- Runs drivers with `QUANT_RESEARCH_OFFLINE=1` (missing cache = hard failure)
- Restores goldens after completion
- Extended block writes drift report to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored)

## Next Steps / Open Items

See `ledger/RESEARCH_LEDGER.md` for full disposition. Notable open items:
- E041/E042 grid artifacts still drift due to ill-conditioned QP (ledger E049) — not re-pinned
- CI gate workflow template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI)

---

*This handoff was created automatically at session start. Update as needed during work.*