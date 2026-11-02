# HANDOFF FOR NEXT AGENTIC WORK SESSION
Timestamp: 2026-11-02T10:44:51Z
Branch/Commit: 0785a99 (chore(kilo): checkpoint agent session)
Repository: Quantitative-Trading-Public-Research-Prompted

## Current State (post-E018)
- **Equity flagship (validated):** Pure time-series momentum on large_liquid (132 US large-caps).
  - 12m lookback, 1m skip, inverse-vol weighting, monthly rebal, base costs 0.5+0.2bps: OOS Sharpe 2.141, β~0.9, turnover ~6-9%, cost-robust.
- **Cross-asset futures sleeve (validated but modest):** Roll-corrected symmetric TSM on 16-contract futures panel (2014-2026).
  - 18m lookback is strongest: OOS Sharpe 0.805, z=3.76 (vs blended placebo), β≈-0.01, bear Sharpe +1.348, turnover 4.9% — **below pre-registered 1.0 gate**.
  - 9m primary: Sharpe 0.680, z=3.33, bear +0.811.
- **Carry:** Realized-roll-yield (252d) is near-significant but rejected at pre-registered gate.
  - Sharpe 0.523, carry-specific placebo z=2.65 (< 3), bear +0.907, turnover 3.1%, β small. Window sensitivity {126,252,504} max at 252d. Concentrated in metals/commodities (HG, ZW, GC) and 6J; negative in equity-index/bonds.
- **Roll methodology:** `src/futures.py` implemented with seam detection/correction (material fix; E015 multi-asset inflated by ~12% → corrected to 1.838).
- **Infrastructure:** All core pipeline working (data, walk-forward, metrics, placebo, universe config, cost modeling, regime analysis). E016/E017/E018 reproduce exactly at SEED=42.

## MOST VALUABLE NEXT TASK (E019) — Pre-registered
**Pre-registered cross-asset portfolio construction: (a) TSM+carry blend grid with fresh gates, and (b) total-portfolio test of the equity flagship + cross-asset futures sleeve.**

### Rationale
- Futures sleeve adds diversification (low correlation to equity flagship ~0.26) and best bear-market profile; need to test if combination improves total-portfolio risk-adjusted returns.
- E018 disclosed non-official blend results (0.70-0.82) suggesting possible improvement, but this was from debugging run — must be pre-registered fresh with correct falsification bar.
- Correct falsification bar: beat TSM-18m (0.805), not the 9m primary (0.680).

### Prerequisites
- E018 complete; artifacts in `experiments/e018_*`, `experiments/run_e017.py`, `experiments/run_e018.py`, `src/futures.py` all present
- Cached data: `data/` has extended 16-contract panel (2014-2026) and `large_liquid` equity data
- Reproducibility verified (E016/E017/E018 bit-identical)

### Concrete Completion Criteria
1. **Pre-register before running** (record in driver docstring + JSON):
   - Blend gates: OOS Sharpe >= 0.8, blended-placebo z >= 3, positive bear Sharpe, |β| <= 0.2, turnover <= 0.08. Falsification: best blend must beat **TSM-18m (0.805)** on OOS Sharpe.
   - Total-portfolio gates: total OOS Sharpe >= 2.0 AND bear-market Sharpe **strictly greater** than equity-only flagship's, at chosen futures weight.

2. **Blend grid (futures panel):** TSM(18m, symmetric, inv-vol, de-seamed) + carry(252d, dollar-neutral) at TSM weights {0.3, 0.5, 0.7}. Report full grid vs pure TSM-18m (0.805) and TSM-9m (0.680) with blended placebo (random TSM+random carry, 50 sims). Compute costs (tc=0.5bps+slippage=0.2bps), turnover, β vs SPY, bear Sharpe, maxDD.

3. **Total-portfolio test:** Equity flagship (pure TSM 12m, long-only, inv-vol, large_liquid) + futures sleeve (TSM-18m symmetric, de-seamed) at futures weights {0.25, 0.5, 0.75}. Report total OOS Sharpe, β vs SPY, bear Sharpe, maxDD, turnover, per-sleeve contribution. **Document execution mismatch** (equity next-day-open vs futures close-to-close) as caveat.

4. **Decide honestly:** If clears pre-registered gates → promote and update README. If not → record negative, move to new strategy family per E016 search order (stat-arb/pairs Gatev et al. 2006, variance risk premium, macro momentum).

5. **Record as E019** in `ledger/RESEARCH_LEDGER.md` with table format matching E016-E018; update `README.md`; commit.

### Blockers/Risks
- Multiple testing (blend + total portfolio) — set gates before running, report all cells.
- E018 debugging disclosed blend Sharpes 0.70-0.82; must not cherry-pick, use conservative falsification (beat 0.805).
- Execution convention mismatch between equity (next-day-open) and futures (close-to-close) — document, don't hide.
- Only 2-3 true bear regimes in 42 folds — bear-Sharpe gates noisy.

### Key Files to Reference
- `experiments/run_e018.py` (template for placebo/construction)
- `experiments/run_e017.py` (futures panel setup)
- `src/futures.py` (roll methodology, carry)
- `src/strategies.py` (TSM, carry)
- `src/backtest.py` (weighting, metrics)
- `ledger/RESEARCH_LEDGER.md` (full history E001-E018)

### Quick Commands
```bash
SEED=42 python3 -m py_compile src/futures.py src/strategies.py src/backtest.py
SEED=42 python3 experiments/run_e017.py  # verify replication
SEED=42 python3 experiments/run_e018.py  # verify replication
```
