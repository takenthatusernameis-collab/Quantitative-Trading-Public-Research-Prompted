"""E039: Extended Macro-Momentum with Additional FRED Themes.

Directional variant of Brooks (2017) "A Half-Century of Macro Momentum"
(AQR white paper, 2017-08-10), extended per the E038 feasibility screen
with additional FRED themes (labor market, yield curve, credit spreads,
financial conditions, commodity prices, consumption, housing).

US-only, ETF-tradable implementation on the repository's existing
sleeve:
- N FRED macro themes (see src/macro.py THEMES), 6m momentum, trailing
  60m z-score, release-lagged (at month-end M, data through M-1).
- 3 asset classes (equity=SPY, bonds=IEF, commodities=GLD) with
  structural signs per theme.
- Equal-weight across the 3*N theme-asset cells, gross exposure
  normalized to 1.0; monthly rebalance at month-end.

PRE-REGISTRATION (set before running; goalposts not moved after):

Primary configuration: 15 themes (5 core Brooks + 10 extended),
6m momentum, 60m z-window, 1m release lag, equal-weight cells,
gross=1, close-to-close primary (v1.2.3 convention policy).

Promotion gates (primary config, c2c, base costs):
  G1 OOS Sharpe (WF-mean) >= 0.8
  G2 block-permutation placebo z >= 3.0 (12m-block null, 50 sims)
  G3 |equity beta vs SPY| <= 0.4 (directional strategy)
  G4 bear-regime mean fold Sharpe > 0
  G5 turnover <= 0.15

Falsification expectations (prioritization v1.2.2):
  FE1 per-cell predictability: mean |Spearman(theme z, next-month
     asset return)| >= 0.03 AND >= 60% of cells have structural-sign-
     consistent Spearman sign. FALSIFIED if mean |rho| <= 0.02.
  FE2 convention robustness: report c2c AND overnight OOS Sharpe for
     the primary config (v1.2.3 policy column).

Sensitivity (reported, NOT gated):
  - theme subsets: {5 core, 15 all}
  - z-score window: {36, 60} months
  - momentum lookback: {3, 6, 12} months
  - cost sweep: {0bps, base 0.5+0.2bps, 10+5bps, 20+5bps}
  - commodity proxy: GLD vs DBC

SEED=42; walk-forward 504/63/63 (42 OOS folds); tc=0.5bps+slippage=0.2bps.

Data integrity (v1.2.5): FRED current-vintage (revised) data; release lag
emulated by 1-reference-month lag; revision look-ahead is a residual
caveat recorded in the ledger. No roll-stitching artifacts (native FRED
series). Public fredgraph.csv endpoint requires no API key.
"""

import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, validation
from src import jsonio
from src import macro
from src.run_experiment import deterministic_timestamp

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

CORE_THEMES = ["growth", "trade", "policy", "sentiment", "inflation"]


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


def run_backtest(w, close, open_, spy_ret, tc=TC_COST, sl=SLIPPAGE,
                 convention="c2c"):
    if convention == "c2c":
        ret = backtest.portfolio_returns_close_to_close(w, close, tc, sl,
                                                        rebalance_freq=1)
    else:
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
    """Pre-registered v1.2.2 falsification test: per-cell predictability."""
    assets = list(macro.ASSET_ETF.keys())
    themes = list(signals.columns)
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
                np.sign(rho) == np.sign(macro.THEME_SIGNS[a].get(k, 0.0)))
            rows.append({
                "theme": k, "asset": a, "rho": float(rho), "p_value": float(p),
                "structural_sign": macro.THEME_SIGNS[a].get(k, 0.0),
                "sign_matches": bool(sign_ok),
            })
    rhos = [r["rho"] for r in rows if not np.isnan(r["rho"])]
    mean_abs = float(np.mean([abs(x) for x in rhos])) if rhos else float("nan")
    n_match = int(sum(r["sign_matches"] for r in rows))
    n_cells = len(rows)
    falsified = bool(not np.isnan(mean_abs) and mean_abs <= 0.02)
    return {
        "cells": rows, "mean_abs_rho": mean_abs,
        "n_sign_match": n_match, "n_cells": n_cells,
        "expectation": "mean |rho| >= 0.03 and >= 60% structural sign matches",
        "falsified_by_preregistered_rule": falsified,
    }


def build_weights(signals, close, themes):
    """Weights restricted to a subset of themes (equal-weight across cells)."""
    signs = {a: {k: macro.THEME_SIGNS[a].get(k, 0.0) for k in themes}
             for a in macro.ASSET_ETF}
    return macro.macro_momentum_weights(signals, close.index,
                                       theme_signs=signs)


def main():
    print("=" * 70)
    print("E039: Extended Macro-Momentum with Additional FRED Themes")
    print("=" * 70)

    close, open_, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    print(f"Loaded {len(close)} days, {len(close.columns)} ETFs "
          f"({close.index.min().date()}..{close.index.max().date()})")

    all_themes = list(macro.THEMES.keys())
    print(f"\nThemes ({len(all_themes)}): {all_themes}")

    print("\n[0] Building release-lagged theme signals "
          f"(lookback={LOOKBACK}m, z-window={ZSCORE_WINDOW}m, lag={RELEASE_LAG}m)...")
    signals = macro.theme_signals(window=LOOKBACK, zscore_window=ZSCORE_WINDOW)
    print(f"    monthly signals: {len(signals)} ({signals.index.min().date()}"
          f"..{signals.index.max().date()})")

    # --- [1] Pre-registered falsification diagnostic (FE1) ---
    print("\n[1] Pre-registered falsification diagnostic (FE1: per-cell predictability)...")
    fals = falsification_diagnostic(signals, close)
    print(f"    mean |rho|={fals['mean_abs_rho']:.4f}  sign matches="
          f"{fals['n_sign_match']}/{fals['n_cells']}  "
          f"falsified={fals['falsified_by_preregistered_rule']}")
    for c in fals["cells"]:
        print(f"      {c['theme']:22s} -> {c['asset']:11s} rho={c['rho']:+.4f} "
              f"(p={c['p_value']:.3f}) sign_ok={c['sign_matches']}")

    # --- [2] Primary run (15 themes, c2c) ---
    print("\n[2] Primary macro momentum portfolio (15 themes, gross=1)...")
    w = macro.macro_momentum_weights(signals, close.index)
    active_days = int((w.abs().sum(axis=1) > 1e-9).sum())
    print(f"    active days={active_days}/{len(w)}  gross range="
          f"{w.abs().sum(axis=1).min():.3f}-{w.abs().sum(axis=1).max():.3f}")
    prim_c2c = run_backtest(w, close, open_, spy_ret, convention="c2c")
    prim_on = run_backtest(w, close, open_, spy_ret, convention="overnight")
    print(f"    c2c:       OOS Sharpe={prim_c2c['oos']:.3f} (std {prim_c2c['oos_std']:.3f})  "
          f"turnover={prim_c2c['turnover']:.4f}  beta={prim_c2c['diag']['equity_beta']:.3f} "
          f"corr={prim_c2c['diag']['corr_spy']:.3f} maxDD={prim_c2c['dd']:.3f} "
          f"pos_folds={prim_c2c['n_pos']}/{len(prim_c2c['fm'])}")
    print(f"    overnight: OOS Sharpe={prim_on['oos']:.3f} (FE2 convention-robustness)")
    print(f"    c2c regime: " + ", ".join(
        f"{k}: n={v['n_folds']} sh={v['sharpe_mean']:.3f}"
        for k, v in prim_c2c["reg"].items()))

    # --- [3] Placebo: 12m-block permutation null (50 sims) ---
    print(f"\n[3] Placebo null ({PLACEBO_N} sims, 12m-block permutation)...")
    rng = np.random.default_rng(SEED)
    placebo_sharpes_c2c = []
    placebo_sharpes_on = []
    for i in range(PLACEBO_N):
        perm = macro.block_permute_signals(signals, block_months=12,
                                            seed=int(rng.integers(1e9)))
        pw = macro.macro_momentum_weights(perm, close.index)
        pr_c2c = backtest.portfolio_returns_close_to_close(
            pw, close, TC_COST, SLIPPAGE, rebalance_freq=1)
        pr_on = backtest.portfolio_returns_rebalance_clean(
            pw, close, open_, TC_COST, SLIPPAGE, rebalance_freq=1)
        placebo_sharpes_c2c.append(backtest.metrics(pr_c2c["net"]).get("sharpe", 0.0))
        placebo_sharpes_on.append(backtest.metrics(pr_on["net"]).get("sharpe", 0.0))
        if (i + 1) % 10 == 0:
            print(f"    ... {i + 1}/{PLACEBO_N} sims")
    pm_c2c = float(np.mean(placebo_sharpes_c2c))
    ps_c2c = float(np.std(placebo_sharpes_c2c))
    z_c2c = float((prim_c2c["oos"] - pm_c2c) / ps_c2c) if ps_c2c > 0 else float("nan")
    pm_on = float(np.mean(placebo_sharpes_on))
    ps_on = float(np.std(placebo_sharpes_on))
    z_on = float((prim_on["oos"] - pm_on) / ps_on) if ps_on > 0 else float("nan")
    print(f"    c2c:       placebo mean={pm_c2c:.3f} std={ps_c2c:.3f}  z={z_c2c:.2f}")
    print(f"    overnight: placebo mean={pm_on:.3f} std={ps_on:.3f}  z={z_on:.2f}")

    # --- [4] Cost sweep (primary, c2c) ---
    print("\n[4] Cost sweep (15 themes, c2c)...")
    cost_rows = []
    for tc, sl in [(0.0, 0.0), (TC_COST, SLIPPAGE), (0.0010, 0.0005),
                   (0.0020, 0.0050)]:
        r = run_backtest(w, close, open_, spy_ret, tc=tc, sl=sl, convention="c2c")
        cost_rows.append({"tc_cost": tc, "slippage": sl, "oos_sharpe": r["oos"],
                          "turnover": r["turnover"], "n_pos_folds": r["n_pos"],
                          "sharpe_std": r["oos_std"]})
        print(f"    tc={tc:.4f} sl={sl:.4f}: OOS={r['oos']:.3f}")

    # --- [5] Theme-subset sensitivity (5 core vs 15 all) ---
    print("\n[5] Theme-subset sensitivity (5 core vs 15 all)...")
    subset_rows = []
    for label, themes in [("5_core", CORE_THEMES), ("15_all", all_themes)]:
        w_sub = build_weights(signals, close, themes)
        r_sub = run_backtest(w_sub, close, open_, spy_ret, convention="c2c")
        subset_rows.append({"n_themes": len(themes), "themes": themes,
                            "oos_sharpe": r_sub["oos"],
                            "turnover": r_sub["turnover"],
                            "beta": r_sub["diag"]["equity_beta"],
                            "bear_sharpe": r_sub["reg"]["bear"]["sharpe_mean"]})
        print(f"    {label}: OOS={r_sub['oos']:.3f} "
              f"bear={r_sub['reg']['bear']['sharpe_mean']:.3f}")

    # --- [6] Z-score window sensitivity ---
    print("\n[6] Z-score window sensitivity (36m vs 60m)...")
    zrows = []
    for zw in [36, 60]:
        s_zw = macro.theme_signals(window=LOOKBACK, zscore_window=zw)
        w_zw = macro.macro_momentum_weights(s_zw, close.index)
        r_zw = run_backtest(w_zw, close, open_, spy_ret, convention="c2c")
        zrows.append({"zscore_window": zw, "oos_sharpe": r_zw["oos"],
                      "turnover": r_zw["turnover"],
                      "bear_sharpe": r_zw["reg"]["bear"]["sharpe_mean"]})
        print(f"    z-window {zw}m: OOS={r_zw['oos']:.3f}")

    # --- [7] Momentum lookback sensitivity ---
    print("\n[7] Momentum lookback sensitivity (3m/6m/12m)...")
    lrows = []
    for lb in [3, 6, 12]:
        s_lb = macro.theme_signals(window=lb, zscore_window=ZSCORE_WINDOW)
        w_lb = macro.macro_momentum_weights(s_lb, close.index)
        r_lb = run_backtest(w_lb, close, open_, spy_ret, convention="c2c")
        lrows.append({"lookback_months": lb, "oos_sharpe": r_lb["oos"],
                      "turnover": r_lb["turnover"],
                      "beta": r_lb["diag"]["equity_beta"],
                      "bear_sharpe": r_lb["reg"]["bear"]["sharpe_mean"]})
        print(f"    {lb}m: OOS={r_lb['oos']:.3f} "
              f"bear={r_lb['reg']['bear']['sharpe_mean']:.3f}")

    # --- [8] Per-theme decomposition ---
    print("\n[8] Per-theme decomposition...")
    theme_rows = []
    for k in all_themes:
        signs = {a: {k: macro.THEME_SIGNS[a].get(k, 0.0)}
                 for a in macro.ASSET_ETF}
        w_t = macro.macro_momentum_weights(signals, close.index,
                                          theme_signs=signs)
        r_t = run_backtest(w_t, close, open_, spy_ret, convention="c2c")
        theme_rows.append({"theme": k, "oos_sharpe": r_t["oos"],
                           "equity_beta": r_t["diag"]["equity_beta"],
                           "turnover": r_t["turnover"],
                           "bear_sharpe": r_t["reg"]["bear"]["sharpe_mean"]})
        print(f"    {k:22s}: OOS={r_t['oos']:+.3f} "
              f"beta={r_t['diag']['equity_beta']:+.3f} "
              f"bear={r_t['reg']['bear']['sharpe_mean']:+.3f}")

    # --- [9] Bear windows ---
    print("\n[9] Bear-market window analysis...")
    bear_rows = []
    for label, lo, hi in BEAR_WINDOWS:
        mask = (prim_c2c["ret"].index >= lo) & (prim_c2c["ret"].index <= hi)
        wret = prim_c2c["ret"].loc[mask, "net"]
        if len(wret) > 2:
            m = backtest.metrics(wret)
            bear_rows.append({"window": label, "sharpe": m.get("sharpe"),
                              "ann_return": m.get("annual_return"),
                              "max_dd": m.get("max_drawdown")})
            print(f"    {label}: Sharpe={m.get('sharpe', 0):.3f} "
                  f"AnnRet={m.get('annual_return', 0):.3f}")

    # --- [10] Commodity-proxy sensitivity (DBC vs GLD) ---
    print("\n[10] Commodity-proxy sensitivity (DBC vs GLD)...")
    df_dbc = data.download(["DBC"], start=START)
    close_dbc = data.get_panel(df_dbc, "Close").dropna(how="all")
    close2 = close.copy()
    close2["GLD"] = close_dbc["DBC"].reindex(close.index).ffill()
    open2 = open_.copy()
    open2["GLD"] = close2["GLD"]
    w2 = macro.macro_momentum_weights(signals, close2.index)
    r_dbc = run_backtest(w2, close2, open2, spy_ret, convention="c2c")
    print(f"    DBC proxy: OOS={r_dbc['oos']:.3f}")

    # --- [11] Theme-signal correlation matrix ---
    print("\n[11] Theme-signal correlation matrix...")
    corr_mat = signals.corr()
    high_pairs = []
    for i, c1 in enumerate(all_themes):
        for c2 in all_themes[i + 1:]:
            v = corr_mat.loc[c1, c2]
            if abs(v) > 0.5:
                high_pairs.append({"theme_a": c1, "theme_b": c2,
                                   "corr": float(v)})
    print(f"    |corr| > 0.5 pairs: {len(high_pairs)}")
    for p in high_pairs:
        print(f"      {p['theme_a']:22s} <-> {p['theme_b']:22s} "
              f"rho={p['corr']:+.3f}")

    # --- [12] Pre-registered gate evaluation ---
    print("\n[12] Pre-registered gate evaluation (15 themes, c2c)...")
    gates = {
        "G1 OOS Sharpe >= 0.8": prim_c2c["oos"] >= GATE_OOS,
        "G2 placebo z (c2c) >= 3.0": z_c2c >= GATE_Z,
        "G3 |beta| <= 0.4": abs(prim_c2c["diag"]["equity_beta"]) <= GATE_BETA,
        "G4 bear Sharpe > 0": prim_c2c["reg"]["bear"]["sharpe_mean"] > GATE_BEAR,
        "G5 turnover <= 0.15": prim_c2c["turnover"] <= GATE_TURNOVER,
    }
    n_pass = sum(gates.values())
    for k, v in gates.items():
        print(f"    [{'PASS' if v else 'FAIL'}] {k}")
    print(f"    {n_pass}/{len(gates)} gates passed")

    # --- [13] Save ---
    result = {
        "experiment": "E039",
        "timestamp": deterministic_timestamp(),
        "source": "Brooks, J. (2017) 'A Half-Century of Macro Momentum', "
                  "AQR Capital Management White Paper, 2017-08-10, "
                  "directional variant extended with 10 additional FRED "
                  "themes per the E038 feasibility screen.",
        "universe": "US ETFs (SPY/IEF/GLD) + FRED macro series",
        "macro_series": {k: v for k, v in macro.THEMES.items()},
        "specification": {
            "themes": all_themes,
            "assets": macro.ASSET_ETF,
            "theme_signs": macro.THEME_SIGNS,
            "lookback_months": LOOKBACK,
            "zscore_window_months": ZSCORE_WINDOW,
            "release_lag_months": RELEASE_LAG,
            "construction": "equal-weight across 3*N theme-asset cells, "
                            "gross exposure normalized to 1.0, monthly "
                            "month-end rebalance, close-to-close primary",
        },
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP,
                         "n_folds": len(prim_c2c["fm"])},
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
            "convention_robustness": {
                "c2c_oos_sharpe": prim_c2c["oos"],
                "overnight_oos_sharpe": prim_on["oos"],
                "c2c_placebo_mean": pm_c2c, "c2c_placebo_std": ps_c2c,
                "c2c_z": z_c2c,
                "overnight_placebo_mean": pm_on,
                "overnight_placebo_std": ps_on,
                "overnight_z": z_on,
            },
        },
        "strategy": {
            "oos_sharpe": prim_c2c["oos"],
            "oos_sharpe_std": prim_c2c["oos_std"],
            "turnover": prim_c2c["turnover"],
            "equity_beta": prim_c2c["diag"]["equity_beta"],
            "corr_spy": prim_c2c["diag"]["corr_spy"],
            "alpha_annual": prim_c2c["diag"]["alpha_annual"],
            "is_sharpe": prim_c2c["diag"]["is_sharpe"],
            "is_ann_return": prim_c2c["diag"]["is_ann_return"],
            "is_ann_vol": prim_c2c["diag"]["is_ann_vol"],
            "is_max_dd": prim_c2c["diag"]["is_max_dd"],
            "max_drawdown": prim_c2c["dd"],
            "time_underwater_days": prim_c2c["uw"],
            "active_days": active_days,
            "n_pos_folds": prim_c2c["n_pos"],
            "regime_analysis": prim_c2c["reg"],
            "acf_lag1": float(validation.autocorrelation_test(
                prim_c2c["ret"]["net"])["acf"][0]),
            "t_stat": float(validation.t_stat(
                prim_c2c["oos"], TEST * len(prim_c2c["fm"]))),
            "fold_metrics": prim_c2c["fm"],
        },
        "placebo": {"n_sim": PLACEBO_N,
                    "method": "12m-block permutation of monthly theme signals"},
        "placebo_c2c": {"mean_sharpe": pm_c2c, "std_sharpe": ps_c2c,
                        "z_score": z_c2c},
        "placebo_overnight": {"mean_sharpe": pm_on, "std_sharpe": ps_on,
                              "z_score": z_on},
        "cost_sensitivity": cost_rows,
        "theme_subset_sensitivity": subset_rows,
        "zscore_window_sensitivity": zrows,
        "lookback_sensitivity": lrows,
        "theme_decomposition": theme_rows,
        "bear_windows": bear_rows,
        "dbc_proxy": {"oos_sharpe": r_dbc["oos"]},
        "theme_signal_correlation": {
            "matrix": corr_mat.to_dict(),
            "high_corr_pairs": high_pairs,
        },
        "data_integrity": {
            "fred_endpoint": "public fredgraph.csv (no API key)",
            "vintage": "current FRED vintage (revised data; release lag "
                       "emulated by 1-reference-month lag; revision "
                       "look-ahead is a residual caveat)",
            "stitching": "none (native FRED series, no continuous-futures "
                         "roll artifacts)",
        },
    }

    out_path = os.path.join("experiments", "e039_extended_macro.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        jsonio.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
