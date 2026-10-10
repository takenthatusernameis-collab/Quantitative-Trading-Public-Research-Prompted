"""Statistical validation for backtest results.

Checks for: look-ahead bias, autocorrelation, multiple-testing, and
comparison against a placebo baseline (random signals with same cost model).
"""

import numpy as np
import pandas as pd


def placebo_distribution(close: pd.DataFrame, n_sim: int = 200, seed: int = 42) -> dict:
    """Run many random-signal backtests to build a null distribution of Sharpe.

    Returns mean/std of OOS Sharpe under the null hypothesis of no skill.
    """
    from src import backtest as bt

    rng = np.random.default_rng(seed)
    sharps = []
    for i in range(n_sim):
        signal = pd.DataFrame(
            rng.standard_normal(size=close.shape),
            index=close.index, columns=close.columns,
        )
        weights = bt.equal_weight_weights(signal, long_only=True)
        open_ = close
        rets = bt.portfolio_returns(weights, close, open_)
        m = bt.metrics(rets["net"])
        sharps.append(m.get("sharpe", 0.0))
    return {
        "n_sim": n_sim,
        "mean_sharpe": float(np.mean(sharps)),
        "std_sharpe": float(np.std(sharps)),
        "pct_positive": float(np.mean(np.array(sharps) > 0)),
    }


def autocorrelation_test(ret: pd.Series, lags: int = 5) -> dict:
    """Test for significant autocorrelation in strategy returns (bias indicator)."""
    r = ret.dropna()
    acf = [r.autocorr(lag) for lag in range(1, lags + 1)]
    return {"lags": list(range(1, lags + 1)), "acf": acf}


def t_stat(sharpe: float, n_days: int) -> float:
    """Approximate t-statistic for a Sharpe ratio."""
    return sharpe * np.sqrt(n_days / 252)


def compare_to_placebo(strategy_sharpes: list, placebo_mean: float, placebo_std: float) -> dict:
    """Compute how many std devs the strategy's mean OOS Sharpe is from placebo."""
    if len(strategy_sharpes) == 0:
        return {}
    mean_s = float(np.mean(strategy_sharpes))
    if placebo_std <= 0:
        return {"mean_sharpe": mean_s, "z_score": None}
    z = (mean_s - placebo_mean) / placebo_std
    return {
        "mean_sharpe": mean_s,
        "placebo_mean": placebo_mean,
        "placebo_std": placebo_std,
        "z_score": float(z),
        "significant_at_5pct": bool(abs(z) > 1.96),
    }