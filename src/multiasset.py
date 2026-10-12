"""Multi-asset time-series momentum on liquid ETFs (E030).

Extends the repository's validated pure time-series-momentum engine
(Moskowitz, Ooi & Pedersen 2012, "Time Series Momentum", JFE; the
equity flagship implemented by ``strategies.time_series_momentum_pure``
+ ``backtest.time_series_momentum_weights``) to a cross-asset ETF
universe spanning US/international/emerging equities, commodities,
fixed income, real estate and defensive sectors.

Why ETFs instead of futures: the E016-E019 experiments showed that
raw yfinance continuous futures contracts (``=F``) contain large
roll-stitching artifacts (median seam gaps 0.3-2.5%) that moved TSM
OOS Sharpe by 21% and flipped the bear-market Sharpe. ETFs carry no
roll seams. Commodity ETFs (USO, DBC) economically embed
contango/backwardation drag -- a real feature of the investable
return stream, not a data artifact.

Construction (identical to the equity flagship, applied per ETF):
- Signal: past ``lookback_days`` (252 = 12m) total return, lagged
  ``skip`` (21 = 1m) trading days to avoid same-month look-ahead.
- Primary (long-only): long ETFs with positive signal,
  inverse-realized-vol (63d) weighted, gross normalized to 1.0.
- Variant (long-short): long positive-signal ETFs, short
  negative-signal ETFs, inverse-vol weighted, gross 1.0 / net 0.
- Monthly (21d) rebalance, close-to-close execution (primary
  convention per ledger PRIORITIZATION.md v1.2.3).
"""

import numpy as np
import pandas as pd
from typing import Dict, List

from src import backtest

MULTI_ASSET_ETFS = [
    # US equities
    "SPY", "QQQ", "IWM",
    # International / emerging
    "EFA", "EEM",
    # Commodities
    "GLD", "USO", "DBC",
    # Fixed income
    "TLT", "IEF", "LQD", "HYG",
    # Real estate
    "VNQ",
    # Defensive sectors
    "XLU", "XLP", "XLV",
]


def multiasset_tsm_signal(
    close: pd.DataFrame,
    lookback_days: int = 252,
    skip: int = 21,
    winsorize: bool = True,
) -> pd.DataFrame:
    """Time-series momentum signal: past ``lookback_days`` return, lagged.

    Returns the raw (or winsorized + cross-sectionally z-scored) past
    return. The z-score is a monotone per-day transform, so it preserves
    the sign of every signal -- the pure-TSM weighting engine keys only
    on the sign -- while giving a well-scaled input for the FE1
    Spearman falsification (which is rank-based and therefore invariant
    to the transform).
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
        return pd.DataFrame(
            (win - mu) / (sd + 1e-12), index=signal.index, columns=signal.columns
        )
    return signal


def multiasset_weights(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    long_only: bool = True,
) -> pd.DataFrame:
    """Target weights for multi-asset TSM (delegates to the flagship engine).

    Long-only: long positive-signal ETFs, inverse-vol weighted, gross 1.0.
    Long-short: long positive / short negative, inverse-vol, gross 1.0.
    """
    return backtest.time_series_momentum_weights(
        signal, close, long_only=long_only, vol_window=vol_window
    )


def _inv_vol(close: pd.DataFrame, vol_window: int) -> np.ndarray:
    rets = close.pct_change()
    vol = rets.rolling(vol_window).std().replace(0, np.nan)
    inv_vol = (1.0 / vol).to_numpy(dtype=float)
    return np.where(np.isnan(inv_vol) | (inv_vol <= 0), np.nan, inv_vol)


def multiasset_placebo_weights(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    vol_window: int = 63,
    long_only: bool = True,
    seed: int = 42,
    n_sim: int = 50,
) -> List[pd.DataFrame]:
    """Placebo null: i.i.d. standard-normal signals, identical construction.

    Preserves the universe, the realized-vol risk budget (a property of
    prices, not the signal), the ~50% participation rate of the
    sign-threshold rule, and the rebalance cadence, while destroying
    any time-series/cross-sectional structure in the TSM signal.

    Vectorized replication of ``backtest.time_series_momentum_weights``
    (verified bit-comparable against the engine in tests): the engine's
    long-only path is ``sign(signal) > 0`` masking of inverse-vol,
    row-normalized; the long-short path is ``sign(signal) * inv_vol``,
    row-normalized to gross 1.0.
    """
    rng = np.random.default_rng(seed)
    valid = signal.notna().to_numpy()
    inv_vol = _inv_vol(close, vol_window)
    n_dates, n_assets = signal.shape

    weights_list: List[pd.DataFrame] = []
    for _ in range(n_sim):
        rand = rng.standard_normal(size=(n_dates, n_assets))
        rand = np.where(valid, rand, np.nan)
        if long_only:
            active = np.where(rand > 0, inv_vol, np.nan)
            raw = np.nan_to_num(active, nan=0.0)
            s = raw.sum(axis=1)
            s = np.where(s == 0, np.nan, s)
            w = raw / s[:, None]
            w = np.nan_to_num(w, nan=0.0)
        else:
            raw = np.sign(rand) * inv_vol
            raw = np.nan_to_num(raw, nan=0.0)
            # The engine's long-short path zeroes any row containing a
            # NaN signal (NaN poisons the per-row normalization sum),
            # so replicate that row-level mask exactly.
            row_has_nan = np.isnan(rand).any(axis=1)
            raw[row_has_nan] = 0.0
            gross = np.abs(raw).sum(axis=1)
            g = np.where(gross == 0, np.nan, gross)
            w = raw / g[:, None]
            w = np.nan_to_num(w, nan=0.0)
        weights_list.append(
            pd.DataFrame(w, index=signal.index, columns=signal.columns)
        )
    return weights_list


def compute_falsification(
    signal: pd.DataFrame,
    close: pd.DataFrame,
    forward_window: int = 21,
) -> Dict:
    """FE1: within-sample predictive content of the multi-asset TSM signal.

    For each date t, Spearman(signal[t], next-``forward_window``-day
    return[t]) across the 16 ETFs. TSM requires high signal (strong
    past trend) to predict higher forward return.

    FE1 passes if mean |Spearman| >= 0.03 AND frac_positive >= 0.60.
    With 16 assets the Spearman statistic is non-degenerate (unlike
    the 2-asset crypto test in E028).

    Spearman is Pearson on mid-ranks (average ties), computed with
    pandas so the module has no scipy dependency.
    """
    def _spearman(x: np.ndarray, y: np.ndarray) -> float:
        rx = pd.Series(x).rank().to_numpy()
        ry = pd.Series(y).rank().to_numpy()
        if np.std(rx) == 0 or np.std(ry) == 0:
            return float("nan")
        return float(np.corrcoef(rx, ry)[0, 1])

    fwd_ret = close.shift(-forward_window) / close - 1.0

    rho_arr = np.full(signal.shape[0], np.nan)
    frac_pos_arr = np.full(signal.shape[0], np.nan)
    pearson_arr = np.full(signal.shape[0], np.nan)

    sig_vals = signal.to_numpy()
    fwd_vals = fwd_ret.to_numpy()
    for i in range(signal.shape[0]):
        m = ~(np.isnan(sig_vals[i]) | np.isnan(fwd_vals[i]))
        if m.sum() >= 3:
            rho = _spearman(sig_vals[i][m], fwd_vals[i][m])
            if np.isfinite(rho):
                rho_arr[i] = abs(rho)
                frac_pos_arr[i] = 1.0 if rho > 0 else 0.0
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

    return {
        "fe1_mean_abs_spearman": mean_abs,
        "fe1_frac_positive": frac_pos,
        "fe1_mean_abs_pearson": mean_abs_pearson,
        "fe1_mean_pearson": mean_pearson,
        "fe1_n_dates": int(len(rho_clean)),
        "fe1_n_assets": int(signal.shape[1]),
        "fe1_gate_mean_abs_ge_0_03": bool(mean_abs >= 0.03) if np.isfinite(mean_abs) else False,
        "fe1_gate_frac_pos_ge_0_60": bool(frac_pos >= 0.60) if np.isfinite(frac_pos) else False,
    }
