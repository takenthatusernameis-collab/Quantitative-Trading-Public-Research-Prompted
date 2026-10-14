"""E023: Economic Trend blend — macro momentum + price trend-following.

Tests the central claim of Brooks, Feilbogen, Ooi & Akant (2024),
"Economic Trend" (SSRN 4710868; AQR white paper): economic trend
(directional macro momentum, Brooks 2017) and price trend-following
(equal-weighted 1m/3m/12m trailing returns) are complementary
(full-sample correlation ~0.3 at the asset level, ~0.4 for aggregate
composites), and a 50/50 equal-risk blend outperforms either approach
standalone with more robust drawdown protection.

US-only, ETF-tradable implementation on the repository's existing
sleeves:
- Sleeve A (economic trend): the E022 directional macro-momentum
  construction (src/macro.py): 5 FRED themes (growth=INDPRO,
  trade=EXUSEU, policy=FEDFUNDS, sentiment=UMCSENT,
  inflation=CPIAUCSL), 6m momentum, 60m trailing z-score,
  release-lagged 1 reference month, structural signs onto 3 asset
  classes (SPY/IEF/GLD), equal-weight across cells, gross=1,
  month-end rebalance.
- Sleeve B (price trend): src/trend.py — equal-weighted 1m/3m/12m
  trailing returns per asset, directional (long positive factor /
  short negative factor), inverse-vol (63d) risk budget, gross=1,
  month-end rebalance. Matches the paper's price-trend construction.
- Blend: w = a*w_macro + (1-a)*w_trend, a in {0.25, 0.50, 0.75};
  both sleeves are gross=1 so the blend is gross=1.

Execution convention (primary): close-to-close for BOTH sleeves
(src/backtest.py::portfolio_returns_close_to_close), so the two
sleeves are directly comparable and the E020 execution-mismatch
critique does not apply. The repository's legacy convention
(next-day-open / overnight-only returns, portfolio_returns_rebalance_
clean) is reported as a secondary column for comparability with
E022 — and doubles as a convention-robustness check on E022 itself.

PRE-REGISTRATION (set before running; goalposts not moved after):

Falsification expectations (prioritization v1.2.2):
  FE1 (correlation premise): inter-sleeve daily net-return
       correlation in [0.10, 0.60] (paper: ~0.3 asset-level,
       ~0.4 aggregate). FALSIFIED if outside the band.
  FE2 (trend-sleeve within-sample mechanism): mean per-asset
       |Spearman(trend factor, next-month return)| >= 0.03 with
       >= 2/3 positive sign matches. FALSIFIED if mean |rho| <= 0.02.

Promotion gates (primary: 50/50 blend, close-to-close, base costs):
  G1 complementarity: OOS Sharpe(blend) > max(OOS Sharpe of either
     sleeve) — the paper's central performance claim.
  G2 drawdown protection: full-period maxDD(blend) strictly better
     (less negative) than BOTH sleeves.
  G3 significance: matched-blend placebo z >= 3.0 (50 sims; both
     sleeves' signals block-permuted with independent seeds, blended
     at the same weight).
  G4 bear regime: mean bear-fold Sharpe(blend) > 0.
  G5 risk: |equity beta vs SPY| <= 0.4 and turnover <= 0.15.
  Promotion requires all five gates.

Documented implementation gaps vs the paper (recorded, not hidden):
  - Universe: 3 US ETFs vs the paper's global multi-asset set
    (equity factors, bond futures, FX, commodities; 6 asset groups).
  - Macro sleeve: 6m momentum + 60m z-score (E022 construction)
    vs the paper's 1-year changes; risk-sentiment proxied by
    UMCSENT vs the paper's 1y equity excess returns; trade proxied
    by EXUSEU vs an FX-vs-export-basket.
  - Risk budget: gross=1 normalization vs the paper's 10% vol target
    (10% vol-target tested as a sensitivity).
  - Sample: 2014-2026 US-only vs 1970-2022 global.
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, validation
from src import macro, trend
from src.run_experiment import deterministic_timestamp

TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
MACRO_LOOKBACK = 6       # months (E022 primary)
ZSCORE_WINDOW = 60       # months
RELEASE_LAG = 1          # months
TREND_LOOKBACKS = (21, 63, 252)   # 1m/3m/12m (paper construction)
TREND_VOL_WINDOW = 63    # days
BLEND_WEIGHTS = (0.25, 0.50, 0.75)   # macro weight; 0.50 primary
PLACEBO_N = 50
SEED = 42
START = "2014-01-01"

# Pre-registered gates (primary blend = 0.50 macro weight)
PRIMARY_BLEND = 0.50
GATE_Z = 3.0
GATE_BETA = 0.4
GATE_TURNOVER = 0.15
GATE_BEAR = 0.0

BEAR_WINDOWS = [("2020_covid", "2020-02-19", "2020-04-07"),
                ("2022_bear", "2022-01-03", "2022-06-16")]


def load_data():
    df = data.download(["SPY", "IEF", "GLD"], start=START)
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    return close, open_


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


def run_c2c(w, close, spy_ret, tc=TC_COST, sl=SLIPPAGE):
    """Primary engine: close-to-close execution for both sleeves."""
    ret = backtest.portfolio_returns_close_to_close(w, close, tc, sl,
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


def run_overnight(w, close, open_, spy_ret, tc=TC_COST, sl=SLIPPAGE):
    """Secondary engine: repository legacy next-day-open convention
    (overnight close->next-open returns), for E022 comparability."""
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


def window_return(ret, lo, hi):
    mask = (ret.index >= lo) & (ret.index <= hi)
    wret = ret.loc[mask, "net"]
    if len(wret) > 2:
        m = backtest.metrics(wret)
        return {"sharpe": m.get("sharpe"),
                "ann_return": m.get("annual_return"),
                "max_dd": m.get("max_drawdown")}
    return {"sharpe": np.nan, "ann_return": np.nan, "max_dd": np.nan}


def trend_predictability(close, lookbacks=TREND_LOOKBACKS):
    """FE2: per-asset Spearman(trend factor, next-month return)."""
    factor = trend.price_trend_signal(close, lookbacks=lookbacks)
    me = close.index.to_series().groupby(close.index.to_period("M")).last()
    me_idx = pd.DatetimeIndex(me.values)
    # next-month close-to-close return, indexed at month-ends
    monthly_ret = close.loc[me_idx].pct_change().shift(-1)
    rows = []
    for col in factor.columns:
        f = factor[col].reindex(me_idx)
        r = monthly_ret[col]
        pair = pd.DataFrame({"f": f, "r": r}).dropna()
        if len(pair) < 12 or pair["f"].std() == 0 or pair["r"].std() == 0:
            rho = np.nan
        else:
            rho, _ = spearmanr(pair["f"], pair["r"])
        rows.append({"asset": col, "rho": float(rho),
                     "n_months": int(len(pair))})
    mean_abs = float(np.mean([abs(r["rho"]) for r in rows
                              if not np.isnan(r["rho"])]))
    n_pos = int(sum(1 for r in rows if r["rho"] > 0))
    return {
        "assets": rows, "mean_abs_rho": mean_abs,
        "n_positive_sign": n_pos, "n_assets": len(rows),
        "expectation": "mean |rho| >= 0.03 and >= 2/3 positive signs",
        "falsified_by_preregistered_rule": bool(mean_abs <= 0.02),
    }


def vol_target_scale(ret_gross, target=0.10, window=756):
    """Trailing-3y vol scaling to a 10% vol target (paper's budget)."""
    vol = (ret_gross.rolling(window).std() * np.sqrt(252)).shift(1)
    return (target / vol.replace(0, np.nan)).clip(upper=5.0).fillna(0.0)


def main():
    print("=" * 70)
    print("E023: Economic Trend Blend (Brooks, Feilbogen, Ooi & Akant 2024)")
    print("=" * 70)

    close, open_ = load_data()
    spy_ret = close["SPY"].pct_change().fillna(0.0)
    print(f"Loaded {len(close)} days ({close.index.min().date()}.."
          f"{close.index.max().date()})")

    # --- [0] Premise verification (prioritization v1.2.1) ---
    print("\n[0] Premise verification (v1.2.1)...")
    e022 = json.load(open(os.path.join("experiments",
                                       "e022_macro_momentum.json")))
    e022_oos = e022["strategy"]["oos_sharpe"]
    premise = {
        "e022_source_citation": "Brooks, J. (2017) 'A Half-Century of "
                                "Macro Momentum', AQR white paper "
                                "(verified; E022's prior 'Brooks & "
                                "Moskowitz 2022' citation was corrected "
                                "in E022)",
        "e023_source_citation": "Brooks, J., Feilbogen, N., Ooi, Y.H. & "
                                "Akant, A. (2024) 'Economic Trend', "
                                "SSRN 4710868 / AQR white paper "
                                "(verified against SSRN and AQR "
                                "publications page)",
        "paper_construction_verified": {
            "economic_trend": "directional macro momentum; 5 themes "
                              "(growth, inflation, international trade, "
                              "monetary policy, risk sentiment); one "
                              "signal per theme; per-asset vol scaling",
            "price_trend": "equal-weighted 1m/3m/12m trailing returns "
                           "per asset, directional",
            "blend": "equal risk-weighted 50/50",
            "correlation_claim": "~0.3 asset-level, ~0.4 aggregate",
            "vol_target": "10% constant volatility, trailing 3y "
                          "covariance",
        },
        "e022_recorded_oos_sharpe": e022_oos,
        "e022_recorded_placebo_z": e022["placebo"]["z_score"],
        "e022_recorded_bear_sharpe":
            e022["strategy"]["regime_analysis"]["bear"]["sharpe_mean"],
        "implementation_gaps_vs_paper": [
            "universe: 3 US ETFs (SPY/IEF/GLD) vs the paper's global "
            "multi-asset set (6 asset groups)",
            "macro sleeve: 6m momentum + 60m z-score (E022) vs the "
            "paper's 1-year changes",
            "risk-sentiment proxied by UMCSENT vs the paper's 1y equity "
            "excess returns; trade proxied by EXUSEU vs FX-vs-export-"
            "basket",
            "risk budget: gross=1 normalization vs the paper's 10% "
            "vol-target (tested as sensitivity)",
            "sample: 2014-2026 US-only vs 1970-2022 global",
        ],
    }
    print(f"    E022 recorded OOS Sharpe={e022_oos:.3f} "
          f"(premise verified against experiments/"
          f"e022_macro_momentum.json)")

    # --- [1] Falsification expectations (v1.2.2) ---
    print("\n[1] Pre-registered falsification diagnostics...")
    signals = macro.theme_signals(window=MACRO_LOOKBACK,
                                  zscore_window=ZSCORE_WINDOW)
    w_macro = macro.macro_momentum_weights(signals, close.index)
    w_trend = trend.price_trend_monthly_weights(close,
                                                lookbacks=TREND_LOOKBACKS,
                                                vol_window=TREND_VOL_WINDOW)

    res_macro = run_c2c(w_macro, close, spy_ret)
    res_trend = run_c2c(w_trend, close, spy_ret)
    fe1_corr = float(np.corrcoef(res_macro["ret"]["net"].fillna(0.0),
                                 res_trend["ret"]["net"].fillna(0.0))[0, 1])
    fe1 = {
        "inter_sleeve_return_corr": fe1_corr,
        "band": [0.10, 0.60],
        "expectation": "corr in [0.10, 0.60] (paper: ~0.3 asset, "
                       "~0.4 aggregate)",
        "passed": bool(0.10 <= fe1_corr <= 0.60),
    }
    fe2 = trend_predictability(close)
    # per-asset weight correlation (asset-level analog)
    me = close.index.to_series().groupby(close.index.to_period("M")).last()
    me_idx = pd.DatetimeIndex(me.values)
    wm, wt = w_macro.loc[me_idx], w_trend.loc[me_idx]
    per_asset_wcorr = {c: float(np.corrcoef(wm[c], wt[c])[0, 1])
                       for c in wm.columns}
    fe1["per_asset_weight_corr"] = per_asset_wcorr
    fe1["per_asset_weight_corr_mean"] = float(np.mean(list(
        per_asset_wcorr.values())))
    print(f"    FE1 inter-sleeve corr={fe1_corr:.3f} "
          f"(per-asset weight corr: "
          f"{ {k: round(v,3) for k,v in per_asset_wcorr.items()} }) "
          f"passed={fe1['passed']}")
    print(f"    FE2 mean |rho|={fe2['mean_abs_rho']:.4f} "
          f"sign matches={fe2['n_positive_sign']}/{fe2['n_assets']} "
          f"falsified={fe2['falsified_by_preregistered_rule']}")

    # --- [2] Sleeve A: economic trend (macro momentum) ---
    print("\n[2] Sleeve A: economic trend (E022 macro momentum)...")
    res_macro_on = run_overnight(w_macro, close, open_, spy_ret)
    print(f"    close-to-close: OOS={res_macro['oos']:.3f} "
          f"maxDD={res_macro['dd']:.3f} beta={res_macro['diag']['equity_beta']:.3f} "
          f"turnover={res_macro['turnover']:.4f}")
    print(f"    repo overnight convention: OOS={res_macro_on['oos']:.3f} "
          f"(E022 recorded {e022_oos:.3f}; replication delta "
          f"{res_macro_on['oos'] - e022_oos:+.3f})")

    # --- [3] Sleeve B: price trend ---
    print("\n[3] Sleeve B: price trend (1m/3m/12m, directional, "
          "inv-vol)...")
    print(f"    close-to-close: OOS={res_trend['oos']:.3f} "
          f"maxDD={res_trend['dd']:.3f} "
          f"beta={res_trend['diag']['equity_beta']:.3f} "
          f"turnover={res_trend['turnover']:.4f}")

    # --- [4] Blend grid + matched placebos ---
    print(f"\n[4] Blend grid {BLEND_WEIGHTS} + matched placebos "
          f"({PLACEBO_N} sims, 12m-block permutation of both sleeves)...")
    placebo = {"macro": [], "trend": [],
               "blend": {a: [] for a in BLEND_WEIGHTS}}
    rng = np.random.default_rng(SEED)
    factor = trend.price_trend_signal(close, lookbacks=TREND_LOOKBACKS)
    for i in range(PLACEBO_N):
        s1 = int(rng.integers(1e9))
        s2 = int(rng.integers(1e9))
        perm_m = macro.block_permute_signals(signals, block_months=12,
                                             seed=s1)
        w_pm = macro.macro_momentum_weights(perm_m, close.index)
        perm_f = trend.block_permute_monthly_factor(factor, block_months=12,
                                                    seed=s2)
        w_pt = trend.price_trend_monthly_weights_from_signal(
            perm_f, close, vol_window=TREND_VOL_WINDOW)
        r_pm = run_c2c(w_pm, close, spy_ret)
        r_pt = run_c2c(w_pt, close, spy_ret)
        placebo["macro"].append(r_pm["oos"])
        placebo["trend"].append(r_pt["oos"])
        for a in BLEND_WEIGHTS:
            w_pb = a * w_pm + (1.0 - a) * w_pt
            placebo["blend"][a].append(run_c2c(w_pb, close, spy_ret)["oos"])
        if (i + 1) % 10 == 0:
            print(f"    ... {i + 1}/{PLACEBO_N} sims")

    pm_mean, pm_std = float(np.mean(placebo["macro"])), float(
        np.std(placebo["macro"]))
    pt_mean, pt_std = float(np.mean(placebo["trend"])), float(
        np.std(placebo["trend"]))
    z_macro = (res_macro["oos"] - pm_mean) / pm_std if pm_std > 0 else np.nan
    z_trend = (res_trend["oos"] - pt_mean) / pt_std if pt_std > 0 else np.nan
    print(f"    macro placebo: mean={pm_mean:.3f} std={pm_std:.3f} "
          f"z={z_macro:.2f}")
    print(f"    trend placebo: mean={pt_mean:.3f} std={pt_std:.3f} "
          f"z={z_trend:.2f}")

    blend_results = {}
    for a in BLEND_WEIGHTS:
        w_b = a * w_macro + (1.0 - a) * w_trend
        res_b = run_c2c(w_b, close, spy_ret)
        pb = placebo["blend"][a]
        pb_mean, pb_std = float(np.mean(pb)), float(np.std(pb))
        z_b = (res_b["oos"] - pb_mean) / pb_std if pb_std > 0 else np.nan
        blend_results[a] = {
            "res": res_b, "placebo_mean": pb_mean,
            "placebo_std": pb_std, "z": float(z_b),
        }
        print(f"    blend macro_w={a:.2f}: OOS={res_b['oos']:.3f} "
              f"z={z_b:.2f} maxDD={res_b['dd']:.3f} "
              f"beta={res_b['diag']['equity_beta']:.3f} "
              f"turnover={res_b['turnover']:.4f} "
              f"bear={res_b['reg']['bear']['sharpe_mean']:.3f}")

    # --- [5] Drawdown / regime analysis (paper's drawdown-protection claim) ---
    print("\n[5] Drawdown-protection analysis...")
    dd_analysis = {}
    for label, res in [("macro", res_macro), ("trend", res_trend)] + [
            (f"blend_{a:.2f}", blend_results[a]["res"]) for a in BLEND_WEIGHTS]:
        wins = {wlabel: window_return(res["ret"], lo, hi)
                for wlabel, lo, hi in BEAR_WINDOWS}
        dd_analysis[label] = {
            "max_dd": res["dd"], "time_underwater_days": res["uw"],
            "bear_regime_sharpe": res["reg"]["bear"]["sharpe_mean"],
            "bear_windows": wins,
        }
        print(f"    {label:10s}: maxDD={res['dd']:.3f} "
              f"bear-regime={res['reg']['bear']['sharpe_mean']:+.3f} "
              + " ".join(f"{k}={v['sharpe']:+.3f}" for k, v in wins.items()))

    # --- [6] Cost sweep (primary 50/50 blend) ---
    print("\n[6] Cost sweep (50/50 blend, close-to-close)...")
    w_primary = PRIMARY_BLEND * w_macro + (1.0 - PRIMARY_BLEND) * w_trend
    cost_rows = []
    for tc, sl in [(0.0, 0.0), (TC_COST, SLIPPAGE), (0.0010, 0.0005),
                   (0.0020, 0.0050)]:
        r = run_c2c(w_primary, close, spy_ret, tc=tc, sl=sl)
        cost_rows.append({"tc_cost": tc, "slippage": sl,
                          "oos_sharpe": r["oos"], "max_dd": r["dd"],
                          "turnover": r["turnover"]})
        print(f"    tc={tc:.4f} sl={sl:.4f}: OOS={r['oos']:.3f} "
              f"maxDD={r['dd']:.3f}")

    # --- [7] Sensitivities ---
    print("\n[7] Sensitivities...")
    # (a) price-trend lookback variants
    sens_trend = []
    for lbs in [(21,), (21, 63, 252), (63, 126, 252)]:
        w_t = trend.price_trend_monthly_weights(close, lookbacks=lbs,
                                                vol_window=TREND_VOL_WINDOW)
        r_t = run_c2c(w_t, close, spy_ret)
        r_b = run_c2c(PRIMARY_BLEND * w_macro + (1.0 - PRIMARY_BLEND) * w_t,
                      close, spy_ret)
        sens_trend.append({
            "lookbacks": list(lbs), "trend_oos": r_t["oos"],
            "trend_max_dd": r_t["dd"], "blend_oos": r_b["oos"],
            "blend_max_dd": r_b["dd"],
        })
        print(f"    trend lookbacks {lbs}: trend OOS={r_t['oos']:.3f} "
              f"blend OOS={r_b['oos']:.3f}")
    # (b) macro lookback variants
    sens_macro = []
    for lb in [3, 6, 12]:
        s_lb = macro.theme_signals(window=lb, zscore_window=ZSCORE_WINDOW)
        w_m = macro.macro_momentum_weights(s_lb, close.index)
        r_m = run_c2c(w_m, close, spy_ret)
        r_b = run_c2c(PRIMARY_BLEND * w_m + (1.0 - PRIMARY_BLEND) * w_trend,
                      close, spy_ret)
        sens_macro.append({
            "lookback_months": lb, "macro_oos": r_m["oos"],
            "macro_max_dd": r_m["dd"], "blend_oos": r_b["oos"],
            "blend_max_dd": r_b["dd"],
        })
        print(f"    macro lookback {lb}m: macro OOS={r_m['oos']:.3f} "
              f"blend OOS={r_b['oos']:.3f}")
    # (c) 10% vol-target blend (paper's risk budget)
    blend_gross = (PRIMARY_BLEND * res_macro["ret"]["gross"] +
                   (1.0 - PRIMARY_BLEND) * res_trend["ret"]["gross"])
    vol_scale = vol_target_scale(blend_gross)
    w_vol = w_primary.mul(vol_scale, axis=0)
    r_vol = run_c2c(w_vol, close, spy_ret)
    print(f"    10% vol-target blend: OOS={r_vol['oos']:.3f} "
          f"maxDD={r_vol['dd']:.3f} "
          f"realized vol={r_vol['diag']['is_ann_vol']:.3f}")

    # --- [8] Repo-convention comparability (E022 replication check) ---
    print("\n[8] Repository-convention comparability (secondary)...")
    res_trend_on = run_overnight(w_trend, close, open_, spy_ret)
    res_blend_on = run_overnight(w_primary, close, open_, spy_ret)
    conv = {
        "macro": {"c2c_oos": res_macro["oos"],
                  "overnight_oos": res_macro_on["oos"]},
        "trend": {"c2c_oos": res_trend["oos"],
                  "overnight_oos": res_trend_on["oos"]},
        "blend_0.50": {"c2c_oos": blend_results[PRIMARY_BLEND]["res"]["oos"],
                       "overnight_oos": res_blend_on["oos"]},
        "e022_replication_delta": res_macro_on["oos"] - e022_oos,
        "note": "The repository's legacy convention attributes overnight "
                "close->next-open returns only; the intraday open->close "
                "component is excluded. The macro sleeve's edge is "
                "overnight-concentrated on this sample.",
    }
    # intraday vs overnight decomposition of the macro sleeve
    w_s = backtest.shift_weights(w_macro)
    overnight_ret = (open_.shift(-1) / close - 1.0)
    intraday_ret = (close / open_ - 1.0)
    g_over = (w_s * overnight_ret).sum(axis=1).dropna()
    g_intra = (w_s * intraday_ret).sum(axis=1).dropna()
    conv["macro_decomposition"] = {
        "overnight_full_sharpe": backtest.metrics(g_over)["sharpe"],
        "intraday_full_sharpe": backtest.metrics(g_intra)["sharpe"],
    }
    print(f"    macro sleeve decomposition: overnight Sharpe="
          f"{conv['macro_decomposition']['overnight_full_sharpe']:.3f}, "
          f"intraday Sharpe="
          f"{conv['macro_decomposition']['intraday_full_sharpe']:.3f}")

    # --- [9] Pre-registered gate evaluation ---
    print("\n[9] Pre-registered gate evaluation (primary 50/50 blend, "
          "close-to-close)...")
    prim = blend_results[PRIMARY_BLEND]["res"]
    sleeve_max_oos = max(res_macro["oos"], res_trend["oos"])
    sleeve_best_dd = max(res_macro["dd"], res_trend["dd"])
    gates = {
        "G1 complementarity (blend OOS > max sleeve OOS)":
            prim["oos"] > sleeve_max_oos,
        "G2 drawdown protection (blend maxDD better than both sleeves)":
            prim["dd"] > sleeve_best_dd,
        "G3 matched-placebo z >= 3.0":
            blend_results[PRIMARY_BLEND]["z"] >= GATE_Z,
        "G4 bear-regime mean fold Sharpe > 0":
            prim["reg"]["bear"]["sharpe_mean"] > GATE_BEAR,
        "G5a |beta vs SPY| <= 0.4":
            abs(prim["diag"]["equity_beta"]) <= GATE_BETA,
        "G5b turnover <= 0.15": prim["turnover"] <= GATE_TURNOVER,
    }
    n_pass = sum(gates.values())
    for k, v in gates.items():
        print(f"    [{'PASS' if v else 'FAIL'}] {k}")
    print(f"    {n_pass}/{len(gates)} gates passed "
          f"(promotion requires all)")

    # --- [10] Save ---
    result = {
        "experiment": "E023",
        "timestamp": deterministic_timestamp(),
        "source": premise["e023_source_citation"],
        "prior_source": premise["e022_source_citation"],
        "central_claim": "Economic trend (directional macro momentum) and "
                         "price trend-following are complementary "
                         "(corr ~0.3 asset-level / ~0.4 aggregate); a 50/50 "
                         "equal-risk blend outperforms either standalone "
                         "with more robust drawdown protection.",
        "universe": "US ETFs (SPY/IEF/GLD) + FRED macro series",
        "specification": {
            "macro_sleeve": {
                "construction": "E022 directional macro momentum "
                                "(src/macro.py)",
                "themes": list(macro.THEMES.keys()),
                "assets": macro.ASSET_ETF,
                "lookback_months": MACRO_LOOKBACK,
                "zscore_window_months": ZSCORE_WINDOW,
                "release_lag_months": RELEASE_LAG,
            },
            "price_trend_sleeve": {
                "construction": "equal-weighted 1m/3m/12m trailing "
                                "returns, directional, inverse-vol (63d), "
                                "gross=1 (src/trend.py)",
                "lookbacks_days": list(TREND_LOOKBACKS),
                "vol_window_days": TREND_VOL_WINDOW,
            },
            "blend": "w = a*w_macro + (1-a)*w_trend; gross=1; month-end "
                     "rebalance",
            "primary_execution": "close-to-close (both sleeves)",
            "secondary_execution": "repository legacy next-day-open "
                                 "(overnight returns), for E022 "
                                 "comparability",
        },
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP,
                         "n_folds": len(res_macro["fm"])},
        "pre_registered": {
            "falsification_expectations": {
                "FE1_correlation_premise": fe1,
                "FE2_trend_predictability": fe2,
            },
            "gates": gates,
            "n_gates_passed": n_pass,
            "promoted": bool(n_pass == len(gates)),
            "gate_thresholds": {
                "placebo_z": GATE_Z, "equity_beta_abs": GATE_BETA,
                "turnover": GATE_TURNOVER, "bear_sharpe": GATE_BEAR,
            },
        },
        "premise_verification": premise,
        "sleeves": {
            "macro_economic_trend": {
                "oos_sharpe": res_macro["oos"],
                "oos_sharpe_std": res_macro["oos_std"],
                "turnover": res_macro["turnover"],
                "equity_beta": res_macro["diag"]["equity_beta"],
                "corr_spy": res_macro["diag"]["corr_spy"],
                "max_drawdown": res_macro["dd"],
                "n_pos_folds": res_macro["n_pos"],
                "regime_analysis": res_macro["reg"],
                "placebo": {"mean_sharpe": pm_mean, "std_sharpe": pm_std,
                            "z_score": float(z_macro)},
                "overnight_convention_oos": res_macro_on["oos"],
            },
            "price_trend": {
                "oos_sharpe": res_trend["oos"],
                "oos_sharpe_std": res_trend["oos_std"],
                "turnover": res_trend["turnover"],
                "equity_beta": res_trend["diag"]["equity_beta"],
                "corr_spy": res_trend["diag"]["corr_spy"],
                "max_drawdown": res_trend["dd"],
                "n_pos_folds": res_trend["n_pos"],
                "regime_analysis": res_trend["reg"],
                "placebo": {"mean_sharpe": pt_mean, "std_sharpe": pt_std,
                            "z_score": float(z_trend)},
                "overnight_convention_oos": res_trend_on["oos"],
            },
        },
        "complementarity": {
            "inter_sleeve_return_corr": fe1_corr,
            "per_asset_weight_corr": per_asset_wcorr,
            "per_asset_weight_corr_mean": fe1["per_asset_weight_corr_mean"],
        },
        "blend_grid": {
            f"macro_weight_{a:.2f}": {
                "oos_sharpe": blend_results[a]["res"]["oos"],
                "oos_sharpe_std": blend_results[a]["res"]["oos_std"],
                "placebo_mean": blend_results[a]["placebo_mean"],
                "placebo_std": blend_results[a]["placebo_std"],
                "z_score": blend_results[a]["z"],
                "equity_beta": blend_results[a]["res"]["diag"]["equity_beta"],
                "corr_spy": blend_results[a]["res"]["diag"]["corr_spy"],
                "max_drawdown": blend_results[a]["res"]["dd"],
                "time_underwater_days": blend_results[a]["res"]["uw"],
                "turnover": blend_results[a]["res"]["turnover"],
                "n_pos_folds": blend_results[a]["res"]["n_pos"],
                "regime_analysis": blend_results[a]["res"]["reg"],
            } for a in BLEND_WEIGHTS
        },
        "drawdown_analysis": dd_analysis,
        "cost_sensitivity": cost_rows,
        "trend_lookback_sensitivity": sens_trend,
        "macro_lookback_sensitivity": sens_macro,
        "vol_target_10pct_blend": {
            "oos_sharpe": r_vol["oos"], "max_dd": r_vol["dd"],
            "turnover": r_vol["turnover"],
            "realized_ann_vol": r_vol["diag"]["is_ann_vol"],
        },
        "convention_comparability": conv,
        "data_integrity": {
            "fred_endpoint": "public fredgraph.csv (no API key); cached "
                             "parquet from E022",
            "vintage": "current FRED vintage (revised data; release lag "
                       "emulated by 1-reference-month lag; revision "
                       "look-ahead is a residual caveat)",
            "stitching": "none (native FRED series and ETF prices; no "
                         "continuous-futures roll artifacts)",
        },
    }

    out_path = os.path.join("experiments", "e023_economic_trend.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
