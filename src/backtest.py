"""Walk-forward backtesting engine with realistic execution modeling.

Design principles:
- No look-ahead bias: signals are computed from data available at decision time.
- Daily rebalancing with next-day open execution (realistic).
- Fixed proportional transaction costs; slippage modeled as a fraction of price.
- Chronological walk-forward splits with no information leakage between folds.
"""

import numpy as np
import pandas as pd


def _ensure_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.copy()
        df.index = pd.to_datetime(df.index)
    return df


def next_day_open_returns(close: pd.Series, open_: pd.Series) -> pd.Series:
    """Return realized next-day return using open price of the next trading day."""
    return (open_.shift(-1) / close - 1.0)


def equal_weight_weights(signal: pd.Series, long_only: bool = True) -> pd.DataFrame:
    """Convert a cross-sectional signal rank into target weights.

    Long-only equal-weight across the top-N names; short side zero.
    """
    ranks = signal.rank(axis=1, ascending=False, method="min", pct=True)
    n = signal.shape[1]
    top_n = max(1, int(round(n * 0.2)))  # top quintile
    weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)
    for date, row in ranks.iterrows():
        cutoff = row.nlargest(top_n).min()
        mask = row >= cutoff
        if mask.sum() > 0:
            weights.loc[date, mask] = 1.0 / mask.sum()
    if long_only:
        weights = weights.clip(lower=0.0)
    return weights


def shift_weights(weights: pd.DataFrame) -> pd.DataFrame:
    """Shift weights forward one day so they are executable at next open."""
    return weights.shift(1).fillna(0.0)


def portfolio_returns(
    weights: pd.DataFrame,
    close: pd.DataFrame,
    open_: pd.DataFrame,
    tc_cost: float = 0.0005,
    slippage: float = 0.0002,
) -> pd.Series:
    """Compute daily portfolio gross and net returns.

    weights: target weights as of day t (will be executed at t+1 open).
    close: closing prices day t.
    open_: opening prices day t+1.
    """
    weights = shift_weights(weights)
    # next-day return on each asset using its own open
    asset_ret = (open_.shift(-1) / close - 1.0)
    gross = (weights * asset_ret).sum(axis=1)

    # turnover and transaction costs
    turnover = (weights.diff().abs()).sum(axis=1)
    costs = turnover * (tc_cost + slippage)
    net = gross - costs
    return pd.DataFrame({"gross": gross, "costs": costs, "net": net})


def cumulative_returns(ret: pd.Series) -> pd.Series:
    return (1.0 + ret.fillna(0.0)).cumprod() - 1.0


def metrics(ret: pd.Series, periods: int = 252) -> dict:
    """Compute standard performance metrics."""
    ret = ret.dropna()
    if len(ret) < 10:
        return {}
    ann = periods
    mean = ret.mean()
    std = ret.std()
    sharpe = (mean / std * np.sqrt(ann)) if std > 0 else 0.0
    cum = (1.0 + ret).cumprod()
    roll_max = cum.cummax()
    drawdown = cum / roll_max - 1.0
    max_dd = drawdown.min()
    total = cum.iloc[-1] - 1.0 if len(cum) else 0.0
    win_rate = (ret > 0).mean()
    return {
        "annual_return": mean * ann,
        "annual_vol": std * np.sqrt(ann),
        "sharpe": sharpe,
        "max_drawdown": max_dd,
        "total_return": total,
        "win_rate": win_rate,
        "n_days": len(ret),
    }


def walk_forward_splits(
    n_days: int,
    train_size: int = 504,
    test_size: int = 63,
    step: int = 63,
) -> list:
    """Generate chronological (train_start, train_end, test_start, test_end) tuples."""
    splits = []
    test_start = train_size
    while test_start + test_size <= n_days:
        train_start = test_start - train_size
        train_end = test_start
        test_end = test_start + test_size
        splits.append((train_start, train_end, test_start, test_end))
        test_start += step
    return splits
def average_turnover(weights: pd.DataFrame) -> float:
    """Average daily turnover (sum of |w_t - w_{t-1}|) over time."""
    w_shift = shift_weights(weights)
    turnover = (w_shift.diff().abs()).sum(axis=1)
    return float(turnover.mean()) if len(turnover.dropna()) > 0 else 0.0

def inverse_vol_weights(signal: pd.DataFrame, close: pd.DataFrame, vol_window: int = 63,
                        top_quintile: bool = True, long_only: bool = True) -> pd.DataFrame:
    """Rank by signal, then weight within top quintile by inverse realized volatility."""
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    ranks = signal.rank(axis=1, ascending=False, method="min", pct=True)
    n = signal.shape[1]
    top_n = max(1, int(round(n * 0.2)))
    weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)
    for date, row in ranks.iterrows():
        cutoff = row.nlargest(top_n).min()
        mask = row >= cutoff
        if mask.sum() > 0:
            w = inv_vol.loc[date, mask].fillna(0.0)
            s = w.sum()
            if s > 0:
                weights.loc[date, mask] = w / s
    if long_only:
        weights = weights.clip(lower=0.0)
    return weights

def portfolio_returns_rebalance(
    weights: pd.DataFrame,
    close: pd.DataFrame,
    open_: pd.DataFrame,
    tc_cost: float = 0.0005,
    slippage: float = 0.0002,
    rebalance_freq: int = 1,  # days between rebalances; 1 = daily
) -> pd.DataFrame:
    """Portfolio returns with less frequent rebalancing."""
    w = shift_weights(weights).copy()
    if rebalance_freq > 1:
        w_new = pd.DataFrame(0.0, index=w.index, columns=w.columns)
        last = pd.Series(0.0, index=w.columns)
        for i in range(len(w)):
            if i % rebalance_freq == 0:
                last = w.iloc[i]
            w_new.iloc[i] = last.values
        w = w_new
    asset_ret = (open_.shift(-1) / close - 1.0)
    gross = (w * asset_ret).sum(axis=1)
    turnover = (w.diff().abs()).sum(axis=1)
    costs = turnover * (tc_cost + slippage)
    net = gross - costs
    return pd.DataFrame({"gross": gross, "costs": costs, "net": net})

def portfolio_returns_rebalance_clean(
    weights: pd.DataFrame,
    close: pd.DataFrame,
    open_: pd.DataFrame,
    tc_cost: float = 0.0005,
    slippage: float = 0.0002,
    rebalance_freq: int = 1,
) -> pd.DataFrame:
    w = shift_weights(weights).copy()
    if rebalance_freq > 1:
        w_new = pd.DataFrame(0.0, index=w.index, columns=w.columns)
        last = pd.Series(0.0, index=w.columns)
        for i in range(len(w)):
            if i % rebalance_freq == 0:
                last = w.iloc[i]
            w_new.iloc[i] = last.values
        w = w_new
    asset_ret = (open_.shift(-1) / close - 1.0)
    gross = (w * asset_ret).sum(axis=1)
    turnover = (w.diff().abs()).sum(axis=1)
    costs = turnover * (tc_cost + slippage)
    net = gross - costs
    return pd.DataFrame({"gross": gross, "costs": costs, "net": net})


def time_series_momentum_weights(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    long_only: bool = True,
    vol_window: int = 63,
) -> pd.DataFrame:
    """Time-series momentum weights: long if signal > 0, flat if signal < 0 (long_only) or short.

    Classic Moskowitz et al. (2012) implementation with absolute threshold at zero.
    Positions scaled by inverse realized volatility for risk parity.
    """
    import numpy as np
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)

    for date in signal.index:
        sig_row = signal.loc[date]
        if long_only:
            mask = sig_row > 0
        else:
            mask = sig_row != 0

        active = mask[mask].index
        if len(active) > 0:
            if long_only:
                # Risk-parity weighting: inverse vol
                w = inv_vol.loc[date, active].fillna(0.0)
                s = w.sum()
                if s > 0:
                    weights.loc[date, active] = w / s
            else:
                # Long-short: sign of signal * inverse vol
                w = np.sign(sig_row[active]) * inv_vol.loc[date, active].fillna(0.0)
                s = w.abs().sum()
                if s > 0:
                    weights.loc[date, active] = w / s

    return weights
