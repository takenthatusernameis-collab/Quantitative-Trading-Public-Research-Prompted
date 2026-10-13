#!/usr/bin/env python3
"""E042: Min-Variance Market-Neutral Portfolio Construction (Confirmatory) from Validated Components.

Follows up the E040 final summary. E040 established that no single
promoted strategy survives the v1.2.3 convention-aligned gates as a
market-neutral total portfolio: the surviving edges are either
equity-beta-bearing (TSM pure flagship, beta ~0.90) or standalone
diversifiers with sub-threshold Sharpe (futures TSM 18m 0.841,
futures carry 0.472, macro momentum 0.006 c2c). The one validated
market-neutral equity sleeve (DN low-beta, OOS 1.053) is a single
sleeve, not a total portfolio.

E042 tests whether a walk-forward optimized blend of the five
validated components can form a market-neutral TOTAL portfolio:

  1. tsm_pure       - equity flagship trend (12m/1m skip, inv-vol,
                        long-only)                [E010/E015]
  2. dn_lowbeta     - equity market-neutral low-beta sort
                        (252d beta, shrink 0.5, 10/10) [E012/E013]
  3. futures_tsm    - cross-asset trend (18m/1m skip, inv-vol,
                        symmetric L/S, de-seamed)  [E018]
  4. futures_carry  - realized-roll-yield carry (252d, dollar-
                        neutral top/bottom half, inv-vol, de-seamed)
                                                                   [E017/E018]
  5. macro_momentum - Brooks (2017) directional macro momentum
                        (5 FRED themes x 3 ETFs, 6m/60m z, 1m lag)
                                                                   [E022]

Each component contributes a daily NET return stream under the
close-to-close convention (v1.2.3 primary), costed at its class
base rate (equity/macro ETF: 0.5bps + 0.2bps slippage; futures:
1.0bps + 0.5bps). The blend is built at the return-stream level:
a walk-forward optimizer assigns non-negative weights to the five
streams (sum=1) subject to market-neutrality, using only the
trailing 504-day formation window at each 21-day rebalance.
  PRE-REGISTRATION (fixed before running; goalposts not moved):

    Primary configuration (faithful replication of the E041
    sensitivity-grid config that produced the 0.979 lead -
    the grid machinery runs n_grid=0, so the confirmatory
    run must use the same estimator):
      - method = min_var (Ledoit-Wolf shrinkage covariance,
        ridge lambda=1e-4, SLSQP; n_grid=0 - NO Dirichlet
        grid overlay, which would turn the estimator into a
        max-Sharpe random search and is NOT the config that
        generated the lead)
      - beta constraint = 0.05 on BOTH equity beta (vs SPY)
        and futures beta (vs equal-weight de-seamed futures
        index)
      - formation window = 504 days, rebalance = 21 days,
        step = 63 days (~38 OOS folds on the warm-up-truncated
        2015-2026 common index)
      - execution = close-to-close, weights executed next-day
        (1-day lag), portfolio-level turnover costed at base
        (0.5bps + 0.2bps)
      - SEED=42

    Diagnostic (reported, NOT gated): the same config with
    the seeded Dirichlet(1) grid overlay (n_grid=2000) -
    the estimator the first E042 execution used by mistake.
    Its OOS degradation quantifies the overlay's in-sample
    overfitting.

    Falsification expectations (v1.2.2):
      FE1 (within-sample diversification): on the formation
        windows, the 5 component return streams must have
        pairwise correlations <= 0.5 in absolute value for
        >= 80% of the 10 pairs. FALSIFIED if < 80% of pairs
        pass (full-sample).
      FE2 (re-defined for min_variance per the E042 task
        spec - min_variance is EXPECTED to have lower
        in-sample Sharpe than 1/N, so the E041 in-sample-
        Sharpe-edge FE2 does not apply): PRIMARY =
        out-of-sample variance reduction vs 1/N,
        annualized variance(OOS net returns of the optimized
        blend) <= 0.90 * annualized variance(OOS net returns
        of the equal-weight 1/N blend over the same OOS
        folds). The in-sample Sharpe edge vs 1/N is reported
        as context only.

    Promotion gates (primary config, close-to-close, base
    costs):
      G1: OOS Sharpe (c2c) >= 0.8
      G2: BETA-CONSTRAINED component-permutation placebo
        z >= 3.0 (50 sims; Dirichlet(1) component-weight
        draws PROJECTED onto the beta <= 0.05 cap via the
        same linprog/SLSQP feasibility machinery at each
        rebalance, same rebalance/execution/cost structure -
        the null is MATCHED to the constraint so the z
        measures timing content, not the constraint's Sharpe
        cost). The UNCONSTRAINED Dirichlet placebo is
        reported as a diagnostic only.
      G3: |beta vs SPY| <= 0.1 (full-sample net-return beta,
        the repository's market-neutrality convention; the
        OOS beta over the union of test folds is reported
        alongside)
      G4: bear-market Sharpe > 0 (mean Sharpe over OOS folds
        where the SPY fold return < -5%)
      G5: average daily turnover <= 0.15

    Robustness (reported, NOT gated):
      - Cost sweep: portfolio-level turnover cost
        x {0, base 0.5+0.2bps, 10+5bps, 20+5bps}.
      - Component-set ablation: all-5 vs macro-inclusive-3
        (the equity sleeves are the c2c-beta source) - via
        the sensitivity grid's component_set dimension.
      - Split-half stability of the min-variance weights
        (mean component weights, L1 distance and per-half
        OOS Sharpe; the E041 max_sharpe solution was
        non-monotonic in the beta cap, so stability is
        verified).
      - Unconstrained Dirichlet placebo (diagnostic).

    Sensitivity grid (reported, NOT gated; no post-hoc
    selection):
      method x {max_sharpe, min_var, risk_parity}
      beta constraint x {0.05, 0.10, 0.15, 0.20}
      rebalance frequency x {21d, 63d}
      component set x {all 5, equity-only (2), futures-only
                       (2), macro-inclusive diversifiers (3)}

  Documented implementation gaps vs the portfolio-construction
  literature (Brandao-Marques et al. 2023; DeMiguel et al.
  2009):
    - 5 components (not "many assets"); the 1/N benchmark is
      the natural null given the small component count.
    - US-only, 2015-2026 sample (warm-up-truncated); the
      published evidence spans longer/global samples.
    - Components are themselves validated strategies, not raw
      factors; their internal costs are embedded in the
      return streams.
Documented implementation gaps vs the portfolio-construction
literature (Brandao-Marques et al. 2023; DeMiguel et al. 2009):
  - 5 components (not "many assets"); the 1/N benchmark is the
    natural null given the small component count.
  - US-only, 2015-2026 sample (warm-up-truncated); the published
    evidence spans longer/global samples.
  - Components are themselves validated strategies, not raw factors;
    their internal costs are embedded in the return streams.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import data, backtest, strategies, futures, macro, portfolio_opt
from src.run_experiment import UNIVERSES
from run_e017 import build_panels, FUTURES_UNIVERSE

# --- repository constants (match E017/E018/E023 conventions) ---
TC_EQUITY = 0.0005      # 0.5bps
SL_EQUITY = 0.0002      # 0.2bps
TC_FUTURES = 0.0010     # 1.0bps
SL_FUTURES = 0.0005     # 0.5bps
TRAIN = 504
TEST = 63
STEP = 63
FORMATION = 504
REBAL = 21
BETA_CONSTRAINT = 0.05
SEED = 42
PLACEBO_N = 50
START = "2014-01-01"
WARMUP = 252            # longest component lookback (252d); the first
                        # 252 days are warm-up and masked out.
# Primary estimator: n_grid=0 - faithful replication of the
# E041 sensitivity-grid config that produced the 0.979 lead
# (the grid machinery runs n_grid=0). The Dirichlet grid
# overlay (n_grid=2000) turns min_var into a max-Sharpe
# random search and is kept as a DIAGNOSTIC only.
PRIMARY_N_GRID = 0
DIAG_N_GRID = 2000

COMPONENTS = [
    "tsm_pure", "dn_lowbeta", "futures_tsm", "futures_carry",
    "macro_momentum",
]

# Pre-registered promotion gates.
GATES = {
    "G1_oos_sharpe_gte_0.8": 0.8,
    "G2_placebo_z_gte_3.0": 3.0,
    "G3_abs_beta_vs_spy_lte_0.1": 0.1,
    "G4_bear_sharpe_gt_0": 0.0,
    "G5_turnover_lte_0.15": 0.15,
}

# Pre-registered falsification expectations.
FE1_PAIR_CORR_MAX = 0.5
FE1_MIN_PAIR_FRAC = 0.80
FE2_MIN_IS_SHARPE_EDGE = 0.2

# Sensitivity grid (reported, not gated).
SENS_METHODS = ["max_sharpe", "min_var", "risk_parity"]
SENS_BETA = [0.05, 0.10, 0.15, 0.20]
SENS_REBAL = [21, 63]
SENS_SETS = {
    "all_5": COMPONENTS,
    "equity_only_2": ["tsm_pure", "dn_lowbeta"],
    "futures_only_2": ["futures_tsm", "futures_carry"],
    "macro_inclusive_3": ["futures_tsm", "futures_carry", "macro_momentum"],
}

# Cost sweep (reported, not gated).
COST_SWEEP = [
    ("zero_cost", 0.0, 0.0),
    ("base_0.5_0.2bps", TC_EQUITY, SL_EQUITY),
    ("high_10_5bps", 0.0010, 0.0005),
    ("stress_20_5bps", 0.0020, 0.0005),
]


def load_equity():
    """large_liquid equity panel + SPY benchmark."""
    df = data.download(UNIVERSES["large_liquid"], start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    return close, open_, spy


def load_macro_close():
    df = data.download(["SPY", "IEF", "GLD"], start=START)
    return data.get_panel(df, "Close").dropna(how="all")


def build_component_returns():
    """Compute the five validated component NET return streams.

    Each stream is the component's daily net return under the
    close-to-close convention (v1.2.3 primary), costed at its class
    base rate, rebalanced every 21 days (macro is monthly by
    construction). Returns a dict of (weights, net returns) per
    component plus the benchmark series.
    """
    eq_close, eq_open, spy = load_equity()

    # 1. TSM pure (equity flagship).
    tsm_sig = strategies.time_series_momentum_pure(
        eq_close, lookback=12, skip=1)
    w_tsm = backtest.time_series_momentum_weights(
        tsm_sig, eq_close, long_only=True, vol_window=63)
    r_tsm = backtest.portfolio_returns_close_to_close(
        w_tsm, eq_close, tc_cost=TC_EQUITY, slippage=SL_EQUITY,
        rebalance_freq=REBAL)["net"]

    # 2. Dollar-neutral low-beta (equity market-neutral).
    beta = strategies.beta_factor(
        eq_close, spy, window=252, skip=1, shrink=0.5)
    dn_sig = -beta
    w_dn = backtest.dollar_neutral_longshort_weights(dn_sig, top_frac=0.1)
    r_dn = backtest.portfolio_returns_close_to_close(
        w_dn, eq_close, tc_cost=TC_EQUITY, slippage=SL_EQUITY,
        rebalance_freq=REBAL)["net"]

    # Futures leg (16-contract de-seamed panel).
    panels = build_panels(FUTURES_UNIVERSE, start=START)
    de_index = panels["de_index"]
    carry_rroll = panels["carry_rroll"]

    # 3. Futures TSM 18m (cross-asset trend, symmetric L/S).
    ftsm_sig = strategies.time_series_momentum_pure(
        de_index, lookback=18, skip=1)
    w_ftsm = backtest.time_series_momentum_weights(
        ftsm_sig, de_index, long_only=False, vol_window=63)
    r_ftsm = backtest.portfolio_returns_close_to_close(
        w_ftsm, de_index, tc_cost=TC_FUTURES, slippage=SL_FUTURES,
        rebalance_freq=REBAL)["net"]

    # 4. Futures carry (realized roll yield, dollar-neutral, inv-vol).
    fvol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    w_carry = backtest.carry_weights(carry_rroll, fvol)
    r_carry = backtest.portfolio_returns_close_to_close(
        w_carry, de_index, tc_cost=TC_FUTURES, slippage=SL_FUTURES,
        rebalance_freq=REBAL)["net"]

    # 5. Macro momentum (Brooks 2017, 5 core themes x 3 ETFs).
    core_themes = ["growth", "trade", "policy", "sentiment", "inflation"]
    signals = macro.theme_signals(
        window=6, zscore_window=60)[core_themes]
    core_theme_signs = {
        a: {k: macro.THEME_SIGNS[a][k] for k in core_themes}
        for a in macro.ASSET_ETF
    }
    mac_close = load_macro_close()
    w_macro = macro.macro_momentum_weights(
        signals, mac_close.index, theme_signs=core_theme_signs)
    r_macro = backtest.portfolio_returns_close_to_close(
        w_macro, mac_close, tc_cost=TC_EQUITY, slippage=SL_EQUITY,
        rebalance_freq=1)["net"]

    comp = {
        "tsm_pure": (w_tsm, r_tsm),
        "dn_lowbeta": (w_dn, r_dn),
        "futures_tsm": (w_ftsm, r_ftsm),
        "futures_carry": (w_carry, r_carry),
        "macro_momentum": (w_macro, r_macro),
    }

    # Warm-up mask: the first WARMUP days are warm-up (the longest
    # component lookback is 252d; the DN all-NaN fallback and the
    # carry zero-signal tie-breaking produce spurious weights before
    # their signals are valid). Mask pre-warm-up returns to NaN and
    # align to the common valid index.
    masked = {}
    for name, (w, r) in comp.items():
        r = r.copy()
        cutoff = r.index[min(WARMUP, len(r) - 1)]
        r.loc[r.index <= cutoff] = np.nan
        masked[name] = (w, r)
    frame = pd.DataFrame({name: masked[name][1] for name in COMPONENTS})
    common = frame.dropna().index
    spy_ret = spy.pct_change().fillna(0.0).reindex(common)
    fut_index_ret = de_index.pct_change().mean(axis=1).fillna(0.0).reindex(common)
    returns = frame.loc[common]
    weights = {name: masked[name][0].reindex(common).fillna(0.0)
               for name in COMPONENTS}
    return {
        "returns": returns,
        "weights": weights,
        "spy": spy.reindex(common).ffill(),
        "spy_ret": spy_ret,
        "fut_index_ret": fut_index_ret,
        "de_index": de_index,
        "eq_close": eq_close,
        "mac_close": mac_close,
    }


def blend_series(component_returns, W, tc, sl):
    """Blended gross/net returns and turnover from component weights.

    Mirrors src.backtest.portfolio_returns_close_to_close: target
    weights set at close t are executed at t+1 (1-day lag) and held
    between rebalance dates; portfolio-level turnover is costed at
    (tc + sl) per unit turnover.
    """
    W_exec = W.shift(1).fillna(0.0)
    gross = (W_exec * component_returns).sum(axis=1)
    turnover = W_exec.diff().abs().sum(axis=1)
    net = gross - turnover * (tc + sl)
    return gross, turnover, net


def fold_metrics(net, index, spy_ret):
    """Walk-forward OOS fold metrics with regime classification."""
    splits = backtest.walk_forward_splits(len(index), TRAIN, TEST, STEP)
    folds = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        te_idx = index[te_s:te_e]
        fold_ret = net.loc[net.index.intersection(te_idx)]
        m = backtest.metrics(fold_ret.dropna())
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(te_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else float("nan")
        m["spy_fold_return"] = spy_win_ret
        m["regime"] = ("bull" if spy_win_ret > 0.02
                       else "bear" if spy_win_ret < -0.02 else "sideways")
        folds.append(m)
    return folds, splits


def regime_summary(folds):
    out = {}
    for regime in ["bull", "bear", "sideways"]:
        rows = [m for m in folds if m.get("regime") == regime]
        sharps = [m["sharpe"] for m in rows
                  if m.get("sharpe") is not None
                  and not np.isnan(m.get("sharpe", float("nan")))]
        out[regime] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sharps)) if sharps else float("nan"),
            "sharpe_pos": int(sum(1 for s in sharps if s > 0)) if sharps else 0,
        }
    return out


def beta_of(net, spy_ret):
    """Full-sample and OOS equity beta vs SPY."""
    common = net.dropna().index.intersection(spy_ret.index)
    y = net.loc[common].values
    x = spy_ret.loc[common].values
    if len(y) > 2 and np.std(x) > 0:
        A = np.vstack([np.ones(len(x)), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        return float(coef[1])
    return float("nan")


def evaluate_blend(net, index, spy_ret, tc, sl, W):
    """Full evaluation of a blended net return stream."""
    folds, splits = fold_metrics(net, index, spy_ret)
    sharps = [m["sharpe"] for m in folds
              if m.get("sharpe") is not None
              and not np.isnan(m.get("sharpe", float("nan")))]
    oos_sharpe = float(np.mean(sharps)) if sharps else float("nan")
    oos_std = float(np.std(sharps)) if sharps else float("nan")
    turnover = backtest.average_turnover(W)
    # Bear Sharpe: folds where SPY fold return < -5% (pre-registered G4).
    bear_rows = [m for m in folds
                 if m.get("spy_fold_return") is not None
                 and not np.isnan(m.get("spy_fold_return", float("nan")))
                 and m["spy_fold_return"] < -0.05]
    bear_sharps = [m["sharpe"] for m in bear_rows
                   if m.get("sharpe") is not None
                   and not np.isnan(m.get("sharpe", float("nan")))]
    bear_sharpe = float(np.mean(bear_sharps)) if bear_sharps else float("nan")
    # OOS equity beta over the union of test folds (the honest
    # out-of-sample market-neutrality measure; the full-sample
    # beta additionally includes the equal-weight bootstrap before
    # the first formation window).
    oos_mask = np.zeros(len(index), dtype=bool)
    for (_, _, te_s, te_e) in splits:
        oos_mask[te_s:te_e] = True
    oos_net = net.loc[index[oos_mask]]
    oos_beta = beta_of(oos_net, spy_ret)
    return {
        "oos_sharpe": oos_sharpe,
        "oos_sharpe_std": oos_std,
        "n_folds": len(splits),
        "positive_folds": int(sum(1 for m in folds
                                if m.get("sharpe") is not None
                                and not np.isnan(m.get("sharpe", float("nan")))
                                and m["sharpe"] > 0)),
        "equity_beta": beta_of(net, spy_ret),
        "oos_equity_beta": oos_beta,
        "turnover": turnover,
        "bear_sharpe": bear_sharpe,
        "bear_folds": len(bear_rows),
        "regime_analysis": regime_summary(folds),
        "is_sharpe": float(backtest.metrics(net.dropna()).get("sharpe", float("nan"))),
        "max_drawdown": float(backtest.metrics(net.dropna()).get("max_drawdown", float("nan"))),
    }


def fe1_diversification(component_returns):
    """FE1: within-sample diversification of the component streams.

    Full-sample pairwise |correlation| matrix plus the per-formation-
    window fraction of pairs with |corr| <= 0.5. FE1 passes if >= 80%
    of the 10 full-sample pairs have |corr| <= 0.5.
    """
    corr = component_returns.corr()
    pairs = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            pairs.append((corr.columns[i], corr.columns[j],
                          float(corr.iloc[i, j])))
    n_pass = sum(1 for _, _, c in pairs if abs(c) <= FE1_PAIR_CORR_MAX)
    frac = n_pass / len(pairs) if pairs else 0.0
    # Per-formation-window fraction (walk-forward view).
    R = component_returns
    n_days = len(R)
    fold_fracs = []
    for pos in range(FORMATION, n_days, REBAL):
        win = R.iloc[pos - FORMATION:pos]
        c = win.corr()
        pp = [abs(float(c.iloc[i, j]))
              for i in range(len(c.columns))
              for j in range(i + 1, len(c.columns))]
        if pp:
            fold_fracs.append(
                sum(1 for v in pp if v <= FE1_PAIR_CORR_MAX) / len(pp))
    return {
        "pair_correlations": [
            {"a": a, "b": b, "corr": c, "abs_pass": abs(c) <= FE1_PAIR_CORR_MAX}
            for a, b, c in pairs
        ],
        "n_pairs": len(pairs),
        "n_pairs_pass": n_pass,
        "pair_frac_pass": float(frac),
        "mean_fold_pair_frac_pass": (float(np.mean(fold_fracs))
                                     if fold_fracs else float("nan")),
        "threshold": FE1_PAIR_CORR_MAX,
        "required_frac": FE1_MIN_PAIR_FRAC,
        "passed": bool(frac >= FE1_MIN_PAIR_FRAC),
    }


def fe2_variance_reduction(component_returns, net_opt, W, index,
                            spy_ret):
    """FE2 (re-defined for min_variance per the E042 task spec).

    Min-variance is EXPECTED to have lower in-sample Sharpe
    than 1/N by construction, so E041's in-sample-Sharpe-edge
    FE2 does not apply. PRIMARY FE2: out-of-sample variance
    reduction vs 1/N - the annualized variance of the
    optimized blend's OOS net returns must be <= 0.90x the
    annualized variance of the equal-weight (1/N) blend's OOS
    net returns over the same OOS folds (same rebalance
    cadence, execution lag and cost treatment). The in-sample
    Sharpe edge vs 1/N is reported as context only.
    """
    N = component_returns.shape[1]
    # 1/N weights at the same rebalance cadence.
    W_1n = pd.DataFrame(np.nan, index=component_returns.index,
                        columns=component_returns.columns)
    for pos in range(0, len(component_returns), REBAL):
        W_1n.iloc[pos] = np.ones(N) / N
    W_1n = W_1n.ffill().fillna(0.0)
    _, _, net_1n = blend_series(
        component_returns, W_1n, TC_EQUITY, SL_EQUITY)

    # OOS mask = union of test folds (same as evaluate_blend).
    folds, splits = fold_metrics(net_opt, index, spy_ret)
    oos_mask = np.zeros(len(index), dtype=bool)
    for (_, _, te_s, te_e) in splits:
        oos_mask[te_s:te_e] = True
    oos_idx = index[oos_mask]
    oos_opt = net_opt.loc[oos_idx].dropna()
    oos_1n = net_1n.loc[oos_idx].dropna()
    common = oos_opt.index.intersection(oos_1n.index)
    oos_opt = oos_opt.loc[common]
    oos_1n = oos_1n.loc[common]
    var_opt = float(np.var(oos_opt, ddof=1) * 252)
    var_1n = float(np.var(oos_1n, ddof=1) * 252)
    var_ratio = var_opt / var_1n if var_1n > 0 else float("nan")

    # Per-fold variance ratios.
    fold_ratios = []
    for (_, _, te_s, te_e) in splits:
        te_idx = index[te_s:te_e]
        a = net_opt.loc[net_opt.index.intersection(te_idx)].dropna()
        b = net_1n.loc[net_1n.index.intersection(te_idx)].dropna()
        c = a.index.intersection(b.index)
        if len(c) > 2:
            vo = float(np.var(a.loc[c], ddof=1) * 252)
            v1 = float(np.var(b.loc[c], ddof=1) * 252)
            if v1 > 0:
                fold_ratios.append(vo / v1)

    # Context: in-sample Sharpe edge vs 1/N (E041-style FE2,
    # NOT the pre-registered FE2 for min_variance).
    R = component_returns
    n_days = len(R)
    diffs = []
    for pos in range(FORMATION, n_days, REBAL):
        win = R.iloc[pos - FORMATION:pos]
        w_opt = W.iloc[pos]
        if not np.isfinite(w_opt).all():
            continue

        def is_sharpe(w):
            mu = win.mean().to_numpy()
            S = portfolio_opt.ledoit_wolf_covariance(
                win.to_numpy()) + 1e-4 * np.eye(win.shape[1])
            var = float(w @ S @ w)
            if var <= 0:
                return float("nan")
            return float(w @ mu) / np.sqrt(var) * np.sqrt(252)

        s_opt = is_sharpe(w_opt.to_numpy())
        s_eq = is_sharpe(np.ones(win.shape[1]) / win.shape[1])
        if np.isfinite(s_opt) and np.isfinite(s_eq):
            diffs.append(s_opt - s_eq)
    mean_diff = float(np.mean(diffs)) if diffs else float("nan")
    return {
        "definition": ("OOS annualized variance(opt) <= 0.90 * "
                       "OOS annualized variance(1/N) over the union "
                       "of test folds (re-defined for min_variance "
                       "per the E042 task spec)"),
        "oos_annualized_variance_opt": var_opt,
        "oos_annualized_variance_1n": var_1n,
        "oos_variance_ratio": float(var_ratio),
        "mean_per_fold_variance_ratio": (
            float(np.mean(fold_ratios)) if fold_ratios
            else float("nan")),
        "n_folds_variance": len(fold_ratios),
        "threshold": 0.90,
        "passed": bool(var_ratio <= 0.90),
        "context_in_sample_sharpe_edge_vs_1n": mean_diff,
        "context_note": ("E041-style in-sample Sharpe edge; min_var "
                         "is expected to be BELOW 1/N in-sample by "
                         "construction, so this is context only, not "
                         "the pre-registered FE2."),
    }


def split_half_stability(component_returns, spy_ret,
                            fut_index_ret):
    """Split-half stability of the min-variance weights.

    Re-runs the primary optimization (min_var, beta<=0.05,
    n_grid=0) independently on the first and second half
    of the common index and compares the mean component
    weights (per-component means, L1 distance, Spearman
    rank correlation across components) and the per-half
    OOS Sharpe. The E041 max_sharpe solution was
    non-monotonic in the beta cap, so stability of the
    min_variance solution is a pre-registered robustness
    check (reported, not gated).
    """
    n_days = len(component_returns)
    half = n_days // 2
    out = {}
    mean_w = {}
    for name, sub in [("first_half",
                        component_returns.iloc[:half]),
                       ("second_half",
                        component_returns.iloc[half:])]:
        sub_spy = spy_ret.reindex(sub.index)
        sub_fut = fut_index_ret.reindex(sub.index)
        W_sub = portfolio_opt.walk_forward_blend_weights(
            sub, benchmark_returns=sub_spy,
            futures_benchmark_returns=sub_fut,
            formation_window=FORMATION, rebalance_freq=REBAL,
            beta_constraint=BETA_CONSTRAINT, method="min_var",
            seed=SEED, n_grid=PRIMARY_N_GRID)
        _, _, net_sub = blend_series(
            sub, W_sub, TC_EQUITY, SL_EQUITY)
        folds, _ = fold_metrics(net_sub, sub.index, sub_spy)
        sharps = [m["sharpe"] for m in folds
                  if m.get("sharpe") is not None
                  and not np.isnan(m.get("sharpe", float("nan")))]
        mw = {col: float(W_sub[col].mean())
              for col in sub.columns}
        mean_w[name] = mw
        out[name] = {
            "n_days": int(len(sub)),
            "start": str(sub.index[0].date()),
            "end": str(sub.index[-1].date()),
            "mean_component_weights": mw,
            "oos_sharpe": (float(np.mean(sharps))
                            if sharps else float("nan")),
            "n_folds": len(folds),
        }
    # L1 distance and Spearman rank correlation between
    # the two halves' mean weight vectors.
    cols = list(component_returns.columns)
    v1 = np.array([mean_w["first_half"][c] for c in cols])
    v2 = np.array([mean_w["second_half"][c] for c in cols])
    l1 = float(np.abs(v1 - v2).sum())
    from scipy.stats import spearmanr
    rho = float(spearmanr(v1, v2).statistic) \
        if len(cols) > 1 and np.std(v1) > 0 and np.std(v2) > 0 \
        else float("nan")
    out["comparison"] = {
        "l1_distance_mean_weights": l1,
        "spearman_rank_corr_mean_weights": rho,
        "per_component_abs_diff": {
            c: float(abs(mean_w["first_half"][c]
                          - mean_w["second_half"][c]))
            for c in cols},
        "stability_note": ("Small L1 / high rank correlation "
                            "between half-mean weights indicates "
                            "the min_variance solution is stable "
                            "across sample splits (unlike the "
                            "E041 max_sharpe solution, which was "
                            "non-monotonic in the beta cap)."),
    }
    return out


def component_attribution(component_returns, spy_ret, W, folds):
    """Per-component OOS Sharpe, beta, turnover and blend weight."""
    out = {}
    for col in component_returns.columns:
        r = component_returns[col]
        # OOS Sharpe of the standalone component stream (same folds).
        index = component_returns.index
        sh = []
        for i, (tr_s, tr_e, te_s, te_e) in enumerate(
                backtest.walk_forward_splits(len(index), TRAIN, TEST, STEP)):
            te_idx = index[te_s:te_e]
            fr = r.loc[r.index.intersection(te_idx)]
            m = backtest.metrics(fr.dropna())
            if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan"))):
                sh.append(m["sharpe"])
        beta = beta_of(r, spy_ret)
        out[col] = {
            "standalone_oos_sharpe": float(np.mean(sh)) if sh else float("nan"),
            "standalone_is_sharpe": float(backtest.metrics(r.dropna()).get("sharpe", float("nan"))),
            "equity_beta": beta,
            "mean_blend_weight": float(W[col].mean()),
            "min_blend_weight": float(W[col].min()),
            "max_blend_weight": float(W[col].max()),
        }
    return out


def sensitivity_grid(component_returns, benchmark_returns,
                     futures_benchmark_returns, index, spy_ret):
    """Pre-registered sensitivity grid (reported, not gated)."""
    rows = []
    for method in SENS_METHODS:
        for bc in SENS_BETA:
            for reb in SENS_REBAL:
                for set_name, cols in SENS_SETS.items():
                    sub = component_returns[cols]
                    sub_bench = (
                        benchmark_returns if any(
                            c in ["tsm_pure", "dn_lowbeta", "macro_momentum"]
                            for c in cols) else None)
                    sub_fb = (
                        futures_benchmark_returns if any(
                            c in ["futures_tsm", "futures_carry"]
                            for c in cols) else None)
                    W = portfolio_opt.walk_forward_blend_weights(
                        sub, benchmark_returns=sub_bench,
                        futures_benchmark_returns=sub_fb,
                        formation_window=FORMATION, rebalance_freq=reb,
                        beta_constraint=bc, method=method,
                        seed=SEED, n_grid=0)
                    gross, turnover, net = blend_series(sub, W, TC_EQUITY, SL_EQUITY)
                    res = evaluate_blend(net, index, spy_ret, TC_EQUITY, SL_EQUITY, W)
                    rows.append({
                        "method": method,
                        "beta_constraint": bc,
                        "rebalance_freq": reb,
                        "component_set": set_name,
                        "oos_sharpe": res["oos_sharpe"],
                        "equity_beta": res["equity_beta"],
                        "turnover": res["turnover"],
                        "bear_sharpe": res["bear_sharpe"],
                        "n_folds": res["n_folds"],
                    })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-sim", type=int, default=PLACEBO_N,
                        help="placebo simulations (default 50)")
    parser.add_argument("--no-sensitivity", action="store_true",
                        help="skip the sensitivity grid")
    parser.add_argument("--out", default=None,
                        help="output JSON path (default: the canonical golden "
                             "path experiments/e042_minvar_market_neutral.json "
                             "for the full pre-registered config only; "
                             "quick/non-primary runs default to "
                             "experiments/e042_minvar_market_neutral_quick.json "
                             "so they cannot silently overwrite the release "
                             "golden)")
    args = parser.parse_args()
    n_sim = args.n_sim

    print("=" * 72)
    print("E042: Min-Variance Market-Neutral Portfolio Construction (Confirmatory) "
          "(Walk-Forward Optimized Blend of 5 Validated Components)")
    print("=" * 72)

    comp = build_component_returns()
    component_returns = comp["returns"]
    spy_ret = comp["spy_ret"]
    fut_index_ret = comp["fut_index_ret"]
    index = component_returns.index
    print(f"\nComponent return streams: {component_returns.shape}")
    print(f"  Common index: {index[0].date()} to {index[-1].date()}")
    print(f"  Components: {list(component_returns.columns)}")
    print(f"  Warm-up masked: first {WARMUP} trading days")

    # ---- FE1: within-sample diversification ----
    print("\n" + "-" * 72)
    print("FE1: Within-sample diversification (pre-registered falsification)")
    print("-" * 72)
    fe1 = fe1_diversification(component_returns)
    print(f"  Pairwise |corr| <= {FE1_PAIR_CORR_MAX}: "
          f"{fe1['n_pairs_pass']}/{fe1['n_pairs']} pairs "
          f"({fe1['pair_frac_pass']*100:.0f}%, need >= {FE1_MIN_PAIR_FRAC*100:.0f}%)")
    for p in fe1["pair_correlations"]:
        print(f"    {p['a']:<16} vs {p['b']:<16} corr={p['corr']:+.3f} "
              f"|corr|<={FE1_PAIR_CORR_MAX}: {p['abs_pass']}")
    print(f"  Mean per-fold pair fraction passing: "
          f"{fe1['mean_fold_pair_frac_pass']:.3f}")
    print(f"  FE1: {'NOT FALSIFIED (passed)' if fe1['passed'] else 'FALSIFIED'}")

    # ---- Primary walk-forward optimized blend ----
    print("\n" + "-" * 72)
    print("Primary: walk-forward min_variance blend "
          "(min_var, beta<=0.05, 504/21/63, c2c, base "
          "costs, n_grid=0 - faithful replication of the "
          "E041 grid config)")
    print("-" * 72)
    W = portfolio_opt.walk_forward_blend_weights(
        component_returns, benchmark_returns=spy_ret,
        futures_benchmark_returns=fut_index_ret,
        formation_window=FORMATION, rebalance_freq=REBAL,
        beta_constraint=BETA_CONSTRAINT, method="min_var",
        seed=SEED, n_grid=PRIMARY_N_GRID)
    gross, turnover, net = blend_series(
        component_returns, W, TC_EQUITY, SL_EQUITY)
    primary = evaluate_blend(net, index, spy_ret,
                                  TC_EQUITY, SL_EQUITY, W)
    print(f"  OOS Sharpe (c2c) = {primary['oos_sharpe']:.3f} "
          f"(std {primary['oos_sharpe_std']:.3f})  "
          f"pos folds {primary['positive_folds']}/{primary['n_folds']}")
    print(f"  Equity beta vs SPY = {primary['equity_beta']:+.4f} "
          f"(OOS {primary['oos_equity_beta']:+.4f})  "
          f"turnover = {primary['turnover']:.4f}  "
          f"bear Sharpe = {primary['bear_sharpe']:+.3f} "
          f"({primary['bear_folds']} bear folds)")
    print(f"  IS Sharpe = {primary['is_sharpe']:.3f}  "
          f"maxDD = {primary['max_drawdown']:.3f}")
    print("  Regime: " + ", ".join(
        f"{k}=n{v['n_folds']}/sh{v['sharpe_mean']:+.3f}"
        for k, v in primary["regime_analysis"].items()))
    print("  Mean component weights: " + ", ".join(
        f"{c}={W[c].mean():.3f}" for c in W.columns))

    # ---- Diagnostic: Dirichlet-grid overlay (n_grid=2000) ----
    # The estimator the first E042 execution used by mistake.
    # The overlay selects the max-Sharpe feasible Dirichlet
    # draw, turning min_var into an in-sample random search.
    print("\n" + "-" * 72)
    print("Diagnostic: Dirichlet-grid overlay (n_grid=2000) "
          "- NOT the pre-registered primary")
    print("-" * 72)
    W_diag = portfolio_opt.walk_forward_blend_weights(
        component_returns, benchmark_returns=spy_ret,
        futures_benchmark_returns=fut_index_ret,
        formation_window=FORMATION, rebalance_freq=REBAL,
        beta_constraint=BETA_CONSTRAINT, method="min_var",
        seed=SEED, n_grid=DIAG_N_GRID)
    _, turnover_diag, net_diag = blend_series(
        component_returns, W_diag, TC_EQUITY, SL_EQUITY)
    diag = evaluate_blend(net_diag, index, spy_ret,
                               TC_EQUITY, SL_EQUITY, W_diag)
    print(f"  OOS Sharpe (c2c) = {diag['oos_sharpe']:.3f} "
          f"beta = {diag['equity_beta']:+.4f} "
          f"turnover = {diag['turnover']:.4f} "
          f"bear Sharpe = {diag['bear_sharpe']:+.3f}")
    print(f"  [overlay effect] OOS Sharpe delta = "
          f"{diag['oos_sharpe'] - primary['oos_sharpe']:+.3f} "
          f"(in-sample Sharpe: {primary['is_sharpe']:.3f} "
          f"-> {diag['is_sharpe']:.3f})")

    # ---- FE2: OOS variance reduction vs 1/N ----
    print("\n" + "-" * 72)
    print("FE2: Out-of-sample variance reduction vs 1/N "
          "(pre-registered falsification, re-defined for "
          "min_variance)")
    print("-" * 72)
    fe2 = fe2_variance_reduction(
        component_returns, net, W, index, spy_ret)
    print(f"  OOS annualized variance: opt={fe2['oos_annualized_variance_opt']:.5f} "
          f"1/N={fe2['oos_annualized_variance_1n']:.5f} "
          f"ratio={fe2['oos_variance_ratio']:.3f} (need <= 0.90)")
    print(f"  Mean per-fold variance ratio: "
          f"{fe2['mean_per_fold_variance_ratio']:.3f}")
    print(f"  [context] in-sample Sharpe edge vs 1/N: "
          f"{fe2['context_in_sample_sharpe_edge_vs_1n']:+.3f} "
          f"(min_var expected below 1/N in-sample)")
    print(f"  FE2: {'NOT FALSIFIED (passed)' if fe2.get('passed', False) else 'FALSIFIED'}")

    # ---- Placebo: beta-constrained (primary G2) ----
    print("\n" + "-" * 72)
    print(f"BETA-CONSTRAINED placebo null ({n_sim} sims, "
          f"Dirichlet(1) draws projected onto the "
          f"beta<={BETA_CONSTRAINT} cap at each rebalance)")
    print("-" * 72)
    rng = np.random.default_rng(SEED)
    cplacebo_net = []
    for sim in range(n_sim):
        pw = portfolio_opt.portfolio_placebo_weights_beta_constrained(
            component_returns, formation_window=FORMATION,
            benchmark_returns=spy_ret,
            futures_benchmark_returns=fut_index_ret,
            beta_constraint=BETA_CONSTRAINT,
            n_simulations=1, seed=int(rng.integers(1 << 30)),
            rebalance_freq=REBAL)[0]
        _, _, pnet = blend_series(
            component_returns, pw, TC_EQUITY, SL_EQUITY)
        folds, _ = fold_metrics(pnet, index, spy_ret)
        sh = [m["sharpe"] for m in folds
              if m.get("sharpe") is not None
              and not np.isnan(m.get("sharpe", float("nan")))]
        cplacebo_net.append(float(np.mean(sh)) if sh else 0.0)
    cpm = float(np.mean(cplacebo_net))
    cps = float(np.std(cplacebo_net))
    cz = (primary["oos_sharpe"] - cpm) / cps if cps > 0 else float("nan")
    print(f"  Placebo OOS Sharpe: mean={cpm:.3f} std={cps:.3f} "
          f"min={min(cplacebo_net):.3f} max={max(cplacebo_net):.3f}")
    print(f"  Placebo z = {cz:.2f} (need >= {GATES['G2_placebo_z_gte_3.0']})")

    # ---- Diagnostic: unconstrained Dirichlet placebo ----
    print("\n" + "-" * 72)
    print(f"Diagnostic: UNCONSTRAINED placebo null "
          f"({n_sim} sims, Dirichlet(1) component weights "
          f"per rebalance) - biased against the constraint")
    print("-" * 72)
    rng = np.random.default_rng(SEED)
    placebo_net = []
    for sim in range(n_sim):
        pw = portfolio_opt.portfolio_placebo_weights(
            component_returns, n_simulations=1, seed=int(rng.integers(1 << 30)),
            rebalance_freq=REBAL)[0]
        _, _, pnet = blend_series(component_returns, pw, TC_EQUITY, SL_EQUITY)
        folds, _ = fold_metrics(pnet, index, spy_ret)
        sh = [m["sharpe"] for m in folds
              if m.get("sharpe") is not None
              and not np.isnan(m.get("sharpe", float("nan")))]
        placebo_net.append(float(np.mean(sh)) if sh else 0.0)
    pm = float(np.mean(placebo_net))
    ps = float(np.std(placebo_net))
    uz = (primary["oos_sharpe"] - pm) / ps if ps > 0 else float("nan")
    print(f"  Placebo OOS Sharpe: mean={pm:.3f} std={ps:.3f} "
          f"min={min(placebo_net):.3f} max={max(placebo_net):.3f}")
    print(f"  Placebo z = {uz:.2f} (diagnostic only)")

    # ---- Cost sweep ----
    print("\n" + "-" * 72)
    print("Cost sweep (portfolio-level turnover cost)")
    print("-" * 72)
    cost_rows = []
    for name, tc, sl in COST_SWEEP:
        _, _, cnet = blend_series(component_returns, W, tc, sl)
        res = evaluate_blend(cnet, index, spy_ret, tc, sl, W)
        cost_rows.append({
            "sweep": name, "tc_cost": tc, "slippage": sl,
            "oos_sharpe": res["oos_sharpe"], "turnover": res["turnover"],
            "equity_beta": res["equity_beta"],
            "bear_sharpe": res["bear_sharpe"],
            "positive_folds": res["positive_folds"],
        })
        print(f"  {name:<18} OOS Sharpe={res['oos_sharpe']:.3f} "
              f"beta={res['equity_beta']:+.4f} turn={res['turnover']:.4f}")

    # ---- Component attribution ----
    print("\n" + "-" * 72)
    print("Component attribution")
    print("-" * 72)
    attribution = component_attribution(
        component_returns, spy_ret, W, None)
    print(f"  {'component':<16} {'OOS Sh':>8} {'beta':>8} "
          f"{'mean w':>8} {'w range':>16}")
    for col, v in attribution.items():
        print(f"  {col:<16} {v['standalone_oos_sharpe']:>+8.3f} "
              f"{v['equity_beta']:>+8.3f} {v['mean_blend_weight']:>8.3f} "
              f"[{v['min_blend_weight']:.2f},{v['max_blend_weight']:.2f}]")

    # ---- Split-half stability (pre-registered robustness) ----
    print("\n" + "-" * 72)
    print("Split-half stability of the min-variance weights "
          "(reported, not gated)")
    print("-" * 72)
    stability = split_half_stability(
        component_returns, spy_ret, fut_index_ret)
    cmp_ = stability["comparison"]
    print(f"  First-half  OOS Sharpe = "
          f"{stability['first_half']['oos_sharpe']:.3f}  "
          f"mean weights = "
          + ", ".join(f"{c}={v:.3f}" for c, v in
                       stability["first_half"]["mean_component_weights"].items()))
    print(f"  Second-half OOS Sharpe = "
          f"{stability['second_half']['oos_sharpe']:.3f}  "
          f"mean weights = "
          + ", ".join(f"{c}={v:.3f}" for c, v in
                       stability["second_half"]["mean_component_weights"].items()))
    print(f"  L1 distance (mean weights) = "
          f"{cmp_['l1_distance_mean_weights']:.3f}  "
          f"Spearman rank corr = "
          f"{cmp_['spearman_rank_corr_mean_weights']:+.3f}")

    # ---- Pre-registered promotion gates ----
    print("\n" + "-" * 72)
    print("Pre-registered promotion gates (primary config, "
          "beta-constrained placebo)")
    print("-" * 72)
    gate_checks = {
        "G1_oos_sharpe_gte_0.8": bool(
            primary["oos_sharpe"] >= GATES["G1_oos_sharpe_gte_0.8"]),
        "G2_placebo_z_gte_3.0": bool(cz >= GATES["G2_placebo_z_gte_3.0"]),
        "G3_abs_beta_vs_spy_lte_0.1": bool(
            abs(primary["equity_beta"]) <= GATES["G3_abs_beta_vs_spy_lte_0.1"]),
        "G4_bear_sharpe_gt_0": bool(
            primary["bear_sharpe"] > GATES["G4_bear_sharpe_gt_0"]),
        "G5_turnover_lte_0.15": bool(
            primary["turnover"] <= GATES["G5_turnover_lte_0.15"]),
    }
    for g, ok in gate_checks.items():
        print(f"  {g:<32} {'PASS' if ok else 'FAIL'}")
    print(f"  [diag] full-sample equity beta = "
          f"{primary['equity_beta']:+.4f}  "
          f"OOS equity beta = {primary['oos_equity_beta']:+.4f} "
          f"(gate bar <= {GATES['G3_abs_beta_vs_spy_lte_0.1']})")
    print(f"  [diag] unconstrained placebo z = {uz:.2f} "
          f"(diagnostic only; the constrained z = {cz:.2f} "
          f"is the pre-registered G2)")
    gate_checks["all_passed"] = all(
        v for k, v in gate_checks.items() if k != "all_passed")
    n_pass = sum(1 for k, v in gate_checks.items()
                 if k != "all_passed" and v)
    print(f"  Gates passed: {n_pass}/5")

    # ---- Sensitivity grid ----
    sens = None
    sens_mn_summary = None
    if not args.no_sensitivity:
        print("\n" + "-" * 72)
        print("Sensitivity grid (reported, not gated)")
        print("-" * 72)
        sens = sensitivity_grid(
            component_returns, spy_ret, fut_index_ret, index, spy_ret)
        best = max(sens, key=lambda r: r["oos_sharpe"])
        print(f"  {len(sens)} configs; best OOS Sharpe="
              f"{best['oos_sharpe']:.3f} "
              f"({best['method']}, beta<={best['beta_constraint']}, "
              f"{best['rebalance_freq']}d, {best['component_set']})")
        by_method = {}
        for r in sens:
            by_method.setdefault(r["method"], []).append(r["oos_sharpe"])
        for m, vals in by_method.items():
            print(f"    {m:<12} mean OOS={np.mean(vals):.3f} "
                  f"max={max(vals):.3f}")
        # Market-neutral (|beta|<=0.1) configs that also clear the
        # Sharpe gate - exploratory, multiple-testing-aware, NOT
        # promoted (the pre-registration forbids post-hoc
        # selection from this grid).
        mn = [r for r in sens
              if abs(r["equity_beta"]) <= BETA_CONSTRAINT
              and r["oos_sharpe"] >= GATES["G1_oos_sharpe_gte_0.8"]]
        mn = sorted(mn, key=lambda r: -r["oos_sharpe"])
        sens_mn_summary = {
            "n_configs_total": len(sens),
            "n_market_neutral_and_sharpe_gte_0.8": len(mn),
            "multiple_testing_note": (
                f"{len(mn)} of {len(sens)} pre-registered sensitivity "
                "configs achieve |beta vs SPY| <= 0.1 with OOS Sharpe "
                ">= 0.8. These are EXPLORATORY (the grid is reported, "
                "not gated); selecting any of them for promotion would "
                "be post-hoc multiple-testing and requires a dedicated "
                "pre-registered confirmatory run with a full placebo "
                "test (G2) before any promotion."),
            "top_configs": mn[:8],
        }
        if mn:
            top = mn[0]
            print(f"  [exploratory] {len(mn)}/{len(sens)} configs are "
                  f"market-neutral (|beta|<=0.1) with OOS>=0.8; "
                  f"strongest: {top['method']} beta<={top['beta_constraint']} "
                  f"{top['rebalance_freq']}d {top['component_set']} "
                  f"OOS={top['oos_sharpe']:.3f} beta={top['equity_beta']:+.3f} "
                  f"(NOT promoted - requires confirmatory run)")

    # ---- Decision ----
    print("\n" + "=" * 72)
    print("E042 Decision")
    print("=" * 72)
    # The hypothesis is "a market-neutral TOTAL portfolio with a
    # significant edge": G1 (OOS Sharpe >= 0.8) and G3 (|beta| <=
    # 0.1) are the defining requirements, G2 (placebo z >= 3) the
    # significance bar, G4/G5 secondary. VALIDATED requires all
    # five; PARTIAL requires the two defining gates (G1 and G3);
    # REJECTED otherwise.
    defining_pass = gate_checks["G1_oos_sharpe_gte_0.8"] and \
        gate_checks["G3_abs_beta_vs_spy_lte_0.1"]
    decision = "VALIDATED" if gate_checks["all_passed"] else (
        "PARTIAL" if defining_pass else "REJECTED")
    print(f"  Gates: {n_pass}/5 -> {decision}")
    print(f"  Defining gates (G1 Sharpe, G3 market-neutral): "
          f"{'BOTH PASS' if defining_pass else 'NOT both pass'}")
    print(f"  FE1 (diversification): "
          f"{'PASS' if fe1['passed'] else 'FAIL'} "
          f"({fe1['pair_frac_pass']*100:.0f}% pairs)")
    print(f"  FE2 (OOS variance reduction vs 1/N): "
          f"{'PASS' if fe2.get('passed', False) else 'FAIL'} "
          f"(var ratio {fe2.get('oos_variance_ratio', float('nan')):.3f})")
    print(f"  Placebo z (beta-constrained, primary) = {cz:.2f}")
    print(f"  Placebo z (unconstrained, diagnostic) = {uz:.2f}")
    print(f"  [diag] Dirichlet-grid overlay (n_grid=2000) "
          f"OOS Sharpe = {diag['oos_sharpe']:.3f} "
          f"(primary n_grid=0 = {primary['oos_sharpe']:.3f})")

    # ---- Save ----
    result = {
        "experiment": "E042",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "description": (
            "Walk-forward optimized market-neutral blend of the "
            "five validated components (equity TSM pure, equity "
            "DN low-beta, futures TSM 18m, futures realized-roll-"
            "yield carry, macro momentum). Close-to-close "
            "convention, class-appropriate base costs, 504-day "
            "formation / 21-day rebalance / 63-day step."),
        "seed": SEED,
        "convention": "close-to-close (v1.2.3 primary)",
        "execution_fidelity_note": (
            "The first E042 execution (committed 2026-10-13 "
            "00:55Z) ran the primary with n_grid=2000, which "
            "adds a seeded Dirichlet(1) grid that selects the "
            "max-Sharpe feasible draw - turning min_var into an "
            "in-sample random search that does NOT replicate the "
            "E041 sensitivity-grid config (n_grid=0) that "
            "produced the 0.979 lead. This corrected re-run uses "
            "n_grid=0 as the pre-registered primary (faithful "
            "replication of the config under test) and keeps the "
            "n_grid=2000 variant as a reported diagnostic. The "
            "G2 placebo is the pre-registered BETA-CONSTRAINED "
            "null (Dirichlet draws projected onto the beta<=0.05 "
            "cap); the unconstrained placebo is a diagnostic. FE2 "
            "is the pre-registered OOS variance reduction vs 1/N "
            "(re-defined for min_variance per the E042 task "
            "spec), not the E041 in-sample Sharpe edge."),
        "costs": {
            "equity_macro": {"tc_cost": TC_EQUITY, "slippage": SL_EQUITY},
            "futures": {"tc_cost": TC_FUTURES, "slippage": SL_FUTURES},
            "portfolio_turnover_primary": {"tc_cost": TC_EQUITY, "slippage": SL_EQUITY},
        },
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP,
                         "formation_window": FORMATION,
                         "rebalance_freq": REBAL, "warmup_days": WARMUP},
        "pre_registered": {
            "primary_method": "min_var",
            "primary_n_grid": PRIMARY_N_GRID,
            "beta_constraint": BETA_CONSTRAINT,
            "beta_constraints": ("|beta vs SPY| <= 0.05 AND |beta vs "
                                 "equal-weight de-seamed futures index| <= 0.05"),
            "optimizer": ("Ledoit-Wolf (2004) shrinkage covariance "
                          "(scaled-identity target), ridge lambda=1e-4, "
                          "SLSQP (n_grid=0: no Dirichlet grid overlay - "
                          "faithful replication of the E041 grid config)"),
            "constraints": "long-only component weights, sum=1",
            "gates": {k: v for k, v in GATES.items()},
            "falsification_expectations": {
                "FE1": ("pairwise |corr| <= 0.5 for >= 80% of the 10 "
                        "component pairs (full-sample)"),
                "FE2": ("OOS annualized variance(opt) <= 0.90 * OOS "
                        "annualized variance(1/N) over the union of test "
                        "folds (re-defined for min_variance per the E042 "
                        "task spec; the E041 in-sample Sharpe edge does "
                        "not apply because min_var is expected to be "
                        "below 1/N in-sample by construction)"),
            },
            "placebo": (f"{n_sim} sims; Dirichlet(1) component-weight "
                        "draws PROJECTED onto the beta<=0.05 cap via "
                        "SLSQP/LP at each rebalance (beta-constrained "
                        "component-permutation null, matched to the "
                        "constraint), same rebalance/execution/cost "
                        "structure"),
            "sensitivity_grid": {
                "method": SENS_METHODS, "beta_constraint": SENS_BETA,
                "rebalance_freq": SENS_REBAL, "component_set": list(SENS_SETS.keys()),
                "note": "reported, not gated; no post-hoc selection",
            },
            "cost_sweep": [c[0] for c in COST_SWEEP],
            "robustness": [
                "cost sweep {0, base, 10+5, 20+5}bps",
                "component-set ablation (all-5 vs macro-inclusive-3) via the sensitivity grid",
                "split-half stability of the min-variance weights",
                "unconstrained Dirichlet placebo (diagnostic)",
                "Dirichlet-grid overlay n_grid=2000 (diagnostic)",
            ],
            "implementation_gaps": [
                "5 components (not 'many assets'); 1/N is the natural null",
                "US-only 2015-2026 warm-up-truncated sample",
                "components are validated strategies with embedded internal costs, not raw factors",
            ],
        },
        "universe": {
            "equity": "large_liquid (130 tickers)",
            "futures": list(FUTURES_UNIVERSE.keys()),
            "macro": ["SPY", "IEF", "GLD"],
            "macro_themes": ["growth", "trade", "policy", "sentiment", "inflation"],
            "n_days_common": int(len(index)),
            "start": str(index[0].date()),
            "end": str(index[-1].date()),
        },
        "fe1_diversification": fe1,
        "fe2_variance_reduction": fe2,
        "primary": primary,
        "diagnostic_dirichlet_grid_overlay": {
            "n_grid": DIAG_N_GRID,
            "note": ("NOT the pre-registered primary. The "
                      "seeded Dirichlet(1) grid selects the "
                      "max-Sharpe feasible draw, turning "
                      "min_var into an in-sample random search. "
                      "This is the estimator the first E042 "
                      "execution (2026-10-13 00:55Z) used by "
                      "mistake; kept as a diagnostic to "
                      "quantify the overlay's OOS cost."),
            "metrics": diag,
            "oos_sharpe_delta_vs_primary": float(
                diag["oos_sharpe"] - primary["oos_sharpe"]),
        },
        "convention_findings": {
            "dn_lowbeta_c2c_equity_beta": attribution.get(
                "dn_lowbeta", {}).get("equity_beta"),
            "dn_lowbeta_overnight_equity_beta_e012": -0.035,
            "finding": (
                "The dollar_neutral_longshort_weights construction "
                "(used as-is per the pre-registered component spec) "
                "is market-neutral under the OVERNIGHT convention "
                "(beta -0.035, the convention under which E012/E013 "
                "validated it) but carries a large POSITIVE equity "
                "beta under the v1.2.3 close-to-close convention "
                "(beta ~ +1.0). E024 audited the dn_lowbeta Sharpe "
                "under both conventions (c2c 1.053 / overnight 1.289) "
                "but did not re-measure its beta under c2c. This "
                "convention-dependence is a primary reason the blend "
                "cannot reach |beta vs SPY| <= 0.1 out-of-sample: the "
                "component believed to be a market-neutral diversifier "
                "is a high-beta equity sleeve under c2c."),
            "dollar_neutral_longshort_weights_direction": (
                "As implemented, dollar_neutral_longshort_weights "
                "sizes the k largest rank-percentiles long and the k "
                "smallest short; under rank(ascending=False) the "
                "largest signal maps to the smallest percentile, so the "
                "book is long the smallest-signal (highest-beta) names "
                "and short the largest-signal (lowest-beta) names - the "
                "reverse of the docstring's 'long the top by signal' and "
                "of the low-beta strategy intent. Used as-is (pre-"
                "registered); recorded here because it determines the "
                "component's c2c beta sign."),
        },
        "placebo_constrained": {
            "definition": ("Beta-constrained component-permutation "
                            "null (PRIMARY G2): Dirichlet(1) draws "
                            "projected onto the beta<=0.05 cap at each "
                            "rebalance via SLSQP/LP, same "
                            "rebalance/execution/cost structure"),
            "mean": cpm, "std": cps, "n_sim": n_sim,
            "z_score": float(cz),
            "min": float(min(cplacebo_net)),
            "max": float(max(cplacebo_net)),
        },
        "placebo_unconstrained": {
            "definition": ("Unconstrained Dirichlet(1) null "
                            "(DIAGNOSTIC): biased against the "
                            "constraint - a negative z measures the "
                            "Sharpe cost of the market-neutrality "
                            "constraint, not a lack of component edge"),
            "mean": pm, "std": ps, "n_sim": n_sim,
            "z_score": float(uz),
            "min": float(min(placebo_net)),
            "max": float(max(placebo_net)),
        },
        "cost_sweep": cost_rows,
        "component_attribution": attribution,
        "split_half_stability": stability,
        "promotion_gates": gate_checks,
        "gates_passed_count": n_pass,
        "decision": decision,
        "sensitivity_market_neutral_summary": sens_mn_summary,
        "component_weights_daily": {
            "dates": [str(d.date()) for d in W.index],
            "components": list(W.columns),
            "weights": [[float(v) for v in W.iloc[i]]
                        for i in range(len(W))],
        },
    }

    # The canonical golden path is reserved for the full pre-registered
    # config (n_sim=PLACEBO_N with the sensitivity grid). Quick and
    # diagnostic runs default to a *_quick.json path so a --n-sim 2
    # verification run cannot silently overwrite the release golden
    # (that exact corruption occurred once and had to be reverted from
    # the v1.2.3 tag).
    full_config = (n_sim == PLACEBO_N) and (not args.no_sensitivity)
    if args.out:
        out_path = args.out
    elif full_config:
        out_path = os.path.join("experiments", "e042_minvar_market_neutral.json")
    else:
        out_path = os.path.join(
            "experiments", "e042_minvar_market_neutral_quick.json")
        print("NOTE: quick (non-primary) configuration - writing to "
              f"{out_path}; the release golden "
              "(experiments/e042_minvar_market_neutral.json) is NOT "
              "overwritten. Run with --n-sim 50 and no --no-sensitivity "
              "to regenerate the canonical golden, or pass --out to "
              "override the output path.")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")

    # Sensitivity saved separately if computed (keeps the main JSON light).
    if sens is not None:
        sens_path = os.path.join(
            "experiments", "e042_sensitivity_grid.json")
        with open(sens_path, "w") as f:
            json.dump({
                "experiment": "E042-sensitivity",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "seed": SEED,
                "n_configs": len(sens),
                "grid": sens,
            }, f, indent=2, default=str)
        print(f"Saved sensitivity grid to {sens_path}")


if __name__ == "__main__":
    main()
