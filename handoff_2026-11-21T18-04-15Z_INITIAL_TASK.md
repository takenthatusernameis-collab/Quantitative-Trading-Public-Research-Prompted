# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T18:04:15Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)

## Project State

- **Research Phase**: Complete (E001–E043)
- **Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Focus**: Verification/reproducibility of surviving strategies

## Quick Commands

```bash
# Fast convention-robustness check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
```

## Key Context for Next Session

1. **Golden files** in `experiments/*.json` are canonical artifacts — verification suite overwrites and restores them
2. **Never leave verification half-finished** — use `--restore-only` to recover if interrupted
3. **Seed 42** is mandatory for all runs (walk-forward + placebo RNG)
4. **Data cache** in `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12)
5. **E029 fundamentals** pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
6. **Optimizer determinism**: Tangency QP is ill-conditioned (1-ulp sensitivity) — do not re-pin E041/E042 to silence drift

## Open Items (from ledger)

- E041: 133 numeric differences remain (ill-conditioned QP, optimizer fault fixed)
- E042: Grid artifacts drift by 29-133 differences (same root cause)
- See `ledger/RESEARCH_LEDGER.md` entries E045, E048, E049 for details

## Initial Task for Next Session

Run the verification suite (`SEED=42 python3 run_all_verification.py`) to confirm current state, review any drift in extended drivers, and address open items if promoting strategies. Do not modify golden artifacts; restore via `--restore-only` if interrupted.

(End of file)
