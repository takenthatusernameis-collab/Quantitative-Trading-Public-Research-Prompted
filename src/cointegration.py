"""Cointegration-based statistical arbitrage (Engle-Granger, Johansen, Copula).

Engle-Granger two-step method:
1. OLS regression: log(P_a) = alpha + beta * log(P_b) + epsilon
2. ADF test on residuals epsilon; select pairs with most negative ADF statistic

Johansen method (trace test, r=1): alternative for robustness.

Copula method: Fit a Gaussian or t-copula to the joint distribution of
standardized log returns. The conditional expectation E[log(P_a) | log(P_b)]
defines the equilibrium spread. Pairs are selected by tail dependence (t-copula)
or by the strength of the linear correlation (Gaussian copula) which implies
mean-reversion in the conditional distribution.

Trading: z-score of spread s_t = log(P_a,t) - beta * log(P_b,t) - alpha
- Entry: |z| >= entry_z
- Exit: |z| <= exit_z
- Dollar-neutral per pair (0.5 long / 0.5 short leg)
- Inverse-vol weighted across active pairs

Performance note: pair formation is O(n_pairs^2 * T) per formation date. The
Engle-Granger ADF is implemented as a vectorized batched AR(1) coefficient
estimator with a Mackinnon p-value lookup (statsmodels.tsa.adfvalues.mackinnonp),
so all candidate pairs on a formation window are tested in a single numpy call
instead of one statsmodels.adfuller() call per pair (which was ~200x slower).
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
from statsmodels.tsa.adfvalues import mackinnonp
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from scipy.stats import norm, t
from scipy.optimize import minimize_scalar

from src import backtest


def _formation_dates(close: pd.DataFrame, formation_window: int, rebalance_freq: int) -> List[pd.Timestamp]:
    """Rebalance/formation dates: every rebalance_freq days starting at formation_window."""
    dates = close.index
    return list(dates[formation_window::rebalance_freq])


def _pair_key(a: str, b: str) -> Tuple[str, str]:
    """Canonical unordered pair key for state tracking."""
    return (a, b) if a <= b else (b, a)


def _batched_engle_granger(log_window: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Vectorized Engle-Granger two-step test over every ordered pair of columns.

    log_window: shape (T, n) of log prices on a single formation window.
    Returns arrays of shape (n, n) each:
      beta[i,j]   : hedge ratio from regressing column i on column j
      alpha[i,j]  : intercept
      adf_stat[i,j]: ADF t-statistic on the residuals (NaN where degenerate)
      adf_pval[i,j]: Mackinnon p-value
      half_life[i,j]: AR(1) half-life of residuals (NaN where not mean-reverting)

    The diagonal and (i,j) vs (j,i) are both computed (regress i on j and
    j on i); callers pick the orientation they need.
    """
    T, n = log_window.shape
    # demean each column for the constant-term regression
    x = log_window - log_window.mean(axis=0, keepdims=True)  # (T, n)
    # OLS of every column on every other column (with constant):
    #   resid_i_on_j = x_i - (cov(x_i, x_j)/var(x_j)) * x_j
    # Batched over j: for each regressor column j, project all columns onto it.
    xxt = (x * x).sum(axis=0)                 # (n,)  sum of squares per column
    xxy = x.T @ x                             # (n, n) cross moment sum_t x_t,a * x_t,b
    # beta[a, j] = sum_t x_a[t] x_j[t] / sum_t x_j[t]^2
    with np.errstate(divide="ignore", invalid="ignore"):
        beta = xxy / xxt.reshape(1, n)
    # residuals: r[t, a, j] = x[t,a] - beta[a,j]*x[t,j]; then transpose to (a,j,t)
    r_taj = x[:, :, None] - beta[None, :, :] * x[:, None, :]   # (T, n, n)
    r = np.transpose(r_taj, (1, 2, 0))  # (n, n, T)
    # AR(1) coefficient of residuals along the time axis
    r0 = r[:, :, :-1]
    r1 = r[:, :, 1:]
    num = (r0 * r1).sum(axis=2)
    den = (r0 * r0).sum(axis=2)
    with np.errstate(divide="ignore", invalid="ignore"):
        rho = num / den                          # (n, n)
    # ADF t-statistic: (rho - 1) / se(rho)
    # se(rho) = sqrt( var(r1 - rho*r0) / (sum(r0^2)^2) )  (OLS std error of rho)
    resid_ar = r1 - rho[:, :, None] * r0
    s2 = (resid_ar * resid_ar).sum(axis=2) / (T - 2)      # (n, n)
    with np.errstate(divide="ignore", invalid="ignore"):
        se = np.sqrt(s2 / (den * den))
        adf_stat = (rho - 1.0) / se
    # Mackinnon p-value (regression with constant, N=1 multivariate -> N=1 here)
    adf_pval = np.asarray([[mackinnonp(float(v), regression="c", N=1) for v in row] for row in adf_stat])
    # half-life: -log(2)/log(rho) for 0 < rho < 1
    with np.errstate(divide="ignore", invalid="ignore"):
        hl = -np.log(2.0) / np.log(rho)
    hl = np.where((rho > 0) & (rho < 1), hl, np.nan)
    # alpha: intercept = mean(y) - beta * mean(x)  (in original log-price space)
    mean_y = log_window.mean(axis=0)                       # (n,)
    alpha = mean_y[None, :] - beta * mean_y[:, None]       # (n, n)
    return beta, alpha, adf_stat, adf_pval, hl

def _engle_granger_test(log_pa: pd.Series, log_pb: pd.Series) -> Tuple[float, float, float, float, float]:
    """Engle-Granger two-step cointegration test (single pair, reference impl).

    Returns: (hedge_ratio, intercept, adf_stat, adf_pval, half_life)
    """
    from statsmodels.tsa.stattools import adfuller
    from statsmodels.regression.linear_model import OLS
    from statsmodels.tools.tools import add_constant

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
    aligned = pd.concat([log_pa, log_pb], axis=1, join="inner").dropna()
    if len(aligned) < 2:
        return np.nan, np.nan, np.nan

    result = coint_johansen(aligned.values, det_order=0, k_ar_diff=1)
    trace_stat = result.lr1[0]  # r=0 (no cointegration)
    trace_stat_1 = result.lr1[1]  # r=1 (at most 1 cointegrating vector)

    eigvec = result.evec[:, 0]
    hedge_ratio = eigvec[1] / eigvec[0] if eigvec[0] != 0 else np.nan

    return float(trace_stat), float(trace_stat_1), float(hedge_ratio)


def _copula_test(
    log_pa: pd.Series,
    log_pb: pd.Series,
    copula_type: str = "gaussian",
) -> Tuple[float, float, float, float, float]:
    """Copula-based cointegration test.

    Fits a copula to the joint distribution of standardized log returns.
    The conditional expectation E[log(P_a) | log(P_b)] gives the equilibrium
    relationship. Returns (hedge_ratio, intercept, copula_stat, half_life, tail_dep).

    For Gaussian copula: copula_stat = |rho| (correlation strength)
    For t-copula: copula_stat = tail_dependence (lambda_u = lambda_l)
    """
    aligned = pd.concat([log_pa, log_pb], axis=1, join="inner").dropna()
    if len(aligned) < 30:
        return np.nan, np.nan, np.nan, np.nan, np.nan

    # Compute log returns
    ret_a = aligned.iloc[:, 0].diff().dropna()
    ret_b = aligned.iloc[:, 1].diff().dropna()

    # Standardize to uniform marginals via empirical CDF (probability integral transform)
    n = len(ret_a)
    u = ret_a.rank(method="average").values / (n + 1)
    v = ret_b.rank(method="average").values / (n + 1)

    if copula_type == "gaussian":
        # Gaussian copula: fit correlation rho
        # MLE for Gaussian copula: rho = sin(pi/2 * spearman_rho)
        spearman_rho = 12 * np.mean(u * v) - 3
        spearman_rho = np.clip(spearman_rho, -0.999, 0.999)
        rho = np.sin(np.pi / 2 * spearman_rho)
        rho = np.clip(rho, -0.999, 0.999)

        # Conditional expectation: E[u | v] = Phi(rho * Phi^{-1}(v))
        # For hedge ratio, use linear regression slope on standardized returns
        std_a = ret_a.std()
        std_b = ret_b.std()
        if std_b > 0:
            hedge_ratio = rho * std_a / std_b
        else:
            hedge_ratio = np.nan

        intercept = ret_a.mean() - hedge_ratio * ret_b.mean() if np.isfinite(hedge_ratio) else np.nan

        # Tail dependence for Gaussian is 0; use |rho| as stat
        copula_stat = float(abs(rho))
        tail_dep = 0.0

        # Half-life from AR(1) on spread residuals
        spread = np.log(aligned.iloc[:, 0].values) - hedge_ratio * np.log(aligned.iloc[:, 1].values) - intercept
        if len(spread) > 1:
            theta = np.corrcoef(spread[:-1], spread[1:])[0, 1]
            if 0 < theta < 1:
                half_life = -np.log(2) / np.log(theta)
            else:
                half_life = np.nan
        else:
            half_life = np.nan

        return float(hedge_ratio), float(intercept), float(copula_stat), float(half_life), float(tail_dep)

    elif copula_type == "t":
        # t-copula: fit rho and degrees of freedom nu via MLE
        # Log-likelihood for t-copula
        def neg_log_lik(params):
            rho, nu = params
            if abs(rho) >= 0.999 or nu <= 2 or nu > 50:
                return 1e10
            # Transform to t-quantiles
            x = t.ppf(u, nu)
            y = t.ppf(v, nu)
            # Bivariate t density
            denom = 1 - rho**2
            if denom <= 0:
                return 1e10
            quad = (x**2 - 2*rho*x*y + y**2) / denom
            log_det = -0.5 * np.log(denom)
            log_c = (np.log(nu) - np.log(np.pi) +
                     np.math.lgamma((nu + 2)/2) - np.math.lgamma(nu/2))
            ll = np.sum(log_c + log_det - 0.5 * (nu + 2) * np.log(1 + quad / nu))
            return -ll

        # Initial guess: Gaussian rho, nu=5
        spearman_rho = 12 * np.mean(u * v) - 3
        spearman_rho = np.clip(spearman_rho, -0.999, 0.999)
        rho_init = np.sin(np.pi / 2 * spearman_rho)
        rho_init = np.clip(rho_init, -0.99, 0.99)

        try:
            res = minimize_scalar(
                lambda nu: neg_log_lik((rho_init, nu)),
                bounds=(2.1, 30),
                method="bounded"
            )
            nu_opt = res.x
            # Re-optimize rho given nu
            res2 = minimize_scalar(
                lambda rho: neg_log_lik((rho, nu_opt)),
                bounds=(-0.99, 0.99),
                method="bounded"
            )
            rho_opt = res2.x
        except Exception:
            rho_opt, nu_opt = rho_init, 5.0

        rho_opt = np.clip(rho_opt, -0.999, 0.999)
        nu_opt = max(2.1, nu_opt)

        # Tail dependence for t-copula: lambda = 2 * t_{nu+1}(-sqrt((nu+1)*(1-rho)/(1+rho)))
        if abs(rho_opt) < 1:
            arg = -np.sqrt((nu_opt + 1) * (1 - rho_opt) / (1 + rho_opt))
            tail_dep = 2 * t.cdf(arg, nu_opt + 1)
        else:
            tail_dep = 1.0

        # Hedge ratio from correlation
        std_a = ret_a.std()
        std_b = ret_b.std()
        if std_b > 0:
            hedge_ratio = rho_opt * std_a / std_b
        else:
            hedge_ratio = np.nan

        intercept = ret_a.mean() - hedge_ratio * ret_b.mean() if np.isfinite(hedge_ratio) else np.nan

        # Half-life
        spread = np.log(aligned.iloc[:, 0].values) - hedge_ratio * np.log(aligned.iloc[:, 1].values) - intercept
        if len(spread) > 1:
            theta = np.corrcoef(spread[:-1], spread[1:])[0, 1]
            if 0 < theta < 1:
                half_life = -np.log(2) / np.log(theta)
            else:
                half_life = np.nan
        else:
            half_life = np.nan

        # Stat is tail dependence (higher = stronger co-movement in tails)
        copula_stat = float(tail_dep)

        return float(hedge_ratio), float(intercept), float(copula_stat), float(half_life), float(tail_dep)

    else:
        return np.nan, np.nan, np.nan, np.nan, np.nan


def find_cointegrated_pairs(
    close: pd.DataFrame,
    formation_window: int = 252,
    max_pairs: int = 20,
    method: str = "engle_granger",
    adf_threshold: float = 0.05,
    min_half_life: int = 1,
    max_half_life: int = 252,
    copula_type: str = "gaussian",
) -> Dict[pd.Timestamp, List[Tuple[str, str, float, float, float, float]]]:
    """Find cointegrated pairs using Engle-Granger, Johansen, or Copula method.

    Returns dict mapping formation date -> list of
    (stock_a, stock_b, hedge_ratio, intercept, stat, half_life).

    For Engle-Granger: stat = ADF t-statistic (most negative = strongest mean-reversion)
    For Johansen: stat = trace statistic (largest = strongest cointegration)
    For Copula: stat = |rho| (Gaussian) or tail_dependence (t-copula) (largest = strongest)

    Walk-forward: at each rebalance date the formation window ends on that date
    and uses only data through it (no look-ahead into the trading period).
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
        arr = window_data.to_numpy(dtype=float)  # (T, n)
        n = len(tickers)
        results: List[Tuple[str, str, float, float, float, float]] = []

        if method == "engle_granger":
            beta, alpha, adf_stat, adf_pval, hl = _batched_engle_granger(arr)
            j_idx, k_idx = np.triu_indices(n, k=1)
            for j, k in zip(j_idx, k_idx):
                b = float(beta[k, j])     # regress col k on col j
                a = float(alpha[k, j])
                s = float(adf_stat[k, j])
                p = float(adf_pval[k, j])
                h = float(hl[k, j])
                if (not np.isnan(p) and p < adf_threshold and
                        not np.isnan(h) and min_half_life <= h <= max_half_life):
                    results.append((tickers[j], tickers[k], b, a, s, h))
            results.sort(key=lambda x: x[4])  # most negative ADF first
        elif method == "johansen":
            for j in range(n):
                for k in range(j + 1, n):
                    log_pa = window_data.iloc[:, j]
                    log_pb = window_data.iloc[:, k]
                    trace_0, trace_1, beta = _johansen_test(log_pa, log_pb)
                    if not np.isnan(beta):
                        results.append((tickers[j], tickers[k], beta, 0.0, trace_0, np.nan))
            results.sort(key=lambda x: -x[4])  # largest trace first
        elif method == "copula":
            for j in range(n):
                for k in range(j + 1, n):
                    log_pa = window_data.iloc[:, j]
                    log_pb = window_data.iloc[:, k]
                    beta, alpha, stat, half_life, tail_dep = _copula_test(log_pa, log_pb, copula_type)
                    if not np.isnan(beta) and not np.isnan(stat):
                        # Filter: require some minimum dependence (rho > 0.3 or tail_dep > 0.05)
                        if (copula_type == "gaussian" and stat < 0.3) or \
                           (copula_type == "t" and stat < 0.05):
                            continue
                        if not np.isnan(half_life) and (half_life < min_half_life or half_life > max_half_life):
                            continue
                        results.append((tickers[j], tickers[k], beta, alpha, stat, half_life))
            results.sort(key=lambda x: -x[4])  # largest stat first
        else:
            raise ValueError(f"Unknown method: {method}")

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
    formation_window: int = 252,
) -> pd.DataFrame:
    """Daily target weights for cointegration-based pairs trading.

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

    pos_cache: Dict[Tuple[str, str], pd.Series] = {}
    seen_pairs = set()
    for pairs in pairs_by_date.values():
        for a, b, beta, alpha, _, _ in pairs:
            k = _pair_key(a, b)
            if k not in seen_pairs:
                seen_pairs.add(k)
                z = _spread_zscore(close, k[0], k[1], beta, alpha, formation_window=formation_window)
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
    formation_window: int = 252,
    seed: int = 42,
) -> List[pd.DataFrame]:
    """Pair-level placebo: random pair matching within universe, identical stateful trading rule.

    Pairs are formed by randomly pairing tickers (no cointegration signal), but
    the identical stateful z-score entry/exit logic and inverse-vol weighting
    are applied. This isolates the cointegration pair-selection skill from the
    trading-rule skill.

    Returns a list of weight DataFrames, one per simulation.
    """
    rng = np.random.default_rng(seed)
    tickers = close.columns.tolist()
    n = len(tickers)
    dates = close.index
    placebo_weights: List[pd.DataFrame] = []

    form_dates = _formation_dates(close, formation_window, rebalance_freq)

    for _ in range(50):
        perm = rng.permutation(n)
        random_pairs: List[Tuple[str, str, float, float, float, float]] = []
        for i in range(0, min(n_pairs * 2, n), 2):
            if i + 1 < n:
                a, b = tickers[perm[i]], tickers[perm[i + 1]]
                random_pairs.append((a, b, 1.0, 0.0, 0.0, np.nan))

        pairs_by_date: Dict[pd.Timestamp, List[Tuple[str, str, float, float, float, float]]] = {
            fd: random_pairs for fd in form_dates
        }
        w = cointegration_weights(
            close, pairs_by_date,
            entry_z=entry_z, exit_z=exit_z,
            vol_window=vol_window, rebalance_freq=rebalance_freq,
            formation_window=formation_window,
        )
        placebo_weights.append(w)

    return placebo_weights
