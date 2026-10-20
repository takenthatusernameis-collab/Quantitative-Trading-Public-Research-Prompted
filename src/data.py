"""Data acquisition and caching for quantitative backtesting.

Uses yfinance as a free, public data source. All timestamps are UTC.
Caches to parquet files in the data/ directory to avoid repeated downloads.
"""

import json
import os
import time
import warnings
from datetime import datetime, timezone
from typing import List, Optional

import pandas as pd
import yfinance as yf

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

VINTAGES_PATH = os.path.join(DATA_DIR, "vintages.json")


def _offline_required() -> bool:
    """True when the environment forbids fetching data from the network.

    The verification suite sets this so that a driver can never silently
    re-download an input that is not pinned in the repository: a missing
    cache entry becomes a hard, named failure instead of a quiet network call
    whose result is not reproducible.
    """
    return offline_required()


def _load_vintages() -> dict:
    """Load the vintages manifest if it exists."""
    if os.path.exists(VINTAGES_PATH):
        try:
            with open(VINTAGES_PATH) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _get_vintage_end_date() -> Optional[str]:
    """Get the pinned end date from vintages manifest when SEED is set."""
    seed = os.environ.get("SEED")
    if seed:
        vintages = _load_vintages()
        # Default to the archive date if no specific entry
        return vintages.get("default_end_date")
    return None


def _resolve_end_date(end: Optional[str] = None) -> str:
    """Resolve the end date with priority: explicit param > END_DATE env > vintage > utcnow."""
    if end is not None:
        return end
    env_end = os.environ.get("END_DATE")
    if env_end:
        return env_end
    vintage_end = _get_vintage_end_date()
    if vintage_end:
        return vintage_end
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def pinned_end_date() -> str:
    """The end date of the pinned data vintage, independent of the clock.

    Use this for any download whose result must stay reproducible over time
    (rather than following the calendar). Falls back to today when no
    vintage is pinned.
    """
    vintage_end = _load_vintages().get("default_end_date")
    if vintage_end:
        return vintage_end
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


import hashlib

from .cache_keys import cache_filename, cache_filename_with_flags
from .offline import OFFLINE_ENV, OfflineDataUnavailable, offline_required


def _cache_path(ticker: str, start: str, end: str) -> str:
    # Use hash to avoid overly long filenames. The naming rule lives in
    # src/cache_keys.py so the cache-coverage audit (scripts/check_data_coverage.py)
    # recomputes exactly the same names.
    return os.path.join(DATA_DIR, cache_filename(ticker, start, end))


def _download_with_retry(tickers: List[str], start: str, end: str, auto_adjust: bool,
                         actions: bool = False,
                         max_retries: int = 3, delay: float = 2.0) -> pd.DataFrame:
    """Download data with exponential-backoff retries for transient rate limits."""
    for attempt in range(1, max_retries + 1):
        raw = yf.download(
            tickers,
            start=start,
            end=end,
            auto_adjust=auto_adjust,
            actions=actions,
            progress=False,
            group_by="ticker",
        )
        if not raw.empty:
            return raw
        if attempt < max_retries:
            time.sleep(delay * attempt)
    raise RuntimeError(f"yfinance returned no data for {tickers} after {max_retries} attempts")


def download(
    tickers: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    auto_adjust: bool = True,
    actions: bool = False,
    force: bool = False,
) -> pd.DataFrame:
    """Download OHLCV data for one or more tickers.

    Returns a DataFrame indexed by Date with a MultiIndex (Ticker, Column).
    With ``actions=True``, also includes Dividends and Stock Splits columns
    (requires ``auto_adjust=False`` to be meaningful).

    The ``end`` parameter can be explicitly provided, or controlled via the
    ``END_DATE`` environment variable. When ``SEED`` is set (for reproducible
    runs), the end date is read from ``data/vintages.json`` if available,
    falling back to the environment variable or current date.
    """
    if start is None:
        start = "2015-01-01"
    end = _resolve_end_date(end)

    cache = os.path.join(
        DATA_DIR, cache_filename_with_flags("|".join(tickers), start, end,
                                            auto_adjust, actions)
    )
    if not force and os.path.exists(cache):
        try:
            df = pd.read_parquet(cache)
            if not df.empty:
                return df
        except Exception as e:
            warnings.warn(f"Cache read failed for {cache}: {e}; re-downloading")

    if _offline_required():
        raise OfflineDataUnavailable(
            f"offline mode: the cached data for this request is missing and the "
            f"network is not allowed. Missing cache file: {cache}\n"
            f"  (n_tickers={len(tickers) if hasattr(tickers, '__len__') else 1}, "
            f"start={start}, end={end}, auto_adjust={auto_adjust}, actions={actions})\n"
            f"  The committed artifacts depend on this input; it must be pinned "
            f"into data/ and recorded in ledger/data_baseline.json."
        )

    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = list(tickers)

    raw = _download_with_retry(tickers, start, end, auto_adjust, actions=actions)

    # Normalize to a consistent MultiIndex (Ticker, Price)
    if isinstance(raw.columns, pd.MultiIndex):
        # yfinance may return (Ticker, Price) or (Price, Ticker); ensure outer = Ticker
        raw.columns.names = ["Level0", "Level1"]
        lvl0 = [str(c) for c in raw.columns.get_level_values(0).unique()]
        lvl1 = [str(c) for c in raw.columns.get_level_values(1).unique()]
        ticker_set = set(str(t) for t in tickers)
        # Outer level is Ticker iff the inner level is NOT entirely tickers
        # (i.e. when group_by="ticker" + actions, yfinance puts Price outer, Ticker inner)
        if set(lvl1).issubset(ticker_set) and not set(lvl0).issubset(ticker_set):
            raw = raw.swaplevel(0, 1, axis=1)
        raw.columns = pd.MultiIndex.from_tuples(
            [(str(c[0]), str(c[1])) for c in raw.columns]
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