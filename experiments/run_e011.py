"""E011: Regime Robustness & Blending Test for TSM + Reversal."""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies


UNIVERSE = [
    "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
    "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
    "BAC","BK","BKNG","BMY","BRK-B","BSX","C","CAT","CCI","CDNS",
    "CHTR","CI","CL","CMCSA","CME","COF","COP","COST","CRM","CSCO",
    "CSX","CVS","CVX","DE","DHR","DIS","DOW","DXCM","EMR","EOG",
    "EQIX","ETN","EXC","FDX","FIS","FTNT","GD","GE","GILD","GM",
    "GOOG","GOOGL","GS","HD","HON","IBM","ICE","INTC","INTU","ISRG",
    "JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LLY","LMT","LOW",
    "LRCX","MA","MCD","MDLZ","MDT","META","MET","MMM","MO","MRK",
    "MS","MSFT","MU","NFLX","NKE","NOW","NVDA","ORCL","PCAR","PEP",
    "PFE","PG","PLD","PM","PNC","PYPL","QCOM","REGN","ROST","RTX",
    "SBUX","SCHW","SLB","SO","SPG","T","TGT","TJX","TMO","TMUS",
    "TSLA","TXN","UNH","UNP","UPS","USB","V","VZ","WBA","WFC",
    "WMT","XOM"
]

TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63


def load_data():
    df = data.download(UNIVERSE, start="2014-01-01")
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    return close, open_


def get_splits(close):
    return backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)


def run_strategy_weights(weights_fn, signal, close, open_, rebalance_freq=1):
    weights = weights_fn(signal, close)
    rets = backtest.portfolio_returns_rebalance_clean(
        weights, close, open_, TC_COST, SLIPPAGE, rebalance_freq
    )
    return rets


def get_fold_metrics(rets, close, splits):
    """Get metrics for each OOS fold."""
    fold_metrics = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = rets.loc[rets.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        m["fold"] = i
        fold_metrics.append(m)
    return fold_metrics


def compute_drawdown(ret):
    """Compute max drawdown and time underwater."""
    cum = (1.0 + ret.fillna(0.0)).cumprod()
    roll_max = cum.cummax()
    dd = cum / roll_max - 1.0
    max_dd = dd.min()
    # Time underwater (days from peak to recovery)
    underwater = (dd < 0).sum()
    return float(max_dd), int(underwater)


def regime_analysis(close, open_, splits, strategy_name, rets_dict):
    """Analyze performance by market regime (SPY return during test period)."""
    # Get SPY benchmark
    bm_df = data.download(["SPY"], start="2014-01-01")
    spy_close = data.get_panel(bm_df, "Close").dropna(how="all")["SPY"]
    spy_ret = spy_close.pct_change().fillna(0.0)

    results = {"bull": {}, "bear": {}, "sideways": {}}
    for strat in rets_dict:
        results["bull"][strat] = []
        results["bear"][strat] = []
        results["sideways"][strat] = []

    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        spy_period_ret = spy_ret.loc[test_idx].sum()

        # Classify regime
        if spy_period_ret > 0.02:
            regime = "bull"
        elif spy_period_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"

        for strat_name, rets in rets_dict.items():
            test_rets = rets.loc[rets.index.intersection(test_idx)]
            m = backtest.metrics(test_rets["net"])
            m["regime"] = regime
            m["spy_return"] = float(spy_period_ret)
            m["fold"] = i
            results[regime][strat_name].append(m)

    return results


def main():
    print("=" * 60)
    print("E011: Regime Robustness & TSM+Reversal Blending")
    print("=" * 60)

    close, open_ = load_data()
    splits = get_splits(close)
    print(f"Loaded {len(close)} days, {len(close.columns)} tickers")
    print(f"Walk-forward splits: {len(splits)} folds")

    # --- Strategy 1: TSM Pure (monthly, inv-vol) ---
    print("\n--- TSM Pure (21d rebal, inv-vol) ---")
    tsm_signal = strategies.time_series_momentum_pure(close, lookback=12, skip=1)
    tsm_weights = backtest.time_series_momentum_weights(tsm_signal, close, long_only=True, vol_window=63)
    tsm_rets = backtest.portfolio_returns_rebalance_clean(
        tsm_weights, close, open_, TC_COST, SLIPPAGE, rebalance_freq=21
    )
    tsm_fold_metrics = get_fold_metrics(tsm_rets, close, splits)
    tsm_sharpe = np.mean([m["sharpe"] for m in tsm_fold_metrics])
    tsm_turnover = backtest.average_turnover(tsm_weights)
    tsm_dd, tsm_underwater = compute_drawdown(tsm_rets["net"])
    print(f"  OOS Sharpe: {tsm_sharpe:.3f}, Turnover: {tsm_turnover:.4f}, MaxDD: {tsm_dd:.3f}")

    # --- Strategy 2: Reversal (10d rebal) ---
    print("\n--- Reversal (10d rebal) ---")
    rev_signal = strategies.reversal(close, lookback=12)
    rev_weights = backtest.equal_weight_weights(rev_signal, long_only=True)
    rev_rets = backtest.portfolio_returns_rebalance_clean(
        rev_weights, close, open_, TC_COST, SLIPPAGE, rebalance_freq=10
    )
    rev_fold_metrics = get_fold_metrics(rev_rets, close, splits)
    rev_sharpe = np.mean([m["sharpe"] for m in rev_fold_metrics])
    rev_turnover = backtest.average_turnover(rev_weights)
    rev_dd, rev_underwater = compute_drawdown(rev_rets["net"])
    print(f"  OOS Sharpe: {rev_sharpe:.3f}, Turnover: {rev_turnover:.4f}, MaxDD: {rev_dd:.3f}")

    # --- Strategy 3: TSM Long-Short ---
    print("\n--- TSM Long-Short (21d rebal, inv-vol) ---")
    tsm_ls_weights = backtest.time_series_momentum_weights(tsm_signal, close, long_only=False, vol_window=63)
    tsm_ls_rets = backtest.portfolio_returns_rebalance_clean(
        tsm_ls_weights, close, open_, TC_COST, SLIPPAGE, rebalance_freq=21
    )
    tsm_ls_fold_metrics = get_fold_metrics(tsm_ls_rets, close, splits)
    tsm_ls_sharpe = np.mean([m["sharpe"] for m in tsm_ls_fold_metrics])
    tsm_ls_turnover = backtest.average_turnover(tsm_ls_weights)
    tsm_ls_dd, tsm_ls_underwater = compute_drawdown(tsm_ls_rets["net"])
    print(f"  OOS Sharpe: {tsm_ls_sharpe:.3f}, Turnover: {tsm_ls_turnover:.4f}, MaxDD: {tsm_ls_dd:.3f}")

    # --- Correlation of daily returns ---
    common_idx = tsm_rets.index.intersection(rev_rets.index)
    tsm_daily = tsm_rets.loc[common_idx, "net"]
    rev_daily = rev_rets.loc[common_idx, "net"]
    tsm_ls_daily = tsm_ls_rets.loc[common_idx, "net"]
    corr_tsm_rev = tsm_daily.corr(rev_daily)
    corr_tsm_tsmls = tsm_daily.corr(tsm_ls_daily)
    corr_rev_tsmls = rev_daily.corr(tsm_ls_daily)
    print(f"\n--- Return Correlations ---")
    print(f"  TSM vs Reversal: {corr_tsm_rev:.3f}")
    print(f"  TSM vs TSM-LS: {corr_tsm_tsmls:.3f}")
    print(f"  Reversal vs TSM-LS: {corr_rev_tsmls:.3f}")

    # --- Blend: TSM + Reversal (equal weight signals, 21d rebal) ---
    print("\n--- Blend: TSM + Reversal (21d rebal) ---")
    # Create blended signal: z-score each then average
    def zscore(x):
        arr = x.to_numpy()
        mu = np.nanmean(arr, axis=1, keepdims=True)
        sd = np.nanstd(arr, axis=1, keepdims=True) + 1e-9
        return pd.DataFrame((arr - mu) / sd, index=x.index, columns=x.columns)

    blend_signal = (zscore(tsm_signal) + zscore(rev_signal)) / 2.0
    blend_weights = backtest.equal_weight_weights(blend_signal, long_only=True)
    blend_rets = backtest.portfolio_returns_rebalance_clean(
        blend_weights, close, open_, TC_COST, SLIPPAGE, rebalance_freq=21
    )
    blend_fold_metrics = get_fold_metrics(blend_rets, close, splits)
    blend_sharpe = np.mean([m["sharpe"] for m in blend_fold_metrics])
    blend_turnover = backtest.average_turnover(blend_weights)
    blend_dd, blend_underwater = compute_drawdown(blend_rets["net"])
    print(f"  OOS Sharpe: {blend_sharpe:.3f}, Turnover: {blend_turnover:.4f}, MaxDD: {blend_dd:.3f}")

    # --- Blend: TSM (inv-vol) + Reversal (eq-weight) ---
    print("\n--- Blend: TSM(inv-vol) + Reversal(eq-wt) ---")
    # Weight TSM by inv-vol, reversal by eq-wt, then combine 50/50
    blend2_weights = (tsm_weights * 0.5) + (rev_weights * 0.5)
    blend2_rets = backtest.portfolio_returns_rebalance_clean(
        blend2_weights, close, open_, TC_COST, SLIPPAGE, rebalance_freq=21
    )
    blend2_fold_metrics = get_fold_metrics(blend2_rets, close, splits)
    blend2_sharpe = np.mean([m["sharpe"] for m in blend2_fold_metrics])
    blend2_turnover = backtest.average_turnover(blend2_weights)
    blend2_dd, blend2_underwater = compute_drawdown(blend2_rets["net"])
    print(f"  OOS Sharpe: {blend2_sharpe:.3f}, Turnover: {blend2_turnover:.4f}, MaxDD: {blend2_dd:.3f}")

    # --- Regime Analysis ---
    print("\n--- Regime Analysis ---")
    rets_dict = {
        "tsm": tsm_rets,
        "reversal": rev_rets,
        "tsm_ls": tsm_ls_rets,
        "blend": blend_rets,
        "blend2": blend2_rets,
    }
    regime_results = regime_analysis(close, open_, splits, "all", rets_dict)

    for regime in ["bull", "bear", "sideways"]:
        for strat in ["tsm", "reversal", "tsm_ls", "blend", "blend2"]:
            reg_data = regime_results[regime].get(strat, [])
            if reg_data:
                sharps = [m["sharpe"] for m in reg_data]
                print(f"  {regime} - {strat}: Sharpe={np.mean(sharps):.3f} (n={len(sharps)})")

    # --- Detailed fold-by-fold for TSM ---
    print("\n--- TSM Fold-by-Fold ---")
    for m in tsm_fold_metrics:
        print(f"  Fold {m['fold']}: Sharpe={m['sharpe']:.3f}, AnnRet={m['annual_return']:.3f}, MaxDD={m['max_drawdown']:.3f}")

    # --- Save results ---
    result = {
        "experiment": "E011",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "universe": "large_liquid",
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP, "n_folds": len(splits)},
        "strategies": {
            "tsm_pure_21d_invvol": {
                "oos_sharpe": float(tsm_sharpe),
                "turnover": float(tsm_turnover),
                "max_drawdown": float(tsm_dd),
                "time_underwater_days": tsm_underwater,
                "fold_metrics": tsm_fold_metrics,
            },
            "reversal_10d": {
                "oos_sharpe": float(rev_sharpe),
                "turnover": float(rev_turnover),
                "max_drawdown": float(rev_dd),
                "time_underwater_days": rev_underwater,
                "fold_metrics": rev_fold_metrics,
            },
            "tsm_long_short_21d": {
                "oos_sharpe": float(tsm_ls_sharpe),
                "turnover": float(tsm_ls_turnover),
                "max_drawdown": float(tsm_ls_dd),
                "time_underwater_days": tsm_ls_underwater,
                "fold_metrics": tsm_ls_fold_metrics,
            },
            "blend_tsm_rev_eqwt_21d": {
                "oos_sharpe": float(blend_sharpe),
                "turnover": float(blend_turnover),
                "max_drawdown": float(blend_dd),
                "time_underwater_days": blend_underwater,
                "fold_metrics": blend_fold_metrics,
            },
            "blend_tsm_invvol_rev_eqwt_21d": {
                "oos_sharpe": float(blend2_sharpe),
                "turnover": float(blend2_turnover),
                "max_drawdown": float(blend2_dd),
                "time_underwater_days": blend2_underwater,
                "fold_metrics": blend2_fold_metrics,
            },
        },
        "correlations": {
            "tsm_vs_reversal": float(corr_tsm_rev),
            "tsm_vs_tsm_ls": float(corr_tsm_tsmls),
            "reversal_vs_tsm_ls": float(corr_rev_tsmls),
        },
        "regime_analysis": {k: {sk: [dict(m) for m in sv] for sk, sv in v.items()} for k, v in regime_results.items()},
    }

    out_path = os.path.join("experiments", "e011_regime_blend.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")

    return result


if __name__ == "__main__":
    main()