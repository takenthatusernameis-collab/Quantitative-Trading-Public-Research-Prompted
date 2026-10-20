"""Macro momentum signals and portfolio construction.

Implements the directional variant of Brooks (2017) "A Half-Century of
Macro Momentum" (AQR white paper, 2017-08-10) for a US-only,
ETF-tradable universe:

- Four macro themes: business cycle (growth), international trade,
  monetary policy, risk sentiment.
- Three asset classes with liquid ETF proxies: equities (SPY),
  government bonds (IEF), commodities (GLD).
- Each theme-asset cell carries a directional position:
  structural sign x standardized theme momentum, equal-weighted across
  the 12 cells, gross exposure normalized to 1.0.
- Monthly rebalance at month-end; executed at next-day open.

Data integrity (prioritization v1.2 screen):
- FRED series are native (not stitched/continuous contracts), so no
  roll-seam artifacts; the main integrity risk is data revision and
  release lag. Mitigation: at the last trading day of month M the
  signal uses macro reference data through month M-1 only (a
  conservative release-lag emulation). Revised-vintage look-ahead is
  a residual caveat recorded in the experiment ledger.
- FRED public CSV endpoint (fredgraph.csv) requires no API key.
"""

import hashlib
import io
import os
import urllib.request
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.data import DATA_DIR
from src.offline import OfflineDataUnavailable, offline_required

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"

# Theme definitions: (theme, FRED series id, momentum type)
#   pct : 6-month percent change of the level (growth-like series)
#   diff: 6-month change of the level (rate/index series)
# Five core themes from Brooks (2017) + extended themes from E038 feasibility screen.
# E038 confirmed all series have 150+ monthly obs from 2014+ (sufficient for 504d WF).
THEMES: Dict[str, dict] = {
    # Core 5 (Brooks 2017 directional variant)
    "growth": {"series": "INDPRO", "kind": "pct",
               "desc": "Industrial production, 6m pct change"},
    "trade": {"series": "EXUSEU", "kind": "pct",
              "desc": "US exports to EU (trade proxy), 6m pct change"},
    "policy": {"series": "FEDFUNDS", "kind": "diff",
               "desc": "Effective federal funds rate, 6m change"},
    "sentiment": {"series": "UMCSENT", "kind": "diff",
                  "desc": "Michigan consumer sentiment, 6m change"},
    "inflation": {"series": "CPIAUCSL", "kind": "pct",
                  "desc": "CPI, 6m pct change"},
    # Extended themes (E038 feasibility screen: all have 150+ obs 2014+)
    "labor_payrolls": {"series": "PAYEMS", "kind": "pct",
                       "desc": "Nonfarm payrolls, 6m pct change"},
    "labor_unemployment": {"series": "UNRATE", "kind": "diff",
                           "desc": "Unemployment rate, 6m change"},
    "yield_curve_10y2y": {"series": "T10Y2Y", "kind": "diff",
                          "desc": "10Y-2Y spread, 6m change"},
    "yield_curve_10y3m": {"series": "T10Y3M", "kind": "diff",
                          "desc": "10Y-3M spread, 6m change"},
    "credit_spreads": {"series": "BAA10Y", "kind": "diff",
                       "desc": "Baa-10Y spread, 6m change"},
    "financial_conditions": {"series": "VIXCLS", "kind": "diff",
                             "desc": "VIX, 6m change"},
    "commodities_oil": {"series": "DCOILWTICO", "kind": "pct",
                        "desc": "WTI crude oil, 6m pct change"},
    "consumption_pce": {"series": "PCEPI", "kind": "pct",
                        "desc": "PCE price index, 6m pct change"},
    "consumption_retail": {"series": "RSAFS", "kind": "pct",
                           "desc": "Retail sales, 6m pct change"},
    "housing_starts": {"series": "HOUST", "kind": "pct",
                       "desc": "Housing starts, 6m pct change"},
}

# Structural sign matrix: asset x theme.
# Documented mapping (Brooks 2017, directional variant):
#   growth improving  -> long equities, short bonds, long commodities
#   trade (export) growth -> procyclical: long equities, short bonds,
#                            long commodities
#   policy tightening (rates rising) -> short equities, short bonds,
#                            short commodities
#   sentiment improving -> long equities, short bonds, long commodities
#   inflation rising  -> short equities, short bonds, long commodities
# Extended themes (E038/E039 pre-registered):
#   labor_payrolls rising (employment growth) -> procyclical: +equity, -bonds, +commodities
#   labor_unemployment rising (unemployment up) -> countercyclical: -equity, +bonds, -commodities
#   yield_curve_10y2y steepening -> reflationary/pro-growth: +equity, -bonds, +commodities
#   yield_curve_10y3m steepening -> reflationary/pro-growth: +equity, -bonds, +commodities
#   credit_spreads widening -> risk-off: -equity, +bonds, -commodities
#   financial_conditions (VIX) rising -> risk-off: -equity, +bonds, -commodities
#   commodities_oil rising -> inflationary: -equity, -bonds, +commodities
#   consumption_pce rising (core inflation) -> inflationary: -equity, -bonds, +commodities
#   consumption_retail rising (consumer strength) -> procyclical: +equity, -bonds, +commodities
#   housing_starts rising -> procyclical: +equity, -bonds, +commodities
# Bonds carry no positive structural sign: no theme's improvement is
# bond-positive; bonds are the risk-off asset (long when the cycle,
# sentiment or policy stance deteriorates).
THEME_SIGNS: Dict[str, Dict[str, float]] = {
    "equity": {
        "growth": +1.0, "trade": +1.0, "policy": -1.0,
        "sentiment": +1.0, "inflation": -1.0,
        "labor_payrolls": +1.0, "labor_unemployment": -1.0,
        "yield_curve_10y2y": +1.0, "yield_curve_10y3m": +1.0,
        "credit_spreads": -1.0, "financial_conditions": -1.0,
        "commodities_oil": -1.0, "consumption_pce": -1.0,
        "consumption_retail": +1.0, "housing_starts": +1.0,
    },
    "bonds": {
        "growth": -1.0, "trade": -1.0, "policy": -1.0,
        "sentiment": -1.0, "inflation": -1.0,
        "labor_payrolls": -1.0, "labor_unemployment": +1.0,
        "yield_curve_10y2y": -1.0, "yield_curve_10y3m": -1.0,
        "credit_spreads": +1.0, "financial_conditions": +1.0,
        "commodities_oil": -1.0, "consumption_pce": -1.0,
        "consumption_retail": -1.0, "housing_starts": -1.0,
    },
    "commodities": {
        "growth": +1.0, "trade": +1.0, "policy": -1.0,
        "sentiment": +1.0, "inflation": +1.0,
        "labor_payrolls": +1.0, "labor_unemployment": -1.0,
        "yield_curve_10y2y": +1.0, "yield_curve_10y3m": +1.0,
        "credit_spreads": -1.0, "financial_conditions": -1.0,
        "commodities_oil": +1.0, "consumption_pce": +1.0,
        "consumption_retail": +1.0, "housing_starts": +1.0,
    },
}

ASSET_ETF = {"equity": "SPY", "bonds": "IEF", "commodities": "GLD"}


def fetch_fred(series_id: str, force: bool = False) -> pd.Series:
    """Download a FRED series via the public CSV endpoint and cache to parquet.

    Returns a Series indexed by reference date (monthly or daily).
    """
    h = hashlib.sha256(series_id.encode()).hexdigest()[:16]
    cache = os.path.join(DATA_DIR, f"fred_{series_id}_{h}.parquet")
    if not force and os.path.exists(cache):
        try:
            df = pd.read_parquet(cache)
            s = df.iloc[:, 0]
            s.index = pd.to_datetime(df.index)
            return pd.Series(pd.to_numeric(s, errors="coerce"), index=s.index, name=series_id)
        except Exception:
            pass
    url = FRED_CSV.format(series_id)
    if offline_required():
        raise OfflineDataUnavailable(
            f"offline mode: the cached FRED series is missing and the network "
            f"is not allowed. Missing cache file: {cache}\n"
            f"  The committed artifacts depend on this input; it must be pinned "
            f"into data/ and recorded in ledger/data_baseline.json."
        )
    raw = urllib.request.urlopen(url, timeout=60).read().decode()
    df = pd.read_csv(io.StringIO(raw))
    df.columns = ["date", series_id]
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=[series_id]).copy()
    df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
    df = df.dropna(subset=[series_id])
    s = pd.Series(df[series_id].values, index=df["date"].values, name=series_id)
    s.index = pd.to_datetime(s.index)
    s = s[~s.index.duplicated(keep="last")].sort_index()
    s.to_frame().to_parquet(cache)
    return s


def _momentum(series: pd.Series, window: int, kind: str) -> pd.Series:
    """Trailing momentum of a monthly series, indexed by reference month."""
    if kind == "pct":
        return series.pct_change(window) * 100.0
    return series.diff(window)


def theme_momentum(release_lag_months: int = 1, window: int = 6) -> pd.DataFrame:
    """Build raw (unstandardized) theme momentum, release-lagged.

    At month M the latest usable reference month is M - release_lag_months
    (conservative emulation of FRED release calendars). Returns a DataFrame
    indexed by month-end reference month with one column per theme.
    """
    cols = {}
    for theme, spec in THEMES.items():
        s = fetch_fred(spec["series"])
        # monthly series: anchor to month start; apply release lag
        m = s.resample("MS").last()
        m = m.dropna()
        avail = m.shift(release_lag_months)  # at month M, data through M-lag
        cols[theme] = _momentum(avail, window, spec["kind"])
    return pd.DataFrame(cols).dropna(how="all")


def theme_signals(window: int = 6, zscore_window: int = 60,
                  min_periods: int = 36) -> pd.DataFrame:
    """Standardized (rolling z-score) theme momentum signals.

    z = (momentum_t - mean(momentum_{t-59..t})) / std(momentum_{t-59..t}),
    computed on release-lagged data so no future information is used.
    """
    mom = theme_momentum(window=window)
    mu = mom.rolling(zscore_window, min_periods=min_periods).mean()
    sd = mom.rolling(zscore_window, min_periods=min_periods).std()
    z = (mom - mu) / sd.replace(0, np.nan)
    return z.dropna(how="all")


def month_end_dates(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Last trading day of each calendar month present in idx."""
    return idx.to_series().groupby(idx.to_period("M")).last().values


def macro_momentum_weights(
    signals: pd.DataFrame,
    daily_index: pd.DatetimeIndex,
    asset_map: Optional[Dict[str, str]] = None,
    theme_signs: Optional[Dict[str, Dict[str, float]]] = None,
) -> pd.DataFrame:
    """Daily target weights for the directional macro momentum portfolio.

    Weights are set on the last trading day of each month (using the
    signal of that month, which embeds the release lag) and held
    constant until the next month-end. Gross exposure normalized to 1.0.
    Returns a DataFrame indexed by daily_index with one column per asset.
    """
    asset_map = asset_map or ASSET_ETF
    theme_signs = theme_signs or THEME_SIGNS
    assets = list(asset_map.keys())
    all_themes = []
    for a in assets:
        for k in theme_signs[a]:
            if k not in all_themes:
                all_themes.append(k)

    me = month_end_dates(daily_index)
    me_idx = pd.DatetimeIndex(me)
    # signal as-of each month-end: last available monthly signal at/before
    sig_at_me = signals.reindex(me_idx, method="ffill")

    w_me = pd.DataFrame(0.0, index=me_idx,
                        columns=[asset_map[a] for a in assets])
    for a in assets:
        total = pd.Series(0.0, index=me_idx)
        for k in all_themes:
            total = total + theme_signs[a].get(k, 0.0) * sig_at_me[k].fillna(0.0)
        w_me[asset_map[a]] = total / len(all_themes)
    gross = w_me.abs().sum(axis=1).replace(0, np.nan)
    w_me = w_me.div(gross, axis=0).fillna(0.0)

    # NaN-initialize so ffill propagates month-end weights across
    # the days between month-ends (0.0 is a valid held weight,
    # not a missing one). Columns are ETF tickers so the frame
    # label-aligns with yfinance price panels in the backtest engine.
    w = pd.DataFrame(np.nan, index=daily_index,
                     columns=[asset_map[a] for a in assets])
    w.loc[me_idx] = w_me
    return w.ffill().fillna(0.0)


def block_permute_signals(signals: pd.DataFrame, block_months: int = 12,
                           seed: int = 42) -> pd.DataFrame:
    """Permute monthly theme signals in contiguous blocks (placebo null).

    Destroys time alignment between macro trends and asset returns while
    preserving each theme's signal distribution and within-block
    persistence. Applied per theme independently.
    """
    rng = np.random.default_rng(seed)
    out = signals.copy()
    n = len(signals)
    starts = list(range(0, n, block_months))
    for col in signals.columns:
        vals = signals[col].to_numpy()
        blocks = [vals[s:s + block_months] for s in starts if s < n]
        order = rng.permutation(len(blocks))
        out[col] = np.concatenate([blocks[i] for i in order])
    return out
