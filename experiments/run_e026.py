#!/usr/bin/env python
"""E026: Equity carry / dividend-yield factor (Koijen, Moskowitz, Pedersen & Vrugt 2018)."""
import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.run_experiment import deterministic_timestamp
from src import jsonio
from src import data, backtest, carry_equity

SEED = 42
UNIVERSE = [
    "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
    "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
    "BAC","BKNG","BMY","BSX","C","CAT","CCI","CDNS",
    "CHTR","CI","CL","CMCSA","CME","COF","COP","COST","CRM","CSCO",
    "CSX","CVS","CVX","DE","DHR","DIS","DOW","DXCM","EMR","EOG",
    "EQIX","ETN","EXC","FDX","FIS","FTNT","GD","GE","GILD","GM",
    "GOOG","GOOGL","GS","HD","HON","IBM","ICE","INTC","ISRG",
    "JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LLY","LMT","LOW",
    "LRCX","MA","MCD","MDLZ","MDT","META","MET","MMM","MO","MRK",
    "MS","MSFT","MU","NFLX","NKE","NOW","NVDA","ORCL","PCAR","PEP",
    "PFE","PG","PLD","PM","PNC","PYPL","QCOM","REGN","ROST","RTX",
    "SBUX","SCHW","SLB","SO","SPG","T","TGT","TJX","TMO","TMUS",
    "TSLA","TXN","UNH","UNP","UPS","USB","V","VZ","WFC",
    "WMT","XOM",
]
TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
TOP_FRAC = 0.2
VOL_WINDOW = 63
YIELD_WINDOW = 252
N_PLACEBO = 50

def load_data():
    df = data.download(UNIVERSE, start="2014-01-01", end="2026-10-11",
                       auto_adjust=False, actions=True)
    close = data.get_panel(df, "Close")
    adj = data.get_panel(df, "Adj Close").dropna(how="all")
    dividends = data.get_panel(df, "Dividends").reindex(columns=adj.columns)
    open_ = data.get_panel(df, "Open").reindex(columns=adj.columns).reindex(adj.index).fillna(adj)
    bm = data.get_benchmark("SPY", start="2014-01-01")
    spy = bm["close"].reindex(adj.index).ffill()
    return adj, dividends, open_, spy

def beta_vs_benchmark(net_ret, bench_ret):
    common = net_ret.index.intersection(bench_ret.index)
    y = net_ret.loc[common].to_numpy()
    x = bench_ret.loc[common].to_numpy()
    if len(y) < 3 or np.std(x) == 0:
        return float("nan"), float("nan"), float("nan")
    A = np.vstack([np.ones(len(x)), x]).T
    alpha, beta_coef = np.linalg.lstsq(A, y, rcond=None)[0]
    corr = float(np.corrcoef(y, x)[0, 1])
    return float(beta_coef), float(alpha * 252), corr

def walk_forward(ret, close, spy_ret):
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    out = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = ret.loc[ret.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        if not m:
            m = {"sharpe": float("nan")}
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(test_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else float("nan")
        if np.isnan(spy_win_ret):
            regime = "sideways"
        elif spy_win_ret > 0.02:
            regime = "bull"
        elif spy_win_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"
        m["regime"] = regime
        out.append(m)
    return out

def regime_summary(fold_metrics):
    res = {}
    for reg in ["bull", "bear", "sideways"]:
        rows = [m for m in fold_metrics if m.get("regime") == reg]
        sh = [m["sharpe"] for m in rows if "sharpe" in m]
        res[reg] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sh)) if sh else float("nan"),
            "sharpe_pos": int(sum(1 for s in sh if s > 0)) if sh else 0,
        }
    return res

def compute_dd(ret):
    ret = ret.dropna()
    if len(ret) == 0: return 0.0
    cum = (1.0 + ret).cumprod()
    dd = cum / cum.cummax() - 1.0
    return float(dd.min())

def executed_turnover(weights, reb=REBAL):
    w = backtest.shift_weights(weights)
    if reb > 1:
        w = backtest._rebalance_weights(w, reb)
    turn = (w.diff().abs()).sum(axis=1)
    return float(turn.mean()) if len(turn) else 0.0

def main():
    np.random.seed(SEED)
    adj, dividends, open_, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)

    # FE1: within-sample predictive content
    sig = carry_equity.dividend_yield_signal(adj, dividends, window=YIELD_WINDOW)
    rets_m = adj.pct_change().shift(-21)  # next-21d return, 21d step approx
    fe1_rhos = []
    fe1_pos = 0
    # sample dates (monthly-ish)
    for i, d in enumerate(sig.index[::REBAL][1:]):
        try:
            s = sig.loc[d]
            rnext = rets_m.loc[d + pd.Timedelta(days=1)] if False else None  # not quite; easier: use actual next rebal
        except Exception:
            pass
    # compute correctly
    fe1_list = []
    for d in sig.index[:-22:REBAL]:
        s = sig.loc[d]
        r = adj.pct_change(21).shift(-21).loc[d]
        common = s.dropna().index.intersection(r.dropna().index)
        if len(common) > 10:
            sr = pd.DataFrame({"s": s[common], "r": r[common]}).corr("spearman").iloc[0,1]
            if np.isfinite(sr):
                fe1_list.append(sr)
    fe1_mean = float(np.mean(np.abs(fe1_list))) if fe1_list else float("nan")
    fe1_frac_pos = float((np.array(fe1_list) > 0).mean()) if fe1_list else float("nan")

    # Primary: dollar-neutral long-short, c2c
    w_dn = carry_equity.carry_equity_weights(sig, adj, vol_window=VOL_WINDOW,
                                             top_frac=TOP_FRAC, long_only=False)
    # rebal monthly
    w_dn_exec = backtest.shift_weights(w_dn)
    w_dn_exec = backtest._rebalance_weights(w_dn_exec, REBAL)
    ret_dn = backtest.portfolio_returns_close_to_close(w_dn_exec, adj, tc_cost=TC_COST,
                                                       slippage=SLIPPAGE, rebalance_freq=REBAL)
    diag_dn = beta_vs_benchmark(ret_dn["net"], spy_ret)
    beta_dn = diag_dn[0]
    dd_dn = compute_dd(ret_dn["net"])
    turn_dn = executed_turnover(w_dn, REBAL)
    fm_dn = walk_forward(ret_dn, adj, spy_ret)
    oos_dn = float(np.mean([m["sharpe"] for m in fm_dn if "sharpe" in m])) if fm_dn else float("nan")
    reg_dn = regime_summary(fm_dn)
    bear_dn = reg_dn["bear"]["sharpe_mean"]

    # Placebo: 50 sims - destroy signal by permuting? or use carry_equity_placebo_weights with seed sequence
    placebo = []
    for i in range(N_PLACEBO):
        pw = carry_equity.carry_equity_placebo_weights(sig, adj, vol_window=VOL_WINDOW,
                                                       top_frac=TOP_FRAC, long_only=False, seed=i+SEED)
        pw = backtest.shift_weights(pw)
        pw = backtest._rebalance_weights(pw, REBAL)
        pr = backtest.portfolio_returns_close_to_close(pw, adj, tc_cost=TC_COST,
                                                       slippage=SLIPPAGE, rebalance_freq=REBAL)
        pm = backtest.metrics(pr["net"])
        placebo.append(pm.get("sharpe", 0.0) if pm else 0.0)
    pmn = float(np.mean(placebo)) if placebo else 0.0
    pstd = float(np.std(placebo)) if placebo else 1.0
    z = (oos_dn - pmn) / pstd if pstd > 0 else float("nan")

    res = {
        "experiment": "E026",
        "timestamp": deterministic_timestamp(),
        "pre_registered": {
            "primary": "dn_longshort",
            "top_frac": TOP_FRAC,
            "yield_window": YIELD_WINDOW,
            "vol_window": VOL_WINDOW,
            "rebalance_freq": REBAL,
            "tc_cost": TC_COST,
            "slippage": SLIPPAGE,
            "convention": "close_to_close",
        },
        "falsification_fe1": {
            "mean_abs_spearman_next21d": fe1_mean,
            "frac_positive": fe1_frac_pos,
            "n_obs": len(fe1_list),
        },
        "dn_longshort": {
            "oos_sharpe": oos_dn,
            "beta_vs_spy": beta_dn,
            "max_dd": dd_dn,
            "turnover": turn_dn,
            "n_folds": len(fm_dn),
            "oos_folds": fm_dn,
            "regime": reg_dn,
            "bear_sharpe": bear_dn,
        },
        "placebo": {
            "n_sims": N_PLACEBO,
            "mean": pmn,
            "std": pstd,
            "z": z,
            "sharpes": placebo,
        },
    }

    out_path = "experiments/e026_equity_carry.json"
    with open(out_path, "w") as f:
        jsonio.dump(res, f, indent=2, default=str)
    print(json.dumps({
        "oos_sharpe": oos_dn,
        "placebo_z": z,
        "beta": beta_dn,
        "turnover": turn_dn,
        "bear_sharpe": bear_dn,
        "fe1_mean_abs": fe1_mean,
        "fe1_frac_pos": fe1_frac_pos,
    }, indent=2))

if __name__ == "__main__":
    main()
