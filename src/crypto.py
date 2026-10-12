"""Crypto cross-asset momentum signals (BTC, ETH).

Implements time-series momentum (TSM) and cross-sectional momentum (XSM)
on cryptocurrency pairs traded 24/7 via yfinance (BTC-USD, ETH-USD).

TSM: long assets with positive 12-month past return (Moskowitz, Ooi & Pedersen
2012 applied to crypto). Variant: dollar-neutral long-short by momentum rank
(long high-momentum, short low-momentum), inverse-vol weighted.

Calendar alignment: crypto trades 24/7; data is reindexed to the equity
trading calendar (SPY business days) with forward-filled closes so that
walk-forward splits and SPY-beta comparison are meaningful. Weekend/holiday
returns are captured in the next business-day close (Friday-close to
Monday-close), which is the correct P&L for a close-to-close convention.

Carry (funding-rate basis) is NOT testable here: yfinance spot has no funding
rate column, and a spot-only carry proxy is degenerate. TSM/XSM is the
testable family, consistent with the literature on crypto momentum.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

from src import backtest


CRYPTO_TICKERS = ["BTC-USD", "ETH-USD"]


def _zscore_cross_section(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectional z-score standardization per day."""
    arr = df.to_numpy()
    mu = np.nanmean(arr, axis=1, keepdims=True)
    sd = np.nanstd(arr, axis=1, keepdims=True) + 1e-12
    z = (arr - mu) / sd
    return pd.DataFrame(z, index=df.index, columns=df.columns)


def crypto_tsm_signal(
    close: pd.DataFrame,
    lookback_days: int = 252,
    skip: int = 21,
    winsorize: bool = True,
) -> pd.DataFrame:
    """Time-series momentum signal: past ``lookback_days`` total return, lagged.

    Args:
        close: Business-day-aligned close prices (index=date, columns=tickers).
        lookback_days: Lookback window in trading days (252 = ~12 months).
        skip: Lag in trading days to avoid same-day look-ahead (21 = ~1 month).
        winsorize: If True, winsorize at 1/99 percentile per day and z-score.

    Returns:
        DataFrame of TSM signals (same shape as close). Positive = momentum.
        The caller inverts or thresholds as needed for weighting.
    """
    ret = close.pct_change(lookback_days)
    signal = ret.shift(skip)

    if winsorize:
        arr = signal.to_numpy()
        with np.errstate(invalid="ignore"):
            lo = np.nanquantile(arr, 0.01, axis=1, keepdims=True)
            hi = np.nanquantile(arr, 0.99, axis=1, keepdims=True)
        win = np.clip(arr, lo, hi)
        with np.errstate(invalid="ignore"):
            mu = np.nanmean(win, axis=1, keepdims=True)
            sd = np.nanstd(win, axis=1, keepdims=True, ddof=1)
        sig = pd.DataFrame((win - mu) / (sd + 1e-12), index=signal.index, columns=signal.columns)
        return sig
    return signal


def crypto_weights(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    top_frac: float = 0.5,
    long_only: bool = True,
) -> pd.DataFrame:
    """Target weights for crypto momentum strategy.

    Long-only (primary): long assets with positive signal, inverse-vol
    weighted within the long selection.  Net exposure = sum of long weights
    (0 to 1.0).

    Dollar-neutral (variant): long top ``top_frac`` by signal, short bottom
    ``top_frac``; each side inverse-vol weighted and scaled to 0.5 gross
    (total gross 1.0, net 0).  With 2 tickers this is long the higher-momentum
    name and short the lower.

    Args:
        signal: Cross-sectional signal (higher = stronger momentum).
        close: Close prices for realized-vol estimation.
        vol_window: Rolling window for realized vol (trading days).
        top_frac: Fraction of names on each side (0.5 = 1 of 2 tickers).
        long_only: If True, only long positive-signal names; if False, DN.

    Returns:
        DataFrame of target weights (same shape as signal).
    """
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol

    ranks = signal.rank(axis=1, ascending=False, method="min", pct=True)
    n = signal.shape[1]
    k = max(1, int(round(n * top_frac)))

    weights = pd.DataFrame(0.0, index=signal.index, columns=signal.columns)

    long_mask = ranks >= (1.0 - top_frac + 1e-12)
    if long_only:
        # Only long positive-signal names
        pos_mask = signal > 0
        mask = long_mask & pos_mask
        raw = inv_vol.where(mask).fillna(0.0)
        s = raw.sum(axis=1).replace(0, np.nan)
        w = raw.div(s, axis=0).fillna(0.0)
        return w.clip(lower=0.0)

    short_mask = ranks <= top_frac + 1e-12
    for mask, scale in ((long_mask, 0.5), (short_mask, -0.5)):
        raw = inv_vol.where(mask).fillna(0.0)
        s = raw.sum(axis=1).replace(0, np.nan)
        side = raw.div(s, axis=0).fillna(0.0).mul(scale)
        weights = weights.add(side, fill_value=0.0)
    return weights


def crypto_placebo_weights(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    top_frac: float = 0.5,
    long_only: bool = True,
    seed: int = 42,
    n_sim: int = 50,
) -> List[pd.DataFrame]:
    """Placebo null: i.i.d. standard-normal signals, identical construction.

    Preserves the universe, vol window, top_frac, rebalance cadence, and
    weighting engine while destroying the TSM signal.  Tests whether the
    cross-sectional ranking itself has skill beyond random noise.

    Vectorized across dates within each simulation for speed.
    """
    rng = np.random.default_rng(seed)
    valid = signal.notna()
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = 1.0 / vol
    inv_vol_arr = inv_vol.to_numpy(dtype=float)
    inv_vol_arr = np.where(np.isnan(inv_vol_arr) | (inv_vol_arr <= 0), np.nan, inv_vol_arr)

    n = signal.shape[1]
    k = max(1, int(round(n * top_frac)))
    n_dates = signal.shape[0]

    weights_list: List[pd.DataFrame] = []
    for _ in range(n_sim):
        rand = rng.standard_normal(size=(n_dates, n))
        rand = np.where(valid.to_numpy(), rand, np.nan)
        ranks = np.zeros_like(rand)
        valid_mask = ~np.isnan(rand)
        # Rank per row (descending so largest random = rank 0 -> percentile ~1)
        for i in range(n_dates):
            if valid_mask[i].sum() > 0:
                r = pd.Series(rand[i]).rank(ascending=False, method="min", pct=True).to_numpy()
                ranks[i] = np.where(valid_mask[i], r, np.nan)

        w = np.zeros_like(rand, dtype=float)
        long_pct = 1.0 - top_frac
        long_mask = ranks >= long_pct + 1e-12
        short_mask = ranks <= top_frac + 1e-12

        if long_only:
            pos_mask = rand > 0
            mask = long_mask & pos_mask
            for i in range(n_dates):
                idx = np.where(mask[i] & ~np.isnan(inv_vol_arr[i]))[0]
                if len(idx) == 0:
                    continue
                iv = inv_vol_arr[i, idx]
                if np.nansum(iv) > 0:
                    w[i, idx] = iv / np.nansum(iv)
        else:
            for i in range(n_dates):
                for mask_arr, scale in ((long_mask, 0.5), (short_mask, -0.5)):
                    idx = np.where(mask_arr[i] & ~np.isnan(inv_vol_arr[i]))[0]
                    if len(idx) == 0:
                        continue
                    iv = inv_vol_arr[i, idx]
                    if np.nansum(iv) > 0:
                        w[i, idx] += (iv / np.nansum(iv)) * scale

        weights_list.append(pd.DataFrame(w, index=signal.index, columns=signal.columns))

    return weights_list


def compute_falsification(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    forward_window: int = 21,
) -> Dict:
    """FE1: within-sample predictive content of the crypto TSM signal.

    For each date t, compute Spearman(signal[t], next-forward_window-day
    return[t]) cross-sectionally.  The signal must show directional
    predictability: high signal -> higher next-period return.

    FE1 passes if:
      mean |Spearman| >= 0.03  AND  frac_positive >= 0.60

    NOTE: with only 2 tickers, Spearman is always +/-1 when both are valid,
    so mean |Spearman| is trivially 1.0.  The frac_positive metric is still
    informative (it tests directional consistency).  Pearson correlation is
    also reported as a continuous alternative.
    """
    from scipy.stats import spearmanr

    fwd_ret = close.shift(-forward_window) / close - 1.0

    rho_arr = np.full(signal.shape[0], np.nan)
    frac_pos_arr = np.full(signal.shape[0], np.nan)
    pearson_arr = np.full(signal.shape[0], np.nan)

    sig_vals = signal.to_numpy()
    fwd_vals = fwd_ret.to_numpy()
    for i in range(signal.shape[0]):
        m = ~(np.isnan(sig_vals[i]) | np.isnan(fwd_vals[i]))
        if m.sum() >= 2:
            rho, _ = spearmanr(sig_vals[i][m], fwd_vals[i][m])
            if np.isfinite(rho):
                rho_arr[i] = abs(rho)
                frac_pos_arr[i] = 1.0 if rho > 0 else 0.0
            if m.sum() >= 2:
                pv = sig_vals[i][m]
                fv = fwd_vals[i][m]
                if np.std(pv) > 0 and np.std(fv) > 0:
                    pearson_arr[i] = float(np.corrcoef(pv, fv)[0, 1])

    rho_clean = rho_arr[~np.isnan(rho_arr)]
    frac_clean = frac_pos_arr[~np.isnan(frac_pos_arr)]
    pearson_clean = pearson_arr[~np.isnan(pearson_arr)]
    mean_abs = float(np.mean(rho_clean)) if len(rho_clean) else float("nan")
    frac_pos = float(np.mean(frac_clean)) if len(frac_clean) else float("nan")
    mean_pearson = float(np.mean(pearson_clean)) if len(pearson_clean) else float("nan")
    mean_abs_pearson = float(np.mean(np.abs(pearson_clean))) if len(pearson_clean) else float("nan")
    n_valid = int(signal.shape[1])

    return {
        "fe1_mean_abs_spearman": mean_abs,
        "fe1_frac_positive": frac_pos,
        "fe1_mean_abs_pearson": mean_abs_pearson,
        "fe1_mean_pearson": mean_pearson,
        "fe1_n_dates": int(len(rho_clean)),
        "fe1_n_assets": n_valid,
        "fe1_warning": "2-asset Spearman degenerate (always +/-1)" if n_valid <= 2 else None,
        "fe1_gate_mean_abs_ge_0_03": bool(mean_abs_pearson >= 0.03) if np.isfinite(mean_abs_pearson) else False,
        "fe1_gate_frac_pos_ge_0_60": bool(frac_pos >= 0.60) if np.isfinite(frac_pos) else False,
    }
