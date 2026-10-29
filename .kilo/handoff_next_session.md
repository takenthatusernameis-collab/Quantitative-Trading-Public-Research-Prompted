# Durable Handoff — Next Session

**Created:** 2026-10-29T10:27:00Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Next task (initial)

No specific objective assigned. Establish a clean baseline before any changes:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If green, proceed only when a concrete objective is provided.

## Open items

- Ill-conditioned tangency/min-var QP drift (~2.6e-05 under 1-ulp perturbation).
- `src/portfolio_opt.py:253` negative-denominator mask.
- Both documented in `ledger/RESEARCH_LEDGER.md`, left for deliberate re-pin decision.

(End of file)
