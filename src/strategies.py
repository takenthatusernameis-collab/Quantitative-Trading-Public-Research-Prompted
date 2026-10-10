"""Strategy signal generators.

Each function takes a DataFrame of close prices (index=date, columns=tickers)
and returns a DataFrame of cross-sectional signals on the same shape.
"""

import numpy as np
import pandas as pd


def momentum(close: pd.DataFrame, lookback: int = 12, skip: int = 1) -> pd.DataFrame:
    """Classic 12-1 Jegadeesh-Titman skip-1 momentum signal."""
    ret = close.pct_change(lookback)
    return ret.shift(skip)


def reversal(close: pd.DataFrame, lookback: int = 12) -> pd.DataFrame:
    """Long-term reversal: negative of prior 12-month return (De Bondt-Thaler)."""
    ret = close.pct_change(lookback * 21)
    return -ret


def short_reversal(close: pd.DataFrame, lookback: int = 21) -> pd.DataFrame:
    """Short-term mean reversion: prior month return inverted."""
    ret = close.pct_change(lookback)
    return -ret


def volatility(close: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Realized volatility (annualized)."""
    rets = close.pct_change()
    return rets.rolling(window).std() * np.sqrt(252)


def size_effect(close: pd.DataFrame, window: int = 252) -> pd.DataFrame:
    """Proxy for size: 1 / market cap is not available; use inverse price as proxy."""
    return 1.0 / close


def value(close: pd.DataFrame, window: int = 60) -> pd.DataFrame:
    """Value proxy: negative of prior 60-month price momentum (long-horizon mean reversion).

    Distinct from reversal (12-month) to avoid signal duplication.
    """
    ret = close.pct_change(window * 21)
    return -ret


def quality(close: pd.DataFrame, vol_window: int = 63, mom_window: int = 12) -> pd.DataFrame:
    """Quality/defensive proxy: low realized volatility + positive short-term momentum.

    Combines the low-vol anomaly (Ang et al. 2006, 2008) with short-horizon momentum.
    Cross-sectional z-score standardization per day.
    """
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std()
    mom = close.pct_change(mom_window)

    def zscore(x: pd.DataFrame) -> pd.DataFrame:
        arr = x.to_numpy()
        mu = np.nanmean(arr, axis=1, keepdims=True)
        sd = np.nanstd(arr, axis=1, keepdims=True) + 1e-9
        z = (arr - mu) / sd
        return pd.DataFrame(z, index=x.index, columns=x.columns)

    vol_z = zscore(vol)
    mom_z = zscore(mom)
    return -(vol_z) + mom_z  # low vol + high momentum => high signal


def max_momentum(close: pd.DataFrame, lookback: int = 6, skip: int = 1) -> pd.DataFrame:
    """Shorter-horizon momentum (6-month) for comparison with 12-month."""
    ret = close.pct_change(lookback * 21)
    return ret.shift(skip)


def mean_reversion_5(close: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """Very short-term mean reversion (5-day)."""
    ret = close.pct_change(window)
    return -ret


def low_vol(close: pd.DataFrame, window: int = 63) -> pd.DataFrame:
    """Low-volatility anomaly: lower realized vol is better."""
    rets = close.pct_change()
    vol = rets.rolling(window).std()
    return -vol  # negative vol => higher signal
def blend_costrobust(close: pd.DataFrame, vol_window: int = 63,
                     rev_lookback: int = 12, mom_window: int = 12) -> pd.DataFrame:
    """Blend of cost-robust signals: reversal, low volatility, and value proxy."""
    rev = reversal(close, lookback=rev_lookback)
    lv = low_vol(close, window=vol_window)
    val = value(close)

    def zscore(x: pd.DataFrame) -> pd.DataFrame:
        arr = x.to_numpy()
        mu = np.nanmean(arr, axis=1, keepdims=True)
        sd = np.nanstd(arr, axis=1, keepdims=True) + 1e-9
        z = (arr - mu) / sd
        return pd.DataFrame(z, index=x.index, columns=x.columns)

    z = (zscore(rev) + zscore(lv) + zscore(val)) / 3.0
    return z


def time_series_momentum(close: pd.DataFrame, lookback: int = 12, skip: int = 1) -> pd.DataFrame:
    """Time-series momentum (trend following): long if own past return positive, short/flat if negative.

    Moskowitz, Ooi, Pedersen (2012) "Time Series Momentum". Uses each asset's own
    past return (absolute momentum) rather than cross-sectional rank.
    Monthly rebalancing implied; lookback in months, skip in months.
    """
    ret = close.pct_change(lookback * 21)
    return ret.shift(skip * 21)


def time_series_momentum_pure(close: pd.DataFrame, lookback: int = 12, skip: int = 1) -> pd.DataFrame:
    """Pure time-series momentum signal for absolute threshold weighting.

    Returns raw past returns (not cross-sectionally ranked). Used with
    backtest.time_series_momentum_weights for classic implementation.
    """
    ret = close.pct_change(lookback * 21)
    return ret.shift(skip * 21)


def beta_factor(
    close: pd.DataFrame,
    market_close: pd.Series,
    window: int = 252,
    skip: int = 1,
    shrink: float = 0.5,
) -> pd.DataFrame:
    """Rolling market beta of each stock vs a broad market index (e.g. SPY).

    Implements the beta estimator used by Frazzini & Pedersen (2014):
    a ``window``-day rolling regression of excess stock returns on excess market
    returns, with a Vasicek-style shrinkage toward 1.0 (``beta = shrink*1 + (1-shrink)*beta_hat``).
    The signal is lagged by ``skip`` days to avoid same-day look-ahead when weights
    formed at close are executed at the next open.

    Returns a DataFrame (index=date, columns=tickers) of per-stock beta.
    """
    r = close.pct_change()
    rm = market_close.pct_change()
    rm = rm.reindex(r.index)

    # rolling cross-moment E[r_i * r_m] and means via vectorised rolling stats
    r_mean = r.rolling(window).mean()
    rm_mean = rm.rolling(window).mean()
    cross_mean = r.mul(rm, axis=0).rolling(window).mean()
    cov = cross_mean - r_mean.mul(rm_mean, axis=0)
    var_m = rm.rolling(window).var(ddof=0)

    beta = cov.div(var_m, axis=0)
    # Vasicek shrink toward 1.0 (constrained investors ~ beta 1)
    beta = shrink * 1.0 + (1.0 - shrink) * beta
    if skip:
        beta = beta.shift(skip)
    return beta


def dollar_neutral_lowbeta(
    close: pd.DataFrame,
    market_close: pd.Series,
    beta_window: int = 252,
    shrink: float = 0.5,
) -> pd.DataFrame:
    """Dollar-neutral low-beta factor signal (Frazzini-Pedersen style).

    Long low-beta stocks, short high-beta stocks; dollar-neutral by construction.
    Returns the raw signal (negative beta) so the caller can apply
    ``backtest.dollar_neutral_longshort_weights``.

    Requires a market-close series (e.g. SPY) to compute rolling beta.
    """
    beta = beta_factor(close, market_close, window=beta_window, skip=1, shrink=shrink)
    return -beta
