"""E022: Macro momentum / trend following on public macro factors.

Directional variant of Brooks (2017) "A Half-Century of Macro
Momentum" (AQR white paper, 2017-08-10; the ledger's prior
"Brooks & Moskowitz 2022" citation was corrected under the
prioritization v1.2.1 premise-verification step).

US-only, ETF-tradable implementation:
- 5 FRED macro themes (growth=INDPRO, trade=EXUSEU,
  policy=FEDFUNDS, sentiment=UMCSENT, inflation=CPIAUCSL),
  6m momentum, trailing 60m z-score, release-lagged
  (at month-end M, data through M-1). Brooks (2017)'s
  business-cycle theme includes inflation; it is split
  here so the commodities sleeve is not collinear with
  equities (rising inflation: -equities, -bonds,
  +commodities).
- 3 asset classes (equity=SPY, bonds=IEF, commodities=GLD)
  with structural signs per theme.
- Equal-weight across the 15 theme-asset cells, gross
  exposure normalized to 1.0; monthly rebalance at
  month-end, next-day open execution.

Pre-registered gates (set before running, NOT moved after):
  - OOS Sharpe >= 0.8
  - placebo z >= 3.0 (12m-block permutation null, 50 sims)
  - |equity beta vs SPY| <= 0.4 (directional strategy; paper
    reports low correlation, not zero beta)
  - bear-regime mean fold Sharpe > 0
  - turnover <= 0.15

Pre-registered falsification expectation (prioritization v1.2.2):
  cheapest rejection test = per-cell predictability.
  Expect mean per-cell |Spearman(z, next-month asset return)|
  >= 0.03 with the structural sign in >= 8/15 cells.
  FALSIFIED if mean |rho| <= 0.02.
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.run_experiment import deterministic_timestamp
from src import data, backtest, macro, validation

TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
LOOKBACK = 6          # months (primary)
ZSCORE_WINDOW = 60    # months
RELEASE_LAG = 1       # months (conservative FRED release-lag emulation)
PLACEBO_N = 50
SEED = 42
START = "2014-01-01"

# Pre-registered gates
GATE_OOS = 0.8
GATE_Z = 3.0
GATE_BETA = 0.4
GATE_BEAR = 0.0
GATE_TURNOVER = 0.15

BEAR_WINDOWS = [("2020_covid", "2020-02-19", "2020-04-07"),
                ("2022_bear", "2022-01-03", "2022-06-16")]


def load_data():
    df = data.download(["SPY", "IEF", "GLD"], start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    spy = close["SPY"]
    return close, open_, spy


def market_diagnostics(ret, spy_ret):
    net = ret["net"].dropna()
    m = backtest.metrics(net)
    common = net.index.intersection(spy_ret.index)
    y = net.loc[common].values
    x = spy_ret.loc[common].values
    if len(y) > 2 and np.std(x) > 0:
        A = np.vstack([np.ones(len(x)), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        alpha, beta_coef = coef[0], coef[1]
        corr = float(np.corrcoef(y, x)[0, 1])
    else:
        alpha, beta_coef, corr = np.nan, np.nan, np.nan
    return {
        "is_sharpe": m.get("sharpe"),
        "is_ann_return": m.get("annual_return"),
        "is_ann_vol": m.get("annual_vol"),
        "is_max_dd": m.get("max_drawdown"),
        "equity_beta": float(beta_coef),
        "alpha_annual": float(alpha * 252),
        "corr_spy": corr,
    }


def compute_dd(ret):
    ret = ret.dropna()
    if len(ret) == 0:
        return 0.0, 0
    cum = (1.0 + ret).cumprod()
    roll = cum.cummax()
    dd = cum / roll - 1.0
    return float(dd.min()), int((dd < 0).sum())


def walk_forward(ret, close, spy_ret):
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    fold_metrics = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = ret.loc[ret.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(test_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else np.nan
        if spy_win_ret > 0.02:
            regime = "bull"
        elif spy_win_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"
        m["regime"] = regime
        m["spy_test_return"] = spy_win_ret
        fold_metrics.append(m)
    return fold_metrics


def regime_summary(fold_metrics):
    out = {}
    for regime in ["bull", "bear", "sideways"]:
        rows = [m for m in fold_metrics if m.get("regime") == regime]
        sharps = [m["sharpe"] for m in rows]
        out[regime] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sharps)) if sharps else float("nan"),
            "sharpe_pos": int(sum(1 for s in sharps if s > 0)) if sharps else 0,
            "ann_return_mean": float(np.mean([m["annual_return"] for m in rows])) if rows else float("nan"),
            "max_dd_mean": float(np.mean([m["max_drawdown"] for m in rows])) if rows else float("nan"),
        }
    return out


def run_backtest(w, close, open_, spy_ret, tc=TC_COST, sl=SLIPPAGE):
    ret = backtest.portfolio_returns_rebalance_clean(w, close, open_, tc, sl,
                                                    rebalance_freq=1)
    diag = market_diagnostics(ret, spy_ret)
    dd, uw = compute_dd(ret["net"])
    fm = walk_forward(ret, close, spy_ret)
    reg = regime_summary(fm)
    oos = float(np.mean([m["sharpe"] for m in fm]))
    oos_std = float(np.std([m["sharpe"] for m in fm]))
    turnover = backtest.average_turnover(w)
    n_pos = int(sum(1 for m in fm if m["sharpe"] > 0))
    return {
        "ret": ret, "diag": diag, "dd": dd, "uw": uw, "fm": fm, "reg": reg,
        "oos": oos, "oos_std": oos_std, "turnover": turnover, "n_pos": n_pos,
    }


def falsification_diagnostic(signals, close):
    """Pre-registered v1.2.2 falsification test: per-cell predictability.

    Spearman corr between theme z (month-end M) and the asset's
    next-month return (close M -> close M+1).
    """
    assets = list(macro.ASSET_ETF.keys())
    themes = list(macro.THEMES.keys())
    monthly_ret = close.resample("MS").last().pct_change().shift(-1)
    rows = []
    for k in themes:
        for a in assets:
            sig = signals[k]
            r = monthly_ret[macro.ASSET_ETF[a]]
            pair = pd.DataFrame({"s": sig, "r": r}).dropna()
            if len(pair) < 12 or pair["s"].std() == 0 or pair["r"].std() == 0:
                rho, p = np.nan, np.nan
            else:
                rho, p = spearmanr(pair["s"], pair["r"])
            sign_ok = (not np.isnan(rho)) and (
                np.sign(rho) == np.sign(macro.THEME_SIGNS[a][k]))
            rows.append({
                "theme": k, "asset": a, "rho": float(rho), "p_value": float(p),
                "structural_sign": macro.THEME_SIGNS[a][k],
                "sign_matches": bool(sign_ok),
            })
    mean_abs = float(np.mean([abs(r["rho"]) for r in rows]))
    n_match = int(sum(r["sign_matches"] for r in rows))
    n_cells = len(rows)
    falsified = bool(mean_abs <= 0.02)
    return {
        "cells": rows, "mean_abs_rho": mean_abs,
        "n_sign_match": n_match, "n_cells": n_cells,
        "expectation": "mean |rho| >= 0.03 and >= 8/15 sign matches",
        "falsified_by_preregistered_rule": falsified,
    }


def main():
    print("=" * 70)
    print("E022: Macro Momentum (Brooks 2017, directional variant)")
    print("=" * 70)

    close, open_, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    print(f"Loaded {len(close)} days, {len(close.columns)} ETFs "
          f"({close.index.min().date()}..{close.index.max().date()})")

    print("\n[0] Building release-lagged theme signals "
          f"(lookback={LOOKBACK}m, z-window={ZSCORE_WINDOW}m, lag={RELEASE_LAG}m)...")
    signals = macro.theme_signals(window=LOOKBACK, zscore_window=ZSCORE_WINDOW)
    sig_14 = signals.loc["2014-01-01":]
    print(f"    monthly signals: {len(signals)} ({signals.index.min().date()}"
          f"..{signals.index.max().date()}), 2014+: {len(sig_14)}")

    # --- Pre-registered falsification expectation (v1.2.2) ---
    print("\n[1] Pre-registered falsification diagnostic (per-cell predictability)...")
    fals = falsification_diagnostic(signals, close)
    print(f"    mean |rho|={fals['mean_abs_rho']:.4f}  sign matches="
          f"{fals['n_sign_match']}/{fals['n_cells']}  "
          f"falsified={fals['falsified_by_preregistered_rule']}")
    for c in fals["cells"]:
        print(f"      {c['theme']:9s} -> {c['asset']:11s} rho={c['rho']:+.4f} "
              f"(p={c['p_value']:.3f}) sign_ok={c['sign_matches']}")

    # --- 2. Primary run ---
    print("\n[2] Primary macro momentum portfolio (gross=1, monthly, next-open)...")
    w = macro.macro_momentum_weights(signals, close.index)
    active_days = int((w.abs().sum(axis=1) > 1e-9).sum())
    print(f"    active days={active_days}/{len(w)}  gross range="
          f"{w.abs().sum(axis=1).min():.3f}-{w.abs().sum(axis=1).max():.3f}")
    prim = run_backtest(w, close, open_, spy_ret)
    print(f"    OOS Sharpe={prim['oos']:.3f} (std {prim['oos_std']:.3f})  "
          f"turnover={prim['turnover']:.4f}  beta={prim['diag']['equity_beta']:.3f} "
          f"corr={prim['diag']['corr_spy']:.3f} maxDD={prim['dd']:.3f} "
          f"pos_folds={prim['n_pos']}/{len(prim['fm'])}")
    print(f"    regime: " + ", ".join(
        f"{k}: n={v['n_folds']} sh={v['sharpe_mean']:.3f}"
        for k, v in prim["reg"].items()))

    # --- 3. Placebo: 12m-block permutation null ---
    print(f"\n[3] Placebo null ({PLACEBO_N} sims, 12m-block permutation)...")
    rng = np.random.default_rng(SEED)
    placebo_sharpes = []
    for i in range(PLACEBO_N):
        perm = macro.block_permute_signals(signals, block_months=12,
                                            seed=int(rng.integers(1e9)))
        pw = macro.macro_momentum_weights(perm, close.index)
        pr = backtest.portfolio_returns_rebalance_clean(
            pw, close, open_, TC_COST, SLIPPAGE, rebalance_freq=1)
        placebo_sharpes.append(backtest.metrics(pr["net"]).get("sharpe", 0.0))
    pm = float(np.mean(placebo_sharpes))
    ps = float(np.std(placebo_sharpes))
    z_score = float((prim["oos"] - pm) / ps) if ps > 0 else float("nan")
    print(f"    placebo mean={pm:.3f} std={ps:.3f}  z={z_score:.2f}")

    # --- 4. Cost sweep ---
    print("\n[4] Cost sweep...")
    cost_rows = []
    for tc, sl in [(0.0, 0.0), (0.0005, 0.0002), (0.0010, 0.0005), (0.0020, 0.0050)]:
        r = run_backtest(w, close, open_, spy_ret, tc=tc, sl=sl)
        cost_rows.append({
            "tc_cost": tc, "slippage": sl, "oos_sharpe": r["oos"],
            "turnover": r["turnover"], "n_pos_folds": r["n_pos"],
            "sharpe_std": r["oos_std"],
        })
        print(f"    tc={tc:.4f} sl={sl:.4f}: OOS={r['oos']:.3f}")

    # --- 5. Lookback sensitivity ---
    print("\n[5] Momentum-lookback sensitivity (3m/6m/12m)...")
    sens_rows = []
    for lb in [3, 6, 12]:
        s_lb = macro.theme_signals(window=lb, zscore_window=ZSCORE_WINDOW)
        w_lb = macro.macro_momentum_weights(s_lb, close.index)
        r_lb = run_backtest(w_lb, close, open_, spy_ret)
        sens_rows.append({"lookback_months": lb, "oos_sharpe": r_lb["oos"],
                          "turnover": r_lb["turnover"],
                          "n_pos_folds": r_lb["n_pos"],
                          "bear_sharpe": r_lb["reg"]["bear"]["sharpe_mean"]})
        print(f"    {lb}m: OOS={r_lb['oos']:.3f} bear={r_lb['reg']['bear']['sharpe_mean']:.3f}")

    # --- 6. Per-theme and per-asset decomposition ---
    print("\n[6] Per-theme decomposition...")
    theme_rows = []
    for k in macro.THEMES.keys():
        signs = {a: {k: macro.THEME_SIGNS[a][k]} for a in macro.ASSET_ETF}
        w_t = macro.macro_momentum_weights(
            signals, close.index, theme_signs=signs)
        r_t = run_backtest(w_t, close, open_, spy_ret)
        theme_rows.append({"theme": k, "oos_sharpe": r_t["oos"],
                           "equity_beta": r_t["diag"]["equity_beta"],
                           "turnover": r_t["turnover"],
                           "bear_sharpe": r_t["reg"]["bear"]["sharpe_mean"]})
        print(f"    {k:9s}: OOS={r_t['oos']:+.3f} beta={r_t['diag']['equity_beta']:+.3f} "
              f"bear={r_t['reg']['bear']['sharpe_mean']:+.3f}")

    # --- 7. Bear windows ---
    print("\n[7] Bear-market window analysis...")
    bear_rows = []
    for label, lo, hi in BEAR_WINDOWS:
        mask = (prim["ret"].index >= lo) & (prim["ret"].index <= hi)
        wret = prim["ret"].loc[mask, "net"]
        if len(wret) > 2:
            m = backtest.metrics(wret)
            bear_rows.append({"window": label, "sharpe": m.get("sharpe"),
                              "ann_return": m.get("annual_return"),
                              "max_dd": m.get("max_drawdown")})
            print(f"    {label}: Sharpe={m.get('sharpe', 0):.3f} "
                  f"AnnRet={m.get('annual_return', 0):.3f}")

    # --- 8. Vol-target sensitivity (10% target, 3y trailing) ---
    print("\n[8] Vol-target sensitivity (10% target, trailing 3y)...")
    gross_ret = prim["ret"]["gross"]
    vol3y = (gross_ret.rolling(756).std() * np.sqrt(252)).shift(1)
    scale = (0.10 / vol3y.replace(0, np.nan)).clip(upper=5.0).fillna(0.0)
    w_vol = w.mul(scale, axis=0)
    r_vol = run_backtest(w_vol, close, open_, spy_ret)
    print(f"    vol-target: OOS={r_vol['oos']:.3f} turnover={r_vol['turnover']:.4f} "
          f"realized vol={r_vol['diag']['is_ann_vol']:.3f}")

    # --- 9. Commodity-proxy sensitivity (DBC instead of GLD) ---
    print("\n[9] Commodity-proxy sensitivity (DBC vs GLD)...")
    df_dbc = data.download(["DBC"], start=START)
    close_dbc = data.get_panel(df_dbc, "Close").dropna(how="all")
    close2 = close.copy()
    close2["GLD"] = close_dbc["DBC"].reindex(close.index).ffill()
    open2 = open_.copy()
    open2["GLD"] = close2["GLD"]
    w2 = macro.macro_momentum_weights(signals, close2.index)
    r_dbc = run_backtest(w2, close2, open2, spy_ret)
    print(f"    DBC proxy: OOS={r_dbc['oos']:.3f}")

    # --- 10. Gate evaluation ---
    print("\n[10] Pre-registered gate evaluation...")
    gates = {
        "OOS Sharpe >= 0.8": prim["oos"] >= GATE_OOS,
        "placebo z >= 3.0": z_score >= GATE_Z,
        "|beta| <= 0.4": abs(prim["diag"]["equity_beta"]) <= GATE_BETA,
        "bear Sharpe > 0": prim["reg"]["bear"]["sharpe_mean"] > GATE_BEAR,
        "turnover <= 0.15": prim["turnover"] <= GATE_TURNOVER,
    }
    n_pass = sum(gates.values())
    for k, v in gates.items():
        print(f"    [{'PASS' if v else 'FAIL'}] {k}")
    print(f"    {n_pass}/{len(gates)} gates passed")

    # --- 11. Save ---
    result = {
        "experiment": "E022",
        "timestamp": deterministic_timestamp(),
        "source": "Brooks, J. (2017) \"A Half-Century of Macro Momentum\", "
                  "AQR Capital Management White Paper, 2017-08-10. "
                  "Directional variant. (Prior ledger citation "
                  "'Brooks & Moskowitz 2022' corrected under v1.2.1 "
                  "premise verification.)",
        "universe": "US ETFs (SPY/IEF/GLD) + FRED macro series",
        "macro_series": {k: v for k, v in macro.THEMES.items()},
        "specification": {
            "themes": list(macro.THEMES.keys()),
            "assets": macro.ASSET_ETF,
            "theme_signs": macro.THEME_SIGNS,
            "lookback_months": LOOKBACK,
            "zscore_window_months": ZSCORE_WINDOW,
            "release_lag_months": RELEASE_LAG,
        "construction": "equal-weight across 15 theme-asset cells, "
                        "gross exposure normalized to 1.0, monthly "
                        "month-end rebalance, next-day-open execution",
            "omitted_sleeves": "FX and 3m-rate asset classes omitted "
                               "(no ETF proxy); long-short within-asset-class "
                               "variant omitted (single market per class)",
        },
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP,
                         "n_folds": len(prim["fm"])},
        "pre_registered": {
            "gates": {
                "oos_sharpe": GATE_OOS, "placebo_z": GATE_Z,
                "equity_beta_abs": GATE_BETA, "bear_sharpe": GATE_BEAR,
                "turnover": GATE_TURNOVER,
            },
            "gate_results": gates,
            "n_gates_passed": n_pass,
            "promoted": bool(n_pass == len(gates)),
            "falsification_expectation": fals["expectation"],
            "falsification_result": fals,
        },
        "strategy": {
            "oos_sharpe": prim["oos"],
            "oos_sharpe_std": prim["oos_std"],
            "turnover": prim["turnover"],
            "equity_beta": prim["diag"]["equity_beta"],
            "corr_spy": prim["diag"]["corr_spy"],
            "alpha_annual": prim["diag"]["alpha_annual"],
            "is_sharpe": prim["diag"]["is_sharpe"],
            "is_ann_return": prim["diag"]["is_ann_return"],
            "is_ann_vol": prim["diag"]["is_ann_vol"],
            "is_max_dd": prim["diag"]["is_max_dd"],
            "max_drawdown": prim["dd"],
            "time_underwater_days": prim["uw"],
            "active_days": active_days,
            "n_pos_folds": prim["n_pos"],
            "regime_analysis": prim["reg"],
            "acf_lag1": float(validation.autocorrelation_test(prim["ret"]["net"])["acf"][0]),
            "t_stat": float(validation.t_stat(prim["oos"], TEST * len(prim["fm"]))),
            "fold_metrics": prim["fm"],
        },
        "placebo": {"n_sim": PLACEBO_N, "mean_sharpe": pm,
                    "std_sharpe": ps, "z_score": z_score,
                    "method": "12m-block permutation of monthly theme signals"},
        "cost_sensitivity": cost_rows,
        "lookback_sensitivity": sens_rows,
        "theme_decomposition": theme_rows,
        "bear_windows": bear_rows,
        "vol_target_10pct": {
            "oos_sharpe": r_vol["oos"], "turnover": r_vol["turnover"],
            "ann_vol": r_vol["diag"]["is_ann_vol"],
        },
        "dbc_proxy": {"oos_sharpe": r_dbc["oos"]},
        "data_integrity": {
            "fred_endpoint": "public fredgraph.csv (no API key)",
            "vintage": "current FRED vintage (revised data; release lag "
                       "emulated by 1-reference-month lag; revision "
                       "look-ahead is a residual caveat)",
            "stitching": "none (native FRED series, no continuous-futures "
                         "roll artifacts)",
        },
    }

    out_path = os.path.join("experiments", "e022_macro_momentum.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
