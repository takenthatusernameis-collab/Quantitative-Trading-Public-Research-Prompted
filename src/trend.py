"""Price trend-following sleeve for the E023 Economic Trend blend.

Implements the directional price-trend-following specification used by
Brooks, Feilbogen, Ooi & Akant (2024), "Economic Trend" (SSRN 4710868,
AQR white paper), as the complement to the macro-momentum sleeve in
``src/macro.py``.

Paper construction (directional variant, US ETF-tradable):
- Price-trend factor per asset = equal-weighted combination of trailing
  1-month, 3-month, and 12-month asset returns (the paper's "equal
  weighted combination of 1-month, 3-month, and 12-month trailing asset
  returns as factors").
- Directional position: long when the factor is positive, short when
  negative (absolute threshold at zero).
- Positions scaled by inverse realized volatility so each active asset
  contributes equal risk; gross exposure normalized to 1.0 per sleeve.
- Monthly month-end rebalance; executed at next-day open.

This is the sleeve whose ~0.3 correlation with economic trend the paper
identifies as the source of complementarity: price trend wins in
persistent drawdowns, economic trend wins in drawdowns with economic
catalysts, and the blend covers both.
"""

import numpy as np
import pandas as pd


def price_trend_signal(close: pd.DataFrame,
                       lookbacks=(21, 63, 252)) -> pd.DataFrame:
    """Trailing-return price-trend factor per asset.

    Equal-weighted mean of the trailing 1m/3m/12m simple returns. The
    factor is NOT cross-sectionally ranked (time-series trend following),
    matching the paper's per-asset construction.
    """
    rets = close.pct_change()
    factor = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    for lb in lookbacks:
        factor = factor + rets.shift(1).rolling(lb).sum()
    return factor / float(len(lookbacks))


def price_trend_weights(
    close: pd.DataFrame,
    lookbacks=(21, 63, 252),
    vol_window: int = 63,
    long_only: bool = False,
) -> pd.DataFrame:
    """Daily target weights for the directional price-trend sleeve.

    Long assets with positive price-trend factor, short assets with
    negative factor; inverse-volatility scaled; gross exposure normalized
    to 1.0 (when long_only=False). Held constant between month-ends by
    the caller's forward-fill.

    Columns are ETF tickers (label-aligned with the price panel).
    """
    signal = price_trend_signal(close, lookbacks=lookbacks)
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    w = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    for date in close.index:
        row = signal.loc[date]
        if row.isna().all():
            continue
        active = row[row != 0].index
        if len(active) == 0:
            continue
        s = row[active]
        wv = inv_vol.loc[date, active].fillna(0.0)
        # directional sign from the factor; inverse-vol risk budget
        raw = np.sign(s) * wv
        gross = raw.abs().sum()
        if gross > 0:
            w.loc[date, active] = raw / gross
        elif long_only:
            # flat when no short side is allowed and factor is negative
            pass
    if long_only:
        w = w.clip(lower=0.0)
        gross = w.sum(axis=1).replace(0, np.nan)
        w = w.div(gross, axis=0).fillna(0.0)
    return w


def month_end_weights(weights: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill monthly weights onto the full daily index.

    Weights are set on the last trading day of each month and held
    constant until the next month-end (monthly rebalance). NaN-
    initialized so ffill propagates the month-end weights across the
    days between month-ends.
    """
    idx = weights.index
    me = idx.to_series().groupby(idx.to_period("M")).last().values
    me_idx = pd.DatetimeIndex(me)
    w = pd.DataFrame(np.nan, index=idx, columns=weights.columns)
    w.loc[me_idx] = weights.loc[me_idx]
    return w.ffill().fillna(0.0)