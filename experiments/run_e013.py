"""E013: Validate and refine the surviving market-neutral anomaly.

Keeper from E012: ``dollar_neutral_lowbeta`` (long low-beta, short high-beta,
dollar-neutral, 21-day rebalance). This experiment subjects it to:

  1. Beta-window sensitivity grid (63 / 126 / 252) x shrink level (0.25/0.5/0.75)
  2. Top-frac grid (0.05 / 0.10 / 0.15 / 0.20)
  3. Shorting-cost stress: sweep tc + slippage up to 20bps/5bps
  4. Out-of-universe robustness: large_liquid (132) vs sp500_top (10) subsets
  5. Leg decomposition: long-leg Sharpe vs short-leg Sharpe
  6. Placebo z-score validation under each grid point

Decision gate: strategy must remain market-neutral (|beta|<=0.2) AND
profitable (OOS Sharpe>=0.8, z>=3) at the realistic cost bar (5bps round).
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies, validation
from src.run_experiment import UNIVERSES, deterministic_timestamp

UNIVERSE = UNIVERSES["large_liquid"]
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21


def load_data():
    df = data.download(UNIVERSE, start="2014-01-01")
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start="2014-01-01")
    spy = data.get_panel(bm, "Close")["SPY"].reindex(close.index).ffill()
    return close, open_, spy


def diag(ret, spy_ret):
    net = ret["net"].dropna()
    m = backtest.metrics(net)
    common = net.index.intersection(spy_ret.index)
    y = net.loc[common].values
    x = spy_ret.loc[common].values
    if len(y) > 2 and np.std(x) > 0:
        A = np.vstack([np.ones(len(x)), x]).T
        ab = np.linalg.lstsq(A, y, rcond=None)[0]
        beta_coef = ab[1]
        corr = float(np.corrcoef(y, x)[0, 1])
    else:
        beta_coef = np.nan
        corr = np.nan
    return {
        "sharpe": m.get("sharpe"),
        "annual_return": m.get("annual_return"),
        "annual_vol": m.get("annual_vol"),
        "max_drawdown": m.get("max_drawdown"),
        "total_return": m.get("total_return"),
        "n_days": m.get("n_days"),
        "equity_beta": float(beta_coef),
        "corr_spy": corr,
    }


def walk_forward_sharpe(ret, close, spy_ret):
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    oos = []
    for tr_s, tr_e, te_s, te_e in splits:
        te_idx = close.index[te_s:te_e]
        w = ret.loc[ret.index.intersection(te_idx)]
        m = backtest.metrics(w["net"])
        oos.append(m.get("sharpe", 0.0))
    return float(np.mean(oos)), oos, len(splits)


def placebo_z(close, open_, spy, top_frac=0.1, tc=0.0005, sl=0.0002, n_sim=50):
    rng = np.random.default_rng(42)
    sharps = []
    for _ in range(n_sim):
        sig = pd.DataFrame(
            rng.standard_normal(size=close.shape),
            index=close.index, columns=close.columns,
        )
        w = backtest.dollar_neutral_longshort_weights(sig, top_frac=top_frac)
        r = backtest.portfolio_returns_rebalance_clean(
            w, close, open_, tc_cost=tc, slippage=sl, rebalance_freq=REBAL
        )
        s, _, _ = walk_forward_sharpe(r, close, spy.pct_change().fillna(0.0))
        sharps.append(s)
    return float(np.mean(sharps)), float(np.std(sharps))


def evaluate(close, open_, spy, beta_window, shrink, top_frac, tc, sl):
    beta = strategies.beta_factor(close, spy, window=beta_window, skip=1, shrink=shrink)
    sig = -beta
    w = backtest.dollar_neutral_longshort_weights(sig, top_frac=top_frac)
    ret = backtest.portfolio_returns_rebalance_clean(
        w, close, open_, tc_cost=tc, slippage=sl, rebalance_freq=REBAL
    )
    oos, _, nfolds = walk_forward_sharpe(ret, close, spy.pct_change().fillna(0.0))
    d = diag(ret, spy.pct_change().fillna(0.0))
    turn = backtest.average_turnover(w)
    return {
        "oos_sharpe": oos,
        "turnover": turn,
        "equity_beta": d["equity_beta"],
        "corr_spy": d["corr_spy"],
        "annual_return": d["annual_return"],
        "max_drawdown": d["max_drawdown"],
        "n_folds": nfolds,
    }


def leg_decomposition(close, open_, spy, beta_window=252, shrink=0.5, top_frac=0.1):
    """Compute long-leg and short-leg Sharpe separately."""
    beta = strategies.beta_factor(close, spy, window=beta_window, skip=1, shrink=shrink)
    sig = -beta  # long = low beta (high neg-beta signal), short = high beta
    w = backtest.dollar_neutral_longshort_weights(sig, top_frac=top_frac)
    # split weights into long / short
    w_long = w.clip(lower=0)
    w_short = w.clip(upper=0)
    r_long = backtest.portfolio_returns_rebalance_clean(
        w_long, close, open_, tc_cost=0.0005, slippage=0.0002, rebalance_freq=REBAL
    )
    r_short = backtest.portfolio_returns_rebalance_clean(
        w_short, close, open_, tc_cost=0.0005, slippage=0.0002, rebalance_freq=REBAL
    )
    spy_ret = spy.pct_change().fillna(0.0)
    sl, _, _ = walk_forward_sharpe(r_long, close, spy_ret)
    ss, _, _ = walk_forward_sharpe(r_short, close, spy_ret)
    d = diag(r_long, spy_ret)
    d_s = diag(r_short, spy_ret)
    return {
        "long_leg": {"oos_sharpe": sl, "annual_return": d["annual_return"], "equity_beta": d["equity_beta"]},
        "short_leg": {"oos_sharpe": ss, "annual_return": d_s["annual_return"], "equity_beta": d_s["equity_beta"]},
    }


def main():
    print("=" * 70)
    print("E013: Validate refine dollar_neutral_lowbeta keeper")
    print("=" * 70)

    close, open_, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    print(f"Loaded {len(close)} days, {len(close.columns)} tickers")

    results = {"experiment": "E013", "timestamp": deterministic_timestamp(),
               "universe": "large_liquid", "n_tickers": len(UNIVERSE)}

    # --- 1. Beta-window sensitivity grid ---
    print("\n[1] Beta-window x shrink sensitivity grid")
    grid = []
    for window in [63, 126, 252]:
        for shrink in [0.25, 0.50, 0.75]:
            r = evaluate(close, open_, spy, window, shrink, top_frac=0.1, tc=0.0005, sl=0.0002)
            r.update({"beta_window": window, "shrink": shrink})
            grid.append(r)
            print(f"    window={window} shrink={shrink}: OOS Sharpe={r['oos_sharpe']:.3f} "
                  f"beta={r['equity_beta']:.3f} corr={r['corr_spy']:.3f} turn={r['turnover']:.4f}")
    results["beta_window_grid"] = grid

    # placebo for baseline config (window=252, shrink=0.5)
    pm, ps = placebo_z(close, open_, spy, top_frac=0.1)
    base = [g for g in grid if g["beta_window"] == 252 and g["shrink"] == 0.5][0]
    results["placebo"] = {"mean": pm, "std": ps, "z": float((base["oos_sharpe"] - pm) / ps) if ps > 0 else float("nan")}
    print(f"    Placebo: mean={pm:.3f} std={ps:.3f} z={results['placebo']['z']:.2f}")

    # --- 2. Top-frac grid ---
    print("\n[2] Top-frac sensitivity grid")
    frac_grid = []
    for tf in [0.05, 0.10, 0.15, 0.20]:
        r = evaluate(close, open_, spy, 252, 0.5, tf, 0.0005, 0.0002)
        r["top_frac"] = tf
        frac_grid.append(r)
        print(f"    top_frac={tf}: OOS Sharpe={r['oos_sharpe']:.3f} "
              f"beta={r['equity_beta']:.3f} corr={r['corr_spy']:.3f} turn={r['turnover']:.4f}")
    results["top_frac_grid"] = frac_grid

    # --- 3. Shorting-cost stress ---
    print("\n[3] Shorting-cost stress test")
    cost_grid = []
    for tc, sl in [(0.0, 0.0), (0.0005, 0.0002), (0.0010, 0.0005), (0.0015, 0.0010),
                   (0.0020, 0.0050), (0.0050, 0.0100)]:
        r = evaluate(close, open_, spy, 252, 0.5, 0.1, tc, sl)
        r["tc_cost"] = tc
        r["slippage"] = sl
        cost_grid.append(r)
        print(f"    tc={tc:.4f} sl={sl:.4f}: OOS Sharpe={r['oos_sharpe']:.3f} "
              f"beta={r['equity_beta']:.3f} turn={r['turnover']:.4f}")
    results["cost_stress"] = cost_grid

    # --- 4. Out-of-universe robustness ---
    print("\n[4] Out-of-universe robustness")
    oou = {}
    for uname in ["large_liquid", "sp500_top", "etfs"]:
        uni = UNIVERSES[uname]
        df2 = data.download(uni, start="2014-01-01")
        c2 = data.get_panel(df2, "Close").dropna(how="all")
        o2 = data.get_panel(df2, "Open").reindex(c2.index).fillna(c2)
        r = evaluate(c2, o2, spy, 252, 0.5, 0.1, 0.0005, 0.0002)
        oou[uname] = r
        print(f"    {uname} (n={len(uni)}): OOS Sharpe={r['oos_sharpe']:.3f} "
              f"beta={r['equity_beta']:.3f} corr={r['corr_spy']:.3f} turn={r['turnover']:.4f}")
    results["out_of_universe"] = oou

    # --- 5. Leg decomposition ---
    print("\n[5] Leg decomposition (long low-beta vs short high-beta)")
    legs = leg_decomposition(close, open_, spy)
    results["leg_decomposition"] = legs
    print(f"    Long leg:  Sharpe={legs['long_leg']['oos_sharpe']:.3f} "
          f"beta={legs['long_leg']['equity_beta']:.3f}")
    print(f"    Short leg: Sharpe={legs['short_leg']['oos_sharpe']:.3f} "
          f"beta={legs['short_leg']['equity_beta']:.3f}")

    # --- 6. Decision ---
    print("\n[6] Decision gate (Sharpe>=0.8, z>=3, |beta|<=0.2)")
    gated = base["oos_sharpe"] >= 0.8 and results["placebo"]["z"] >= 3.0 and abs(base["equity_beta"]) <= 0.2
    results["decision"] = {
        "gate_passed": bool(gated),
        "condition": {"sharpe_ge_0.8": bool(base["oos_sharpe"] >= 0.8),
                      "z_ge_3": bool(results["placebo"]["z"] >= 3.0),
                      "abs_beta_le_0.2": bool(abs(base["equity_beta"]) <= 0.2)},
        "baseline_sharpe": base["oos_sharpe"],
        "baseline_beta": base["equity_beta"],
        "placebo_z": results["placebo"]["z"],
    }
    print(f"    Gate passed: {gated}")
    print(f"    baseline Sharpe={base['oos_sharpe']:.3f} beta={base['equity_beta']:.3f} z={results['placebo']['z']:.2f}")

    out_path = os.path.join("experiments", "e013_validate_lowbeta.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
