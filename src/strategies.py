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
