# Handoff for Next Agentic Work Session

**Timestamp:** 2026-11-28T02:52:41Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

This is an independent reproducible quantitative-strategy research project on 2014–2026 US equities, futures, and macro data. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
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

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Key Notes for Next Session

1. **Reproducibility**: Always use `SEED=42` for walk-forward + placebo RNG
2. **Golden files**: `experiments/*.json` are canonical artifacts - never commit verification output
3. **Data**: Cached parquet in `data/` (gitignored except pinned vintages)
4. **Recovery**: If verification interrupted, use `SEED=42 python3 run_all_verification.py --restore-only`
4. **Lint/Typecheck**: Run `python3 -m py_compile` on changed files

## Active Concerns

- No CI workflow currently (template at `.github/workflow-templates/verification-gate.yml`)
- E041/E042 tangency QP is ill-conditioned but fixed by E050 exact active-set enumeration (bit-reproducible)
- E029 fundamentals snapshot is pinned in `data/fundamentals/` for offline reproducibility