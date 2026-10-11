"""Futures roll methodology and carry construction.

yfinance serves front-month continuous futures (ticker suffix ``=F``).
These series are stitched at the data provider's (undocumented) roll
date, so every contract switch injects an artificial overnight gap
equal to the one-period basis between the expiring and the new
contract. For financial futures the gap is small (a few bps per
quarter); for commodities it can be extreme: CL=F printed -37.63 on
2020-04-20 (the expiring May contract traded negative) and +10.01 on
2020-04-21 (the June contract), a ~126% overnight "return" that is
purely a stitching artifact and would dominate any naive backtest.

This module provides:

1. ``detect_seams`` - data-driven roll-seam detection. Within each
   contract's expected roll window (business days 1-18 of the roll
   month: every month for commodity roots, Mar/Jun/Sep/Dec for
   quarterly financial roots), the seam is the trading day whose
   overnight futures move deviates most from the paired spot ETF's
   move. The spot ETF tracks the same underlying, so a large
   futures-only gap is a stitching artifact, not a market move.
   Outlier days (futures-vs-spot excess gap > 50%) are flagged as
   seams regardless of calendar (data errors, roll wedges such as
   the April 2020 CL event).

2. ``deseam_returns`` / ``deseam_index`` - a de-seamed return
   series: seam-day futures returns are replaced by the paired spot
   ETF return, a proxy for the true underlying move. This removes
   the basis jump while preserving the actual market direction on
   the roll day (standard ratio back-adjustment zeroes the seam-day
   return instead; anchoring to the spot ETF is strictly more
   informative). The synthetic index built from these returns is
   suitable for signal generation and performance measurement.

3. ``basis_carry`` - the carry proxy of Koijen, Moskowitz,
   Pedersen & Vrugt (2018, "Carry", JFE): carry = (S - F) / S,
   the return of a long futures position if the spot price is
   unchanged. Positive in backwardation (commodities), for
   high-interest-rate currencies (FX futures price below spot when
   the foreign rate exceeds the domestic rate), and for high-yield
   bonds/equities (yield exceeds financing).
"""

import numpy as np
import pandas as pd

# Roll cadence per contract root.
QUARTERLY_ROOTS = {"ES", "NQ", "YM", "RTY", "ZB", "ZN", "6E", "6B", "6J"}
MONTHLY_ROOTS = {"GC", "SLV", "CL", "NG", "SB", "ZC"}


def root_of(ticker: str) -> str:
    return ticker.split("=")[0].upper()


def cadence_of(ticker: str) -> str:
    """Expected roll cadence for a continuous futures ticker."""
    root = root_of(ticker)
    if root in QUARTERLY_ROOTS:
        return "quarterly"
    if root in MONTHLY_ROOTS:
        return "monthly"
    return "monthly"


def _roll_months(dates, cadence):
    """(year, month) pairs present in the index for the cadence."""
    months = sorted({(d.year, d.month) for d in dates})
    if cadence == "quarterly":
        return [(y, m) for (y, m) in months if m in (3, 6, 9, 12)]
    return months


def detect_seams(
    fut: pd.Series,
    spot: pd.Series,
    cadence: str = "monthly",
    win_start: int = 1,
    win_end: int = 18,
    cal_threshold: float = 0.0015,
    outlier_threshold: float = 0.5,
) -> pd.DatetimeIndex:
    """Detect roll-seam dates in a stitched front-month futures series.

    Two detectors:
    - Calendar: within each expected roll window, the day with the
      maximum absolute excess overnight move (futures return minus
      paired spot ETF return) is a seam if the excess exceeds
      ``cal_threshold`` (15 bps).
    - Outlier: any day whose excess move exceeds
      ``outlier_threshold`` (50%) is a seam regardless of calendar
      (roll wedges, negative-price events, data errors).

    Returns a sorted DatetimeIndex of seam dates.
    """
    fut = fut.dropna()
    spot = spot.reindex(fut.index).ffill()
    r_fut = fut.pct_change()
    r_spot = spot.pct_change()
    excess = (r_fut - r_spot).abs()

    seam_pos = set()

    # Calendar-based detection inside expected roll windows.
    for (y, m) in _roll_months(fut.index, cadence):
        pos = [i for i, d in enumerate(fut.index) if d.year == y and d.month == m]
        if len(pos) <= win_end:
            continue
        window = pos[win_start - 1: win_end]
        if not window:
            continue
        best = max(window, key=lambda i: float(excess.iloc[i]))
        if float(excess.iloc[best]) >= cal_threshold:
            seam_pos.add(best)

    # Outlier-based detection on any day.
    for i in range(1, len(excess)):
        if float(excess.iloc[i]) >= outlier_threshold:
            seam_pos.add(i)

    if not seam_pos:
        return pd.DatetimeIndex([])
    seams = fut.index[sorted(seam_pos)]
    return pd.DatetimeIndex(seams)


def deseam_returns(
    fut: pd.Series,
    spot: pd.Series,
    seams: pd.DatetimeIndex,
) -> pd.Series:
    """Return series with seam-day returns replaced by the spot ETF return."""
    r_fut = fut.pct_change()
    r_spot = spot.reindex(fut.index).ffill().pct_change()
    clean = r_fut.copy()
    for s in seams:
        if s in clean.index and s in r_spot.index:
            clean.loc[s] = r_spot.loc[s]
    return clean


def deseam_index(clean_ret: pd.Series, base: float = 100.0) -> pd.Series:
    """Synthetic price index built from a (de-seamed) return series."""
    return (1.0 + clean_ret.fillna(0.0)).cumprod() * base


def basis_carry(fut: pd.Series, spot: pd.Series, cap: float = 0.35) -> pd.Series:
    """Raw basis carry proxy (KMPV 2018): carry = (S - F) / S, winsorized.

    Only meaningful when ``fut`` and ``spot`` are quoted in identical
    units (true spot vs futures on the same underlying). With ETF
    proxies the unit multipliers differ (one GLD share ~= 0.09 oz of
    gold vs one GC contract = 100 oz), so use
    ``normalized_basis_carry`` for cross-contract comparisons.
    The cap bounds pathological prints such as negative oil futures
    (2020-04-20) that would otherwise produce carry > 1.
    """
    s = spot.reindex(fut.index).ffill()
    carry = (s - fut) / s
    return carry.clip(-cap, cap)


def normalized_basis_carry(
    fut: pd.Series,
    spot: pd.Series,
    window: int = 252,
    cap: float = 0.35,
) -> pd.Series:
    """Scale-invariant carry proxy for futures-vs-ETF pairs.

    The raw basis (S - F)/S is dominated by the (unknown, slowly
    drifting) unit ratio between one ETF share and one futures
    contract, so it cannot be compared across contracts. We therefore
    normalize each contract's F/S ratio by its own rolling median over
    the past ``window`` days, lagged one day to avoid look-ahead:

        carry = 1 - (F/S)_t / median(F/S)_{t-window..t-1}

    Positive when the futures trades cheap relative to its own recent
    norm (more backwardated / less contangoed than usual), matching
    the sign of the KMPV carry (positive in backwardation). With
    ETF-fee drag (~0.4%/yr) far slower than the 252d window, the
    median absorbs the unit ratio; the signal is the deviation of
    the basis from its own norm.
    """
    s = spot.reindex(fut.index).ffill()
    ratio = fut / s
    norm = ratio.rolling(window, min_periods=window // 2).median().shift(1)
    carry = 1.0 - ratio / norm
    return carry.clip(-cap, cap)


def realized_roll_yield(
    fut: pd.Series,
    spot: pd.Series,
    seams: pd.DatetimeIndex,
    window: int = 252,
    cap: float = 0.35,
) -> pd.Series:
    """Trailing realized roll yield from detected seam excess gaps.

    At each roll seam the raw futures return exceeds the paired spot
    ETF return by the one-period basis jump between the expiring and
    the new contract (contango: positive gap; backwardation: negative
    gap). The negative trailing sum over ``window`` days is the
    realized roll yield of a continuously-rolled position over the
    past year: positive in backwardation, negative in contango.
    Unit-free (a difference of returns), so it needs no multiplier
    adjustment. Lagged one day (a seam is only known after it occurs).
    """
    r_fut = fut.pct_change()
    r_spot = spot.reindex(fut.index).ffill().pct_change()
    excess = r_fut - r_spot
    seam_mask = pd.Series(False, index=fut.index)
    seam_mask.loc[seam_mask.index.intersection(pd.DatetimeIndex(seams))] = True
    seam_excess = excess.where(seam_mask, 0.0)
    rroll = -seam_excess.rolling(window, min_periods=1).sum().shift(1)
    return rroll.clip(-cap, cap)
