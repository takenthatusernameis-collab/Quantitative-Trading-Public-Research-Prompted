# Handoff for Next Agentic Work Session

**Created:** 2026-10-28T04:23:24Z
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Repository in clean post-checkpoint state.

## Initial Task (Start Here)

**Primary Objective:** Investigate and optimize the TSM + DN low-beta blend, with a focus on weight allocation and risk decomposition. If a simple improvement is found, pre-register and test a minimal confirmatory run (with placebo) before promotion; otherwise document a clear negative result.

This is the highest-value unexploited lever given the current evidence (blend_tsm_dnlowbeta is the strongest market-neutral strategy to date).

## Current State Summary

- **Validated keepers (large_liquid, net-of-cost):**
  1. `blend_tsm_dnlowbeta` (50/50 TSM pure + DN low-beta): OOS Sharpe ~1.625, β≈-0.05, turnover ~6.4%, MaxDD ~-0.217 (E014) — best market-neutral Sharpe so far
  2. `dollar_neutral_lowbeta` (DN low-beta): OOS Sharpe ~1.287, z~7.10, β small negative, validated (E012/E013)
  3. `time_series_momentum_pure` (12m, inv-vol, monthly): OOS Sharpe ~2.14 net in cost-robust form, low turnover (1.34%) but long-only equity beta (E010)
  4. `reversal` (12m/10d): strong net Sharpe, low turnover (E005/E007)

- **Notes:**
  - TSM and reversal are highly correlated (≈0.89) as both are long-only equity-beta strategies.
  - Canonical BAB rejected. Simple DN low-beta sort is the validated market-neutral keeper.
  - 50/50 blend gives near-zero beta (-0.05) by offsetting TSM's long exposure with DN's short leg (not by equal risk contribution). Weight optimization is warranted.

## Concrete Plan

### 1) Understand beta mechanics (quick)
- [ ] Decompose exposures: compute TSM and DN low-beta weights/exposures and see how they combine to β≈-0.05 at 50/50.
- [ ] Document the mechanism in notes (will inform allocation).

### 2) Weight optimization grid
- [ ] Grid search TSM/DN ratios: e.g. `0/100, 25/75, 50/50, 60/40, 70/30, 75/25, 80/20, 100/0` (monthly rebal). Evaluate on large_liquid.
- [ ] Metrics: OOS Sharpe (net-of-cost), annualized return/vol, MaxDD, turnover, β vs SPY, correlation to pure strategies, and performance in 2022/COVID stress.
- [ ] Consider simple risk-parity style heuristic (target equal risk contribution) as a candidate.

### 3) Validate promising candidates
- [ ] For any candidate that improves Sharpe ≥ +0.02 or meaningfully reduces MaxDD with |β|<0.2, run placebo validation (walk-forward placebo). Do **not** promote without passing placebo.
- [ ] If introducing a new blend variant as code, pre-register gates/falsification expectations before running.

### 4) Document
- [ ] If improved: add/update E015 (or new experiment) in `ledger/RESEARCH_LEDGER.md` with keep decision, rationale, and key stats.
- [ ] If not improved: record negative result with evidence (grid table + best candidate) and close out.

## Prerequisites & Constraints

- **Reproducibility:** Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps) and next-day open execution.
- **Baselines:** `experiments/*.json` are golden artifacts. `run_all_verification.py` backs up and restores them; never manually overwrite goldens to "fix" drift. Use `--restore-only` if tree is dirty from an interrupted run.
- **Data:** Use cached data in `data/`. If adding new inputs, commit them and update `ledger/data_baseline.json` via `scripts/check_data_coverage.py --update`. E029 fundamentals are pinned; be aware of offline constraints.
- **Verification:** Run `SEED=42 bash scripts/check.sh` before committing. For deeper checks: `make verify-quick` / `make verify-extended` as needed.
- **Market-neutral:** DN short leg is cost-bearing; be careful not to leak beta. Watch turnover.

## Quick Commands

```bash
# Sanity check
SEED=42 bash scripts/check.sh

# Run core drivers quickly
SEED=42 python3 run_all_verification.py --skip-slow

# Inspect strategies/backtest
grep -n "blend_tsm_dnlowbeta" src/strategies.py
grep -n "dollar_neutral_lowbeta" src/strategies.py
```

## Key Files

- `ledger/RESEARCH_LEDGER.md` — authoritative research record
- `src/strategies.py` — strategy implementations
- `src/backtest.py` — backtest engine
- `experiments/run_e014.py` — blend reference
- `run_all_verification.py`, `scripts/check.sh` — verification
