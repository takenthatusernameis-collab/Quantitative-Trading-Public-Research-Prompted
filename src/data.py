"""Data acquisition and caching for quantitative backtesting.

Uses yfinance as a free, public data source. All timestamps are UTC.
Caches to parquet files in the data/ directory to avoid repeated downloads.
"""

import os
from datetime import datetime
from typing import List, Optional

import pandas as pd
import yfinance as yf

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def _cache_path(ticker: str, start: str, end: str) -> str:
    safe = ticker.replace("/", "_").replace("^", "")
    return os.path.join(DATA_DIR, f"{safe}_{start}_{end}.parquet")


def download(
    tickers: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    auto_adjust: bool = True,
    force: bool = False,
) -> pd.DataFrame:
    """Download adjusted OHLCV data for one or more tickers.

    Returns a DataFrame indexed by Date with a MultiIndex (Ticker, Column).
    """
    if start is None:
        start = "2015-01-01"
    if end is None:
        end = datetime.utcnow().strftime("%Y-%m-%d")

    cache = _cache_path("|".join(tickers), start, end)
    if not force and os.path.exists(cache):
        try:
            df = pd.read_parquet(cache)
            if not df.empty:
                return df
        except Exception:
            pass

    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=auto_adjust,
        progress=False,
        group_by="ticker",
    )
    if raw.empty:
        raise RuntimeError(f"yfinance returned no data for {tickers}")

    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = list(tickers)

    # Normalize to a consistent MultiIndex (Ticker, Price)
    if isinstance(raw.columns, pd.MultiIndex):
        # yfinance may return (Ticker, Price) or (Price, Ticker); ensure outer = Ticker
        raw.columns.names = ["Ticker", "Price"]
        if raw.columns.names[0] != "Ticker":
            raw = raw.swaplevel(0, 1, axis=1)
            raw.columns.names = ["Ticker", "Price"]
        # flatten any nested tuples that arose from prior wrapping
        raw.columns = pd.MultiIndex.from_tuples(
            [(str(c[0]), str(c[-1])) for c in raw.columns]
        )
        raw.columns.names = ["Ticker", "Price"]
        raw = raw.sort_index(axis=1)
    else:
        raw.columns = pd.MultiIndex.from_product([tickers, raw.columns])
        raw.columns.names = ["Ticker", "Price"]

    raw.index = pd.to_datetime(raw.index).tz_localize(None)
    raw.to_parquet(cache)
    return raw


def wide_close(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """Return a single-ticker DataFrame with standard columns."""
    if isinstance(df.columns, pd.MultiIndex):
        sub = df[ticker].copy()
    else:
        sub = df.copy()
    # flatten any remaining nested tuples
    if isinstance(sub.columns, pd.MultiIndex):
        sub.columns = [str(c[-1]) for c in sub.columns]
    else:
        sub.columns = [str(c) for c in sub.columns]
    sub = sub[["Open", "High", "Low", "Close", "Volume"]]
    sub.columns = [c.lower() for c in sub.columns]
    return sub.dropna(subset=["close"])


def get_panel(df: pd.DataFrame, field: str = "Close") -> pd.DataFrame:
    """Return a wide DataFrame of a single price field across all tickers."""
    if isinstance(df.columns, pd.MultiIndex):
        if "Price" in df.columns.names:
            panel = df.xs(field, level="Price", axis=1)
        else:
            panel = df[field]
    else:
        panel = df[[field]].copy()
        panel.columns = ["close"]
    return panel


def get_benchmark(ticker: str = "SPY", **kwargs) -> pd.DataFrame:
    return wide_close(download([ticker], **kwargs), ticker)