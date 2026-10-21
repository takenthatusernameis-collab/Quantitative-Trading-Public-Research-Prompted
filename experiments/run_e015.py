"""E015: Blend weight optimization + multi-asset universe test.

Extends E014 (blend_tsm_dnlowbeta at fixed 50/50) by:

  Part 1 - Weight optimization: sweep the TSM/DN weight ratio on the
           large_liquid equity universe to find the optimal risk/return
           tradeoff (OOS Sharpe, turnover, beta, maxDD, bear Sharpe,
           placebo z).
  Part 2 - Multi-asset universe: test the blend (and its pure components)
           on a cross-asset ETF + liquid-futures universe to verify the
           market-neutral low-beta anomaly and time-series momentum
           generalize beyond US large-cap equities.

Design:
  - Walk-forward 504/63/63 (42 OOS folds), monthly (21d) rebalance,
    next-day-open execution, tc=0.5bps + slippage=0.2bps.
  - TSM: 12-month lookback, 1-month skip, inverse-vol weighting, long-only.
  - DN low-beta: 252d rolling beta vs SPY, Vasicek shrink 0.5, 10/10 sort,
    dollar-neutral by construction.
  - Components computed once; blended as tsm_w * w_tsm + dn_w * w_dn.
  - Blended placebo null: random TSM + random DN combined at 50/50 (50 sims).
"""

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies, validation, multiasset
from src import jsonio
from src.run_experiment import UNIVERSES, deterministic_timestamp

TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
SEED = 42
PLACEBO_N_SIM = 50

# TSM weight grid; DN weight = 1 - TSM weight.
# Include 0.0 (pure DN) and 1.0 (pure TSM) as bounds.
WEIGHT_GRID = [0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0]

MULTI_ASSET_UNIVERSE = UNIVERSES["multi_asset"]
FUTURES_UNIVERSE = UNIVERSES["futures_only"]


def load_universe(universe, start="2014-01-01"):
    """Download and prepare close/open/benchmark data for a universe."""
    df = data.download(universe, start=start)
    close = data.get_panel(df, "Close")
    # drop tickers that failed to download (all-NaN columns)
    close = close.dropna(axis=1, how="all")
    # drop dates with no data at all
    close = close.dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start=start)
    spy = data.get_panel(bm, "Close").dropna(how="all")["SPY"].reindex(close.index).ffill()
    return close, open_, spy


def market_diagnostics(ret, spy_ret):
    """Full-sample metrics + market-neutrality diagnostics (equity beta, corr)."""
    net = ret["net"].dropna()
    m = backtest.metrics(net)
    common = net.index.intersection(spy_ret.index)
    y = net.loc[common].values
    x = spy_ret.loc[common].values
    if len(y) > 2 and np.std(x) > 0:
        A = np.vstack([np.ones(len(x)), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        alpha, beta_coef = float(coef[0]), float(coef[1])
        corr = float(np.corrcoef(y, x)[0, 1])
    else:
        alpha, beta_coef, corr = float("nan"), float("nan"), float("nan")
    return {
        "sharpe": m.get("sharpe"),
        "annual_return": m.get("annual_return"),
        "annual_vol": m.get("annual_vol"),
        "max_drawdown": m.get("max_drawdown"),
        "total_return": m.get("total_return"),
        "n_days": m.get("n_days"),
        "equity_beta": beta_coef,
        "alpha_annual": alpha * 252,
        "corr_spy": corr,
    }


def walk_forward(ret, close, spy_ret):
    """Walk-forward OOS fold metrics with regime classification."""
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    fold_metrics = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = ret.loc[ret.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(test_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else float("nan")
        if spy_win_ret > 0.02:
            regime = "bull"
        elif spy_win_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"
        m["regime"] = regime
        m["spy_test_return"] = spy_win_ret
        fold_metrics.append(m)
    return fold_metrics, splits


def regime_summary(fold_metrics):
    out = {}
    for regime in ["bull", "bear", "sideways"]:
        rows = [m for m in fold_metrics if m.get("regime") == regime]
        sharps = [m["sharpe"] for m in rows if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        out[regime] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sharps)) if sharps else float("nan"),
            "sharpe_pos": int(sum(1 for s in sharps if s > 0)) if sharps else 0,
        }
    return out


def compute_drawdown(ret):
    ret = ret.dropna()
    if len(ret) == 0:
        return 0.0, 0
    cum = (1.0 + ret).cumprod()
    roll = cum.cummax()
    dd = cum / roll - 1.0
    underwater = int((dd < 0).sum())
    return float(dd.min()), underwater


def compute_components(close, open_, spy):
    """Precompute TSM and DN weights once for efficient weight-grid evaluation."""
    tsm_signal = strategies.time_series_momentum_pure(close, lookback=12, skip=1)
    tsm_w = backtest.time_series_momentum_weights(
        tsm_signal, close, long_only=True, vol_window=63
    )
    beta = strategies.beta_factor(close, spy, window=252, skip=1, shrink=0.5)
    dn_w = backtest.dollar_neutral_longshort_weights(-beta, top_frac=0.1)
    return tsm_w, dn_w


def evaluate_blend(close, open_, spy, tsm_w, dn_w, tsm_weight, dn_weight):
    """Evaluate a blend of precomputed TSM and DN weights."""
    blended_w = tsm_weight * tsm_w + dn_weight * dn_w
    ret = backtest.portfolio_returns_rebalance_clean(
        blended_w, close, open_, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    spy_ret = spy.pct_change().fillna(0.0)
    diag = market_diagnostics(ret, spy_ret)
    fm, splits = walk_forward(ret, close, spy_ret)
    sharpes = [
        m["sharpe"]
        for m in fm
        if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))
    ]
    oos_sharpe = float(np.mean(sharpes)) if sharpes else float("nan")
    oos_std = float(np.std(sharpes)) if sharpes else float("nan")
    turn = backtest.average_turnover(blended_w)
    dd, uw = compute_drawdown(ret["net"])
    reg = regime_summary(fm)
    n_pos = int(sum(1 for m in fm if m.get("sharpe") is not None and m.get("sharpe", 0) > 0))
    return {
        "weights": {"tsm": tsm_weight, "dn": dn_weight},
        "is_sharpe": diag["sharpe"],
        "is_ann_return": diag["annual_return"],
        "is_ann_vol": diag["annual_vol"],
        "oos_sharpe": oos_sharpe,
        "oos_sharpe_std": oos_std,
        "turnover": turn,
        "equity_beta": diag["equity_beta"],
        "corr_spy": diag["corr_spy"],
        "alpha_annual": diag["alpha_annual"],
        "max_drawdown": dd,
        "time_underwater_days": uw,
        "positive_folds": n_pos,
        "n_folds": len(splits),
        "n_tickers": int(close.shape[1]),
        "regime_analysis": reg,
        "fold_metrics": fm,
    }


def blended_placebo(close, open_, spy, tsm_weight=0.5, dn_weight=0.5, n_sim=PLACEBO_N_SIM):
    """Blended placebo null: random TSM + random DN combined at given weights."""
    rng = np.random.default_rng(SEED)
    spy_ret = spy.pct_change().fillna(0.0)
    sharps = []
    for _ in range(n_sim):
        tsm_sig = pd.DataFrame(
            rng.standard_normal(size=close.shape), index=close.index, columns=close.columns,
        )
        tsm_w = backtest.time_series_momentum_weights(
            tsm_sig, close, long_only=True, vol_window=63
        )
        dn_sig = pd.DataFrame(
            rng.standard_normal(size=close.shape), index=close.index, columns=close.columns,
        )
        dn_w = backtest.dollar_neutral_longshort_weights(dn_sig, top_frac=0.1)
        bw = tsm_weight * tsm_w + dn_weight * dn_w
        r = backtest.portfolio_returns_rebalance_clean(
            bw, close, open_, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        fm, _ = walk_forward(r, close, spy_ret)
        s = [m["sharpe"] for m in fm if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        sharps.append(float(np.mean(s)) if s else 0.0)
    pm = float(np.mean(sharps))
    ps = float(np.std(sharps))
    return pm, ps


def weight_grid_experiment():
    """Part 1: Test weight grid on large_liquid universe."""
    print("=" * 70)
    print("E015 Part 1: Blend weight optimization (large_liquid, 132 equities)")
    print("=" * 70)

    close, open_, spy = load_universe(UNIVERSES["large_liquid"])
    print(f"Loaded: {len(close)} days, {close.shape[1]} tickers")

    print("\nPrecomputing TSM and DN component weights...")
    tsm_w, dn_w = compute_components(close, open_, spy)

    print("\nBlended placebo null (50 random TSM+DN combos at 50/50)...")
    pm, ps = blended_placebo(close, open_, spy, tsm_weight=0.5, dn_weight=0.5)
    print(f"  Placebo: mean Sharpe={pm:.3f}  std={ps:.3f}  n_sim={PLACEBO_N_SIM}")

    results = {}
    print("\nWeight grid results:")
    for tw in WEIGHT_GRID:
        dw = 1.0 - tw
        label = f"tsm_{tw:.1f}_dn_{dw:.1f}"
        r = evaluate_blend(close, open_, spy, tsm_w, dn_w, tw, dw)
        z = float((r["oos_sharpe"] - pm) / ps) if ps > 0 else float("nan")
        r["placebo_z"] = z
        r["placebo_mean"] = pm
        r["placebo_std"] = ps
        results[label] = r
        bear_sh = r["regime_analysis"]["bear"]["sharpe_mean"]
        print(
            f"  {label:<18} OOS_Sharpe={r['oos_sharpe']:.3f}  z={z:.2f}  "
            f"turn={r['turnover']:.4f}  beta={r['equity_beta']:.3f}  "
            f"corr={r['corr_spy']:.3f}  maxDD={r['max_drawdown']:.3f}  "
            f"bear_Sh={bear_sh:.3f}  pos={r['positive_folds']}/{r['n_folds']}"
        )

    # Find optimal by OOS Sharpe
    best_label = max(results, key=lambda k: results[k]["oos_sharpe"])
    best = results[best_label]
    print(f"\n  Best by OOS Sharpe: {best_label} (Sharpe={best['oos_sharpe']:.3f})")

    return results, (pm, ps), best_label, best


def multi_asset_experiment():
    """Part 2: Test blend and components on multi-asset universe."""
    print("\n" + "=" * 70)
    print("E015 Part 2: Multi-asset universe test (ETFs + futures)")
    print("=" * 70)

    close, open_, spy = load_universe(MULTI_ASSET_UNIVERSE)
    print(f"Loaded multi-asset: {len(close)} days, {close.shape[1]} tickers")
    print(f"  Tickers: {list(close.columns)}")
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    print(f"  Walk-forward folds: {len(splits)}")

    tsm_w, dn_w = compute_components(close, open_, spy)

    results = {}
    print("\nWeight grid on multi-asset:")
    for tw in [0.3, 0.4, 0.5, 0.6, 0.7]:
        dw = 1.0 - tw
        label = f"tsm_{tw:.1f}_dn_{dw:.1f}"
        r = evaluate_blend(close, open_, spy, tsm_w, dn_w, tw, dw)
        results[label] = r
        bear_sh = r["regime_analysis"]["bear"]["sharpe_mean"]
        print(
            f"  {label:<18} OOS_Sharpe={r['oos_sharpe']:.3f}  "
            f"turn={r['turnover']:.4f}  beta={r['equity_beta']:.3f}  "
            f"corr={r['corr_spy']:.3f}  maxDD={r['max_drawdown']:.3f}  "
            f"bear_Sh={bear_sh:.3f}"
        )

    # Pure components on multi-asset
    for tw_label, tw, dw in [("pure_dn", 0.0, 1.0), ("pure_tsm", 1.0, 0.0)]:
        r = evaluate_blend(close, open_, spy, tsm_w, dn_w, tw, dw)
        results[tw_label] = r
        print(
            f"  {tw_label:<18} OOS_Sharpe={r['oos_sharpe']:.3f}  "
            f"turn={r['turnover']:.4f}  beta={r['equity_beta']:.3f}  "
            f"corr={r['corr_spy']:.3f}  maxDD={r['max_drawdown']:.3f}"
        )

    # Cross-asset breakdown by regime
    best_multi = results.get("tsm_0.5_dn_0.5", {})

    return results, best_multi


def futures_only_experiment():
    """Part 2b: Test blend at 50/50 on a futures-only universe."""
    print("\n" + "-" * 60)
    print("E015 Part 2b: Futures-only universe test (12 liquid futures)")
    print("-" * 60)

    close, open_, spy = load_universe(FUTURES_UNIVERSE)
    print(f"Loaded futures: {len(close)} days, {close.shape[1]} tickers")
    print(f"  Tickers: {list(close.columns)}")
    if close.shape[1] < 5:
        print("  Too few tickers; skipping futures-only test.")
        return {}

    tsm_w, dn_w = compute_components(close, open_, spy)
    r = evaluate_blend(close, open_, spy, tsm_w, dn_w, 0.5, 0.5)
    print(
        f"  futures_blend_50/50   OOS_Sharpe={r['oos_sharpe']:.3f}  "
        f"turn={r['turnover']:.4f}  beta={r['equity_beta']:.3f}  "
        f"corr={r['corr_spy']:.3f}  maxDD={r['max_drawdown']:.3f}"
    )
    return {"futures_blend_50_50": r}


def main():
    print("=" * 70)
    print("E015: Blend Weight Optimization + Multi-Asset Universe Test")
    print("=" * 70)

    # ---- Part 1: Weight grid on large_liquid ----
    grid_results, (pm, ps), best_label, best = weight_grid_experiment()

    # ---- Part 2: Multi-asset universe ----
    multi_results, best_multi = multi_asset_experiment()

    # ---- Part 2b: Futures-only ----
    futures_results = futures_only_experiment()

    # ---- Summary ----
    print("\n" + "=" * 70)
    print("E015 Summary")
    print("=" * 70)
    print(f"\nWeight optimization (large_liquid):")
    print(f"  Best weight: {best_label}  OOS Sharpe={best['oos_sharpe']:.3f}  "
          f"z={best['placebo_z']:.2f}  turn={best['turnover']:.4f}  "
          f"beta={best['equity_beta']:.3f}")
    if best_label != "tsm_0.5_dn_0.5":
        print(f"  (E014 baseline 50/50: Sharpe={grid_results['tsm_0.5_dn_0.5']['oos_sharpe']:.3f})")
    print(f"\nMulti-asset (large_liquid -> cross-asset):")
    if "tsm_0.5_dn_0.5" in multi_results:
        r = multi_results["tsm_0.5_dn_0.5"]
        print(f"  50/50 blend: OOS Sharpe={r['oos_sharpe']:.3f}  turn={r['turnover']:.4f}  "
              f"beta={r['equity_beta']:.3f}  corr={r['corr_spy']:.3f}")

    # ---- Save ----
    result = {
        "experiment": "E015",
        "timestamp": deterministic_timestamp(),
        "description": "Blend weight optimization (TSM/DN ratio grid) + multi-asset universe test.",
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP},
        "rebalance_freq_days": REBAL,
        "tsm_config": {"lookback_months": 12, "skip_months": 1, "vol_window": 63, "long_only": True},
        "dn_config": {"beta_window": 252, "shrink": 0.5, "top_frac": 0.1, "lag": 1},
        "weight_optimization": {
            "universe": "large_liquid",
            "n_tickers": len(UNIVERSES["large_liquid"]),
            "grid": WEIGHT_GRID,
            "placebo": {"mean": pm, "std": ps, "n_sim": PLACEBO_N_SIM, "type": "blended (random TSM + random DN, 50/50)"},
            "results": grid_results,
            "best_label": best_label,
            "best": {k: v for k, v in best.items() if k != "fold_metrics"},
        },
        "multi_asset": {
            "universe": MULTI_ASSET_UNIVERSE,
            "n_tickers_requested": len(MULTI_ASSET_UNIVERSE),
            "n_tickers_downloaded": multi_results.get("tsm_0.5_dn_0.5", {}).get("n_tickers", 0),
            "results": {k: {kk: vv for kk, vv in v.items() if kk != "fold_metrics"} for k, v in multi_results.items()},
            "futures_only": {k: {kk: vv for kk, vv in v.items() if kk != "fold_metrics"} for k, v in futures_results.items()},
        },
    }

    out_path = os.path.join("experiments", "e015_blend_optimization.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        jsonio.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
