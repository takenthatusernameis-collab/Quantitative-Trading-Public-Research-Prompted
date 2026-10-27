# Handoff for Next Agentic Work Session

**Created:** 2026-10-27T23:46:21Z
**Session Context:** Research phase complete (E001–E014). Core strategies validated; market-neutral keeper (dollar-neutral low-beta) and best blend (TSM + DN low-beta) identified.

## Current State Summary

- **Top performing strategies (net-of-cost, large_liquid universe):**
  1. `blend_tsm_dnlowbeta` (50/50 TSM pure + DN low-beta): OOS Sharpe 1.625, β≈-0.05, turnover 6.4%, MaxDD -0.217 (E014) — **highest Sharpe market-neutral strategy**
  2. `dollar_neutral_lowbeta` (DN low-beta, 10/10): OOS Sharpe 1.287, z=7.10, β≈-0.035, turnover 6.4% (E012/E013 validated)
  3. `time_series_momentum_pure` (12m lookback, inv-vol, monthly): OOS Sharpe 2.141 gross / highly cost-robust, turnover 1.34% but long-only equity beta (E010)
  4. `reversal` (12m, 10d rebal): OOS Sharpe ~2.29 net on large_liquid, low turnover (E005/E007)

- **Key findings:**
  - TSM and reversal are highly correlated (0.89) as both are long-only equity-beta strategies
  - Canonical BAB rejected (negative Sharpe); simple dollar-neutral low-beta sort is the validated market-neutral keeper
  - Blending TSM+DN gives near-zero beta (-0.05) by offsetting TSM long exposure with DN short leg — achieves best Sharpe with improved drawdown

## Most Valuable Next Task

**Optimize the TSM+DN blend weights and test for additional diversification.**

### Rationale
- The blend currently uses fixed 50/50 weights but beta ended up near-zero due to DN short leg offsetting TSM long exposure (not the intended 50/50 risk allocation). Optimizing weights could improve risk-adjusted returns.
- Repository has only one validated market-neutral strategy (DN low-beta). Adding a third uncorrelated component (pairs trading, cross-asset carry, or ETF stat-arb) would improve diversification beyond what we've achieved.
- Under v1.1 prioritization, complementarity matters. Current blend is the best so far but may be suboptimal.

### Concrete Steps
1. **Weight optimization**: Grid search TSM/DN blend ratios (e.g., 0/100, 25/75, 50/50, 75/25, 100/0) with monthly rebalancing. Evaluate Sharpe, beta vs SPY, turnover, max DD, bear-market performance. Consider risk-parity style allocation.
2. **Analyze beta decomposition**: Understand why 50/50 gives β≈-0.05 vs expected β≈0.5. Document mechanics for future blends.
3. **Test third component**: Explore simple pairs trading (Gatev et al. 2006) on large_liquid — identify cointegrated pairs, test distance method with proper lookbacks. Market-neutral pairs could add diversification.
4. **Regime stress test**: Focus on 2022 bear market and COVID periods for any new configurations.
5. **Document results**: Create E015 entry in `ledger/RESEARCH_LEDGER.md` with findings.

### Prerequisites
- Infrastructure ready: `src/backtest.py` supports custom weighting, walk-forward engine works, placebo validation available
- Strategies implemented: `time_series_momentum_pure`, `dollar_neutral_lowbeta` registered in STRATEGIES
- Data cached: `data/` has large_liquid parquet files

### Success Criteria
- Find blend weights that improve Sharpe ≥1.65 or reduce max DD significantly while maintaining |β| < 0.2
- If adding third component, demonstrate correlation < 0.3 to existing blend and positive contribution
- All results pass placebo validation if new signal introduced
- Document in ledger with clear keep/reject decision

### Warnings
- Do **not** modify `experiments/*.json` golden files or re-pin baselines without explicit reason — verification suite restores them
- Always use `SEED=42` for reproducibility
- Follow cost model (tc=0.5bps + slippage=0.2bps) and next-day open execution
- Market-neutral strategies require careful shorting-cost consideration (DN short leg is cost-bearing)
- Run `SEED=42 bash scripts/check.sh` before committing to verify integrity

## Quick Reference
- **Run full verification:** `SEED=42 python3 run_all_verification.py --full` (~15 min)
- **Quick check:** `SEED=42 bash scripts/check.sh` (~seconds)
- **Key files:** `ledger/RESEARCH_LEDGER.md`, `src/strategies.py`, `src/backtest.py`, `experiments/run_e*.py`
