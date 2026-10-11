"""Cointegration-based statistical arbitrage (Engle-Granger, Johansen).

Engle-Granger two-step method:
1. OLS regression: log(P_a) = alpha + beta * log(P_b) + epsilon
2. ADF test on residuals epsilon; select pairs with most negative ADF statistic

Johansen method (trace test, r=1): alternative for robustness.

Trading: z-score of spread s_t = log(P_a,t) - beta * log(P_b,t) - alpha
- Entry: |z| >= entry_z
- Exit: |z| <= exit_z
- Dollar-neutral per pair (0.5 long / 0.5 short leg)
- Inverse-vol weighted across active pairs
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant

from src import backtest


def _formation_dates(close: pd.DataFrame, formation_window: int, rebalance_freq: int) -> List[pd.Timestamp]:
    """Rebalance/formation dates: every rebalance_freq days starting at formation_window."""
    dates = close.index
    return list(dates[formation_window::rebalance_freq])


def _pair_key(a: str, b: str) -> Tuple[str, str]:
    """Canonical unordered pair key for state tracking."""
    return (a, b) if a <= b else (b, a)


def _engle_granger_test(log_pa: pd.Series, log_pb: pd.Series) -> Tuple[float, float, float, float]:
    """Engle-Granger two-step cointegration test.

    Returns: (hedge_ratio, intercept, adf_stat, adf_pval, half_life)
    """
    aligned = pd.concat([log_pa, log_pb], axis=1, join="inner").dropna()
    if len(aligned) < 2:
        return np.nan, np.nan, np.nan, np.nan, np.nan
    log_pa_a = aligned.iloc[:, 0].values
    log_pb_a = aligned.iloc[:, 1].values

    X = add_constant(log_pb_a)
    model = OLS(log_pa_a, X).fit()
    alpha = model.params[0]
    beta = model.params[1]
    resid = model.resid

    adf_result = adfuller(resid, autolag="AIC")
    adf_stat = adf_result[0]
    adf_pval = adf_result[1]

    # Half-life of mean reversion: -log(2) / log(1 + theta) where theta is AR(1) coeff of residuals
    if len(resid) > 1:
        theta = np.corrcoef(resid[:-1], resid[1:])[0, 1]
        if theta < 1.0 and theta > 0:
            half_life = -np.log(2) / np.log(theta)
        else:
            half_life = np.nan
    else:
        half_life = np.nan

    return float(beta), float(alpha), float(adf_stat), float(adf_pval), float(half_life)


def _johansen_test(log_pa: pd.Series, log_pb: pd.Series) -> Tuple[float, float, float]:
    """Johansen cointegration test (trace statistic for r=1).

    Returns: (trace_stat_0, trace_stat_1, hedge_ratio_approx)
    """
    from statsmodels.tsa.vector_ar.vecm import coint_johansen

    aligned = pd.concat([log_pa, log_pb], axis=1, join="inner").dropna()
    if len(aligned) < 2:
        return np.nan, np.nan, np.nan

    result = coint_johansen(aligned.values, det_order=0, k_ar_diff=1)
    trace_stat = result.lr1[0]  # r=0 (no cointegration)
    trace_stat_1 = result.lr1[1]  # r=1 (at most 1 cointegrating vector)

    # Eigenvector for r=1 gives the hedge ratio (first column, normalized to first asset = 1)
    eigvec = result.evec[:, 0]
    hedge_ratio = eigvec[1] / eigvec[0] if eigvec[0] != 0 else np.nan

    return float(trace_stat), float(trace_stat_1), float(hedge_ratio)


def find_cointegrated_pairs(
    close: pd.DataFrame,
    formation_window: int = 252,
    max_pairs: int = 20,
    method: str = "engle_granger",
    adf_threshold: float = 0.05,
    min_half_life: int = 1,
    max_half_life: int = 252,
) -> Dict[pd.Timestamp, List[Tuple[str, str, float, float, float, float]]]:
    """Find cointegrated pairs using Engle-Granger or Johansen method.

    Returns dict mapping formation date -> list of
    (stock_a, stock_b, hedge_ratio, intercept, adf_stat_or_trace, half_life).
    """
    dates = close.index
    log_close = np.log(close)
    pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float, float, float, float]]] = {}

    for form_end in _formation_dates(close, formation_window, 21):
        i = dates.get_indexer([form_end], method="pad")[0]
        if i < formation_window:
            pairs_by_date[form_end] = []
            continue
        form_start = dates[i - formation_window]
        window_data = log_close.loc[form_start:form_end].dropna(axis=1, how="any")
        if window_data.shape[1] < 2:
            pairs_by_date[form_end] = []
            continue

        tickers = window_data.columns.tolist()
        n = len(tickers)
        results = []

        for j in range(n):
            for k in range(j + 1, n):
                a, b = tickers[j], tickers[k]
                log_pa = window_data[a]
                log_pb = window_data[b]

                if method == "engle_granger":
                    beta, alpha, adf_stat, adf_pval, half_life = _engle_granger_test(log_pa, log_pb)
                    if (not np.isnan(adf_pval) and adf_pval < adf_threshold and
                        not np.isnan(half_life) and min_half_life <= half_life <= max_half_life):
                        results.append((a, b, beta, alpha, adf_stat, half_life))
                elif method == "johansen":
                    trace_0, trace_1, beta = _johansen_test(log_pa, log_pb)
                    if not np.isnan(beta):
                        alpha = 0.0  # Not directly estimated in this simplified version
                        results.append((a, b, beta, alpha, trace_0, np.nan))

        # Sort by ADF stat (most negative = strongest mean reversion) or trace stat
        if method == "engle_granger":
            results.sort(key=lambda x: x[4])  # ADF stat (most negative first)
        else:
            results.sort(key=lambda x: -x[4])  # Trace stat (larger = more evidence)

        pairs_by_date[form_end] = results[:max_pairs]

    return pairs_by_date


def _stateful_positions(z: pd.Series, entry_z: float, exit_z: float) -> pd.Series:
    """Stateful pair position from a z-score series.

    Entry at |z| >= entry_z (sign = -sign(z): negative z -> long spread).
    Hold until |z| <= exit_z, then flat. NaN z keeps the current state.
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


def _spread_zscore(close: pd.DataFrame, a: str, b: str,
                   beta: float, alpha: float,
                   formation_window: int) -> pd.Series:
    """Z-score of spread s_t = log(P_a) - beta*log(P_b) - alpha using formation window stats."""
    spread = np.log(close[a]) - beta * np.log(close[b]) - alpha
    if formation_window <= 0:
        return pd.Series(np.nan, index=spread.index)
    roll_mean = spread.rolling(formation_window, min_periods=formation_window).mean()
    roll_std = spread.rolling(formation_window, min_periods=formation_window).std()
    valid = (
        spread.notna()
        .rolling(formation_window, min_periods=formation_window)
        .sum()
        == formation_window
    )
    z = (spread - roll_mean) / roll_std
    z = z.where(valid & roll_std.notna() & (roll_std > 0))
    return z


def _pair_vol(close: pd.DataFrame, vol: pd.DataFrame, a: str, b: str, date) -> float:
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


def cointegration_weights(
    close: pd.DataFrame,
    pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float, float, float, float]]],
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    vol_window: int = 63,
    rebalance_freq: int = 21,
) -> pd.DataFrame:
    """Daily target weights for cointegration-based pairs trading.

    For each rebalance date, select the most recent formation period's pairs,
    read their stateful positions (computed from data available at that date),
    and aggregate into dollar-neutral, inverse-vol-weighted target weights.
    Weights are held constant between rebalances.
    """
    dates = close.index
    tickers = close.columns

    form_dates = sorted(pairs_by_date.keys())
    if not form_dates:
        return pd.DataFrame(0.0, index=dates, columns=tickers)

    vol = _precompute_vol(close, vol_window)

    # Pre-compute stateful positions for every candidate pair over the full history
    pos_cache: Dict[Tuple[str, str], pd.Series] = {}
    seen_pairs = set()
    for pairs in pairs_by_date.values():
        for a, b, beta, alpha, _, _ in pairs:
            k = _pair_key(a, b)
            if k not in seen_pairs:
                seen_pairs.add(k)
                z = _spread_zscore(close, k[0], k[1], beta, alpha, formation_window=252)
                pos_cache[k] = _stateful_positions(z, entry_z, exit_z)

    rebalance_days = set(dates[::rebalance_freq]) if rebalance_freq > 1 else set(dates)

    rebalance_weights = pd.DataFrame(0.0, index=dates, columns=tickers)

    for date in dates:
        if date not in rebalance_days:
            continue
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

        active = []
        for a, b, beta, alpha, _, _ in active_pairs:
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

    weights = pd.DataFrame(0.0, index=dates, columns=tickers)
    active_rebalance_dates = [
        d for d in rebalance_weights.index
        if (rebalance_weights.loc[d].abs() > 1e-9).any()
    ]
    if not active_rebalance_dates:
        return weights
    arr = np.asarray(active_rebalance_dates)
    idx = np.searchsorted(arr, dates, side="right") - 1
    for j, k in enumerate(idx):
        if k >= 0:
            weights.iloc[j] = rebalance_weights.loc[arr[k]].to_numpy()
    return weights


def cointegration_placebo_weights(
    close: pd.DataFrame,
    n_pairs: int,
    entry_z: float = 2.0,
    exit_z: float = 0.5,
    vol_window: int = 63,
    rebalance_freq: int = 21,
    seed: int = 42,
) -> List[pd.DataFrame]:
    """Pair-level placebo: random pair matching within universe, identical stateful trading rule."""
    rng = np.random.default_rng(seed)
    tickers = close.columns.tolist()
    n = len(tickers)
    dates = close.index
    placebo_weights: List[pd.DataFrame] = []

    form_dates = _formation_dates(close, 252, rebalance_freq)

    for _ in range(50):
        perm = rng.permutation(n)
        random_pairs: List[Tuple[str, str, float, float, float, float]] = []
        for i in range(0, min(n_pairs * 2, n), 2):
            if i + 1 < n:
                a, b = tickers[perm[i]], tickers[perm[i + 1]]
                # For placebo, use beta=1, alpha=0 (simple log spread)
                random_pairs.append((a, b, 1.0, 0.0, 0.0, np.nan))

        pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float, float, float, float]]] = {
            fd: random_pairs for fd in form_dates
        }
        w = cointegration_weights(
            close, pairs_by_date,
            entry_z=entry_z, exit_z=exit_z,
            vol_window=vol_window, rebalance_freq=rebalance_freq,
        )
        placebo_weights.append(w)

    return placebo_weights