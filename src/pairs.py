"""Pairs trading / statistical arbitrage (Gatev, Goetzmann & Rouwenhorst 2006).

Distance method:
- Formation period: 12 months (252 trading days) - find pairs with minimum
  sum of squared differences between normalized price series.
- Trading period: 6 months (126 trading days) - trade the spread of selected
  pairs using z-score entry/exit.
- Pair selection: top-K pairs by distance (standardized price distance).
- Signal: z-score of spread; enter at |z| >= entry_z, exit at |z| <= exit_z.
- Dollar-neutral per pair; inverse-vol weighted across pairs.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional

from src import backtest


def normalize_prices(close: pd.DataFrame) -> pd.DataFrame:
    """Normalize price series to start at 1.0 for distance computation."""
    first_valid = close.bfill().iloc[0]
    return close.div(first_valid, axis=1)


def find_pairs_distance(
    close: pd.DataFrame,
    formation_window: int = 252,
    max_pairs: int = 20,
) -> List[Tuple[str, str, float]]:
    """Find cointegrated pairs using the distance method (Gatev et al. 2006).

    For each formation window ending at date t, compute the sum of squared
    differences between normalized price series for all stock pairs.
    Select the top max_pairs pairs with smallest distance.

    Returns list of (stock_a, stock_b, hedge_ratio) where hedge_ratio = 1.0
    (equal dollar weights in the original paper; beta-neutral variant can
    use OLS hedge ratio).
    """
    norm_close = normalize_prices(close)
    pairs_by_date = {}

    dates = close.index
    for i in range(formation_window, len(dates)):
        form_end = dates[i]
        form_start = dates[i - formation_window]
        window_data = norm_close.loc[form_start:form_end]

        # Drop columns with any NaN in formation window
        window_data = window_data.dropna(axis=1, how="any")
        if window_data.shape[1] < 2:
            pairs_by_date[form_end] = []
            continue

        tickers = window_data.columns.tolist()
        n = len(tickers)
        distances = []

        for j in range(n):
            for k in range(j + 1, n):
                s1 = window_data[tickers[j]].values
                s2 = window_data[tickers[k]].values
                # Sum of squared differences (distance)
                dist = np.sum((s1 - s2) ** 2)
                distances.append((dist, tickers[j], tickers[k]))

        distances.sort(key=lambda x: x[0])
        selected = distances[:max_pairs]
        # hedge_ratio = 1.0 for equal dollar weights (distance method)
        pairs_by_date[form_end] = [(a, b, 1.0) for _, a, b in selected]

    return pairs_by_date


def compute_spread_zscore(
    close: pd.DataFrame,
    pair: Tuple[str, str, float],
    formation_window: int = 252,
    trading_window: int = 126,
) -> pd.Series:
    """Compute z-score of the spread for a single pair over the trading period.

    Spread = log(price_a) - hedge_ratio * log(price_b)  (log-price spread)
    z-score = (spread - mean(spread_formation)) / std(spread_formation)
    """
    stock_a, stock_b, hedge_ratio = pair

    if stock_a not in close.columns or stock_b not in close.columns:
        return pd.Series(dtype=float)

    # Log prices for spread
    log_a = np.log(close[stock_a])
    log_b = np.log(close[stock_b])

    spread = log_a - hedge_ratio * log_b
    spread = spread.dropna()

    if len(spread) < formation_window + trading_window:
        return pd.Series(dtype=float)

    # Rolling z-score using formation window stats
    zscore = pd.Series(index=spread.index, dtype=float)

    for i in range(formation_window, len(spread) - trading_window + 1):
        form_spread = spread.iloc[i - formation_window:i]
        trade_spread = spread.iloc[i:i + trading_window]

        mean_f = form_spread.mean()
        std_f = form_spread.std()
        if std_f == 0 or np.isnan(std_f):
            continue

        z = (trade_spread - mean_f) / std_f
        zscore.loc[trade_spread.index] = z

    return zscore.dropna()


def pairs_weights(
    close: pd.DataFrame,
    pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float]]],
    entry_z: float = 2.0,
    exit_z: float = 0.0,
    vol_window: int = 63,
    max_pairs: int = 20,
) -> pd.DataFrame:
    """Compute daily portfolio weights for pairs trading.

    For each date, find the active formation period's pairs, compute spread
    z-scores, and generate position signals. Dollar-neutral per pair,
    inverse-vol weighted across active pairs.

    Args:
        close: Price DataFrame (index=date, columns=tickers)
        pairs_by_date: Dict mapping formation end date -> list of (a, b, hedge_ratio)
        entry_z: Z-score threshold to enter position
        exit_z: Z-score threshold to exit position (0 = mean reversion target)
        vol_window: Window for inverse volatility weighting
        max_pairs: Maximum number of pairs to trade

    Returns:
        DataFrame of target weights (index=date, columns=tickers)
    """
    dates = close.index
    tickers = close.columns
    weights = pd.DataFrame(0.0, index=dates, columns=tickers)

    # Pre-compute all pair z-scores
    pair_zscores = {}
    for form_end, pairs in pairs_by_date.items():
        for pair in pairs:
            z = compute_spread_zscore(close, pair)
            if not z.empty:
                pair_zscores[(form_end, pair[0], pair[1])] = z

    # For each date, find the most recent formation period
    form_dates = sorted(pairs_by_date.keys())

    for i, date in enumerate(dates):
        # Find formation period that ended on or before this date
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

        # Get z-scores for active pairs on this date
        pair_signals = {}
        for pair in active_pairs:
            key = (active_form, pair[0], pair[1])
            if key in pair_zscores:
                z_series = pair_zscores[key]
                if date in z_series.index:
                    z = z_series[date]
                    if not np.isnan(z):
                        # Generate signal: -1 if z > entry_z (short spread: short A, long B),
                        # +1 if z < -entry_z (long spread: long A, short B), 0 if |z| < exit_z
                        # This is a stateful signal - need to track position
                        pair_signals[pair] = z

        if not pair_signals:
            continue

        # Simple stateless approach: signal = -sign(z) * (|z| >= entry_z)
        # Exit when |z| < exit_z (handled by signal going to 0)
        raw_signals = {}
        for pair, z in pair_signals.items():
            if abs(z) >= entry_z:
                raw_signals[pair] = -np.sign(z)  # negative z -> long spread (long A, short B)
            elif abs(z) <= exit_z:
                raw_signals[pair] = 0.0
            # else: maintain previous position (not tracked here; stateless)

        if not raw_signals:
            continue

        # Convert to dollar-neutral weights per pair
        # For each pair with signal s: weight_a = s * 0.5, weight_b = -s * 0.5
        # Then inverse-vol weight across pairs
        pair_weights = {}
        for pair, sig in raw_signals.items():
            if sig == 0:
                continue
            a, b, hr = pair
            if a not in close.columns or b not in close.columns:
                continue
            # Dollar-neutral: 50% long, 50% short per pair
            pair_weights[pair] = sig * 0.5

        if not pair_weights:
            continue

        # Inverse volatility weighting across pairs
        rets = close.pct_change()
        vol = rets.rolling(vol_window).std().replace(0, np.nan)

        # Compute pair-level volatility (portfolio of two legs)
        pair_vols = {}
        for pair in pair_weights:
            a, b, hr = pair
            if a in vol.columns and b in vol.columns:
                v_a = vol.loc[date, a] if date in vol.index else np.nan
                v_b = vol.loc[date, b] if date in vol.index else np.nan
                if not np.isnan(v_a) and not np.isnan(v_b) and v_a > 0 and v_b > 0:
                    # Pair volatility (equal dollar weight)
                    pair_vol = np.sqrt((v_a**2 + v_b**2) / 4)
                    pair_vols[pair] = pair_vol

        if not pair_vols:
            continue

        # Inverse vol weights
        inv_vol = {p: 1.0 / v for p, v in pair_vols.items()}
        total_inv = sum(inv_vol.values())
        if total_inv == 0:
            continue

        for pair, sig_weight in pair_weights.items():
            if pair in inv_vol:
                w = sig_weight * inv_vol[pair] / total_inv
                a, b, hr = pair
                weights.loc[date, a] = weights.loc[date, a] + w
                weights.loc[date, b] = weights.loc[date, b] - w

    return weights


def pairs_weights_vectorized(
    close: pd.DataFrame,
    pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float]]],
    entry_z: float = 2.0,
    exit_z: float = 0.0,
    vol_window: int = 63,
    formation_window: int = 252,
    trading_window: int = 126,
) -> pd.DataFrame:
    """Vectorized version of pairs_weights for efficiency.

    Computes all pair z-scores upfront using rolling windows, then generates
    signals and weights efficiently.
    """
    dates = close.index
    tickers = close.columns
    weights = pd.DataFrame(0.0, index=dates, columns=tickers)

    # Pre-compute z-scores for all pairs at all dates
    # This is more efficient than per-date computation
    all_pair_zscores = {}

    for form_end, pairs in pairs_by_date.items():
        for pair in pairs:
            z = compute_spread_zscore(close, pair, formation_window, trading_window)
            if not z.empty:
                all_pair_zscores[(form_end, pair[0], pair[1])] = z

    if not all_pair_zscores:
        return weights

    # For each date, determine active formation period and compute weights
    form_dates = sorted(pairs_by_date.keys())
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)

    for i, date in enumerate(dates):
        if i < formation_window:
            continue

        # Find active formation period
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

        # Get z-scores for active pairs on this date
        active_signals = {}
        for pair in active_pairs:
            key = (active_form, pair[0], pair[1])
            if key in all_pair_zscores:
                z_series = all_pair_zscores[key]
                if date in z_series.index:
                    z = z_series[date]
                    if not np.isnan(z):
                        if abs(z) >= entry_z:
                            active_signals[pair] = -np.sign(z)
                        elif abs(z) <= exit_z:
                            active_signals[pair] = 0.0

        if not active_signals:
            continue

        # Compute inverse-vol weights across active pairs
        pair_inv_vols = {}
        for pair, sig in active_signals.items():
            if sig == 0:
                continue
            a, b, hr = pair
            if a in vol.columns and b in vol.columns and date in vol.index:
                v_a = vol.loc[date, a]
                v_b = vol.loc[date, b]
                if not np.isnan(v_a) and not np.isnan(v_b) and v_a > 0 and v_b > 0:
                    pair_vol = np.sqrt((v_a**2 + v_b**2) / 4)
                    if pair_vol > 0:
                        pair_inv_vols[pair] = 1.0 / pair_vol

        if not pair_inv_vols:
            continue

        total_inv = sum(pair_inv_vols.values())
        if total_inv == 0:
            continue

        for pair, sig in active_signals.items():
            if sig == 0 or pair not in pair_inv_vols:
                continue
            w = sig * 0.5 * pair_inv_vols[pair] / total_inv
            a, b, hr = pair
            weights.loc[date, a] += w
            weights.loc[date, b] -= w

    return weights


def pairs_placebo_weights(
    close: pd.DataFrame,
    n_pairs: int = 20,
    n_sim: int = 50,
    seed: int = 42,
) -> List[pd.DataFrame]:
    """Generate placebo weights for pairs trading by random pair matching.

    Returns list of weight DataFrames for each simulation.
    """
    rng = np.random.default_rng(seed)
    tickers = close.columns.tolist()
    n = len(tickers)
    dates = close.index
    placebo_weights = []

    for sim in range(n_sim):
        # Randomly pair tickers
        perm = rng.permutation(n)
        random_pairs = []
        for i in range(0, min(n_pairs * 2, n), 2):
            if i + 1 < n:
                a = tickers[perm[i]]
                b = tickers[perm[i + 1]]
                random_pairs.append((a, b, 1.0))

        # Create fake pairs_by_date (use all dates with same pairs)
        # This is a simplified null - pairs are random but formation/trading
        # logic is preserved
        pairs_by_date = {}
        form_dates = dates[252::126]  # monthly formation updates
        for fd in form_dates:
            pairs_by_date[fd] = random_pairs[:n_pairs]

        w = pairs_weights_vectorized(
            close, pairs_by_date, entry_z=2.0, exit_z=0.0,
            vol_window=63, formation_window=252, trading_window=126
        )
        placebo_weights.append(w)

    return placebo_weights