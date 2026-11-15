# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-15T19:09:59Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

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

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42`
- **Golden files**: `experiments/*.json` are committed artifacts — never commit verification output
- **Recovery**: If verification is interrupted, run `--restore-only` or `git checkout -- experiments/`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced.
- **Optimizer**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049)

## Pending / Open Items
- E041 drift: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- E041/E042 grid artifacts still drift by 29-133 differences — see ledger open item
- CI gate template at `.github/workflow-templates/verification-gate.yml` — maintainer must create via GitHub UI

## Last Verification Status
Run `SEED=42 python3 run_all_verification.py` to verify current state.