# Agentic Work Session Handoff

**Timestamp:** 2026-11-11T02:21:36Z
**Session ID:** Initial handoff for next agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Verification suite operational with multiple tiers (check, verify-quick, verify-extended, verify-full)

## Next Steps for Continuation
1. **Review the research ledger** (`ledger/RESEARCH_LEDGER.md`) for validated strategies and open items
2. **Run baseline verification** to confirm environment integrity:
   ```bash
   SEED=42 bash scripts/check.sh
   # or
   make check
   ```
3. **Choose verification tier** based on time budget:
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended`
   - Full (~15 min): `SEED=42 python3 run_all_verification.py --full`

## Key Constraints
- **Never leave verification half-finished** — golden artifacts in `experiments/*.json` are backed up and restored; interrupted runs leave driver output in working tree
- **Do not commit verification output** — restore before committing: `python3 run_all_verification.py --restore-only`
- **Seed must be 42** for reproducibility (walk-forward + placebo RNG)
- **Data cache coverage is enforced** — all `data.download()` calls must have pinned cache files

## Open Items (from ledger)
- E041 optimizer determinism: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP)
- E030 drift: previously re-pinned, now reproduces with 0 differences
- E029: now offline-reproducible with pinned fundamentals snapshot

## Quick Reference Commands
```bash
# Individual experiments
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
```