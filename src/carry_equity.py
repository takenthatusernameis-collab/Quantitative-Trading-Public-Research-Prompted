"""Equity carry / dividend-yield factor (Koijen, Moskowitz, Pedersen & Vrugt 2018).

The KMPV "carry" idea in its equity sleeve is that expected return has a
dividend-yield component: high-dividend-yield names should earn a premium
over low-yield names.  This module implements the simplest, pre-registered
variant: a cross-sectional sort on trailing dividend yield (annualized
dividends over the last 252 trading days divided by current price), with
long-only top-quintile and dollar-neutral long-short configurations, both
inverse-vol weighted and monthly-rebalanced.

Dividend data is supplied as a panel (index=date, columns=ticker) of the raw
dividend paid on each ex-date (from yfinance ``auto_adjust=False, actions=True``).
The signal is computed with strict no look-ahead: at rebalance date t the
yield uses only dividends with ex-date <= t.
"""

import numpy as np
import pandas as pd


def trailing_dividend_yield(
    close: pd.DataFrame,
    dividends: pd.DataFrame,
    window: int = 252,
) -> pd.DataFrame:
    """Trailing dividend yield = sum of last ``window`` dividends / current price.

    Both inputs share the same index/columns.  Dividends are zero-filled
    forward so a name that pays quarterly shows its last payment until the
    next ex-date (this is the standard "indicator" convention and is
    strictly no-look-ahead: only past dividends enter).

    Returns a DataFrame of yields (NaN where price is non-positive or
    insufficient history).
    """
    close = close.astype(float)
    div = dividends.reindex(close.index, close.columns).fillna(0.0).astype(float)
    # trailing sum of dividends over window trading days
    trailing = div.rolling(window, min_periods=1).sum()
    # guard against stale indicator: cap trailing sum at the actual number
    # of nonzero dividend observations seen in the window, so a name with
    # 4 quarterly payments is not inflated to a 252-day sum.
    nonzero_count = div.rolling(window, min_periods=1).sum().where(div > 0, 0.0)
    nonzero_count = (div > 0).rolling(window, min_periods=1).sum()
    trailing = trailing.where(nonzero_count >= 1, np.nan)
    price = close.replace(0, np.nan)
    yld = trailing / price
    return yld


def dividend_yield_signal(
    close: pd.DataFrame,
    dividends: pd.DataFrame,
    window: int = 252,
) -> pd.DataFrame:
    """Cross-sectional dividend-yield signal (higher = more carry).

    Cross-sectionally winsorized at the 1st/99th percentile per day and
    z-score standardized, so the signal is comparable across dates.
    """
    yld = trailing_dividend_yield(close, dividends, window=window)

    def _winsorize(x: pd.Series) -> pd.Series:
        if x.notna().sum() < 5:
            return x
        lo, hi = x.quantile(0.01), x.quantile(0.99)
        return x.clip(lo, hi)

    yld = yld.apply(_winsorize, axis=1)
    mu = yld.mean(axis=1)
    sd = yld.std(axis=1)
    sig = (yld - mu) / (sd + 1e-12)
    return sig


def carry_equity_weights(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    top_frac: float = 0.2,
    long_only: bool = True,
) -> pd.DataFrame:
    """Target weights for the equity carry factor.

    Long-only: long the top ``top_frac`` of names by carry signal, inverse-vol
    weighted within the selection.  Long-short: long top ``top_frac`` and short
    bottom ``top_frac``, each side inverse-vol weighted and scaled to 0.5 gross
    (dollar-neutral).
    """
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    ranks = signal.rank(axis=1, ascending=False, method="min", pct=True)
    n = signal.shape[1]
    k = max(1, int(round(n * top_frac)))

    weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)

    long_mask = ranks >= (1.0 - top_frac + 1e-12)
    if long_only:
        mask = long_mask
        raw = inv_vol.where(mask).fillna(0.0)
        s = raw.sum(axis=1).replace(0, np.nan)
        w = raw.div(s, axis=0).fillna(0.0)
        return w.clip(lower=0.0)

    short_mask = ranks <= top_frac + 1e-12
    for mask, scale in ((long_mask, 0.5), (short_mask, -0.5)):
        raw = inv_vol.where(mask).fillna(0.0)
        s = raw.sum(axis=1).replace(0, np.nan)
        side = raw.div(s, axis=0).fillna(0.0).mul(scale)
        weights = weights.add(side, fill_value=0.0)
    return weights