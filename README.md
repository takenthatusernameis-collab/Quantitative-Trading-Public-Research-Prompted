# Quantitative Trading Public Research

Iterative research-driven quantitative strategy discovery.

## Repository Layout

- `PROMPT.MD` — mission and operating instructions
- `src/` — Python code
  - `data.py` — yfinance data acquisition + parquet caching
  - `backtest.py` — walk-forward engine, execution modeling, metrics
  - `strategies.py` — signal generators
  - `run_experiment.py` — single-strategy runner
  - `batch_run.py` — all-strategies comparison table
  - `validate.py` — placebo/null distribution + statistical checks
- `experiments/` — JSON results per strategy + summary
- `ledger/` — research ledger and prioritization procedure
- `data/` — parquet caches (gitignored)

## Quick Start

```bash
pip install yfinance pandas numpy scipy pyarrow
python3 src/batch_run.py        # run all strategies, print comparison
python3 src/validate.py         # placebo validation + statistical checks
```

## Key Findings (v1.1 - Broad Equity Universe)

| Strategy | OOS Sharpe | z vs Placebo | Positive Folds |
|---|---|---|---|
| **time_series_momentum (12m, 21d, inv-vol)** | **2.141** | **40.84** | **32/42** |
| reversal (12-month, 10d) | 2.288 | 29.46 | 34/42 |
| reversal (12-month, daily) | 2.103 | 29.46 | 34/42 |
| low_vol | 1.748 | 33.38 | 34/42 |
| quality (low-vol+mom) | 1.523 | 30.75 | 33/42 |
| momentum_6m | 1.335 | 30.85 | 30/42 |
| momentum (12m) | 1.248 | 29.30 | 31/42 |
| value | 1.120 | 24.82 | 24/42 |
| short_reversal | 0.776 | 21.10 | 25/42 |
| mean_reversion_5 | 0.087 | 18.03 | 26/42 |
| **random (placebo)** | **-0.656** | — | 0/50 |

Placebo baseline (50 random sims) has mean Sharpe **-0.656**. All strategies clear placebo with large z-scores. Results on 132 large-liquid US equities (2014-2026), walk-forward OOS.

## Caveats

- Single data source (yfinance); results on 132 large-liquid US equities (v1.1). Previous v1.0 used ETF-only universe.
- `auto_adjust=True` merges open/close adjustments; open-price execution is approximate.
- No parameter optimization yet — all signals use fixed, literature-standard parameters.
- Survivorship bias and delisting effects may not be fully captured by yfinance.
- Results are not independently validated against alternative data or brokers.

### Market-Neutral Discovery (E012 - large_liquid, walk-forward OOS)

All strategies tested prior to E012 were long-only equity-beta (+signal) and
correlated with SPY. E012 introduced the first genuinely market-neutral tests:
Betting Against Beta (Frazzini & Pedersen 2014) and a dollar-neutral low-beta sort.

| Strategy | OOS Sharpe | z vs Placebo | β vs SPY | Turnover | 2020-COVID Sharpe |
|---|---|---|---|---|---|
| **dollar-neutral low-beta (10/10, 21d)** | **1.287** | **7.78** | -0.035 | 0.064 | +1.440 |
| BAB (beta-neutral, canonical) | -0.629 | -0.67 | -0.003 | 0.041 | -4.239 |
| random (market-neutral placebo) | -0.477 | — | — | — | — |

- The **dollar-neutral low-beta sort** is the repository's first market-neutral strategy
  that is both beta-neutral (|β|<0.05, corr SPY ≈ -0.03) AND profitable (z=7.78). It complements
  the long-only `low_vol` factor (Sharpe 1.75, β≈0.7) by adding market-neutrality.
- The **canonical BAB factor** is market-neutral by construction but is negative on
  2014-2026 (OOS Sharpe -0.629, below the random market-neutral placebo) and collapses
  in the 2020 funding shock (Sharpe -4.24). Recorded as a rejected, regime-dependent candidate.
- Placebo baseline (50 random dollar-neutral sims): mean Sharpe -0.477.

### E013: Validation of the Dollar-Neutral Low-Beta Keeper

The keeper passed all gates (Sharpe ≥0.8, z ≥3, |β| ≤0.2) and survives realistic
shorting-cost stress:

| Parameter | Value |
|---|---|
| OOS Sharpe (baseline 252d/0.5/10pct) | 1.287 |
| Placebo z-score | 7.10 |
| Equity beta vs SPY | -0.035 |
| Corr vs SPY | -0.032 |
| Sharpe at 5bps round cost | 0.812 (still passes gate) |
| Sharpe at 0bps cost | 1.310 |

- **Beta-window sensitivity**: Sharpe robust across 63/126/252-day windows (1.18–1.29);
  252d optimal with lowest turnover (0.064). Shrink level (0.25/0.5/0.75) has no effect
  (rankings invariant to monotonic shrink).
- **Top-frac grid**: Sharpe improves as top_frac shrinks (0.05→1.48, 0.10→1.29, 0.15→1.15,
  0.20→1.11); default 0.10 retained as breadth-stable tradeoff.
- **Out-of-universe**: passes on 132-stock equity universe (1.287) and 10-stock ETF universe
  (0.877); fails on 10-name equity subset (0.680) — requires breadth for beta ranking.
- **Leg decomposition**: long low-beta leg Sharpe=1.744 (β=-0.096); short high-beta leg
  Sharpe=-1.621 (β=0.061) — net profit from long leg offsetting short losses, maintaining zero beta.

### E014: Beta-Aware Blended Portfolio (TSM + Dollar-Neutral Low-Beta)

Combining the market-neutral DN low-beta keeper with pure time-series momentum:

| Strategy | OOS Sharpe | Turnover | β vs SPY | Corr SPY | MaxDD | Bear Sharpe |
|---|---|---|---|---|---|---|
| **blend_tsm_dnlowbeta (50/50, 21d)** | **1.625** | **0.064** | **-0.051** | **-0.069** | **-0.217** | **-1.60** |
| TSM pure (21d, inv-vol) | 0.867 | 0.091 | ~0.90 | ~0.90 | -0.298 | -1.62 |
| DN Low-Beta (10/10, 21d) | 1.287 | 0.064 | -0.035 | -0.032 | -0.295 | -0.77 |

- The **blend achieves the highest OOS Sharpe (1.625) of any strategy tested** — exceeding both components individually.
- Maintains **near-zero market beta (-0.051)** with low turnover (6.4%) and improved max drawdown (-0.217).
- Cost-robust: low turnover preserves Sharpe under realistic costs.
- **Promoted as core blended portfolio candidate** — the repository's highest-Sharpe market-neutral strategy.
- *Superseded by E015: pure TSM at monthly rebalance (Sharpe 2.141) outperforms the 50/50 blend on both universes. See E015 below.*.

### Net-of-Cost Performance (large_liquid, walk-forward OOS)

The existing table follows.

| Strategy | Turnover (daily) | Base (0.5bps+0.2bps) | High (20bps+5bps) |
|---|---|---|---|
| **time_series_momentum (21d, inv-vol)** | **0.013** | **2.14** | **2.04** |
| reversal (10d) | 0.028 | 2.29 | 1.92 |
| reversal (daily) | 0.09 | 2.10 | 1.64 |
| low_vol | 0.05 | 1.75 | 1.55 |
| momentum_6m | 0.14 | 1.34 | 0.56 |
| quality | 0.30 | 1.52 | 0.29 |
| momentum | 0.44 | 1.25 | -0.92 |

Cost-robustness: **time_series_momentum** and low_vol/reversal survive high costs best. High-turnover strategies degrade sharply. TSM is the most cost-robust (4.7% Sharpe drop at 20bps+5bps vs 22% for reversal).

### E015: Blend Weight Optimization + Multi-Asset Universe Test

Whether the E014 50/50 blend weight is optimal, and whether the DN low-beta anomaly and TSM generalize to a cross-asset universe.

**Weight Optimization (large_liquid, 130 tickers)**

| Blend (TSM/DN) | OOS Sharpe | z vs Placebo | Turnover | β vs SPY | MaxDD | Bear Sharpe | Positive Folds |
|---|---|---|---|---|---|---|---|
| 0/1.0 (pure DN) | 1.289 | 1.82 | 0.064 | -0.035 | -0.295 | -0.538 | 30/42 |
| 0.3/0.7 | 1.459 | 2.76 | 0.064 | -0.045 | -0.225 | -0.847 | 29/42 |
| 0.4/0.6 | 1.537 | 3.19 | 0.064 | -0.048 | -0.200 | -0.923 | 30/42 |
| 0.5/0.5 (E014) | 1.627 | 3.68 | 0.064 | -0.051 | -0.217 | -0.986 | 32/42 |
| 0.6/0.4 | 1.728 | 4.23 | 0.064 | -0.054 | -0.234 | -1.036 | 34/42 |
| 0.7/0.3 | 1.838 | 4.84 | 0.064 | -0.057 | -0.250 | -1.071 | 33/42 |
| **1.0/0.0 (pure TSM)** | **2.141** | **6.50** | **0.064** | **-0.066** | **-0.315** | **-1.051** | **32/42** |

> *Note*: E014 tested TSM at daily rebalance (Sharpe 0.867); E015 tests TSM at monthly rebalance (2.141). At monthly rebal, pure TSM outperforms the E014 50/50 blend on all metrics.

**Multi-Asset Universe (41 tickers: ETFs + futures)**

| Blend (TSM/DN) | OOS Sharpe | Turnover | β vs SPY | MaxDD | Bear Sharpe | Positive Folds |
|---|---|---|---|---|---|---|
| Pure DN (0/1) | 0.342 | 0.053 | -0.040 | -0.403 | -0.760 | 23/43 |
| 0.5/0.5 | 0.746 | 0.063 | -0.026 | -0.202 | -0.589 | 29/43 |
| 0.7/0.3 | 1.164 | 0.067 | -0.020 | -0.145 | -0.440 | 34/43 |
| **Pure TSM (1.0/0)** | **2.086** | **0.074** | **-0.012** | **-0.068** | **+0.101** | **36/43** |

- **Pure TSM is the repository's flagship strategy**: highest OOS Sharpe on both universes (2.141 equities, 2.086 multi-asset), cost-robust (4.7% Sharpe drop at 20bps+5bps), low turnover (6-7%), and the *only* strategy with positive bear-market Sharpe on multi-asset (+0.10).
- **The DN low-beta blend is suboptimal**: the DN component *reduces* Sharpe on both universes. DN collapses on multi-asset (0.342 vs 1.289 on equities) — the low-beta anomaly is equity-specific.
- **Futures-only universe (12 tickers)**: too narrow for DN beta ranking; 50/50 blend Sharpe -0.020.
- See `experiments/e015_blend_optimization.json` for full results.

**Decision**: Promote pure TSM as the core strategy. DN low-beta keeper is equity-only. Next: test TSM on a properly-rolled futures universe and add a carry signal (E016).

### E016: Roll-Corrected Futures TSM + Carry [2026-10-11]

First experiment on a dedicated futures universe with a proper roll
methodology (`src/futures.py`): data-driven roll-seam detection (futures-vs-
paired-spot-ETF excess overnight gaps inside expected roll windows + 50%
outlier rule), seam-day returns replaced by the spot ETF return, and a
scale-invariant normalized-basis carry signal (KMPV 2018). Universe: 13
futures contracts (ES, NQ, YM, RTY, ZB, ZN, GC, SI, CL, NG, 6E, 6B, 6J)
vs paired spot ETFs, 2017-07 to 2026-10 (RTY=F data starts 2017-07),
28 OOS folds, monthly rebalance, symmetric long/short TSM.

| Strategy | OOS Sharpe | z vs Placebo | β vs SPY | MaxDD | Bear Sharpe | Turnover |
|---|---|---|---|---|---|---|
| TSM raw stitched (uncorrected) | 0.590 | — | +0.01 | -0.086 | **-1.061** | 0.061 |
| **TSM de-seamed (roll-corrected)** | **0.717** | **3.06** | **-0.03** | -0.125 | **+0.146** | 0.058 |
| carry (normalized basis) | -0.235 | 0.14 | -0.03 | -0.154 | -0.583 | 0.159 |
| carry (realized roll yield) | +0.218 | 1.53 | +0.01 | -0.133 | +0.437 | 0.027 |
| blend TSM+carry (50/50) | 0.414 | 2.13 | -0.03 | -0.097 | -0.087 | 0.104 |
| random (blended placebo, 50 sims) | -0.281 | — | — | — | — | — |

- **Roll methodology is material**: de-seaming improves TSM OOS Sharpe by
  21% (0.590 → 0.717) and flips bear-market Sharpe from -1.06 to +0.15.
  Raw stitched futures contain large artifacts (median seam gaps 0.3-2.5%;
   CL printed -306% / -127% overnight on 2020-04-20/21 — the negative-oil
   roll wedge — replaced by USO-proxy returns of -10.9% / -25.1%).
   **E015's multi-asset results used raw stitched futures (7 of 41 tickers)
   and are contaminated for the futures sleeve. E017 quantified the
   contamination: pure TSM multi-asset OOS Sharpe 2.086 (raw, exactly
   replicated) → 1.838 de-seamed, delta -0.248.**
- **TSM on rolled futures is a modest, distinguishable edge** (Sharpe 0.717,
  z=3.06, β=-0.03, positive bear Sharpe, 5.8% turnover), driven by
  equity-index futures (ES +1.01, NQ +0.84 standalone) and metals
  (GC +0.65, SI +0.70); oil negative (-0.60), bonds flat. Lookback-robust
  6-18m (0.64-0.89). Below the pre-registered 1.5 gate.
- **Carry failed on 2017-2026** (normalized basis -0.235; realized roll
  yield +0.218, z=1.53, but best-in-E016 bear Sharpe +0.437 and lowest
  turnover 2.7%). The TSM+carry blend dilutes TSM (0.414 < 0.717). Carry
  rejected on this sample; re-test on the 2014-2026 sample (E017).
- Pre-registered promotion gates for the blend: **FAILED** (Sharpe 0.414 <
  1.5; bear Sharpe -0.087 < 0; z 2.13 < 3; |β| and maxDD passed).
- See `experiments/e016_futures_tsm_carry.json` for full results.

### E017: Extended (2014-2026) Roll-Corrected Futures Panel [2026-10-11]

Re-validation on the full sample: RTY=F dropped (yfinance history starts
2017-07), breadth added (HG/CPER, ZW/WEAT, ZS/SOYB, ZC/CORN). 16
contracts, 3205 common trading days (2014-01-02 to 2026-10-09), 42 OOS
folds. Pre-registered primary TSM lookback 9m (from the E016 short-sample
grid: 9m/18m both 0.89 vs 12m 0.72; 9m = shortest robust horizon).
Pre-registered gates: OOS Sharpe >= 1.0, placebo z >= 3, positive bear
Sharpe, |β| <= 0.2.

| Strategy | OOS Sharpe | z vs Placebo | β vs SPY | MaxDD | Bear Sharpe | Turnover | Pos Folds |
|---|---|---|---|---|---|---|---|
| tsm raw stitched (9m) | 0.225 | — | -0.000 | -0.085 | -0.050 | 0.075 | 25/42 |
| **tsm de-seamed (9m, primary)** | **0.680** | **3.33** | **-0.009** | **-0.101** | **+0.811** | **0.067** | 25/42 |
| carry (normalized basis) | 0.010 | 1.04 | -0.017 | -0.198 | -0.288 | 0.211 | 23/42 |
| **carry (realized roll yield)** | **0.523** | **2.80** | **+0.014** | **-0.081** | **+0.907** | **0.031** | 28/42 |
| blend TSM+carry (50/50) | 0.463 | 2.59 | -0.013 | -0.069 | +0.427 | 0.131 | 30/42 |
| random (blended placebo, 50 sims) | -0.294 (std 0.292) | — | — | — | — | — | — |

- **Roll methodology is ~3x more material on the extended sample**:
  de-seaming improves TSM 0.225 → 0.680 (vs 0.590 → 0.717 on E016's
  short sample). Raw stitched futures are unusable for trend measurement.
- **Promotion gates FAILED (honestly reported, goalposts not moved)**:
  blend (0.463 < 1.0, z 2.59 < 3); primary TSM (0.680 < 1.0; but z 3.33,
  bear +0.811, |β| 0.009 all pass). Rolled-futures TSM is a validated
  modest cross-asset diversifier, not a flagship.
- **Realized-roll-yield carry more than doubled** on the longer sample
  (0.218 → 0.523, z 1.53 → 2.80, bear +0.437 → +0.907, turnover 3.1%)
  — the repo's best bear-market strategy and cheapest to trade; z=2.80
  remains below the 3.0 bar. Fate open → E018 (carry-specific placebo,
  window sensitivity, per-contract decomposition).
- **Normalized-basis carry robustly rejected** (0.010 on 2014-2026 after
  -0.235 on 2017-2026) — dead on two independent samples.
- Lookback sensitivity (extended): 6m 0.558, 9m 0.680 (primary),
  12m 0.435, 18m 0.805 (top on both samples; flagged for a pre-registered
  confirmatory run in E018).
- Per-contract TSM (9m): ES +0.78, NQ +0.79, YM +0.65, GC +0.64,
  SI +0.40 drive the book; FX futures negative (6E -0.30); bonds flat.
- Sample-period isolation: same 16-contract universe on 2017-07+ gives
  TSM(9m) 0.939 vs 0.680 on 2014-2026 — 2014-2017 was a weak trend
  regime; the E016 window was regime-favorable.
- **E016 replication exact**: 13-contract panel, 2017-07+, 12m TSM
  reproduces every E016 number to 3 decimals (de-seamed 0.717 = 0.717).
- **E015 multi-asset corrected**: pure TSM (12m, long-only) on the
  41-ticker universe = 2.086 raw (exact replication of E015) → **1.838
  de-seamed** (β -0.016, maxDD -0.152, turnover 0.074). E015's flagship
  multi-asset result was inflated ~12% by roll-seam artifacts.
- See `experiments/e017_extended_futures.json` for full results.

### E018: Realized-Roll-Yield Carry Validation + 18m TSM Confirmatory Run [2026-10-11]

Decisive validation of carry's fate (E017 left it open at z=2.80
against a *blended* placebo) and a pre-registered confirmatory run
of the 18m TSM lookback. Same 16-contract 2014-2026 panel
(3205 days, 42 folds); E017's 9m grid re-run as a replication
anchor (all five strategies reproduce E017 exactly).

**Carry validation (pre-registered gate: Sharpe >= 0.5, carry-specific z >= 3, bear Sharpe > 0, |β| <= 0.2, turnover <= 0.05):**

| Test | OOS Sharpe | z (carry-specific null) | β vs SPY | Bear Sharpe | Turnover | Pos Folds |
|---|---|---|---|---|---|---|
| **carry (realized roll yield, 252d, primary)** | **0.523** | **2.65** | **+0.014** | **+0.907** | **0.031** | **28/42** |
| carry, 126d window | 0.298 | 2.26 | +0.006 | +1.073 | 0.046 | 24/42 |
| carry, 504d window | 0.266 | 1.83 | +0.011 | +0.917 | 0.025 | 24/42 |
| carry-specific placebo (50 sims) | -0.347 (std 0.328) | — | — | — | — | — |

- **Carry gate FAILED on z (4/5 passed)**: against the correct
  carry-specific null (seam-calendar-preserving permutation of
  seam excess gaps, 50 sims), realized-roll-yield carry earns
  z=2.65 < 3.0. REJECTED as a standalone promoted component;
  retained as a near-significant diversifier (best bear-market
  Sharpe +0.907, lowest turnover 3.1% in the repo).
- **Window sensitivity peaks at the pre-registered 252d** (0.523
  vs 0.298/0.266 at 126d/504d); no window clears z>=3 — the
  signal is window-dependent.
- **Per-contract decomposition is economically plausible but weak**:
  edge concentrates in backwardation-prone commodities (HG +0.69,
  ZW +0.41, GC +0.41, SI +0.31) and 6J (+0.47); equity-index
  (NQ -0.55, ES -0.19) and bond (ZN -0.52) futures negative.
  The persistent roll-yield *level* does not predict the timing
  Sharpe (CL: highest mean roll yield +0.029, Sharpe +0.03) and
  per-contract signal/forward-return correlations are negligible
  (|corr| <= 0.04) — the cross-sectional sort, not the level,
  carries the signal.

**TSM lookback grid + pre-registered 18m confirmatory run (E017 gate bar: Sharpe >= 1.0, z >= 3, bear > 0, |β| <= 0.2):**

| Lookback | OOS Sharpe | z (blended placebo) | β vs SPY | Bear Sharpe | Turnover | Pos Folds |
|---|---|---|---|---|---|---|
| 6m | 0.558 | 2.92 | -0.014 | +0.389 | 0.083 | 24/42 |
| **9m (registered primary)** | **0.680** | **3.33** | **-0.009** | **+0.811** | **0.067** | **25/42** |
| 12m | 0.435 | 2.49 | -0.011 | +0.601 | 0.060 | 24/42 |
| **18m (confirmatory)** | **0.805** | **3.76** | **-0.010** | **+1.348** | **0.049** | **23/42** |

- **18m TSM gate FAILED on Sharpe (3/4 passed)**: 0.805 < 1.0
  despite z=3.76, the repo's best bear Sharpe (+1.348) and lowest
  futures turnover (4.9%). Goalposts not moved — 9m (0.680)
  remains the registered primary; 18m recorded as the best
  near-gate variant.
- **Blend grid not run** per pre-registration (carry failed its
  gate). A debugging run (`--n-sim 2`) incidentally computed
  deterministic blend Sharpe of 0.703/0.821/0.814 (TSM weight
  0.3/0.5/0.7) — disclosed in the ledger, NOT part of E018's
  official results; deferred to a fresh pre-registered E019.
- TSM(9m)-vs-carry(252d) signal correlation: 0.262.
- See `experiments/e018_carry_validation.json` for full results.

### E019: Pre-registered Cross-Asset Portfolio Construction [2026-10-11]

Two construction-level questions with fresh pre-registration
(all gates set before running; matched-per-cell placebos — an
improvement over E017/E018's single 50/50 blended null):

**Part A — TSM(18m)+carry(252d) blend grid, extended futures
panel (gates: OOS Sharpe >= 0.8, matched-placebo z >= 3, bear
> 0, |β| <= 0.2, turnover <= 0.08; falsification: beat
TSM-18m 0.805):**

| TSM weight | OOS Sharpe | z (matched null) | β | Bear Sharpe | Turnover | Gates | Beats TSM-18m |
|---|---|---|---|---|---|---|---|
| 0.3 | 0.725 | 4.68 | +0.007 | +1.436 | 0.033 | FAIL (Sharpe) | no |
| **0.5** | **0.858** | **5.84** | **+0.002** | **+1.627** | **0.036** | **PASS** | **YES** |
| **0.7** | **0.876** | **5.83** | **-0.003** | **+1.465** | **0.041** | **PASS** | **YES** |

**Part B — Total portfolio: equity flagship (TSM 12m,
long-only, inv-vol, large_liquid) + futures sleeve (TSM-18m,
de-seamed), common calendar (3205 days, 42 folds; gates: total
OOS Sharpe >= 2.0 AND bear Sharpe strictly > equity-only's):**

| Futures weight | OOS Sharpe | z (placebo) | β | Bear Sharpe | MaxDD | Turnover | Gates |
|---|---|---|---|---|---|---|---|
| 0.00 equity-only (common cal.) | 2.157 | — | -0.065 | -0.816 | -0.313 | 0.064 | (reference) |
| 1.00 futures-only | 0.805 | 3.76* | -0.010 | +1.348 | -0.093 | 0.049 | (reference) |
| **0.25** | **2.175** | **6.32** | **-0.051** | **-0.516** | **-0.243** | **0.060** | **PASS** |
| **0.50** | **2.034** | **4.32** | **-0.037** | **+0.059** | **-0.176** | **0.056** | **PASS** |
| 0.75 | 1.533 | 3.38 | -0.024 | +0.800 | -0.108 | 0.053 | FAIL (Sharpe) |

- **Inter-sleeve correlation +0.210** — the diversification
  channel is real. Per-sleeve return contribution at w=0.25:
  equity 92% / futures 8%.
- **Promoted**: (a) futures-sleeve blend at TSM weight 0.5
  (best bear Sharpe +1.627, lowest turnover 0.036; 0.7 is the
  best-Sharpe alternative); (b) total portfolio at **25%
  futures weight** — the only tested construction that beats
  the equity flagship on OOS Sharpe (2.175 vs 2.157) while
  improving bear Sharpe (-0.816→-0.516), maxDD (-0.313→
  -0.243) and turnover (0.064→0.060) simultaneously. The 50%
  weight is the defensive alternative: positive bear Sharpe
  (+0.059) and nearly half the maxDD (-0.176) at a 0.12
  OOS-Sharpe cost.
- E018 anchors replicated exactly (TSM-18m 0.805, carry 0.523;
  50/50 blended placebo -0.294 ± 0.292 reproduced).
- **Honest caveats**: (1) the +0.018 OOS improvement at w=0.25
  is within fold noise (per-fold Sharpe std 2.2-2.4, SE ≈ 0.37)
  — promotion rests on the pre-registered gates and the
  risk-profile improvements, not the point estimate; (2)
  execution-mismatch: equity sleeve earns close→next-open
  returns, futures sleeve close→close — the blend mixes
  conventions (E020 robustness test); (3) the 25% portfolio's
  bear Sharpe is still negative; only the 50% weight achieves
  a positive bear Sharpe; (4) the long-only equity placebo
  embeds the equity premium (z-scores measure timing skill);
  (5) BK/WBA missing from the equity panel (130/132 tickers).
- **Premise correction**: the E018 handoff claimed the equity
  flagship "carries full equity beta (~0.9)" — false for the
  registered monthly-rebalanced construction (β = -0.065,
  E015-recorded -0.066, re-verified here). The total-portfolio
  test is a return-stream-diversification test, not a
  beta-offset test.
- See `experiments/e019_cross_asset_portfolio.json` for full
  results.

### E020: Robustness Validation of the Promoted E019 Total Portfolio [2026-10-11]

Pre-registered robustness battery on the E019 promoted total portfolio (equity flagship + futures sleeve) with gates set before running.

**Part A — Execution-Convention Alignment (promotion-critical gate: OOS Sharpe >= 2.0 on aligned convention):**

| Construction | Futures Weight | OOS Sharpe | β vs SPY | Bear Sharpe | MaxDD | Gates |
|---|---|---|---|---|---|---|
| next_open (E019, mixed) | 0.25 | 2.175 | -0.051 | -0.516 | -0.243 | (reference) |
| next_open (E019, mixed) | 0.50 | 2.034 | -0.037 | +0.059 | -0.176 | (reference) |
| **equity_only close_to_close** | **0.00** | **1.739** | **-0.119** | **-0.719** | **-0.335** | **(aligned baseline)** |
| **total close_to_close** | **0.25** | **1.745** | **-0.092** | **-0.558** | **-0.264** | **FAIL (OOS<2.0)** |
| **total close_to_close** | **0.50** | **1.706** | **-0.064** | **-0.206** | **-0.187** | **FAIL (OOS<2.0)** |

**Part A gate: FAILED** — the convention-aligned 25% portfolio OOS Sharpe (1.745) breaches the 2.0 gate. The E019 promotion is convention-dependent.

**Part B — Cost Sweep (mixed convention, measurement only):**

| Cost Scenario | Futures Weight | OOS Sharpe | High-Cost 2.0 Gate Survives |
|---|---|---|---|
| base (0.5+0.2bps) | 0.25 | 2.175 | n/a |
| base (0.5+0.2bps) | 0.50 | 2.034 | n/a |
| **high (20+5bps)** | **0.25** | **2.054** | **YES (barely)** |
| **high (20+5bps)** | **0.50** | **1.886** | **NO** |

**Part C — Equity Lookback Sensitivity (mixed convention, 25% futures weight):**

| Lookback | Total OOS Sharpe | Total Bear Sharpe | OOS>=2.0? |
|---|---|---|---|
| 9m | 2.147 | -0.510 | YES |
| **12m (primary)** | **2.175** | **-0.516** | **YES** |
| 18m | 2.094 | -0.393 | YES |

**Part D — Futures-Sleeve Variant (mixed convention, 25% weight, falsification: blend must beat pure TSM-18m):**

| Sleeve | Sleeve OOS | Total OOS | Beats Pure? |
|---|---|---|---|
| pure TSM-18m | 0.805 | 2.175 | (reference) |
| blend TSM weight 0.5 | 0.858 | 2.221 | **YES** (+0.046) |
| blend TSM weight 0.7 | 0.876 | 2.207 | **YES** (+0.032) |

**Part E — Fine Futures-Weight Grid (mixed convention):**

| Futures Weight | OOS Sharpe | Bear Sharpe | MaxDD | Turnover |
|---|---|---|---|---|
| 0.10 | 2.173 | -0.719 | -0.285 | 0.0625 |
| 0.20 | 2.178 | -0.593 | -0.257 | 0.0609 |
| **0.25** | **2.175** | **-0.516** | **-0.243** | **0.0602** |
| 0.30 | 2.166 | -0.427 | -0.229 | 0.0594 |
| 0.50 | 2.034 | +0.059 | -0.176 | 0.0563 |
| 0.60 | 1.884 | +0.370 | -0.149 | 0.0548 |

**Decision: DEMOTE the E019 promotion.** The Part A convention-alignment gate failed — the mixed next-open/close-to-close convention inflated equity sleeve returns. The convention-aligned equity flagship itself drops from 2.157 to 1.739 OOS Sharpe. The promoted cross-asset portfolio is not robust to execution-convention alignment. The next task (E021) is pairs trading / statistical arbitrage on the large_liquid universe.

- See `experiments/e020_robustness.json` for full results.

## Status

- `src/`: `data.py`, `backtest.py`, `strategies.py`, `futures.py`, `run_experiment.py`, `batch_run.py`, `validate.py`, `validation.py`.
- `src/futures.py` (E016): roll-seam detection, de-seamed futures indices, normalized-basis carry, realized roll yield. `strategies.carry_signal`, `backtest.carry_weights`.
- `src/macro.py` (E022): FRED public-CSV fetcher + parquet cache, release-lagged theme momentum (5 themes), structural theme→asset sign matrix, month-end-anchored directional macro momentum weights, 12m-block signal permutation placebo.
- `src/pairs.py` (E021): distance-method pairs (`find_pairs_distance`, `pairs_weights`, `pairs_placebo_weights`).
- New in E012: `strategies.beta_factor`, `backtest.bab_weights`, `backtest.dollar_neutral_longshort_weights`, driver `experiments/run_e012.py`. See `ledger/RESEARCH_LEDGER.md` (E001-E013).
- New in E013: `strategies.dollar_neutral_lowbeta` signal, market-neutral CLI path in `run_experiment.py`, driver `experiments/run_e013.py`.
- New in E014: `strategies.blend_tsm_dnlowbeta` signal, blend strategy registered in `run_experiment.py` STRATEGIES.
- New in E015: `experiments/run_e015.py` driver for blend weight optimization (TSM/DN ratio grid) + multi-asset (ETF/futures) universe test. Fixed `PLACEBO_N_SIM` typo for reproducible runs.
- New in E016: `experiments/run_e016.py` driver (roll-corrected futures TSM + carry + blend + placebo + cost sweep + per-contract/lookback validation); `experiments/e016_futures_tsm_carry.json`.
- New in E017: `experiments/run_e017.py` driver (extended 16-contract 2014-2026 panel, pre-registered 9m primary lookback, sample-period isolation, E016 replication, E015 multi-asset re-validation with de-seamed futures); `experiments/e017_extended_futures.json`.
- New in E018: `experiments/run_e018.py` driver (carry-specific seam-calendar-preserving placebo, roll-yield window sensitivity {126/252/504}, per-contract carry decomposition, TSM lookback grid with blended-placebo z-scores, pre-registered 18m confirmatory run, conditional blend grid); `experiments/e018_carry_validation.json`, `experiments/e018_run.log`.
- New in E019: `experiments/run_e019.py` driver (pre-registered TSM(18m)+carry(252d) blend grid with matched-per-cell placebos — w*random-TSM + (1-w)*permuted-carry — and total-portfolio test of the equity flagship + futures sleeve at futures weights {0.25/0.5/0.75} with matched total-portfolio placebos); `experiments/e019_cross_asset_portfolio.json`, `experiments/e019_run.log`.
- **New in E020**: `experiments/run_e020.py` driver (pre-registered robustness battery: execution-convention alignment, cost sweep, equity lookback sensitivity, futures-sleeve variant, fine weight grid); `experiments/e020_robustness.json`. **E019 promotion DEMOTED** — Part A gate (convention-aligned OOS Sharpe >= 2.0) failed: 25% portfolio drops to 1.745 OOS Sharpe under close-to-close equity execution (vs 2.175 under mixed next-open/close-to-close).
- `data.py`: added retry logic for yfinance downloads (cache-read failure no longer silently falls through to flaky download).
- Run all baseline strategies: `python3 src/batch_run.py --universe large_liquid`
- Run placebo validation: `python3 src/validate.py --universe large_liquid`
- Run market-neutral experiment: `python3 experiments/run_e012.py`
- Run keeper validation: `python3 experiments/run_e013.py`
- Run market-neutral strategy via CLI: `python3 -m src.run_experiment dollar_neutral_lowbeta --universe large_liquid`
- Run blended portfolio: `python3 -m src.run_experiment blend_tsm_dnlowbeta --universe large_liquid`
- Run E015 weight optimization + multi-asset test: `python3 experiments/run_e015.py`
- Run E016 futures TSM + carry: `python3 experiments/run_e016.py`
- Run E017 extended futures panel: `python3 experiments/run_e017.py`
- Run E018 carry validation + 18m TSM confirmatory: `python3 experiments/run_e018.py`
- Run E019 cross-asset portfolio construction: `python3 experiments/run_e019.py`
- Run E020 robustness validation: `python3 experiments/run_e020.py`
- Run E021 pairs trading: `python3 experiments/run_e021.py`
- Run E022 macro momentum: `python3 experiments/run_e022.py`

### E021: Pairs Trading / Statistical Arbitrage (Gatev et al. 2006) [2026-10-11]

First new strategy family since E012. Distance-method pairs on large_liquid: 12-month (252d) formation of normalized prices, top-20 pairs by minimum sum of squared differences, z-score entry/exit (enter |z|>=2, exit |z|<=0), stateful positions, dollar-neutral per pair, inverse-vol weighted, monthly rebalance, next-day-open execution, 42 OOS folds.

| Metric | Value | Gate | Result |
|---|---|---|---|
| OOS Sharpe | 0.315 | >= 0.8 | FAIL |
| Placebo z (pair-level, 50 sims) | 0.77 | >= 3.0 | FAIL |
| Equity β vs SPY | +0.002 | <= 0.1 | PASS |
| Bear-market Sharpe (regime) | +0.457 | > 0 | PASS |
| Turnover (daily) | 0.018 | <= 0.15 | PASS |
| Positive OOS folds | 23/42 | — | — |
| MaxDD | -0.045 | — | — |

- **REJECTED (3/5 gates)**. The distance method's OOS Sharpe is statistically indistinguishable from the pair-level placebo (random pair matching, identical stateful rule: mean -0.012, std 0.427). No formation/max-pairs configuration clears the 0.8 gate (126d/10p 0.264, 252d/10p -0.334, 252d/30p -0.007, 378d/20p -0.350). Cost-robust only at low costs (0bps 0.519, 20bps -1.257). Bear windows: 2020-COVID +1.114, 2022-bear -0.790.
- **Audit note**: the pre-existing `src/pairs.py` was defective (stateless signal forced every entry to close the next day; only 31/300 active days in a synthetic test). Rewritten with stateful position logic, fixed formation-window semantics (no look-ahead), vectorized pair selection, and precomputed rolling z-score; the full 50-sim placebo sweep now runs in ~46s.
- See `experiments/e021_pairs_trading.json` for full results.

**Decision**: Pairs trading is not promoted. The family is deprioritized, not abandoned (cointegration/copula/order-flow variants remain untested). Next task (E022): macro momentum / trend following on public macro factors (Brooks & Moskowitz 2022), FRED data.

### E022: Macro Momentum on Public Macro Factors (Brooks 2017) [2026-10-11]

Directional variant of Brooks (2017) "A Half-Century of Macro
Momentum" (AQR white paper — the E021 handoff's "Brooks &
Moskowitz 2022" citation was corrected under the v1.2.1
premise-verification step). US-only, ETF-tradable: 5 FRED
themes (growth=INDPRO, trade=EXUSEU, policy=FEDFUNDS,
sentiment=UMCSENT, inflation=CPIAUCSL; 6m momentum, trailing
60m z-score, release-lagged 1 reference month) mapped with
structural signs onto 3 asset classes (SPY/IEF/GLD),
equal-weighted across 15 cells, gross=1, monthly month-end
rebalance, next-day-open execution, 42 OOS folds.

| Metric | Value | Gate | Result |
|---|---|---|---|
| OOS Sharpe | 0.428 | >= 0.8 | FAIL |
| Placebo z (block-permutation null, 50 sims) | 2.00 | >= 3.0 | FAIL |
| Equity β vs SPY | -0.011 | <= 0.4 | PASS |
| Bear-regime Sharpe | +0.792 | > 0 | PASS |
| Turnover (daily) | 0.0206 | <= 0.15 | PASS |
| Positive OOS folds | 25/42 | — | — |
| MaxDD | -0.198 | — | — |

- **REJECTED (3/5 gates)**: macro momentum is a real but
  sub-threshold edge on 2014-2026 — positive OOS Sharpe with
  near-zero market beta and genuine crisis alpha (2020-COVID
  window Sharpe +2.01, 2022-bear +1.87, bear-regime folds
  +0.79 vs bull +0.36), but placebo z=2.00 < 3.0 and Sharpe
  0.428 < 0.8. Goalposts not moved.
- **Pre-registered falsification expectation (v1.2.2) NOT
  falsified**: mean per-cell |Spearman(z, next-month return)|
  = 0.077 (>= 0.03) with 11/15 structural sign matches
  (>= 8/15) — the signals carry predictive content, concentrated
  in bond cells (growth→bonds ρ=-0.154, inflation→bonds
  ρ=-0.099, policy→commodities ρ=-0.144).
- **Per-theme decomposition**: policy (monetary-policy
  momentum) is the strongest theme (+0.651; consistent with
  post-FOMC drift literature), trade +0.365, growth -0.272,
  sentiment -0.255, inflation -0.199.
- **Sensitivity**: lookback 6m primary (3m 0.186, 12m 0.084);
  DBC (broad commodities) materially beats the GLD gold proxy
  (0.698 vs 0.428); 10% vol-target lifts Sharpe to 0.570 at
  9.96% realized vol; cost-robust to 10bps (0.344), fails at
  20bps (-0.189).
- **Data integrity**: native FRED series (no roll-stitching
  artifacts); residual caveat = revised vintage + release lag
  (mitigated by conservative 1-month lag). FX and 3m-rate
  sleeves omitted (no ETF proxy); long-short within-asset-class
  variant omitted (single market per class).
- See `experiments/e022_macro_momentum.json` for full results.

**Decision**: Macro momentum is not promoted as a standalone
component. It is retained as a validated, near-significant
diversifier (β≈0, bear-market alpha, corr -0.03 vs SPY). Next
task (E023): test the "Economic Trend" combination claim
(Brooks, Feilbogen, Ooi & Akant 2024, SSRN 4710868) — macro
momentum + price trend-following blend — since the paper's
central claim is that the two are complementary (corr ~0.3) and
the blend improves risk-adjusted returns and drawdown
protection.
