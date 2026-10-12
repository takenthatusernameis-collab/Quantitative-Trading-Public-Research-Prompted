"""Idiosyncratic-volatility (IVOL) anomaly (Ang, Hodrick, Xing & Zhang 2006).

IVOL = residual volatility from regressing daily stock returns on market factor(s)
over a trailing window. The anomaly: high IVOL predicts lower future returns
("lottery ticket" preference / limits-to-arbitrage).

Primary construction (pre-registered):
- Factor model: CAPM (daily stock return ~ SPY return), trailing 252 trading days
- IVOL = residual standard deviation from the regression
- Monthly (21d) rebalance, dollar-neutral long-short
- Long bottom quintile (low IVOL), short top quintile (high IVOL)
- Inverse-vol weighted across active names, monthly rebalance
- Close-to-close execution convention (primary per v1.2.3)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

from src import backtest


def idiosyncratic_vol_signal(
    close: pd.DataFrame,
    market_close: pd.Series,
    window: int = 252,
    skip: int = 1,
) -> pd.DataFrame:
    """Compute idiosyncratic volatility (IVOL) for each stock.

    Uses vectorized rolling CAPM regression:
    - IVOL = sqrt(Var(r) - Cov(r, rm)^2 / Var(rm)) * sqrt(252)
      where r = stock returns, rm = market returns
    - This is the residual variance from regressing r on rm

    Args:
        close: DataFrame of close prices (index=date, columns=tickers)
        market_close: Series of market benchmark close prices (e.g., SPY)
        window: Lookback window in trading days for the regression
        skip: Days to lag the signal (to avoid look-ahead when weights
              formed at close t are executed at t+1)

    Returns:
        DataFrame of IVOL values (higher = more idiosyncratic risk).
        The caller should invert (negative IVOL) so low IVOL = high signal.
    """
    rets = close.pct_change()
    rm = market_close.pct_change()
    rm = rm.reindex(rets.index)

    # Vectorized rolling moments
    r_mean = rets.rolling(window).mean()
    rm_mean = rm.rolling(window).mean()
    cross_mean = rets.mul(rm, axis=0).rolling(window).mean()
    cov = cross_mean - r_mean.mul(rm_mean, axis=0)
    var_r = rets.rolling(window).var(ddof=0)
    var_rm = rm.rolling(window).var(ddof=0)

    # Residual variance = Var(r) - Cov(r, rm)^2 / Var(rm)
    # This is Var(r) * (1 - rho^2) where rho = correlation(r, rm)
    resid_var = var_r - (cov ** 2).div(var_rm, axis=0)
    resid_var = resid_var.clip(lower=0)  # numerical precision
    ivol = np.sqrt(resid_var) * np.sqrt(252)

    if skip:
        ivol = ivol.shift(skip)

    return ivol


def _zscore_cross_section(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectional z-score standardization per day."""
    arr = df.to_numpy()
    mu = np.nanmean(arr, axis=1, keepdims=True)
    sd = np.nanstd(arr, axis=1, keepdims=True) + 1e-9
    z = (arr - mu) / sd
    return pd.DataFrame(z, index=df.index, columns=df.columns)


def ivol_weights(
    ivol_signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    top_frac: float = 0.2,
) -> pd.DataFrame:
    """Dollar-neutral IVOL weights: long low-IVOL, short high-IVOL.

    Computes weights for ALL dates (daily). The caller (backtest engine)
    handles rebalancing frequency via _rebalance_weights.

    Vectorized implementation for speed: ranks all dates at once,
    then computes inverse-vol weights per date.

    Args:
        ivol_signal: IVOL values (higher = more idiosyncratic risk).
                     Low IVOL should get positive weight (long).
        close: Close prices for volatility estimation
        vol_window: Window for realized volatility estimation
        top_frac: Fraction of names on each side (e.g., 0.2 = quintile)

    Returns:
        DataFrame of target weights (gross 1.0 per side, net 0).
    """
    # Invert IVOL so low IVOL = high signal (we want to long low IVOL)
    signal = -ivol_signal

    # Cross-sectional z-score for ranking stability
    signal_z = _zscore_cross_section(signal)

    # Realized volatility for inverse-vol weighting
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    n = signal_z.shape[1]
    k = max(1, int(round(n * top_frac)))

    # Vectorized ranking across all dates
    ranks = signal_z.rank(axis=1, ascending=False, method="min", pct=False)
    arr = ranks.to_numpy(dtype=float)
    valid = ~np.isnan(arr)
    m = valid.sum(axis=1)

    # Precompute inverse vol array (aligned)
    inv_vol_arr = inv_vol.to_numpy(dtype=float)
    inv_vol_arr = np.where(np.isnan(inv_vol_arr) | (inv_vol_arr <= 0), np.nan, inv_vol_arr)

    w = np.zeros_like(arr)

    # Full rows: enough valid names for both sides
    full = m >= 2 * k
    if full.any():
        r = np.where(full)[0]
        # For valid entries, use rank; for NaN, use inf/-inf to exclude
        a_small = np.where(valid[r], arr[r], np.inf)   # NaN -> +inf (excluded from smallest rank)
        a_large = np.where(valid[r], arr[r], -np.inf)  # NaN -> -inf (excluded from largest rank)
        # Long = highest signal (lowest rank number = 1 is best)
        long_pos = np.argpartition(a_large, kth=n - k, axis=1)[:, n - k:]
        # Short = lowest signal (highest rank number)
        short_pos = np.argpartition(a_small, kth=k - 1, axis=1)[:, :k]

        for i, row_idx in enumerate(r):
            long_idx = long_pos[i]
            short_idx = short_pos[i]
            # Inverse-vol weighting
            long_iv = inv_vol_arr[row_idx, long_idx]
            short_iv = inv_vol_arr[row_idx, short_idx]
            if np.nansum(long_iv) > 0:
                w[row_idx, long_idx] = (long_iv / np.nansum(long_iv)) * 0.5
            if np.nansum(short_iv) > 0:
                w[row_idx, short_idx] = (short_iv / np.nansum(short_iv)) * -0.5

    # Other rows: fall back to pandas for exact semantics (rare)
    other = (~full) & (m > 0)
    if other.any():
        col_index = {c: i for i, c in enumerate(signal_z.columns)}
        for pos in np.where(other)[0]:
            row = signal_z.iloc[pos]
            vol_row = inv_vol.iloc[pos] if pos < len(inv_vol) else pd.Series(np.nan, index=signal_z.columns)
            valid_names = row.notna() & vol_row.notna() & (vol_row > 0)
            if valid_names.sum() < 2 * k:
                continue
            row_valid = row[valid_names]
            vol_valid = vol_row[valid_names]
            ranked_valid = row_valid.rank(ascending=False, method="min")
            n_valid = len(row_valid)
            long_idx = [col_index[c] for c in row_valid[ranked_valid <= k].index]
            short_idx = [col_index[c] for c in row_valid[ranked_valid > (n_valid - k)].index]
            if long_idx:
                long_iv = vol_valid[row_valid.index[long_idx]].values if False else [vol_row[c] for c in row_valid[ranked_valid <= k].index]
                long_iv = np.array([vol_row[c] for c in row_valid[ranked_valid <= k].index])
                if np.nansum(long_iv) > 0:
                    w[pos, long_idx] = (long_iv / np.nansum(long_iv)) * 0.5
            if short_idx:
                short_iv = np.array([vol_row[c] for c in row_valid[ranked_valid > (n_valid - k)].index])
                if np.nansum(short_iv) > 0:
                    w[pos, short_idx] = (short_iv / np.nansum(short_iv)) * -0.5

    return pd.DataFrame(w, index=signal_z.index, columns=signal_z.columns)


def ivol_placebo_weights(
    ivol_signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    top_frac: float = 0.2,
    seed: int = 42,
    n_sim: int = 50,
) -> List[pd.DataFrame]:
    """Placebo: random cross-sectional signals with same IVOL weighting construction.

    Preserves the inverse-vol / dollar-neutral construction but replaces the
    IVOL signal with random noise. Tests whether pair/name selection has skill.

    Vectorized for speed: generates random ranks for all simulations at once.
    """
    rng = np.random.default_rng(seed)
    dates = ivol_signal.index
    tickers = ivol_signal.columns.tolist()
    n = len(tickers)
    k = max(1, int(round(n * top_frac)))
    n_dates = len(dates)

    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol
    inv_vol_arr = inv_vol.to_numpy(dtype=float)
    inv_vol_arr = np.where(np.isnan(inv_vol_arr) | (inv_vol_arr <= 0), np.nan, inv_vol_arr)

    placebo_weights_list = []

    for _ in range(n_sim):
        # Generate random ranks for all dates at once
        rand_ranks = rng.random((n_dates, n))
        # Set NaN where inv_vol is NaN
        rand_ranks = np.where(np.isnan(inv_vol_arr), np.nan, rand_ranks)

        w = np.zeros((n_dates, n), dtype=float)

        # Valid count per row
        valid = ~np.isnan(rand_ranks)
        m = valid.sum(axis=1)
        full = m >= 2 * k

        if full.any():
            r = np.where(full)[0]
            a_small = np.where(valid[r], rand_ranks[r], np.inf)
            a_large = np.where(valid[r], rand_ranks[r], -np.inf)
            long_pos = np.argpartition(a_large, kth=n - k, axis=1)[:, n - k:]
            short_pos = np.argpartition(a_small, kth=k - 1, axis=1)[:, :k]

            for i, row_idx in enumerate(r):
                long_idx = long_pos[i]
                short_idx = short_pos[i]
                long_iv = inv_vol_arr[row_idx, long_idx]
                short_iv = inv_vol_arr[row_idx, short_idx]
                if np.nansum(long_iv) > 0:
                    w[row_idx, long_idx] = (long_iv / np.nansum(long_iv)) * 0.5
                if np.nansum(short_iv) > 0:
                    w[row_idx, short_idx] = (short_iv / np.nansum(short_iv)) * -0.5

        placebo_weights_list.append(pd.DataFrame(w, index=dates, columns=tickers))

    return placebo_weights_list


def compute_falsification(
    close: pd.DataFrame,
    market_close: pd.Series,
    ivol_signal: pd.DataFrame,
    window: int = 252,
) -> Dict:
    """Compute falsification expectation (FE1): predictive content of IVOL.

    FE1: mean |Spearman(IVOL[t], next-month return[t])| >= 0.03
         AND >= 60% negative (high IVOL -> lower next-month return)
    """
    from scipy.stats import spearmanr

    rets = close.pct_change()
    rm = market_close.pct_change().reindex(rets.index)

    # Next 21-day (monthly) return
    fwd_ret = rets.shift(-21).rolling(21).apply(lambda x: (1 + x).prod() - 1, raw=True)

    spearman_vals = []
    neg_frac_vals = []

    dates = ivol_signal.index
    for date in dates:
        if date not in rets.index:
            continue
        ivol_row = ivol_signal.loc[date]
        ret_row = fwd_ret.loc[date] if date in fwd_ret.index else pd.Series(np.nan, index=close.columns)

        valid = ivol_row.notna() & ret_row.notna()
        if valid.sum() < 10:
            continue

        ivol_vals = ivol_row[valid].values
        ret_vals = ret_row[valid].values

        try:
            rho, _ = spearmanr(ivol_vals, ret_vals)
            if np.isfinite(rho):
                spearman_vals.append(abs(rho))
                # High IVOL -> lower return means negative correlation
                neg_frac_vals.append(1.0 if rho < 0 else 0.0)
        except Exception:
            continue

    return {
        "fe1_mean_abs_spearman": float(np.mean(spearman_vals)) if spearman_vals else np.nan,
        "fe1_frac_negative": float(np.mean(neg_frac_vals)) if neg_frac_vals else np.nan,
        "fe1_n_dates": len(spearman_vals),
    }