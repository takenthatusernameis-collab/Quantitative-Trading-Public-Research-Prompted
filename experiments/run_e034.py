#!/usr/bin/env python
"""E034: Cross-asset TSM revisit (de-risked ETF universe, rank-preserving placebo)."""

import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, strategies

SEED = 42
np.random.seed(SEED)

DE_RISKED_ETFS = [
    "TLT", "IEF", "LQD", "HYG", "GLD", "DBC", "VNQ", "EEM", "EFA", "SPY",
]

TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
VOL_WINDOW = 63
LOOKBACK = 252
SKIP = 21
TC_COST = 0.0005
SLIPPAGE = 0.0002
N_PLACEBO = 50

close = None
spy = None


def load_data():
    global close, spy
    df = data.download(DE_RISKED_ETFS, start="2014-01-01", end="2026-10-11")
    close_df = data.get_panel(df, "Close").dropna(how="all")
    bm = data.get_benchmark("SPY", start="2014-01-01")
    spy_s = bm["close"].reindex(close_df.index).ffill()
    close = close_df
    spy = spy_s
    return close, spy


def beta_vs_benchmark(net_ret, bench_s):
    bench = bench_s.pct_change().reindex(net_ret.index).ffill()
    y = net_ret.values
    x = bench.values
    mask = (~np.isnan(y)) & (~np.isnan(x))
    if mask.sum() < 3:
        return float("nan"), float("nan"), float("nan")
    y2 = y[mask]
    x2 = x[mask]
    if np.std(x2) == 0:
        return float("nan"), float("nan"), float("nan")
    A = np.vstack([np.ones(len(x2)), x2]).T
    try:
        alpha, beta = np.linalg.lstsq(A, y2, rcond=None)[0]
    except Exception:
        beta = np.cov(y2, x2, bias=True)[0, 1] / (np.var(x2) + 1e-18)
        alpha = np.mean(y2) - beta * np.mean(x2)
    try:
        corr = float(np.corrcoef(y2, x2)[0, 1])
    except Exception:
        corr = float("nan")
    return float(beta), float(alpha * 252), corr


def fe1_check():
    signal = close.pct_change(LOOKBACK).shift(SKIP)
    next_ret = close.pct_change(REBAL)
    spears = []
    for i in range(len(signal.index) - REBAL):
        s = signal.iloc[i]
        nr = next_ret.iloc[i + REBAL]
        common = s.dropna().index.intersection(nr.dropna().index)
        if len(common) >= 2:
            try:
                spears.append(s.loc[common].corr(nr.loc[common], method="spearman"))
            except Exception:
                pass
    if len(spears) == 0:
        return 0.0, 0.0, 0
    spears = np.array(spears)
    return float(np.mean(np.abs(spears))), float(np.mean(spears > 0)), len(spears)


def wf_metrics(long_only=True):
    signal = close.pct_change(LOOKBACK).shift(SKIP)
    w = backtest.time_series_momentum_weights(signal, close, long_only=long_only, vol_window=VOL_WINDOW)
    rets = backtest.portfolio_returns_close_to_close(w, close, tc_cost=TC_COST, slippage=SLIPPAGE)
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    oos_sharpes = []
    folds = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        rtest = rets["net"].loc[rets["net"].index.intersection(test_idx)]
        m = backtest.metrics(rtest) if len(rtest) > 0 else {}
        if not m or m.get("n_days", 0) == 0:
            m = {"sharpe": float("nan"), "annual_return": float("nan"), "annual_vol": float("nan"),
                 "max_drawdown": float("nan"), "total_return": float("nan"), "win_rate": float("nan"), "n_days": 0}
        m["fold"] = i
        oos_sharpes.append(m["sharpe"])
        folds.append(m)
    return folds, oos_sharpes, rets


def rank_preserving_placebo(n_sim=50):
    signal = close.pct_change(LOOKBACK).shift(SKIP)
    sharps = []
    rng = np.random.default_rng(SEED)
    for _ in range(n_sim):
        sig_perm = signal.copy()
        for date in signal.index:
            row = signal.loc[date].dropna()
            if len(row) == 0:
                continue
            ordered = row.sort_values()
            new_idx = rng.permutation(ordered.index)
            new_row = pd.Series(ordered.values, index=new_idx)
            sig_perm.loc[date, new_row.index] = new_row.values
        w = backtest.time_series_momentum_weights(sig_perm, close, long_only=True, vol_window=VOL_WINDOW)
        rets = backtest.portfolio_returns_close_to_close(w, close, tc_cost=TC_COST, slippage=SLIPPAGE)
        m = backtest.metrics(rets["net"])
        sharps.append(m.get("sharpe", 0.0))
    return {
        "n_sim": n_sim,
        "mean_sharpe": float(np.mean(sharps)),
        "std_sharpe": float(np.std(sharps)),
        "pct_positive": float(np.mean(np.array(sharps) > 0)),
    }

def main():
    load_data()
    print(f"Loaded: {close.shape}, de-risked={list(close.columns)}")
    abs_sp, frac_pos, n = fe1_check()
    print(f"FE1: mean|Spearman|={abs_sp:.4f}, frac_pos={frac_pos:.4f} (n={n})")
    folds, oos_sharpes, rets = wf_metrics(long_only=True)
    oos_mean = float(np.mean([s for s in oos_sharpes if not np.isnan(s)]))
    oos_std = float(np.std([s for s in oos_sharpes if not np.isnan(s)]))
    print(f"OOS WF mean Sharpe={oos_mean:.4f}, std={oos_std:.4f}, pos={sum(1 for s in oos_sharpes if s>0)}/{len(oos_sharpes)}")
    b, a, c = beta_vs_benchmark(rets["net"], spy)
    print(f"beta={b:.4f}, corr={c:.4f}")
    pl = rank_preserving_placebo(n_sim=N_PLACEBO)
    print(f"Placebo ({N_PLACEBO} sims): mean={pl['mean_sharpe']:.4f}, std={pl['std_sharpe']:.4f}")
    z = (oos_mean - pl["mean_sharpe"]) / pl["std_sharpe"] if pl["std_sharpe"] > 0 else float("nan")
    print(f"z={z:.4f}")
    # turnover
    turnover = float((backtest.shift_weights(backtest.time_series_momentum_weights(close.pct_change(LOOKBACK).shift(SKIP), close, long_only=True, vol_window=VOL_WINDOW)).diff().abs()).sum(axis=1).mean())
    # bear regime
    folds_bear = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)):
        test_idx = close.index[te_s:te_e]
        spy_win = spy.reindex(test_idx).pct_change().dropna()
        if len(spy_win) == 0:
            regime = "sideways"
        else:
            spy_win_ret = float(spy_win.sum())
            if spy_win_ret > 0.02:
                regime = "bull"
            elif spy_win_ret < -0.02:
                regime = "bear"
            else:
                regime = "sideways"
        rtest = rets["net"].loc[rets["net"].index.intersection(test_idx)]
        m = backtest.metrics(rtest) if len(rtest) > 0 else {"sharpe": float("nan")}
        folds_bear.append((regime, m.get("sharpe", float("nan"))))
    bear_sharpes = [s for r, s in folds_bear if r == "bear" and not np.isnan(s)]
    bear_mean = float(np.mean(bear_sharpes)) if bear_sharpes else float("nan")
    out = {
        "experiment": "E034",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "universe": DE_RISKED_ETFS,
        "fe1": {
            "mean_abs_spearman": abs_sp,
            "frac_positive": frac_pos,
            "n_dates": n,
            "fe1_gate_mean_abs_ge_0_03": abs_sp >= 0.03,
            "fe1_gate_frac_pos_ge_0_60": frac_pos >= 0.60,
        },
        "oos": {
            "mean_sharpe": oos_mean,
            "std_sharpe": oos_std,
            "n_pos_folds": sum(1 for s in oos_sharpes if s > 0),
            "n_folds": len(oos_sharpes),
        },
        "beta": {"beta_vs_spy": b, "alpha_annual": a, "corr_spy": c},
        "placebo_rank_preserving": pl,
        "placebo_z": z,
        "turnover_daily": turnover,
        "bear": {"n_bear_folds": len(bear_sharpes), "bear_sharpe_mean": bear_mean},
        "gates": {
            "G1_oos_sharpe_ge_0.8": {"value": oos_mean, "threshold": 0.8, "pass": oos_mean >= 0.8},
            "G2_placebo_z_ge_3.0": {"value": z if not np.isnan(z) else float("nan"), "threshold": 3.0, "pass": (not np.isnan(z) and z >= 3.0)},
            "G3_abs_beta_le_0.2": {"value": abs(b) if not np.isnan(b) else float("nan"), "threshold": 0.2, "pass": (not np.isnan(b) and abs(b) <= 0.2)},
            "G4_bear_sharpe_gt_0": {"value": bear_mean if not np.isnan(bear_mean) else float("nan"), "threshold": 0.0, "pass": (not np.isnan(bear_mean) and bear_mean > 0.0)},
            "G5_turnover_le_0.15": {"value": turnover, "threshold": 0.15, "pass": turnover <= 0.15},
        },
    }
    with open(os.path.join("experiments", "e034_cross_asset_tsm.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("saved experiments/e034_cross_asset_tsm.json")
    for k, v in out["gates"].items():
        print(f"{k}: pass={v['pass']} (val={v['value']})")


if __name__ == "__main__":
    main()
