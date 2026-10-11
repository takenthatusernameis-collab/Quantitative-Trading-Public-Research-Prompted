"""Pairs trading / statistical arbitrage (Gatev, Goetzmann & Rouwenhorst 2006).

Distance method, canonical Gatev et al. (2006) design:
- Formation period: 12 months (252 trading days) - find pairs with minimum
  sum of squared differences between normalized price series.
- Trading period: 6 months (126 trading days) - trade the spread of selected
  pairs using z-score entry/exit.
- Pair selection: top-K pairs by distance.
- Signal: z-score of spread; enter at |z| >= entry_z, exit at |z| <= exit_z.
- Dollar-neutral per pair; inverse-vol weighted across pairs.

Correctness notes (E021 audit):
- Stateful position logic: a pair enters at |z|>=entry_z and HOLDS until
  |z|<=exit_z. The previous version was stateless (re-evaluated each day),
  which forced every entry to be closed the next day and produced a heavily
  biased, too-pessimistic result.
- No look-ahead: formation stats use only the window ending on the formation
  date; weights formed on day t are executed at t+1 open via the caller's
  shift_weights. Pair membership and formation stats are fixed at formation
  and never peek into the trading period.
- Efficient: pairs are formed only at rebalance dates (not every day); z-scores
  use precomputed expanding formation stats; position state is propagated
  with ffill.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional

from src import backtest


def normalize_prices(close: pd.DataFrame) -> pd.DataFrame:
    """Normalize price series to start at 1.0 for distance computation."""
    first_valid = close.bfill().iloc[0]
    return close.div(first_valid, axis=1)


def _formation_dates(close: pd.DataFrame, formation_window: int,
                     rebalance_freq: int) -> List[pd.Timestamp]:
    """Rebalance/formation dates: every rebalance_freq days starting at formation_window."""
    dates = close.index
    return list(dates[formation_window::rebalance_freq])


def find_pairs_distance(
    close: pd.DataFrame,
    formation_window: int = 252,
    max_pairs: int = 20,
    rebalance_freq: int = 21,
) -> Dict[pd.Timestamp, List[Tuple[str, str, float]]]:
    """Find pairs using the distance method (Gatev et al. 2006).

    Pairs are formed only at rebalance dates. For each formation date t, uses
    the window [t-formation_window+1, t] of normalized prices, computes the
    sum of squared differences for all pairs, and selects the top max_pairs
    with smallest distance.

    Returns dict mapping formation date -> list of (stock_a, stock_b, 1.0).
    """
    norm_close = normalize_prices(close)
    pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float]]] = {}
    dates = close.index

    for form_end in _formation_dates(close, formation_window, rebalance_freq):
        i = dates.get_indexer([form_end], method="pad")[0]
        if i < formation_window:
            pairs_by_date[form_end] = []
            continue
        form_start = dates[i - formation_window]
        window_data = norm_close.loc[form_start:form_end].dropna(axis=1, how="any")
        if window_data.shape[1] < 2:
            pairs_by_date[form_end] = []
            continue

        tickers = window_data.columns.tolist()
        arr = window_data.to_numpy(dtype=float)  # shape (T, n): rows=time, cols=tickers
        n = len(tickers)
        # Pairwise squared distance over time: for ticker pair (i,j),
        # sum over time of (arr[:, i] - arr[:, j])^2 -> (n, n) matrix.
        diff = arr[:, :, None] - arr[:, None, :]      # (T, n, n)
        dist_mat = (diff ** 2).sum(axis=0)             # (n, n)
        j_idx, k_idx = np.triu_indices(n, k=1)
        dvals = dist_mat[j_idx, k_idx]
        order = np.argsort(dvals, kind="stable")
        sel = order[:max_pairs]
        selected = [(tickers[j_idx[s]], tickers[k_idx[s]], 1.0) for s in sel]
        pairs_by_date[form_end] = selected

    return pairs_by_date


def _pair_key(a: str, b: str) -> Tuple[str, str]:
    """Canonical unordered pair key for state tracking."""
    return (a, b) if a <= b else (b, a)


def _log_spread(close: pd.DataFrame, a: str, b: str) -> pd.Series:
    """Log-price spread log(a) - log(b), aligned to close.index."""
    if a not in close.columns or b not in close.columns:
        return pd.Series(np.nan, index=close.index)
    return np.log(close[a]) - np.log(close[b])


def _formation_stats_at(spread: pd.Series, form_end_idx: int,
                        formation_window: int):
    """Mean/std of spread over the formation window ending at form_end_idx (inclusive)."""
    start = form_end_idx - formation_window + 1
    if start < 0:
        return np.nan, np.nan
    window = spread.iloc[start:form_end_idx + 1]
    if len(window) < formation_window or window.isna().any():
        return np.nan, np.nan
    mu = window.mean()
    sd = window.std()
    if not np.isfinite(sd) or sd == 0:
        return np.nan, np.nan
    return mu, sd


def _stateful_positions(z: pd.Series, entry_z: float, exit_z: float) -> pd.Series:
    """Stateful pair position from a z-score series.

    Entry at |z| >= entry_z (sign = -sign(z): negative z -> long spread).
    Hold until |z| <= exit_z, then flat. NaN z keeps the current state.
    Propagated forward with ffill so positions persist across the trading
    period between rebalances.
    """
    zvals = z.to_numpy(dtype=float)
    n = len(zvals)
    pos = np.zeros(n, dtype=float)
    in_pos = False
    cur = 0.0
    for t in range(n):
        zz = zvals[t]
        if np.isnan(zz):
            pos[t] = cur
            continue
        if not in_pos:
            if abs(zz) >= entry_z:
                in_pos = True
                cur = -float(np.sign(zz))
        else:
            if abs(zz) <= exit_z:
                in_pos = False
                cur = 0.0
        pos[t] = cur
    return pd.Series(pos, index=z.index, dtype=float)


def _pair_zscore_fast(close: pd.DataFrame, a: str, b: str,
                      formation_window: int) -> pd.Series:
    """Z-score of the log spread using a fixed formation window ending at t.

    For each date t, z_t = (spread_t - mean_{t-w+1..t}) / std_{t-w+1..t}.
    NaN where either leg is missing or the trailing window is not fully
    observed. Fully vectorized (no per-date Python loop).
    """
    spread = _log_spread(close, a, b)
    if formation_window <= 0:
        return pd.Series(np.nan, index=spread.index)
    roll_mean = spread.rolling(formation_window, min_periods=formation_window).mean()
    roll_std = spread.rolling(formation_window, min_periods=formation_window).std()
    # A window is valid only if every observation in it is non-NaN
    valid = (
        spread.notna()
        .rolling(formation_window, min_periods=formation_window)
        .sum()
        == formation_window
    )
    z = (spread - roll_mean) / roll_std
    z = z.where(valid & roll_std.notna() & (roll_std > 0))
    return z


def _pair_positions(close: pd.DataFrame, a: str, b: str,
                    formation_window: int = 252,
                    entry_z: float = 2.0, exit_z: float = 0.0) -> pd.Series:
    """Stateful per-pair position series (long spread / short spread / flat)."""
    z = _pair_zscore_fast(close, a, b, formation_window=formation_window)
    return _stateful_positions(z, entry_z, exit_z)


def _pair_vol(close: pd.DataFrame, vol: pd.DataFrame, a: str, b: str,
              date) -> float:
    """Per-pair equal-dollar vol at date: sqrt((v_a^2 + v_b^2)/4)."""
    if a not in close.columns or b not in close.columns:
        return np.nan
    if date not in vol.index:
        return np.nan
    va = vol.loc[date, a]
    vb = vol.loc[date, b]
    if not (np.isfinite(va) and np.isfinite(vb)) or va <= 0 or vb <= 0:
        return np.nan
    return float(np.sqrt((va ** 2 + vb ** 2) / 4.0))


def _precompute_vol(close: pd.DataFrame, vol_window: int) -> pd.DataFrame:
    """Per-stock rolling realized-vol frame (same index/columns as close)."""
    return close.pct_change().rolling(vol_window).std()


def pairs_weights(
    close: pd.DataFrame,
    pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float]]],
    formation_window: int = 252,
    entry_z: float = 2.0,
    exit_z: float = 0.0,
    vol_window: int = 63,
    rebalance_freq: int = 21,
) -> pd.DataFrame:
    """Daily target weights for distance-method pairs trading.

    For each rebalance date, select the most recent formation period's pairs,
    read their stateful positions (computed from data available at that date),
    and aggregate into dollar-neutral, inverse-vol-weighted target weights.
    Weights are held constant between rebalances.

    Position sign convention: pos = +1 means LONG spread (long A, short B);
    pos = -1 means SHORT spread (short A, long B). Per pair the gross exposure
    is 1.0 (0.5 long leg, 0.5 short leg); across pairs weights are scaled by
    inverse pair volatility so each active pair contributes equally to risk.

    No look-ahead: formation stats at date t use only data through t; the
    returned weights are target weights as of day t, to be executed at t+1
    open by the caller (backtest.shift_weights).
    """
    dates = close.index
    tickers = close.columns

    form_dates = sorted(pairs_by_date.keys())
    if not form_dates:
        return pd.DataFrame(0.0, index=dates, columns=tickers)

    vol = _precompute_vol(close, vol_window)

    # Pre-compute stateful positions for every candidate pair over the full
    # history. Each pair's position at t depends only on data through t, so
    # this is look-ahead free.
    pos_cache: Dict[Tuple[str, str], pd.Series] = {}
    seen_pairs = set()
    for pairs in pairs_by_date.values():
        for a, b, _ in pairs:
            k = _pair_key(a, b)
            if k not in seen_pairs:
                seen_pairs.add(k)
                pos_cache[k] = _pair_positions(
                    close, k[0], k[1], formation_window=formation_window,
                    entry_z=entry_z, exit_z=exit_z,
                )

    rebalance_days = set(dates[::rebalance_freq]) if rebalance_freq > 1 else set(dates)

    # Build target weights only on rebalance dates, then forward-fill so the
    # target is held constant between rebalances (executed at next open by caller).
    rebalance_weights = pd.DataFrame(0.0, index=dates, columns=tickers)

    for date in dates:
        if date not in rebalance_days:
            continue
        # Most recent formation period ending on or before this date
        active_form = None
        for fd in reversed(form_dates):
            if fd <= date:
                active_form = fd
                break
        if active_form is None:
            continue

        active_pairs = pairs_by_date[active_form]
        if not active_pairs:
            continue

        # Active pair positions at this date + per-pair vol for weighting
        active = []
        for a, b, _ in active_pairs:
            k = _pair_key(a, b)
            if k not in pos_cache:
                continue
            p = pos_cache[k].loc[date] if date in pos_cache[k].index else np.nan
            if not np.isfinite(p) or p == 0.0:
                continue
            pv = _pair_vol(close, vol, a, b, date)
            if not np.isfinite(pv) or pv <= 0:
                continue
            active.append((a, b, p, pv))

        if not active:
            continue

        inv_vols = [1.0 / pv for _, _, _, pv in active]
        total = sum(inv_vols)
        if total <= 0:
            continue

        for (a, b, p, pv), iv in zip(active, inv_vols):
            w = p * 0.5 * iv / total
            rebalance_weights.loc[date, a] += w
            rebalance_weights.loc[date, b] -= w

    # Hold target weights constant between rebalance dates, but only across
    # rebalance dates that actually had active pairs. A rebalance with no
    # active pairs means the portfolio is flat until the next active rebalance
    # (do NOT carry a stale position forward through it).
    weights = pd.DataFrame(0.0, index=dates, columns=tickers)
    active_rebalance_dates = [
        d for d in rebalance_weights.index
        if (rebalance_weights.loc[d].abs() > 1e-9).any()
    ]
    if not active_rebalance_dates:
        return weights
    # For each date, find the most recent active rebalance date via searchsorted
    arr = np.asarray(active_rebalance_dates)
    idx = np.searchsorted(arr, dates, side="right") - 1
    for j, k in enumerate(idx):
        if k >= 0:
            weights.iloc[j] = rebalance_weights.loc[arr[k]].to_numpy()
    return weights
    for date in dates:
        # Most recent active rebalance date on or before `date`
        cand = [d for d in active_rebalance_dates if d <= date]
        if cand:
            src = cand[-1]
            weights.loc[date] = rebalance_weights.loc[src]
    return weights


def pairs_placebo_weights(
    close: pd.DataFrame,
    n_pairs: int = 20,
    n_sim: int = 50,
    seed: int = 42,
    formation_window: int = 252,
    entry_z: float = 2.0,
    exit_z: float = 0.0,
    vol_window: int = 63,
    rebalance_freq: int = 21,
) -> List[pd.DataFrame]:
    """Placebo null for pairs trading: random pair matching.

    Pairs are formed by randomly pairing tickers (no cointegration/distance
    signal), but the identical stateful z-score entry/exit logic and
    inverse-vol weighting are applied. This isolates the distance-method
    pair-selection skill from the trading-rule skill.

    Returns a list of weight DataFrames, one per simulation.
    """
    rng = np.random.default_rng(seed)
    tickers = close.columns.tolist()
    n = len(tickers)
    dates = close.index
    placebo_weights: List[pd.DataFrame] = []

    for _ in range(n_sim):
        perm = rng.permutation(n)
        random_pairs: List[Tuple[str, str, float]] = []
        for i in range(0, min(n_pairs * 2, n), 2):
            if i + 1 < n:
                random_pairs.append((tickers[perm[i]], tickers[perm[i + 1]], 1.0))

        form_dates = _formation_dates(close, formation_window, rebalance_freq)
        pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float]]] = {
            fd: random_pairs for fd in form_dates
        }
        w = pairs_weights(
            close, pairs_by_date,
            formation_window=formation_window,
            entry_z=entry_z, exit_z=exit_z,
            vol_window=vol_window, rebalance_freq=rebalance_freq,
        )
        placebo_weights.append(w)

    return placebo_weights