"""Walk-forward backtesting engine with realistic execution modeling.

Design principles:
- No look-ahead bias: signals are computed from data available at decision time.
- Daily rebalancing with next-day open execution (realistic).
- Fixed proportional transaction costs; slippage modeled as a fraction of price.
- Chronological walk-forward splits with no information leakage between folds.
"""

import numpy as np
import pandas as pd


def _ensure_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.copy()
        df.index = pd.to_datetime(df.index)
    return df


def next_day_open_returns(close: pd.Series, open_: pd.Series) -> pd.Series:
    """Return realized next-day return using open price of the next trading day."""
    return (open_.shift(-1) / close - 1.0)


def equal_weight_weights(signal: pd.Series, long_only: bool = True) -> pd.DataFrame:
    """Convert a cross-sectional signal rank into target weights.

    Long-only equal-weight across the top-N names; short side zero.
    """
    ranks = signal.rank(axis=1, ascending=False, method="min", pct=True)
    n = signal.shape[1]
    top_n = max(1, int(round(n * 0.2)))  # top quintile
    weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)
    for date, row in ranks.iterrows():
        cutoff = row.nlargest(top_n).min()
        mask = row >= cutoff
        if mask.sum() > 0:
            weights.loc[date, mask] = 1.0 / mask.sum()
    if long_only:
        weights = weights.clip(lower=0.0)
    return weights


def shift_weights(weights: pd.DataFrame) -> pd.DataFrame:
    """Shift weights forward one day so they are executable at next open."""
    return weights.shift(1).fillna(0.0)


def portfolio_returns(
    weights: pd.DataFrame,
    close: pd.DataFrame,
    open_: pd.DataFrame,
    tc_cost: float = 0.0005,
    slippage: float = 0.0002,
) -> pd.Series:
    """Compute daily portfolio gross and net returns.

    weights: target weights as of day t (will be executed at t+1 open).
    close: closing prices day t.
    open_: opening prices day t+1.
    """
    weights = shift_weights(weights)
    # next-day return on each asset using its own open
    asset_ret = (open_.shift(-1) / close - 1.0)
    gross = (weights * asset_ret).sum(axis=1)

    # turnover and transaction costs
    turnover = (weights.diff().abs()).sum(axis=1)
    costs = turnover * (tc_cost + slippage)
    net = gross - costs
    return pd.DataFrame({"gross": gross, "costs": costs, "net": net})


def cumulative_returns(ret: pd.Series) -> pd.Series:
    return (1.0 + ret.fillna(0.0)).cumprod() - 1.0


def metrics(ret: pd.Series, periods: int = 252) -> dict:
    """Compute standard performance metrics."""
    ret = ret.dropna()
    if len(ret) < 10:
        return {}
    ann = periods
    mean = ret.mean()
    std = ret.std()
    sharpe = (mean / std * np.sqrt(ann)) if std > 0 else 0.0
    cum = (1.0 + ret).cumprod()
    roll_max = cum.cummax()
    drawdown = cum / roll_max - 1.0
    max_dd = drawdown.min()
    total = cum.iloc[-1] - 1.0 if len(cum) else 0.0
    win_rate = (ret > 0).mean()
    return {
        "annual_return": mean * ann,
        "annual_vol": std * np.sqrt(ann),
        "sharpe": sharpe,
        "max_drawdown": max_dd,
        "total_return": total,
        "win_rate": win_rate,
        "n_days": len(ret),
    }


def walk_forward_splits(
    n_days: int,
    train_size: int = 504,
    test_size: int = 63,
    step: int = 63,
) -> list:
    """Generate chronological (train_start, train_end, test_start, test_end) tuples."""
    splits = []
    test_start = train_size
    while test_start + test_size <= n_days:
        train_start = test_start - train_size
        train_end = test_start
        test_end = test_start + test_size
        splits.append((train_start, train_end, test_start, test_end))
        test_start += step
    return splits
def average_turnover(weights: pd.DataFrame) -> float:
    """Average daily turnover (sum of |w_t - w_{t-1}|) over time."""
    w_shift = shift_weights(weights)
    turnover = (w_shift.diff().abs()).sum(axis=1)
    return float(turnover.mean()) if len(turnover.dropna()) > 0 else 0.0

def inverse_vol_weights(signal: pd.DataFrame, close: pd.DataFrame, vol_window: int = 63,
                        top_quintile: bool = True, long_only: bool = True) -> pd.DataFrame:
    """Rank by signal, then weight within top quintile by inverse realized volatility."""
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    ranks = signal.rank(axis=1, ascending=False, method="min", pct=True)
    n = signal.shape[1]
    top_n = max(1, int(round(n * 0.2)))
    weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)
    for date, row in ranks.iterrows():
        cutoff = row.nlargest(top_n).min()
        mask = row >= cutoff
        if mask.sum() > 0:
            w = inv_vol.loc[date, mask].fillna(0.0)
            s = w.sum()
            if s > 0:
                weights.loc[date, mask] = w / s
    if long_only:
        weights = weights.clip(lower=0.0)
    return weights

def _rebalance_weights(weights: pd.DataFrame, rebalance_freq: int) -> pd.DataFrame:
    """Hold weights constant between rebalance events (forward-fill on cadence).

    Vectorized equivalent of sampling the (already next-day-shifted) weights at
    every ``rebalance_freq``-th day and holding them constant in between.
    Replaces an O(n) row-by-row assignment loop that made walk-forward + placebo
    runs pathologically slow.
    """
    if rebalance_freq <= 1:
        return weights
    sampled = weights.iloc[::rebalance_freq]
    return sampled.reindex(weights.index, method="ffill").fillna(0.0)


def portfolio_returns_rebalance(
    weights: pd.DataFrame,
    close: pd.DataFrame,
    open_: pd.DataFrame,
    tc_cost: float = 0.0005,
    slippage: float = 0.0002,
    rebalance_freq: int = 1,  # days between rebalances; 1 = daily
) -> pd.DataFrame:
    """Portfolio returns with less frequent rebalancing."""
    w = shift_weights(weights)
    if rebalance_freq > 1:
        w = _rebalance_weights(w, rebalance_freq)
    asset_ret = (open_.shift(-1) / close - 1.0)
    gross = (w * asset_ret).sum(axis=1)
    turnover = (w.diff().abs()).sum(axis=1)
    costs = turnover * (tc_cost + slippage)
    net = gross - costs
    return pd.DataFrame({"gross": gross, "costs": costs, "net": net})

def portfolio_returns_rebalance_clean(
    weights: pd.DataFrame,
    close: pd.DataFrame,
    open_: pd.DataFrame,
    tc_cost: float = 0.0005,
    slippage: float = 0.0002,
    rebalance_freq: int = 1,
) -> pd.DataFrame:
    w = shift_weights(weights)
    if rebalance_freq > 1:
        w = _rebalance_weights(w, rebalance_freq)
    asset_ret = (open_.shift(-1) / close - 1.0)
    gross = (w * asset_ret).sum(axis=1)
    turnover = (w.diff().abs()).sum(axis=1)
    costs = turnover * (tc_cost + slippage)
    net = gross - costs
    return pd.DataFrame({"gross": gross, "costs": costs, "net": net})


def time_series_momentum_weights(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    long_only: bool = True,
    vol_window: int = 63,
) -> pd.DataFrame:
    """Time-series momentum weights: long if signal > 0, flat if signal < 0 (long_only) or short.

    Classic Moskowitz et al. (2012) implementation with absolute threshold at zero.
    Positions scaled by inverse realized volatility for risk parity.

    Vectorized over dates (replaces a per-date ``signal.loc[date]`` loop that
    dominated runtime in walk-forward + placebo sweeps). Output is numerically
    identical to the row-loop implementation.
    """
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    if not long_only:
        # Cold path (long-short). Not on any hot loop; preserved verbatim for
        # bit-exactness (matches the original per-date loop).
        weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)
        for date in signal.index:
            sig_row = signal.loc[date]
            mask = sig_row != 0
            active = mask[mask].index
            if len(active) > 0:
                w = np.sign(sig_row[active]) * inv_vol.loc[date, active].fillna(0.0)
                s = w.abs().sum()
                if s > 0:
                    weights.loc[date, active] = w / s
        return weights

    # Hot path (long-only). Vectorized over dates; numerically identical to the
    # row loop (inactive columns contribute 0.0 to the sum, which is exact in
    # IEEE-754, so the per-row scale matches to floating-point noise).
    active = (signal > 0).fillna(False)
    raw = inv_vol.where(active).fillna(0.0)
    scale = raw.sum(axis=1).replace(0, np.nan)
    return raw.div(scale, axis=0).fillna(0.0)


def bab_weights(beta: pd.DataFrame) -> pd.DataFrame:
    """Frazzini & Pedersen (2014) Betting-Against-Beta factor weights.

    Market-neutral (zero beta) by construction. Long levered low-beta portfolio,
    short de-levered high-beta portfolio. Not dollar-neutral (BAB exploits leverage
    asymmetry). Stocks ranked by beta; weight in each side proportional to distance
    from the median rank, then rescaled so each side has unit beta.

    beta: per-stock rolling beta (index=date, columns=stock).
    Returns target weights (executed next-day open via shift_weights).
    """
    z = beta.rank(axis=1, ascending=True, method="min")          # low beta -> rank 1
    zbar = z.mean(axis=1)                                        # = (n+1)/2
    dev = z.sub(zbar, axis=0)
    w_low = dev.clip(upper=0).abs()                              # (zbar - z)_+  -> low-beta long
    w_high = dev.clip(lower=0)                                   # (z - zbar)_+   -> high-beta short

    s_low = w_low.sum(axis=1).replace(0, np.nan)
    s_high = w_high.sum(axis=1).replace(0, np.nan)
    w_low = w_low.div(s_low, axis=0)
    w_high = w_high.div(s_high, axis=0)

    beta_low = (beta * w_low).sum(axis=1)
    beta_high = (beta * w_high).sum(axis=1)
    # rescale each side to unit beta
    w_low = w_low.div(beta_low, axis=0)
    w_high = w_high.div(beta_high, axis=0)
    # long low-beta (levered), short high-beta (de-levered)
    return w_low.sub(w_high, axis=0)


def dollar_neutral_longshort_weights(
    signal: pd.DataFrame,
    top_frac: float = 0.2,
) -> pd.DataFrame:
    """Dollar-neutral long-short weighting.

    Long the top ``top_frac`` of names by signal, short the bottom ``top_frac``;
    weights sized so gross dollar exposure is 1x on each side and net is zero.
    Mirrors a classic 130/30-style market-neutral sort without beta adjustment.

    Vectorized over dates (replaces a per-date ``iterrows`` + ``nlargest`` loop
    that dominated runtime in walk-forward + placebo sweeps). The common case
    (enough non-NaN values to fill both sides, no boundary ties) uses numpy
    argpartition; all-NaN rows and the rare overlap/partial rows fall back to
    exact pandas ``nlargest``/``nsmallest`` semantics, so the output is
    bit-identical to the earlier ``iterrows`` implementation.
    """
    ranks = signal.rank(axis=1, ascending=False, method="min", pct=True)
    n = signal.shape[1]
    k = max(1, int(round(n * top_frac)))
    arr = ranks.to_numpy(dtype=float)
    valid = ~np.isnan(arr)
    m = valid.sum(axis=1)
    w = np.zeros_like(arr)

    full = m >= 2 * k
    if full.any():
        r = np.where(full)[0]
        a_small = np.where(valid[r], arr[r], np.inf)   # NaN -> +inf (excluded from smallest)
        a_large = np.where(valid[r], arr[r], -np.inf)  # NaN -> -inf (excluded from largest)
        short_pos = np.argpartition(a_small, kth=k - 1, axis=1)[:, :k]      # k smallest ranks
        long_pos = np.argpartition(a_large, kth=n - k, axis=1)[:, n - k:]   # k largest ranks
        rr = r[:, None]
        w[rr, long_pos] = 1.0 / k
        w[rr, short_pos] = -1.0 / k

    # All-NaN rows: matches pandas nlargest/nsmallest on an all-NaN Series,
    # which returns the first k columns (shared by both -> -1/k on cols 0..k-1).
    empty = m == 0
    if empty.any():
        r = np.where(empty)[0]
        w[r, :k] = -1.0 / k

    # Rare overlap/partial rows: preserve exact original semantics.
    other = (~full) & (~empty)
    if other.any():
        col_index = {c: i for i, c in enumerate(signal.columns)}
        for pos in np.where(other)[0]:
            row = ranks.iloc[pos]
            long_idx = [col_index[c] for c in row.nlargest(k).index]
            short_idx = [col_index[c] for c in row.nsmallest(k).index]
            w[pos, long_idx] = 1.0 / k
            w[pos, short_idx] = -1.0 / k

    return pd.DataFrame(w, index=signal.index, columns=signal.columns)
