# Handoff — Agentic Work Session

**Timestamp:** 2026-11-18T04:51:44Z
**Session ID:** (auto-generated)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Context

**Quantitative Trading Research Repository** — Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Current State

- All 43 experiments completed (E001–E043)
- Verification suite operational: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`
- Golden artifacts in `experiments/*.json` are canonical baselines
- Data cache pinned at 2026-10-11/2026-10-12 vintages (`data/vintages.json`, `data/fundamentals_vintages.json`)
- `SEED=42` required for reproducibility

## Key Commands

```bash
# Fast convention check
SEED=42 make check

# Quick verification (~8 min)
SEED=42 make verify-quick

# Extended verification (~21 min)
SEED=42 make verify-extended

# Full verification (~15 min)
SEED=42 make verify-full

# Individual experiments
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

## Critical Notes

- **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. Use `--restore-only` if interrupted.
- **Golden baseline integrity**: `ledger/golden_baseline.json` pins SHA-256 of canonical artifacts. Do not re-pin without ledger entry.
- **Data coverage invariant**: All `data.download()` call sites must have committed, SHA-pinned cache files (`ledger/data_baseline.json`).
- **Optimizer determinacy**: `src/portfolio_opt.py` validates on constraints, not solver status (SLSQP status 8 is acceptable at constrained optimum).

## Open Items (from ledger)

- E041: 133 numeric differences remain (1-ulp QP sensitivity) — do not re-pin
- E042 grid artifacts drift similarly — do not re-pin
- CI workflow template at `.github/workflow-templates/verification-gate.yml` — maintainer must create via GitHub UI

## Next Steps

1. Run `make check` to verify current state
2. If clean, proceed with any pending verification or analysis tasks
3. Check `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion status

---

*Generated automatically at session start. Update this file before ending session.*