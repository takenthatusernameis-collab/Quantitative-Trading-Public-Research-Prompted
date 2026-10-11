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


def _weights_from_signal(signal: pd.DataFrame,
                        close: pd.DataFrame,
                        vol_window: int = 63,
                        long_only: bool = False) -> pd.DataFrame:
    """Directional inverse-vol weights from a precomputed trend-factor signal.

    Long assets with positive factor, short assets with negative factor;
    inverse-volatility scaled; gross exposure normalized to 1.0 (when
    long_only=False). Separated from :func:`price_trend_weights` so the
    placebo can swap in a block-permuted signal while keeping the
    volatility risk-budget (a property of prices, not the signal) intact.
    """
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
    return _weights_from_signal(signal, close, vol_window=vol_window,
                                long_only=long_only)


def month_end_weights(weights: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill monthly weights onto the full daily index.

    Weights are set on the last trading day of each month and held
    constant until the next month-end. NaN-initialized so ffill
    propagates the month-end weights across the days between
    month-ends.
    """
    idx = weights.index
    me = idx.to_series().groupby(idx.to_period("M")).last().values
    me_idx = pd.DatetimeIndex(me)
    w = pd.DataFrame(np.nan, index=idx, columns=weights.columns)
    w.loc[me_idx] = weights.loc[me_idx]
    return w.ffill().fillna(0.0)


def block_permute_signal(signal: pd.DataFrame, block_months: int = 12,
                         seed: int = 42) -> pd.DataFrame:
    """Permute a monthly-indexed signal in contiguous blocks (placebo null).

    Destroys time alignment with forward returns while preserving each
    asset's signal distribution and within-block persistence. Applied
    per asset (column) independently. Used for the price-trend sleeve's
    matched placebo in the E023 Economic Trend blend.
    """
    rng = np.random.default_rng(seed)
    out = signal.copy()
    n = len(signal)
    starts = list(range(0, n, block_months))
    for col in signal.columns:
        vals = signal[col].to_numpy()
        blocks = [vals[s:s + block_months] for s in starts if s < n]
        order = rng.permutation(len(blocks))
        out[col] = np.concatenate([blocks[i] for i in order])
    return out


def price_trend_monthly_weights(
    close: pd.DataFrame,
    lookbacks=(21, 63, 252),
    vol_window: int = 63,
    long_only: bool = False,
) -> pd.DataFrame:
    """Month-end-anchored directional price-trend weights.

    Convenience wrapper around :func:`price_trend_weights` +
    :func:`month_end_weights`: weights are set on the last trading day
    of each month (using signals available at that close) and held
    constant until the next month-end. This matches the rebalance
    cadence of the macro momentum sleeve (E022) so the two sleeves
    can be blended on a common calendar.
    """
    w = price_trend_weights(close, lookbacks=lookbacks, vol_window=vol_window,
                           long_only=long_only)
    return month_end_weights(w)


def block_permute_monthly_factor(signal: pd.DataFrame, block_months: int = 12,
                                  seed: int = 42) -> pd.DataFrame:
    """Permute a daily-indexed trend factor at month-end nodes in blocks.

    Extracts the last row of each calendar month, permutes each asset's
    month-end factor values in contiguous 12-month blocks, and
    forward-fills the permuted month-end values onto the full daily
    index. Preserves each asset's factor distribution and within-block
    persistence while destroying time alignment with forward returns.
    Used for the price-trend sleeve's matched placebo in the E023
    Economic Trend blend.
    """
    idx = signal.index
    me = idx.to_series().groupby(idx.to_period("M")).last().values
    me_idx = pd.DatetimeIndex(me)
    me_sig = signal.reindex(me_idx)
    rng = np.random.default_rng(seed)
    n = len(me_idx)
    starts = list(range(0, n, block_months))
    out_me = me_sig.copy()
    for col in me_sig.columns:
        vals = me_sig[col].to_numpy()
        blocks = [vals[s:s + block_months] for s in starts if s < n]
        order = rng.permutation(len(blocks))
        out_me[col] = np.concatenate([blocks[i] for i in order])
    out = pd.DataFrame(np.nan, index=idx, columns=signal.columns)
    out.loc[me_idx] = out_me
    return out.ffill()


def price_trend_monthly_weights_from_signal(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    long_only: bool = False,
) -> pd.DataFrame:
    """Month-end-anchored weights from a precomputed trend-factor signal.

    Same construction as :func:`price_trend_monthly_weights` but takes the
    factor signal directly (e.g. a block-permuted copy for the matched
    placebo). The volatility risk budget is derived from prices, not the
    signal, so it is preserved across placebo permutations.
    """
    w = _weights_from_signal(signal, close, vol_window=vol_window,
                             long_only=long_only)
    return month_end_weights(w)