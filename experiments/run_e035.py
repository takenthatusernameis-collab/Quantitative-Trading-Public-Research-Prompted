#!/usr/bin/env python
"""E035: Liquidity anomaly (Amihud illiquidity) on the large_liquid universe.

Pre-registered design (see ledger entry E035):
  - Source: Amihud (2002) "Illiquidity and stock returns"; Pastor-Stambaugh
    (2003) illiquidity beta noted as an accounting-dependent variant that is
    out of scope given v1.2.4 fundamentals DATA-INFEASIBLE (E033).
  - Signal: Amihud illiq = mean_t( |r_t| / (P_t * V_t) ) over a trailing lookback,
    cross-sectionally winsorized; lagged SKIP=21 days (causal).
  - Construction PRIMARY: dollar-neutral long-short (long HIGH illiquidity / high
    illiquidity-risk premium), inverse-realized-vol weighted within each side,
    top & bottom quintile (top_frac=0.2), gross 1.0, monthly (21d) rebalance,
    close-to-close (primary v1.2.3 convention). tc=0.5bps + slippage=0.2bps.
  - Pre-registered FE1: mean |Spearman(signal[t], next-21d ret[t])| >= 0.03 AND
    >= 60% positive (expected sign is POSITIVE: high illiq -> high return).
  - Gates (promotion requires ALL):
      G1 OOS c2c Sharpe >= 0.8
      G2 rank-preserving placebo z >= 3.0 (preserve per-date value distribution,
          destroy signal->return link; recommended for cross-sectional sorts)
      G3 |beta vs SPY| <= 0.2
      G4 bear-market Sharpe > 0
      G5 turnover (daily) <= 0.15
  - Sensitivity (reported, not gated): lookback {126, 252}; top_frac {0.1, 0.2}.
  - Cost sweep (reported): {0, base 0.5+0.2bps, 10bps+5bps, 20bps+5bps}.
  - Conventions (v1.2.3): report c2c (primary, gated) AND overnight columns.
  - SEED=42. Walk-forward 504/63/63, 42 OOS folds.
"""

import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, strategies
from src.run_experiment import deterministic_timestamp

SEED = 42
np.random.seed(SEED)

UNIVERSE_NAME = "large_liquid"
DE_RISKED = False  # use full large_liquid per handoff
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
VOL_WINDOW = 63
LOOKBACK = 252
SKIP = 21
TC_COST = 0.0005
SLIPPAGE = 0.0002
N_PLACEBO = 50
TOP_FRAC = 0.2

close = None
open_ = None
volume = None
spy = None


def load_data():
    global close, open_, volume, spy
    from src.run_experiment import UNIVERSES
    universe = list(UNIVERSES[UNIVERSE_NAME])
    df = data.download(universe, start="2014-01-01", end="2026-10-12")
    close_df = data.get_panel(df, "Close").dropna(how="all")
    vol_df = data.get_panel(df, "Volume").reindex(close_df.index)
    open_df = data.get_panel(df, "Open").reindex(close_df.index)
    # Drop tickers with no usable volume history (e.g., delisted/renamed names).
    vol_days = vol_df.notna().sum(axis=0)
    keep = vol_days[vol_days >= 2000].index
    close_df = close_df[keep]
    vol_df = vol_df[keep]
    open_df = open_df[keep]
    bm = data.get_benchmark("SPY", start="2014-01-01", end="2026-10-12")
    spy_s = bm["close"].reindex(close_df.index).ffill()
    close, volume, open_, spy = close_df, vol_df, open_df, spy_s
    return close, open_, volume, spy


def make_signal():
    raw = strategies.amihud_iliquidity(close, volume, lookback=LOOKBACK, winsor=0.01)
    signal = raw.shift(SKIP)
    return signal


def fe1_check(signal):
    next_ret = close.pct_change(REBAL)
    spears = []
    for i in range(len(signal.index) - REBAL):
        s = signal.iloc[i]
        nr = next_ret.iloc[i + REBAL]
        common = s.dropna().index.intersection(nr.dropna().index)
        if len(common) >= 2:
            try:
                spears.append(s.loc[common].corr(nr.loc[common], method="spearman"))
            except Exception:
                pass
    spears = np.array(spears)
    return float(np.nanmean(np.abs(spears))), float(np.nanmean(spears > 0)), len(spears)


def exec_weights(signal, vol, rebalance=REBAL, top_frac=TOP_FRAC):
    w = backtest.carry_weights(signal, vol, top_frac=top_frac)
    w_exec = backtest.shift_weights(w)
    if rebalance > 1:
        w_exec = backtest._rebalance_weights(w_exec, rebalance)
    return w_exec


def wf_sharpe_by_returns(net_ret, spy_idx=None):
    """Mean OOS Sharpe over walk-forward folds for an already-aligned net return series."""
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    sharpes = []
    n_pos = 0
    for (tr_s, tr_e, te_s, te_e) in splits:
        test_idx = close.index[te_s:te_e]
        r = net_ret.loc[net_ret.index.intersection(test_idx)]
        m = backtest.metrics(r) if len(r) > 0 else {}
        s = m.get("sharpe", np.nan)
        sharpes.append(s)
        if not np.isnan(s) and s > 0:
            n_pos += 1
    vals = [s for s in sharpes if not np.isnan(s)]
    return float(np.mean(vals)) if vals else float("nan"), n_pos, len(sharpes)


def beta_vs_benchmark(net_ret, bench_s):
    bench = bench_s.pct_change().reindex(net_ret.index).ffill()
    y = net_ret.values
    x = bench.values
    mask = (~np.isnan(y)) & (~np.isnan(x))
    if mask.sum() < 3 or np.std(x[mask]) == 0:
        return float("nan"), float("nan"), float("nan")
    y2, x2 = y[mask], x[mask]
    A = np.vstack([np.ones(len(x2)), x2]).T
    alpha, beta = np.linalg.lstsq(A, y2, rcond=None)[0]
    corr = float(np.corrcoef(y2, x2)[0, 1])
    return float(beta), float(alpha * 252), corr


def bear_sharpe(net_ret):
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    out = []
    for (tr_s, tr_e, te_s, te_e) in splits:
        test_idx = close.index[te_s:te_e]
        spy_win = spy.reindex(test_idx).pct_change().dropna()
        if len(spy_win) == 0:
            regime = "sideways"
        else:
            r = float(spy_win.sum())
            regime = "bull" if r > 0.02 else ("bear" if r < -0.02 else "sideways")
        rtest = net_ret.loc[net_ret.index.intersection(test_idx)]
        m = backtest.metrics(rtest) if len(rtest) > 0 else {"sharpe": np.nan}
        out.append((regime, m.get("sharpe", np.nan)))
    bear = [s for r, s in out if r == "bear" and not np.isnan(s)]
    return float(np.mean(bear)) if bear else float("nan"), len(bear)


def build_weights_and_returns(signal, vol, rebalance=REBAL, top_frac=TOP_FRAC,
                              tc_cost=TC_COST, slippage=SLIPPAGE):
    w_exec = exec_weights(signal, vol, rebalance=rebalance, top_frac=top_frac)
    asset_ret_c2c = close.pct_change()
    asset_ret_ovn = open_ / close.shift(1) - 1.0
    gross_c2c = (w_exec * asset_ret_c2c).sum(axis=1)
    gross_ovn = (w_exec * asset_ret_ovn).sum(axis=1)
    daily_turnover = w_exec.diff().abs().sum(axis=1)
    total_cost = tc_cost + slippage
    net_c2c = gross_c2c - daily_turnover * total_cost
    net_ovn = gross_ovn - daily_turnover * total_cost
    return {
        "w_exec": w_exec,
        "gross_c2c": gross_c2c,
        "net_c2c": net_c2c,
        "gross_overnight": gross_ovn,
        "net_overnight": net_ovn,
        "daily_turnover": daily_turnover,
    }


def cost_sweep(gross_c2c, daily_turnover):
    levels = [
        ("0bps", 0.0, 0.0),
        ("base_0.5bps+0.2bps", 0.0005, 0.0002),
        ("10bps+5bps", 0.0010, 0.0005),
        ("20bps+5bps", 0.0020, 0.0005),
    ]
    out = {}
    for name, tc, slip in levels:
        net = gross_c2c - daily_turnover * (tc + slip)
        sharpe, npos, nfolds = wf_sharpe_by_returns(net)
        out[name] = {"total_cost_bps": (tc + slip) * 1e4, "oos_sharpe": sharpe,
                     "n_pos_folds": npos, "n_folds": nfolds}
    return out


def rank_preserving_placebo(signal, vol, n_sim=N_PLACEBO, seed=SEED):
    """Null: preserve per-date signal value distribution, destroy signal->return link.

    For each date the sorted signal values are reassigned to a random permutation of
    the assets. This preserves the per-date rank/magnitude distribution (and hence the
    number of long/short positions and the volatility budget that depends only on
    prices) while shuffling which asset receives which signal value, so any
    signal->return relationship is destroyed. Appropriate for cross-sectional
    rank/volume sorts (a pure i.i.d. null is too lenient here, as E030 showed for
    rank-signals).
    """
    rng = np.random.default_rng(seed)
    S = signal.to_numpy(dtype=np.float32)
    n_dates, n_assets = S.shape
    finite = np.isfinite(S)
    # sorted ascending values per row (NaNs ignored by take_along_axis ordering)
    order = np.argsort(np.where(finite, S, np.inf), axis=1, kind="stable")
    sorted_vals = np.take_along_axis(S, order, axis=1)
    sharps = []
    for _ in range(n_sim):
        rand = rng.random((n_dates, n_assets))
        perm = np.argsort(rand, axis=1)
        perm_vals = np.take_along_axis(sorted_vals, perm, axis=1)
        sig_perm = pd.DataFrame(perm_vals.astype(float), index=signal.index, columns=signal.columns)
        w_exec = exec_weights(sig_perm, vol)
        asset_ret_c2c = close.pct_change()
        gross = (w_exec * asset_ret_c2c).sum(axis=1)
        dt = w_exec.diff().abs().sum(axis=1)
        net = gross - dt * (TC_COST + SLIPPAGE)
        m = backtest.metrics(net)
        sharps.append(m.get("sharpe", 0.0))
    return {
        "n_sim": n_sim,
        "mean_sharpe": float(np.mean(sharps)),
        "std_sharpe": float(np.std(sharps)),
        "pct_positive": float(np.mean(np.array(sharps) > 0)),
    }


def sensitivity_grid(vol):
    grid = []
    for lb in (126, 252):
        for tf in (0.1, 0.2):
            sig = strategies.amihud_iliquidity(close, volume, lookback=lb, winsor=0.01).shift(SKIP)
            res = build_weights_and_returns(sig, vol, rebalance=REBAL, top_frac=tf)
            sharpe, npos, nfolds = wf_sharpe_by_returns(res["net_c2c"])
            b, a, c = beta_vs_benchmark(res["net_c2c"], spy)
            turn = float(res["daily_turnover"].mean())
            grid.append({
                "lookback": lb, "top_frac": tf,
                "oos_sharpe": sharpe, "n_pos_folds": npos, "n_folds": nfolds,
                "turnover_daily": turn, "beta_vs_spy": b,
            })
    return grid


def main():
    load_data()
    print(f"Loaded: close={close.shape}, vol tickers={volume.shape[1]}, SPY dates={len(spy)}")
    signal = make_signal()
    vol = close.pct_change().rolling(VOL_WINDOW).std()

    # FE1
    abs_s, frac_pos, n = fe1_check(signal)
    print(f"FE1: mean|Spearman|={abs_s:.4f}, frac_pos={frac_pos:.4f} (n={n})")

    # Primary weights + returns (c2c + overnight)
    res = build_weights_and_returns(signal, vol, rebalance=REBAL, top_frac=TOP_FRAC)
    net_c2c = res["net_c2c"]
    net_ovn = res["net_overnight"]
    daily_turnover = res["daily_turnover"]
    turnover_mean = float(daily_turnover.mean())

    # OOS (c2c primary) + per-fold sharpes
    fold_sharpes = []
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    for (tr_s, tr_e, te_s, te_e) in splits:
        test_idx = close.index[te_s:te_e]
        r = net_c2c.loc[net_c2c.index.intersection(test_idx)]
        m = backtest.metrics(r) if len(r) > 0 else {"sharpe": np.nan}
        fold_sharpes.append(m.get("sharpe", np.nan))
    flat = np.array([s for s in fold_sharpes if not np.isnan(s)], dtype=float)
    oos_sharpe = float(np.mean(flat)) if flat.size else float("nan")
    oos_std = float(np.std(flat)) if flat.size else float("nan")
    n_pos = int(np.sum(flat > 0))
    n_folds = len(fold_sharpes)
    print(f"OOS c2c Sharpe={oos_sharpe:.4f}, pos={n_pos}/{n_folds}, turnover={turnover_mean:.4f}")

    # Beta
    b, a, c = beta_vs_benchmark(net_c2c, spy)
    print(f"beta={b:.4f}, corr={c:.4f}")

    # Bear
    bear_mean, n_bear = bear_sharpe(net_c2c)
    print(f"bear folds={n_bear}, bear Sharpe={bear_mean:.4f}")

    # Overnight convention
    oos_ovn, n_pos_o, n_folds_o = wf_sharpe_by_returns(net_ovn)
    full_ovn = backtest.metrics(net_ovn)
    print(f"OOS overnight Sharpe={oos_ovn:.4f}, full overnight Sharpe={full_ovn.get('sharpe')}")

    # Placebo
    pl = rank_preserving_placebo(signal, vol)
    z = (oos_sharpe - pl["mean_sharpe"]) / pl["std_sharpe"] if pl["std_sharpe"] > 0 else float("nan")
    print(f"Placebo (rank-preserving, {N_PLACEBO}): mean={pl['mean_sharpe']:.4f}, std={pl['std_sharpe']:.4f}, z={z:.4f}")

    # Cost sweep
    sweep = cost_sweep(res["gross_c2c"], res["daily_turnover"])
    for k, v in sweep.items():
        print(f"cost {k}: oos_sharpe={v['oos_sharpe']:.4f}")

    # Sensitivity
    grid = sensitivity_grid(vol)
    for g in grid:
        print(f"sensitivity lb={g['lookback']} tf={g['top_frac']}: sharpe={g['oos_sharpe']:.4f} turn={g['turnover_daily']:.4f} beta={g['beta_vs_spy']:.4f}")

    # (fold_sharpes computed above in the OOS c2c section)
    out = {
        "experiment": "E035",
        "timestamp": deterministic_timestamp(),
        "universe": UNIVERSE_NAME,
        "n_assets": int(close.shape[1]),
        "assets": list(close.columns),
        "source": "Amihud (2002) Illiquidity and stock returns; Pastor-Stambaugh (2003) noted as accounting-dependent alternative",
        "signal_spec": {
            "measure": "amihud_iliquidity = mean_t(|r_t|/(P_t*V_t)) over trailing LOOKBACK",
            "lookback": LOOKBACK, "skip": SKIP, "winsor": 0.01,
            "price_basis": "yfinance auto_adjust=True adjusted close; volume raw share volume",
            "expected_sign": "positive (long high illiquidity premium)",
        },
        "construction": {
            "type": "dollar_neutral_longshort",
            "weighting": "inverse_realized_vol (63d), top/bottom quintile",
            "top_frac": TOP_FRAC,
            "gross_exposure_per_side": 0.5,
            "rebalance_freq": REBAL,
            "convention": "close_to_close (primary v1.2.3)",
            "tc_cost": TC_COST, "slippage": SLIPPAGE,
        },
        "fe1": {
            "mean_abs_spearman": abs_s,
            "frac_positive": frac_pos,
            "n_dates": n,
            "fe1_gate_mean_abs_ge_0_03": bool(abs_s >= 0.03),
            "fe1_gate_frac_pos_ge_0_60": bool(frac_pos >= 0.60),
        },
        "oos": {
            "mean_sharpe": oos_sharpe,
            "std_sharpe": oos_std,
            "n_pos_folds": n_pos,
            "n_folds": n_folds,
        },
        "folds": [{"fold": i, "sharpe": (None if np.isnan(s) else float(s))} for i, s in enumerate(fold_sharpes)],
        "beta": {"beta_vs_spy": float(b), "alpha_annual": float(a), "corr_spy": float(c)},
        "placebo_rank_preserving": pl,
        "placebo_z": z,
        "turnover_daily": turnover_mean,
        "bear": {"n_bear_folds": n_bear, "bear_sharpe_mean": float(bear_mean)},
        "conventions": {
            "c2c_oos_sharpe": oos_sharpe,
            "overnight_oos_sharpe": oos_ovn,
            "overnight_full_sharpe": full_ovn.get("sharpe"),
        },
        "cost_sweep": sweep,
        "sensitivity": grid,
        "gates": {
            "G1_oos_sharpe_ge_0.8": {"value": oos_sharpe, "threshold": 0.8, "pass": bool(oos_sharpe >= 0.8)},
            "G2_placebo_z_ge_3.0": {"value": (None if np.isnan(z) else z), "threshold": 3.0,
                                    "pass": bool((not np.isnan(z)) and z >= 3.0)},
            "G3_abs_beta_le_0.2": {"value": (None if np.isnan(b) else abs(b)), "threshold": 0.2,
                                   "pass": bool((not np.isnan(b)) and abs(b) <= 0.2)},
            "G4_bear_sharpe_gt_0": {"value": (None if np.isnan(bear_mean) else bear_mean), "threshold": 0.0,
                                    "pass": bool((not np.isnan(bear_mean)) and bear_mean > 0)},
            "G5_turnover_le_0.15": {"value": turnover_mean, "threshold": 0.15, "pass": bool(turnover_mean <= 0.15)},
        },
    }
    path = os.path.join("experiments", "e035_illiquidity.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"saved {path}")
    for k, v in out["gates"].items():
        print(f"{k}: pass={v['pass']} (val={v['value']})")


if __name__ == "__main__":
    main()
