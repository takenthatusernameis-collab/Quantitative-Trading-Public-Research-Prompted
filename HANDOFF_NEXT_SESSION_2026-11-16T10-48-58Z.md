# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-16T10:48:58Z
**HEAD:** `94a00f7cf6c7815d4bf639c33a7cf0e4a37bc8f5` (2026-11-16 10:48:47 +0000) "chore(kilo): checkpoint agent session"

## Repository State: CLOSED / BASELINE CLEAN

- **Research phase complete** (E001–E043 per AGENTS.md; ledger entries through E065).
- **All verification gates pass:** `SEED=42 bash scripts/check.sh` → `=== All checks passed ===` (exit 0).
- **Golden artifacts intact:** 107/107 pinned SHA-256 fingerprints in `ledger/golden_baseline.json` match working tree.
- **Data coverage enforced:** 35/35 pinned inputs present, tracked, and unchanged (`ledger/data_baseline.json`).
- **Convention robustness verified:** 15/15 strategies match recorded c2c/overnight decomposition (policy v1.2.3: primary = close-to-close).
- **No live verification run:** `.verify_snapshot/` absent.
- **Working tree clean:** only gitignored `__pycache__/*.pyc` noise; `git diff --stat HEAD -- experiments/` → empty.

## Surviving Validated Strategies (from E040 close-out)

| Strategy | OOS Sharpe (c2c) | OOS Sharpe (overnight) | Beta vs SPY | Key Property |
|---|---|---|---|---|
| TSM Pure (Equity Flagship) | 1.739 | 2.157 | -0.119 (c2c) / -0.065 (ovn) | Cost-robust, equity-β-bearing |
| Dollar-Neutral Low-Beta Sort | 1.053 | 1.287 | +1.02 (c2c) / -0.035 (ovn) | Market-neutral under overnight only |
| Futures TSM 18m (de-seamed) | 0.805 | balanced | -0.010 | Cross-asset trend, positive bear Sharpe |
| Futures Carry (Roll Yield) | 0.523 | balanced | +0.014 | Best bear-market Sharpe in repo (+0.91) |
| Macro Momentum (Brooks 2017) | 0.006 | 0.428 | -0.011 | Genuine crisis alpha (COVID +2.01, 2022 +1.87) |
| Low-Vol Flagship (unlevered) | 1.728 | not reported | +1.084 | Strongest equity-c2c edge, β-bearing |

## All Other Experiments: REJECTED or DATA-INFEASIBLE

34 experiments (E021–E039, E041–E043) are rejected with honest negatives or data-infeasible. Key closure results:
- **E041** (max-sharpe market-neutral blend): REJECTED 3/5 (G3 |β|≤0.1 fails, G2 placebo z fails)
- **E042** (min-variance confirmatory): PARTIAL 4/5 (G1/G3/G4/G5 pass, G2 placebo z 1.73 < 3.0 fails)
- **E042b** (sensitivity-grid lead): REJECTED 4/5 (G2 placebo z 1.96 < 3.0 fails)
- **E049/E050**: Exact KKT enumeration closes tangency QP open item; E041/E042 grid artifacts now reproduce 0 diffs.

## Open Items (documented, not actionable)

1. **Tangency QP ill-conditioning** (E049): 1-ulp perturbation still moves `min_var` answers by ~1e-05; E041/E042 grid artifacts would still drift by 29-133 diffs if re-pinned. Do NOT re-pin to silence — see ledger E049.
2. **DN low-beta c2c β sign reversal** (E041 finding): component is only market-neutral under overnight convention, not c2c.

## Constraints for Next Session

- **SEED=42** always (walk-forward + placebo RNG).
- **No goalpost moves:** gates, tolerances, decisions, and validated constructions are frozen.
- **No golden re-pins** without explicit `--update` (visible in diff).
- **No verification output committed:** if a run is interrupted, restore with `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- **Primary convention = close-to-close** (v1.2.3); mixed-convention portfolios prohibited.

## Available Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; structural match, numeric_tol=1e-4)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

## Next Bounded Task (if any)

The repository is closed. No new strategy family is warranted on free public data sources (all exhausted: price/volume, fundamentals, crypto, futures, macro, options). The surviving edges are the six component strategies above.

If a new session is started, the only valid action is **conformance re-verification**:
1. `SEED=42 bash scripts/check.sh` — confirm baseline still clean.
2. Report closure (as E051–E065 did).
3. Update this handoff with accurate HEAD and timestamp.

No commit should be made unless explicitly requested.
