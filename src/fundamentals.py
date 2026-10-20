"""Fundamental accounting factors: profitability (Novy-Marx 2013) and investment (Titman, Wei & Xing 2008).

Both factors are computed from yfinance quarterly financial statements and balance
sheets.  The repo's only public fundamental data source is yfinance, whose history
depth is limited (see experiments/e029_fundamental_feasibility.json): quarterly income
statements start ~2025-01-31 and balance sheets start ~2021-10-31.  A full 2014-2026
walk-forward with a 504-day formation window is therefore NOT possible with this data
source.  This module therefore supports an in-sample / short out-of-sample mechanism
test over the available window only; the driver enforces that no OOS Sharpe gate is
evaluated on data the source cannot provide.

Signal construction (no look-ahead):
- Gross profitability (Novy-Marx 2013): GP = (Total Revenue - Cost Of Revenue)
  / Total Assets, summed over the trailing 4 quarters (TTM).  High GP -> high signal.
- Asset growth (Titman et al. 2008): (Total Assets_t - Total Assets_{t-4Q})
  / Total Assets_{t-4Q}.  Low growth -> high signal (low investment predicts higher
  future returns).

Both signals are cross-sectionally winsorized 1/99 and z-score standardized per day.
"""

import hashlib
import json
import os
import time
import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from src.offline import OfflineDataUnavailable, offline_required

# yfinance field names (verified against the live feed in the feasibility probe)
REV_FIELD = "Total Revenue"
COGS_FIELD = "Cost Of Revenue"
GP_FIELD = "Gross Profit"
TA_FIELD = "Total Assets"

# Where the fundamentals cache lives, next to the price cache.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_ROOT, "data")
FUND_DIR = os.path.join(DATA_DIR, "fundamentals")
FUND_VINTAGES_PATH = os.path.join(DATA_DIR, "fundamentals_vintages.json")
os.makedirs(FUND_DIR, exist_ok=True)


def _fingerprint(df: pd.DataFrame) -> str:
    """Stable hash of a panel's values + index + columns (order-independent)."""
    h = hashlib.sha256()
    h.update(repr(sorted(df.index.astype(str))).encode())
    h.update(repr(sorted(df.columns.astype(str))).encode())
    h.update(pd.util.hash_pandas_object(df.fillna("NaN"), index=True)
             .values.tobytes())
    return h.hexdigest()[:16]


def _load_fund_vintages() -> dict:
    if os.path.exists(FUND_VINTAGES_PATH):
        try:
            with open(FUND_VINTAGES_PATH) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _resolve_fund_vintage() -> Optional[str]:
    """Pinned fundamentals vintage when SEED is set (offline reproduction)."""
    if os.environ.get("SEED"):
        return _load_fund_vintages().get("default_vintage")
    return None


def _fund_cache_path(tickers: List[str], vintage: Optional[str]) -> str:
    key = "|".join(sorted(set(tickers)))
    h = hashlib.sha256(key.encode()).hexdigest()[:16]
    tag = vintage or "live"
    return os.path.join(FUND_DIR, f"fundamentals_{h}_{tag}.parquet")


def _write_fund_cache(path: str, name: str, df: pd.DataFrame) -> None:
    df = df.copy()
    df.index.name = "period_end"
    df.columns.name = "ticker"
    df.to_parquet(path)
    with open(path + ".meta.json", "w") as f:
        json.dump({"panel": name, "fingerprint": _fingerprint(df),
                   "shape": list(df.shape)}, f, indent=2)


def _read_fund_cache(path: str) -> Optional[pd.DataFrame]:
    try:
        df = pd.read_parquet(path)
        if df.empty:
            return None
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        warnings.warn(f"fundamentals cache read failed for {path}: {e}")
        return None


def fetch_fundamentals(tickers: List[str],
                       force: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Download quarterly income statements and balance sheets for ``tickers``.

    Returns (revenue, cogs, total_assets) DataFrames, each indexed by period-end date
    with tickers as columns.  Missing fields are NaN.  Fields are kept in separate
    panels so callers can combine them without a name collision (the COGS field
    overwrote the revenue field in an earlier version of this module).

    Offline reproduction: when ``SEED`` is set, the driver reads the pinned
    fundamentals vintage (``data/fundamentals_vintages.json``) instead of the live
    yfinance feed.  The panels are cached as parquet under ``data/fundamentals/`` so
    the committed vintage can be regenerated and re-pinned deliberately.
    """
    import yfinance as yf

    vintage = None if force else _resolve_fund_vintage()
    cache = _fund_cache_path(tickers, vintage)

    def _from_cache():
        rev = _read_fund_cache(cache + ".rev.parquet")
        cogs = _read_fund_cache(cache + ".cogs.parquet")
        ta = _read_fund_cache(cache + ".ta.parquet")
        if rev is not None and cogs is not None and ta is not None:
            return rev, cogs, ta
        return None

    if vintage and not force:
        hit = _from_cache()
        if hit is not None:
            print(f"    [fundamentals] using pinned vintage {vintage} (offline)")
            return hit

    if offline_required():
        raise OfflineDataUnavailable(
            f"offline mode: the pinned fundamentals vintage is missing and the "
            f"network is not allowed. Missing cache file: {cache}\n"
            f"  The committed artifacts depend on this input; the snapshot must "
            f"be pinned into data/fundamentals/ and recorded in "
            f"ledger/data_baseline.json."
        )

    rev_d, cogs_d, ta_d = {}, {}, {}
    for t in tickers:
        try:
            tk = yf.Ticker(t)
            qf = tk.quarterly_financials
            bs = tk.balancesheet
        except Exception:
            continue
        if REV_FIELD in qf.index:
            rev_d[t] = qf.loc[REV_FIELD]
        if COGS_FIELD in qf.index:
            cogs_d[t] = qf.loc[COGS_FIELD]
        if TA_FIELD in bs.index:
            ta_d[t] = bs.loc[TA_FIELD]
        time.sleep(0.05)  # rate-limit courtesy
    rev = pd.DataFrame(rev_d)
    cogs = pd.DataFrame(cogs_d)
    ta = pd.DataFrame(ta_d)
    rev = rev.dropna(how="all")
    cogs = cogs.dropna(how="all")
    ta = ta.dropna(how="all")

    if vintage:
        _write_fund_cache(cache + ".rev.parquet", "revenue", rev)
        _write_fund_cache(cache + ".cogs.parquet", "cogs", cogs)
        _write_fund_cache(cache + ".ta.parquet", "total_assets", ta)
        print(f"    [fundamentals] cached pinned vintage {vintage}")
    return rev, cogs, ta


def gross_profit(rev: pd.DataFrame, cogs: pd.DataFrame) -> pd.DataFrame:
    """Gross profit per quarter = Total Revenue - Cost Of Revenue.

    Only names present in BOTH panels get a value; names missing Cost Of Revenue
    are left NaN (they are excluded from the gross-profitability signal rather than
    being given a biased fallback).
    """
    return rev - cogs


def _ttm_quarters(df: pd.DataFrame, n_q: int = 4) -> pd.DataFrame:
    """Trailing sum of the last ``n_q`` reported values per name.

    Operates on the RAW (irregular) report grid: for each name, sums the last n_q
    non-NaN values as of each report date.  This avoids the all-NaN grid rows that
    appear when panels with different fiscal calendars are unioned (those rows
    break a plain rolling() sum).  Output is indexed by the union of report dates.
    """
    out = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)
    for col in df.columns:
        s = df[col].dropna()
        if len(s) >= n_q:
            out[col] = s.rolling(n_q, min_periods=n_q).sum()
    return out


def _winsorize_zscore(df: pd.DataFrame, lo: float = 0.01, hi: float = 0.99) -> pd.DataFrame:
    """Cross-sectional winsorize at lo/hi then z-score standardize per day."""
    arr = df.to_numpy(dtype=float)
    with np.errstate(invalid="ignore"):
        lo_v = np.nanquantile(arr, lo, axis=1, keepdims=True)
        hi_v = np.nanquantile(arr, hi, axis=1, keepdims=True)
    win = np.clip(arr, lo_v, hi_v)
    with np.errstate(invalid="ignore"):
        mu = np.nanmean(win, axis=1, keepdims=True)
        sd = np.nanstd(win, axis=1, keepdims=True, ddof=1)
    z = (win - mu) / (sd + 1e-12)
    return pd.DataFrame(z, index=df.index, columns=df.columns)


def _ttm_per_name(df: pd.DataFrame, n_q: int) -> pd.DataFrame:
    """Trailing sum of the last ``n_q`` reported quarters, per name.

    Operates on each name's RAW report grid (the irregular dates yfinance
    returns): for each name, sums the last n_q non-NaN values as of each report
    date.  Forward-filling the panel first would make a rolling sum count the
    same stale value four times, which is wrong for TTM.

    Returns a DataFrame indexed by the union of report dates.
    """
    out = pd.DataFrame(index=df.index, columns=df.columns, dtype=float)
    for col in df.columns:
        s = df[col].dropna()
        if len(s) >= n_q:
            out[col] = s.rolling(n_q, min_periods=n_q).sum()
    return out


def _align_to_calendar(report_df: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    """Forward-fill a per-name report panel onto the daily trading calendar.

    Strictly no look-ahead: at trading date t the value used is the most recent
    report with report date <= t.
    """
    out = pd.DataFrame(index=close.index, columns=report_df.columns, dtype=float)
    for col in report_df.columns:
        s = report_df[col].dropna()
        if len(s):
            out[col] = s.reindex(close.index, method="ffill")
    return out


def _quarter_grid(start: pd.Timestamp, end: pd.Timestamp) -> pd.DatetimeIndex:
    """Uniform quarterly grid of quarter-END dates spanning [start, end].

    Each grid step is the last day of a calendar quarter (months 3/6/9/12).  This is
    the grid onto which each name's last reported value is forward-filled before
    the TTM sums are taken; using quarter-ends (rather than the raw, irregular
    report dates) keeps the two panels (income statement and balance sheet, which
    have different fiscal calendars) aligned on the same dates so the profitability
    ratio is well-defined.
    """
    months = []
    d = pd.Timestamp(year=start.year, month=1, day=1)
    while d <= end:
        m = d.month
        if m in (3, 6, 9, 12):
            # use the LAST day of the quarter so the grid step coincides with the
            # quarter-end report dates yfinance returns (e.g. 2025-03-31, not 2025-03-01)
            months.append(pd.Timestamp(year=d.year, month=m, day=1) + pd.offsets.MonthEnd(0))
        d = d + pd.DateOffset(months=1)
    if not months:
        return pd.DatetimeIndex([start])
    return pd.DatetimeIndex(months)


def gross_profit_signal(rev: pd.DataFrame, cogs: pd.DataFrame, ta: pd.DataFrame,
                        close: pd.DataFrame, n_q: int = 4) -> pd.DataFrame:
    """Cross-sectional gross-profitability signal (Novy-Marx 2013).

    GP_t = sum of trailing n_q quarters of (Revenue - Cost Of Revenue) / Total Assets.
    High GP -> high signal.  Winsorized 1/99 and z-score standardized per day.

    The income-statement and balance-sheet panels have different fiscal calendars,
    so they are each forward-filled onto a single uniform quarterly grid (covering
    the earliest report date across all panels) before the TTM sums are taken; this
    keeps the two TTM panels aligned on the same dates so the profitability ratio
    is well-defined (a plain per-column rolling sum on the raw union grid leaves
    the two panels misaligned and the ratio empty).
    """
    grid = _quarter_grid(min(rev.index.min(), ta.index.min()),
                         max(rev.index.max(), ta.index.max()))
    # Forward-fill each panel onto the COMMON grid first (strictly no-look-ahead:
    # at grid date t each name uses its most recent report with report date <= t),
    # then take the TTM sum on that grid.  The two panels therefore share the same
    # dates and the profitability ratio is well-defined; without this common grid
    # the two TTM panels are misaligned and the ratio is empty.
    gp = gross_profit(rev, cogs).reindex(grid, method="ffill")
    bal = ta.reindex(grid, method="ffill")
    gp_ttm = _ttm_per_name(gp, n_q)
    ta_ttm = _ttm_per_name(bal, n_q)
    gp_ratio = gp_ttm / ta_ttm.replace(0, np.nan)
    sig = _align_to_calendar(gp_ratio, close)
    sig = sig.iloc[n_q - 1:]
    return _winsorize_zscore(sig)


def asset_growth_signal(ta: pd.DataFrame, close: pd.DataFrame,
                         n_q: int = 4) -> pd.DataFrame:
    """Cross-sectional asset-growth signal (Titman, Wei & Xing 2008).

    g_t = (Total Assets_t - Total Assets_{t-4Q}) / Total Assets_{t-4Q}.
    Low growth -> high signal, so the signal is the NEGATIVE of asset growth.

    Computed on the same uniform quarterly grid as the profitability signal so the
    two are directly comparable; a position shift of ``n_q`` grid steps is exactly
    one fiscal year on this grid.
    """
    grid = _quarter_grid(ta.index.min(), ta.index.max())
    ff = ta.reindex(grid, method="ffill")
    lag = ff.shift(n_q)
    growth = (ff - lag) / lag.replace(0, np.nan)
    sig = _align_to_calendar(-growth, close)
    sig = sig.iloc[n_q - 1:]
    return _winsorize_zscore(sig)


def row_spearman(a: pd.DataFrame, b: pd.DataFrame):
    """Per-row (cross-sectional) Spearman correlation of a vs b."""
    ar = a.rank(axis=1, method="average")
    br = b.rank(axis=1, method="average")
    rho = np.full(a.shape[0], np.nan)
    av = ar.to_numpy()
    bv = br.to_numpy()
    for i in range(a.shape[0]):
        m = ~(np.isnan(av[i]) | np.isnan(bv[i]))
        if m.sum() >= 3:
            x = av[i][m] - av[i][m].mean()
            y = bv[i][m] - bv[i][m].mean()
            den = np.sqrt((x * x).sum() * (y * y).sum())
            rho[i] = float((x * y).sum() / den) if den > 0 else np.nan
    return rho
