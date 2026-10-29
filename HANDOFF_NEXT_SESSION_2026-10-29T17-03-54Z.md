# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T17-03-54Z
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification baseline integrity guards are in place.

## Current State Summary

- **Top performing strategies (net-of-cost, large_liquid universe):**
  1. `blend_tsm_dnlowbeta` (50/50 TSM pure + DN low-beta): OOS Sharpe ~1.625, β≈-0.05, turnover ~6.4% (E014) — best Sharpe market-neutral strategy
  2. `dollar_neutral_lowbeta` (DN low-beta): OOS Sharpe ~1.287, validated (E012/E013)
  3. `time_series_momentum_pure` (12m lookback, inv-vol, monthly): OOS Sharpe ~2.141 gross, highly cost-robust, long-only (E010)
  4. `reversal` (12m, 10d rebal): OOS Sharpe ~2.29 net, low turnover (E005/E007)

- **Key findings:**
  - TSM and reversal highly correlated (0.89); both long-only equity-beta
  - Canonical BAB rejected; simple DN low-beta sort is validated market-neutral keeper
  - 50/50 blend gives near-zero beta by offsetting TSM long with DN short leg

## Highest-Value Next Task

**Optimize TSM+DN blend weights and evaluate adding a diversifier.**

### Rationale
- Fixed 50/50 is not risk-parity; beta ended up near-zero due to DN short leg offsetting TSM long exposure. Optimize weights for risk-adjusted return / drawdown.
- Only one validated market-neutral strategy exists. A third low-correlation component could improve diversification.

### Concrete Steps
1. **Weight optimization**: Grid search TSM/DN ratios (e.g., 0/100, 25/75, 50/50, 75/25, 100/0), monthly rebal. Evaluate Sharpe, β vs SPY, turnover, MaxDD, bear-market performance (focus 2022, COVID). Consider risk-parity style.
2. **Beta decomposition**: Document mechanics of why 50/50 gives β≈-0.05 vs expected.
3. **Test third component (optional but high value)**: Explore simple pairs trading (Gatev et al. 2006) on large_liquid (cointegrated pairs, distance method). Require correlation < 0.3 to existing blend and positive contribution.
4. **Regime stress tests**: Explicit focus on stressed periods.
5. **Document**: Add E015 entry to `ledger/RESEARCH_LEDGER.md` with keep/reject decision.

### Prerequisites
- `src/backtest.py` supports custom weighting; walk-forward + placebo available
- Strategies `time_series_momentum_pure`, `dollar_neutral_lowbeta` registered in `src/strategies.py`
- Data cached in `data/` (large_liquid)

### Success Criteria
- Find weights improving Sharpe ≥1.65 or meaningfully reducing MaxDD while maintaining |β| < 0.2
- If third component added: corr < 0.3 to blend, positive contribution, passes placebo if new signal
- Document in ledger with clear decision

### Warnings (critical)
- **Never modify `experiments/*.json`** golden files or re-pin baselines without explicit reason — verification suite restores them
- Always use `SEED=42`
- Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution
- Market-neutral requires careful shorting-cost consideration
- Before committing: run `SEED=42 bash scripts/check.sh` (and consider `make verify-quick` if touching drivers)
- If golden/baseline guards fail, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` (see AGENTS.md)
- Data coverage: adding inputs requires committing files and re-pinning `ledger/data_baseline.json` via `scripts/check_data_coverage.py --update`

## Quick Reference
- Quick check: `SEED=42 bash scripts/check.sh`
- Quick verification: `SEED=42 python3 run_all_verification.py --verify-quick` or `make verify-quick` (~8 min)
- Extended: `make verify-extended` (~21 min); Full: `make verify-full` (~15 min)
- Key files: `ledger/RESEARCH_LEDGER.md`, `src/strategies.py`, `src/backtest.py`, `src/portfolio_opt.py`, `experiments/run_e*.py`
" filePath="/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/HANDOFF_NEXT_SESSION_2026-10-29T17-03-54Z.md