"""E012: Market-neutral / equity-beta-neutral strategy test.

Tests the most valuable untried class identified in E001-E011: strategies that
are NOT simply long-only equity beta + signal (the core limitation of the
existing strategy set, all of which are ~SPY-correlated and negative in bear
markets per E011).

Primary experiment: Betting Against Beta (Frazzini & Pedersen 2014), a
beta-neutral factor (long levered low-beta, short de-levered high-beta).
Also tests a simpler dollar-neutral low-beta sort as a robustness variant.

Design:
  - Universe: large_liquid (132 US equities) + SPY benchmark, 2014-2026
  - Market-neutral by construction (BAB beta = 0); dollar-neutral variant net 0
  - Monthly (21d) rebalancing, next-day-open execution
  - Costs: base 0.5bps+0.2bps (incl. shorting) and high 20bps+5bps
  - Walk-forward 504/63/63 (42 OOS folds); 50-sim market-neutral placebo null
  - Validation: placebo z-score, autocorr, equity beta, SPY correlation,
    regime (bear 2020-COVID / 2022, bull, sideways) Sharpe
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
TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21  # monthly, per Frazzini-Pedersen
BETA_WINDOW = 252


def load_data():
    df = data.download(UNIVERSE, start="2014-01-01")
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start="2014-01-01")
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
        alpha = coef[0]
        beta_coef = coef[1]
        corr = float(np.corrcoef(y, x)[0, 1])
    else:
        alpha, beta_coef, corr = np.nan, np.nan, np.nan
    return {
        "is_sharpe": m.get("sharpe"),
        "is_ann_return": m.get("annual_return"),
        "is_ann_vol": m.get("annual_vol"),
        "is_max_dd": m.get("max_drawdown"),
        "is_total_return": m.get("total_return"),
        "is_win_rate": m.get("win_rate"),
        "is_n_days": m.get("n_days"),
        "equity_beta": float(beta_coef),
        "alpha_annual": float(alpha * 252),
        "corr_spy": corr,
    }


def compute_dd(ret):
    ret = ret.dropna()
    if len(ret) == 0:
        return 0.0, 0
    cum = (1.0 + ret).cumprod()
    roll = cum.cummax()
    dd = cum / roll - 1.0
    return float(dd.min()), int((dd < 0).sum())


def walk_forward(ret, close, spy_ret):
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    fold_metrics = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = ret.loc[ret.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(test_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else np.nan
        if spy_win_ret > 0.02:
            regime = "bull"
        elif spy_win_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"
        m["regime"] = regime
        m["spy_test_return"] = spy_win_ret
        fold_metrics.append(m)
    return fold_metrics


def regime_summary(fold_metrics):
    out = {}
    for regime in ["bull", "bear", "sideways"]:
        rows = [m for m in fold_metrics if m.get("regime") == regime]
        sharps = [m["sharpe"] for m in rows]
        out[regime] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sharps)) if sharps else float("nan"),
            "sharpe_pos": int(sum(1 for s in sharps if s > 0)) if sharps else 0,
            "ann_return_mean": float(np.mean([m["annual_return"] for m in rows])) if rows else float("nan"),
            "max_dd_mean": float(np.mean([m["max_drawdown"] for m in rows])) if rows else float("nan"),
        }
    return out


def main():
    print("=" * 70)
    print("E012: Market-Neutral Strategies (Betting Against Beta + variants)")
    print("=" * 70)

    close, open_, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    print(f"Loaded {len(close)} days, {len(close.columns)} tickers; folds={len(splits)}")

    # --- 1. Beta signal (Frazzini-Pedersen: 1yr rolling, shrink to 1, lagged 1d) ---
    print("\n[1] Computing rolling beta factor (window=252, shrink=0.5, skip=1)...")
    beta = strategies.beta_factor(close, spy, window=BETA_WINDOW, skip=1, shrink=0.5)
    print(f"    beta coverage (rows with any non-NaN beta): {beta.notna().any(axis=1).sum()}/{len(beta)}")

    results = {}

    # --- 2. BAB (beta-neutral) ---
    print("\n[2] BAB (beta-neutral) - monthly rebal, Frazzini-Pedersen construction")
    bab_w = backtest.bab_weights(beta)
    bab_ret = backtest.portfolio_returns_rebalance_clean(
        bab_w, close, open_, TC_COST, SLIPPAGE, rebalance_freq=REBAL
    )
    bab_fm = walk_forward(bab_ret, close, spy_ret)
    bab_diag = market_diagnostics(bab_ret, spy_ret)
    bab_dd, bab_uw = compute_dd(bab_ret["net"])
    bab_reg = regime_summary(bab_fm)
    bab_sharpe = float(np.mean([m["sharpe"] for m in bab_fm]))
    bab_turn = backtest.average_turnover(bab_w)
    print(f"    OOS Sharpe={bab_sharpe:.3f}  turnover={bab_turn:.4f}  "
          f"equity_beta={bab_diag['equity_beta']:.3f}  corr_spy={bab_diag['corr_spy']:.3f}  "
          f"maxDD={bab_dd:.3f}")
    print(f"    regime: bear={bab_reg['bear']}")
    results["bab_beta_neutral_21d"] = {
        "source": "Frazzini & Pedersen (2014) 'Betting Against Beta', JFE 111(1):1-25",
        "mechanism": "Long levered low-beta stocks, short de-levered high-beta stocks. "
                     "Beta-neutral by construction (each side rescaled to unit beta).",
        "oos_sharpe": bab_sharpe,
        "oos_sharpe_std": float(np.std([m["sharpe"] for m in bab_fm])),
        "turnover": bab_turn,
        "equity_beta": bab_diag["equity_beta"],
        "corr_spy": bab_diag["corr_spy"],
        "alpha_annual": bab_diag["alpha_annual"],
        "is_sharpe": bab_diag["is_sharpe"],
        "is_ann_return": bab_diag["is_ann_return"],
        "is_ann_vol": bab_diag["is_ann_vol"],
        "max_drawdown": bab_dd,
        "time_underwater_days": bab_uw,
        "regime_analysis": bab_reg,
        "acf_lag1": float(validation.autocorrelation_test(bab_ret["net"])["acf"][0]),
        "t_stat": float(validation.t_stat(bab_sharpe, TEST * len(bab_fm))),
        "fold_metrics": bab_fm,
    }

    # --- 3. Dollar-neutral low-beta sort (simpler variant) ---
    print("\n[3] Dollar-neutral low-beta sort (long bottom-10pct beta, short top-10pct, 21d)")
    lowbeta_signal = -beta
    dn_w = backtest.dollar_neutral_longshort_weights(lowbeta_signal, top_frac=0.1)
    dn_ret = backtest.portfolio_returns_rebalance_clean(
        dn_w, close, open_, TC_COST, SLIPPAGE, rebalance_freq=REBAL
    )
    dn_fm = walk_forward(dn_ret, close, spy_ret)
    dn_diag = market_diagnostics(dn_ret, spy_ret)
    dn_dd, dn_uw = compute_dd(dn_ret["net"])
    dn_reg = regime_summary(dn_fm)
    dn_sharpe = float(np.mean([m["sharpe"] for m in dn_fm]))
    dn_turn = backtest.average_turnover(dn_w)
    print(f"    OOS Sharpe={dn_sharpe:.3f}  turnover={dn_turn:.4f}  "
          f"equity_beta={dn_diag['equity_beta']:.3f}  corr_spy={dn_diag['corr_spy']:.3f}  "
          f"maxDD={dn_dd:.3f}")
    print(f"    regime: bear={dn_reg['bear']}")
    results["dollar_neutral_lowbeta_21d"] = {
        "source": "Low-beta sort, dollar-neutral (10/10 pct long-short). Simple variant.",
        "mechanism": "Long bottom-10% beta stocks, short top-10%, dollar-neutral. "
                     "Zero net dollar exposure by construction; near-zero market beta.",
        "oos_sharpe": dn_sharpe,
        "oos_sharpe_std": float(np.std([m["sharpe"] for m in dn_fm])),
        "turnover": dn_turn,
        "equity_beta": dn_diag["equity_beta"],
        "corr_spy": dn_diag["corr_spy"],
        "alpha_annual": dn_diag["alpha_annual"],
        "is_sharpe": dn_diag["is_sharpe"],
        "is_ann_return": dn_diag["is_ann_return"],
        "is_ann_vol": dn_diag["is_ann_vol"],
        "max_drawdown": dn_dd,
        "time_underwater_days": dn_uw,
        "regime_analysis": dn_reg,
        "acf_lag1": float(validation.autocorrelation_test(dn_ret["net"])["acf"][0]),
        "t_stat": float(validation.t_stat(dn_sharpe, TEST * len(dn_fm))),
        "fold_metrics": dn_fm,
    }

    # --- 4. Placebo null: random market-neutral long-short ---
    print("\n[4] Market-neutral placebo null (50 random dollar-neutral sims)...")
    rng = np.random.default_rng(42)
    placebo_sharpes = []
    for i in range(50):
        sig = pd.DataFrame(
            rng.standard_normal(size=close.shape),
            index=close.index, columns=close.columns,
        )
        w = backtest.dollar_neutral_longshort_weights(sig, top_frac=0.1)
        r = backtest.portfolio_returns_rebalance_clean(
            w, close, open_, TC_COST, SLIPPAGE, rebalance_freq=REBAL
        )
        placebo_sharpes.append(backtest.metrics(r["net"]).get("sharpe", 0.0))
    pm = float(np.mean(placebo_sharpes))
    ps = float(np.std(placebo_sharpes))
    print(f"    Placebo: mean Sharpe={pm:.3f} std={ps:.3f} pct_positive={np.mean(np.array(placebo_sharpes)>0)*100:.1f}%")

    for key in results:
        results[key]["placebo_mean"] = pm
        results[key]["placebo_std"] = ps
        results[key]["placebo_z"] = float((results[key]["oos_sharpe"] - pm) / ps) if ps > 0 else float("nan")
        results[key]["z_above_1_96"] = bool(results[key]["placebo_z"] > 1.96)
        print(f"    z-score {key}: {results[key]['placebo_z']:.2f}")

    # --- 5. Cost sensitivity for BAB ---
    print("\n[5] Cost sensitivity (BAB): sweep tc/slippage")
    cost_rows = []
    for tc, sl in [(0.0, 0.0), (0.0005, 0.0002), (0.0010, 0.0005), (0.0020, 0.0050)]:
        r = backtest.portfolio_returns_rebalance_clean(
            bab_w, close, open_, tc_cost=tc, slippage=sl, rebalance_freq=REBAL
        )
        fm = walk_forward(r, close, spy_ret)
        npos = int(sum(1 for m in fm if m["sharpe"] > 0))
        cost_rows.append({
            "tc_cost": tc, "slippage": sl,
            "oos_sharpe": float(np.mean([m["sharpe"] for m in fm])),
            "turnover": backtest.average_turnover(bab_w),
            "n_pos_folds": npos,
            "sharpe_std": float(np.std([m["sharpe"] for m in fm])),
        })
        print(f"    tc={tc:.4f} sl={sl:.4f}: OOS Sharpe={cost_rows[-1]['oos_sharpe']:.3f} "
              f"(std {cost_rows[-1]['sharpe_std']:.3f}) pos={npos}/{len(fm)}")
    results["cost_sensitivity"] = cost_rows

    # --- 6. Bear-window analysis ---
    print("\n[6] Bear-market window analysis (2020-COVID, 2022-bear)")
    for label, lo, hi in [("2020_covid", "2020-02-19", "2020-04-07"),
                          ("2022_bear", "2022-01-03", "2022-06-16")]:
        win_mask = (close.index >= lo) & (close.index <= hi)
        for key, ret in [("bab_beta_neutral_21d", bab_ret),
                         ("dollar_neutral_lowbeta_21d", dn_ret)]:
            wret = ret.loc[ret.index[win_mask].intersection(ret.index), "net"]
            if len(wret) > 2:
                m = backtest.metrics(wret)
                results[key][f"sharpe_{label}"] = m.get("sharpe")
                print(f"    {key} {label}: Sharpe={m.get('sharpe',0):.3f} "
                      f"AnnRet={m.get('annual_return',0):.3f} MaxDD={m.get('max_drawdown',0):.3f}")

    # --- 7. Cross-correlations ---
    print("\n[7] Cross-correlations of daily net returns")
    common = bab_ret.index.intersection(dn_ret.index)
    corr_bd = float(bab_ret.loc[common, "net"].corr(dn_ret.loc[common, "net"]))
    corr_bm = float(bab_ret.loc[common, "net"].corr(spy_ret.loc[common]))
    corr_dm = float(dn_ret.loc[common, "net"].corr(spy_ret.loc[common]))
    results["correlations"] = {
        "bab_vs_dollar_neutral": corr_bd,
        "bab_vs_spy": corr_bm,
        "dollar_neutral_vs_spy": corr_dm,
    }
    print(f"    BAB vs DN={corr_bd:.3f}  BAB vs SPY={corr_bm:.3f}  DN vs SPY={corr_dm:.3f}")

    # --- Save ---
    strat_keys = ["bab_beta_neutral_21d", "dollar_neutral_lowbeta_21d"]
    result = {
        "experiment": "E012",
        "timestamp": deterministic_timestamp(),
        "universe": "large_liquid",
        "n_tickers": len(UNIVERSE),
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP, "n_folds": len(splits)},
        "rebalance_freq_days": REBAL,
        "beta_window": BETA_WINDOW,
        "beta_shrink": 0.5,
        "placebo": {"n_sim": 50, "mean_sharpe": pm, "std_sharpe": ps},
        "strategies": {
            k: {kk: vv for kk, vv in results[k].items()} for k in strat_keys
        },
        "cost_sensitivity": cost_rows,
        "correlations": results["correlations"],
    }

    out_path = os.path.join("experiments", "e012_market_neutral.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
