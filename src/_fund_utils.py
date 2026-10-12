"""Helpers shared by the fundamental-factor module."""

import numpy as np
import pandas as pd


def winsorize_zscore(df: pd.DataFrame, lo: float = 0.01, hi: float = 0.99) -> pd.DataFrame:
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