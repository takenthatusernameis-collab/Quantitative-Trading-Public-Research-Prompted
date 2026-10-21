#!/usr/bin/env python
"""E030: Multi-asset TSM extension (liquid ETFs)

Seven consecutive non-macro strategy families failed or were
data-infeasible on 2014-2026 large_liquid (E021 distance pairs,
E025 cointegration pairs, E026 equity carry, E027 IVOL, E028
crypto TSM, E029 fundamental accounting factors).  The next
candidate per the E029 handoff search order and prioritization
v1.2.3 is a multi-asset TSM extension: apply the repository's
validated pure time-series-momentum engine (Moskowitz, Ooi &
Pedersen 2012, JFE; the equity flagship) to a cross-asset ETF
universe spanning equities, commodities, fixed income and real
estate.

Why ETFs: E016-E019 showed raw yfinance continuous futures
(``=F``) contain roll-stitching artifacts that moved TSM OOS
Sharpe by 21% and flipped the bear-market Sharpe.  ETFs carry
no roll seams.  Commodity ETFs (USO, DBC) economically embed
contango/backwardation drag -- a real feature of the investable
return stream, not a data artifact.

Pre-registered specification (primary = TSM long-only):
- Universe: 16 liquid ETFs (SPY, QQQ, IWM, EFA, EEM, GLD, USO,
  DBC, TLT, IEF, LQD, HYG, VNQ, XLU, XLP, XLV), yfinance
  daily adjusted closes, 2014-01-02 to 2026-10-09.
- Signal: 12-month (252 trading-day) past total return, lagged
  1 month (21 trading days) to avoid same-month look-ahead.
  Winsorized 1/99 and z-scored per day (monotone transform:
  sign-preserving for the TSM engine, rank-invariant for FE1).
- Construction PRIMARY: long-only -- long ETFs with positive
  signal, inverse-realized-vol (63d) weighted, gross 1.0.
- Variant: long-short -- long positive-signal ETFs, short
  negative-signal ETFs, inverse-vol weighted, gross 1.0 / net 0.
- Monthly (21d) rebalance, close-to-close execution (primary
  convention per ledger PRIORITIZATION.md v1.2.3).
- Costs: base tc=0.5bps + slippage=0.2bps.
- Walk-forward: 504-day formation / 63-day test / 63-day step
  (42 OOS folds).
- SEED=42.

Pre-registered primary gates:
  G1: OOS Sharpe (c2c, WF-mean)        >= 0.8
  G2: Placebo z (matched OOS-WF null)  >= 3.0
  G3: |beta vs SPY|                     <= 0.2
  G4: Bear-market Sharpe (SPY regime)   > 0
  G5: Turnover (daily)                  <= 0.15

Placebo convention (methodological note): G2 is evaluated on the
MATCHED null -- the distribution of the same estimator (mean of
per-fold 63-day OOS Sharpes) under i.i.d. signals -- because the
strategy's headline OOS metric is itself the mean of per-fold
Sharpes.  The repo's earlier convention (E026/E027/E028) compared
the strategy's mean-of-fold OOS Sharpe against the placebo's
FULL-SAMPLE Sharpe, an estimator mismatch that inflates z in bull
markets (mean-of-fold > full-sample under positive drift, and the
full-sample null is depressed by the zero-weight signal warmup).
Both z values are reported; the full-sample-convention z is kept
as a comparability diagnostic and its inflation is quantified.

Falsification expectation (v1.2.2):
  FE1 (within-sample predictive content): mean |Spearman(TSM
        signal[t], next-21d return[t])| >= 0.03 AND >= 60% of
        dates positive (stronger past trend -> higher next-month
        return).  With 16 ETFs the Spearman statistic is
        non-degenerate (unlike the 2-asset crypto test E028).

Sensitivity grid (reported, not gated):
  lookback {126, 252, 378} x {long_only, long_short}
  cost {0, base, +10bps/+5bps, +20bps/+5bps}

Placebo null: 50 simulations of i.i.d. standard-normal signals
through the identical engine (universe, inverse-vol risk budget,
sign-threshold participation rate, rebalance cadence preserved;
signal structure destroyed).  The vectorized placebo is verified
bit-comparable against backtest.time_series_momentum_weights.
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest
from src import jsonio
from src.run_experiment import deterministic_timestamp
from src import multiasset, validation

SEED = 42
np.random.seed(SEED)

ETF_TICKERS = multiasset.MULTI_ASSET_ETFS
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


def load_data():
    """Download the 16-ETF panel and the SPY benchmark."""
    df = data.download(ETF_TICKERS, start="2014-01-01", end="2026-10-11")
    close = data.get_panel(df, "Close").dropna(how="all")
    bm = data.get_benchmark("SPY", start="2014-01-01")
    spy = bm["close"].reindex(close.index).ffill()
    return close, spy


def feasibility_check():
    """Pre-implementation data-integrity screen for the ETF universe."""
    print("[FEASIBILITY] Downloading 16-ETF universe from yfinance...")
    df = data.download(ETF_TICKERS, start="2014-01-01", end="2026-10-11")
    close = data.get_panel(df, "Close")

    report = {"tickers": {}, "roll_artifact_note": None}
    for t in ETF_TICKERS:
        if t not in close.columns:
            report["tickers"][t] = {"status": "MISSING"}
            continue
        s = close[t].dropna()
        report["tickers"][t] = {
            "n_trading_days": int(len(s)),
            "first_date": str(s.index[0].date()),
            "last_date": str(s.index[-1].date()),
            "nan_frac_in_panel": float(close[t].isna().mean()),
            "price_range": [float(s.min()), float(s.max())],
        }

    # ETFs carry no roll-stitching artifacts (no continuous-contract
    # splicing).  Commodity ETFs economically embed contango/backwardation
    # drag (USO, DBC) -- a real cost of the investable stream, recorded
    # here so it is not confused with a data artifact.
    report["roll_artifact_note"] = (
        "ETFs have no roll seams (unlike =F continuous futures contracts; "
        "see E016-E019). Commodity ETFs (USO, DBC) economically embed "
        "contango/backwardation drag -- a real feature of the investable "
        "return stream, not a data artifact."
    )

    feasible = all(
        r.get("n_trading_days", 0) > 500
        for r in report["tickers"].values()
    )
    report["feasible"] = bool(feasible)
    return report


def beta_vs_benchmark(net_ret, bench_ret):
    common = net_ret.index.intersection(bench_ret.index)
    y = net_ret.loc[common].to_numpy()
    x = bench_ret.loc[common].to_numpy()
    if len(y) < 3 or np.std(x) == 0:
        return float("nan"), float("nan"), float("nan")
    A = np.vstack([np.ones(len(x)), x]).T
    alpha, beta_coef = np.linalg.lstsq(A, y, rcond=None)[0]
    corr = float(np.corrcoef(y, x)[0, 1])
    return float(beta_coef), float(alpha * 252), corr


def walk_forward(ret, close, spy_ret):
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    out = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = ret.loc[ret.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"]) if len(test_rets) > 0 else {}
        if not m:
            m = {"sharpe": float("nan"), "annual_return": float("nan"),
                 "annual_vol": float("nan"), "max_drawdown": float("nan"),
                 "total_return": float("nan"), "win_rate": float("nan"),
                 "n_days": 0}
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(test_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else float("nan")
        if np.isnan(spy_win_ret):
            regime = "sideways"
        elif spy_win_ret > 0.02:
            regime = "bull"
        elif spy_win_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"
        m["regime"] = regime
        m["spy_test_return"] = spy_win_ret
        out.append(m)
    return out


def regime_summary(fold_metrics):
    res = {}
    for reg in ["bull", "bear", "sideways"]:
        rows = [m for m in fold_metrics if m.get("regime") == reg]
        sh = [m["sharpe"] for m in rows]
        res[reg] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sh)) if sh else float("nan"),
            "sharpe_pos": int(sum(1 for s in sh if s > 0)) if sh else 0,
            "ann_return_mean": float(np.mean([m["annual_return"] for m in rows])) if rows else float("nan"),
            "max_dd_mean": float(np.mean([m["max_drawdown"] for m in rows])) if rows else float("nan"),
        }
    return res


def compute_dd(ret):
    ret = ret.dropna()
    if len(ret) == 0:
        return 0.0, 0
    cum = (1.0 + ret).cumprod()
    dd = cum / cum.cummax() - 1.0
    return float(dd.min()), int((dd < 0).sum())


def executed_turnover(weights, reb=REBAL):
    w = backtest.shift_weights(weights)
    w = backtest._rebalance_weights(w, reb)
    turn = (w.diff().abs()).sum(axis=1)
    return float(turn.mean()) if len(turn) else 0.0


def portfolio_ret(weights, close, tc=TC_COST, sl=SLIPPAGE, reb=REBAL):
    return backtest.portfolio_returns_close_to_close(
        weights, close, tc_cost=tc, slippage=sl, rebalance_freq=reb
    )


def analyze(weights, close, spy_ret, label):
    ret = portfolio_ret(weights, close)
    net = ret["net"]
    is_m = backtest.metrics(net.dropna())
    folds = walk_forward(ret, close, spy_ret)
    wf_sharpe = float(np.mean([m["sharpe"] for m in folds])) if folds else float("nan")
    wf_std = float(np.std([m["sharpe"] for m in folds])) if folds else float("nan")
    beta, alpha, corr = beta_vs_benchmark(net, spy_ret)
    turn = executed_turnover(weights)
    dd, uw = compute_dd(net)
    pos_folds = int(sum(1 for m in folds if m["sharpe"] > 0))
    reg = regime_summary(folds)
    # Named SPY bear windows (crisis-alpha diagnostic)
    bear_windows = {}
    for lab, lo, hi in [("spy_bear_2018", "2018-09-20", "2018-12-24"),
                        ("covid_crash", "2020-02-19", "2020-03-23"),
                        ("spy_bear_2022", "2022-01-03", "2022-10-12")]:
        mask = (close.index >= lo) & (close.index <= hi)
        wret = net.loc[net.index[mask]]
        if len(wret) > 2:
            bear_windows[lab] = backtest.metrics(wret)
    acf = validation.autocorrelation_test(net)
    tstat = validation.t_stat(wf_sharpe, TEST * len(folds))
    return {
        "label": label,
        "in_sample": is_m,
        "beta_vs_spy": beta,
        "alpha_annual": alpha,
        "corr_spy": corr,
        "oos_wf_sharpe": wf_sharpe,
        "oos_wf_sharpe_std": wf_std,
        "turnover_daily": turn,
        "max_drawdown": dd,
        "time_underwater_days": uw,
        "n_pos_folds": pos_folds,
        "n_folds": len(folds),
        "t_stat": tstat,
        "acf_lag1": float(acf["acf"][0]) if acf["acf"] else float("nan"),
        "regime_analysis": reg,
        "bear_windows": bear_windows,
        "folds": folds,
    }


def per_asset_decomp(weights, close):
    w = backtest.shift_weights(weights)
    w = backtest._rebalance_weights(w, REBAL)
    ret = close.pct_change()
    contrib = (w * ret).mean(axis=0).dropna().sort_values(key=lambda s: s.abs(), ascending=False)
    gross = w.sum(axis=1).replace(0, np.nan)
    return {
        "contributors": {k: float(v) for k, v in contrib.items()},
        "avg_gross_exposure": float(np.nanmean(gross)) if len(gross) else float("nan"),
    }


def placebo_z_for(signal, close, long_only, n_sim=N_PLACEBO):
    """Placebo null: i.i.d. signals through the identical engine.

    Returns (mean_full_sample_sharpe, std_full_sample_sharpe,
    mean_oos_wf_sharpe, std_oos_wf_sharpe, sharpe_list) where the
    full-sample convention matches E026/E027/E028 (G2 gate) and the
    OOS-WF convention is the matched null (reported as a diagnostic).
    """
    spy_ret = None
    pw_list = multiasset.multiasset_placebo_weights(
        signal, close, vol_window=VOL_WINDOW, long_only=long_only,
        seed=SEED, n_sim=n_sim
    )
    full_sharpes = []
    oos_sharpes = []
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    spy = data.get_benchmark("SPY", start="2014-01-01")["close"].reindex(close.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)
    for pw in pw_list:
        pr = portfolio_ret(pw, close)
        pm = backtest.metrics(pr["net"].dropna())
        full_sharpes.append(pm.get("sharpe", 0.0))
        fold_sharpes = []
        for (tr_s, tr_e, te_s, te_e) in splits:
            test_idx = close.index[te_s:te_e]
            test_rets = pr.loc[pr.index.intersection(test_idx)]
            if len(test_rets) > 0:
                fm = backtest.metrics(test_rets["net"])
                fold_sharpes.append(fm.get("sharpe", 0.0))
        oos_sharpes.append(float(np.mean(fold_sharpes)) if fold_sharpes else 0.0)
    return {
        "n_sim": n_sim,
        "mean_full_sample_sharpe": float(np.mean(full_sharpes)),
        "std_full_sample_sharpe": float(np.std(full_sharpes, ddof=0)),
        "mean_oos_wf_sharpe": float(np.mean(oos_sharpes)),
        "std_oos_wf_sharpe": float(np.std(oos_sharpes, ddof=0)),
        "full_sample_sharpe_list": full_sharpes,
        "oos_wf_sharpe_list": oos_sharpes,
    }


def main():
    print("=" * 72)
    print("E030: Multi-asset TSM extension (16 liquid ETFs)")
    print("=" * 72)

    # --- Feasibility check (gate before implementation) ---
    print("\n[0] Feasibility check (data-integrity screen)...")
    fea = feasibility_check()
    print(json.dumps(fea, indent=2, default=str))
    if not fea.get("feasible", False):
        print("FEASIBILITY FAILED: data not sufficient. Aborting.")
        return

    # --- Load data ---
    close, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    print(f"\nLoaded: {close.shape[0]} business days, {close.shape[1]} ETFs "
          f"({close.index[0].date()} to {close.index[-1].date()}); folds={len(splits)}")

    # --- ETF correlation matrix (diversification diagnostic) ---
    corr_mat = close.pct_change().corr()
    print("\n[0b] ETF return correlation matrix (diagnostic)...")
    print(corr_mat.round(2).to_string())

    # --- Compute signal ---
    print("\n[1] Computing TSM signal (252d lookback, 21d skip, winsorize 1/99, z-score)...")
    sig = multiasset.multiasset_tsm_signal(close, lookback_days=LOOKBACK, skip=SKIP)
    print(f"    signal non-NaN cells: {int(sig.notna().sum().sum())} / {sig.size}")

    # --- FE1 (falsification, computed BEFORE walk-forward) ---
    print("\n[2] Falsification FE1 (within-sample predictive content)...")
    fe1 = multiasset.compute_falsification(sig, close, forward_window=21)
    print(f"    mean|Spearman|={fe1['fe1_mean_abs_spearman']:.4f}  "
          f"frac_positive={fe1['fe1_frac_positive']:.3f}  (n={fe1['fe1_n_dates']})")

    results = {}

    # --- Primary: TSM long-only ---
    print("\n[3] PRIMARY: TSM long-only (long positive-momentum ETFs, inv-vol weighted)...")
    w_lo = multiasset.multiasset_weights(sig, close, vol_window=VOL_WINDOW, long_only=True)
    lo = analyze(w_lo, close, spy_ret, "tsm_long_only_primary")
    results["primary"] = lo
    print(f"    OOS Sharpe(WF)={lo['oos_wf_sharpe']:.3f}  beta={lo['beta_vs_spy']:.3f}  "
          f"corr_spy={lo['corr_spy']:.3f}  turn={lo['turnover_daily']:.4f}  "
          f"maxDD={lo['max_drawdown']:.3f}  pos={lo['n_pos_folds']}/{lo['n_folds']}")
    print(f"    regime bear: {lo['regime_analysis']['bear']}")

    # --- Variant: TSM long-short ---
    print("\n[4] VARIANT: TSM long-short (long positive / short negative momentum, inv-vol)...")
    w_dn = multiasset.multiasset_weights(sig, close, vol_window=VOL_WINDOW, long_only=False)
    dn = analyze(w_dn, close, spy_ret, "tsm_long_short_variant")
    results["variant_long_short"] = dn
    print(f"    OOS Sharpe(WF)={dn['oos_wf_sharpe']:.3f}  beta={dn['beta_vs_spy']:.3f}  "
          f"corr_spy={dn['corr_spy']:.3f}  turn={dn['turnover_daily']:.4f}  "
          f"maxDD={dn['max_drawdown']:.3f}  pos={dn['n_pos_folds']}/{dn['n_folds']}")
    print(f"    regime bear: {dn['regime_analysis']['bear']}")

    # --- Placebo null (50 sims, i.i.d. signals, both constructions) ---
    print(f"\n[5] Placebo null ({N_PLACEBO} sims, i.i.d. signals, identical engine)...")
    pl_lo = placebo_z_for(sig, close, long_only=True)
    pl_dn = placebo_z_for(sig, close, long_only=False)
    placebo_z_lo = ((lo["oos_wf_sharpe"] - pl_lo["mean_full_sample_sharpe"])
                    / pl_lo["std_full_sample_sharpe"]
                    if pl_lo["std_full_sample_sharpe"] > 0 else float("nan"))
    placebo_z_dn = ((dn["oos_wf_sharpe"] - pl_dn["mean_full_sample_sharpe"])
                    / pl_dn["std_full_sample_sharpe"]
                    if pl_dn["std_full_sample_sharpe"] > 0 else float("nan"))
    placebo_z_lo_oos = ((lo["oos_wf_sharpe"] - pl_lo["mean_oos_wf_sharpe"])
                        / pl_lo["std_oos_wf_sharpe"]
                        if pl_lo["std_oos_wf_sharpe"] > 0 else float("nan"))
    placebo_z_dn_oos = ((dn["oos_wf_sharpe"] - pl_dn["mean_oos_wf_sharpe"])
                        / pl_dn["std_oos_wf_sharpe"]
                        if pl_dn["std_oos_wf_sharpe"] > 0 else float("nan"))
    print(f"    LO: full-sample null mean={pl_lo['mean_full_sample_sharpe']:.4f} "
          f"std={pl_lo['std_full_sample_sharpe']:.4f}  z={placebo_z_lo:.3f}  "
          f"(matched-OOS z={placebo_z_lo_oos:.3f})")
    print(f"    DN: full-sample null mean={pl_dn['mean_full_sample_sharpe']:.4f} "
          f"std={pl_dn['std_full_sample_sharpe']:.4f}  z={placebo_z_dn:.3f}  "
          f"(matched-OOS z={placebo_z_dn_oos:.3f})")
    results["placebo"] = {
        "long_only": pl_lo,
        "long_short": pl_dn,
        "placebo_z_long_only_repo_convention": placebo_z_lo,
        "placebo_z_long_short_repo_convention": placebo_z_dn,
        "placebo_z_long_only_matched_oos": placebo_z_lo_oos,
        "placebo_z_long_short_matched_oos": placebo_z_dn_oos,
        "convention_note": (
            "G2 gate uses the MATCHED-OOS placebo z (mean of per-fold OOS "
            "Sharpes under i.i.d. signals, same estimator as the strategy's "
            "headline OOS metric). The repo-convention z (full-sample placebo "
            "Sharpe vs strategy OOS-WF-mean) is reported for comparability "
            "with E026/E027/E028; it is inflated by an estimator mismatch "
            "(see ledger E030 entry for details)."
        ),
    }

    # --- Cost sensitivity (primary long-only) ---
    print("\n[6] Cost sweep (primary long-only)...")
    cost_scenarios = [
        (0.0, 0.0, "zero"),
        (TC_COST, SLIPPAGE, "base"),
        (0.010, 0.005, "high_10bps5bps"),
        (0.020, 0.005, "high_20bps5bps"),
    ]
    cost_rows = []
    for tc, sl, label in cost_scenarios:
        ret = portfolio_ret(w_lo, close, tc=tc, sl=sl)
        fm = walk_forward(ret, close, spy_ret)
        npos = int(sum(1 for m in fm if m["sharpe"] > 0))
        sharpe = float(np.mean([m["sharpe"] for m in fm])) if fm else float("nan")
        sharpe_std = float(np.std([m["sharpe"] for m in fm])) if fm else float("nan")
        cost_rows.append({
            "tc_cost": tc, "slippage": sl, "scenario": label,
            "oos_sharpe": sharpe,
            "n_pos_folds": npos,
            "sharpe_std": sharpe_std,
        })
        print(f"    {label}: tc={tc:.4f} sl={sl:.4f}: Sharpe={sharpe:.3f} pos={npos}/{len(fm)}")
    results["cost_sensitivity"] = cost_rows

    # --- Sensitivity grid ---
    print("\n[7] Sensitivity grid (lookback x construction)...")
    sens = []
    for lb in [126, 252, 378]:
        sig_s = multiasset.multiasset_tsm_signal(close, lookback_days=lb, skip=SKIP)
        for lo_flag, tag in [(True, "tsm_long_only"), (False, "tsm_long_short")]:
            w = multiasset.multiasset_weights(sig_s, close, vol_window=VOL_WINDOW, long_only=lo_flag)
            ret = portfolio_ret(w, close)
            fm = walk_forward(ret, close, spy_ret)
            beta_s, _, _ = beta_vs_benchmark(ret["net"], spy_ret)
            turn_s = executed_turnover(w)
            shr = float(np.mean([m["sharpe"] for m in fm])) if fm else float("nan")
            sens.append({
                "lookback": lb, "construction": tag,
                "oos_sharpe": shr, "beta_vs_spy": beta_s, "turnover": turn_s,
            })
            print(f"    lookback={lb} {tag}: Sharpe={shr:.3f} beta={beta_s:.3f} turn={turn_s:.4f}")
    results["sensitivity"] = sens

    # --- Per-asset decomposition (primary) ---
    print("\n[8] Per-asset decomposition (primary long-only)...")
    pad = per_asset_decomp(w_lo, close)
    results["per_asset_decomposition"] = pad
    print(f"    avg gross exposure: {pad['avg_gross_exposure']:.3f}")
    print(f"    top contributors: {dict(list(pad['contributors'].items())[:5])}")

    # --- FE1 (predictive content) ---
    print("\n[9] Falsification FE1 (predictive content)...")
    print(f"    mean|Spearman|={fe1['fe1_mean_abs_spearman']:.4f}  "
          f"frac_positive={fe1['fe1_frac_positive']:.3f}  "
          f"(n={fe1['fe1_n_dates']})")

    # --- Gates + decision (primary) ---
    gates = {
        "G1_oos_sharpe_ge_0.8": {
            "value": lo["oos_wf_sharpe"], "threshold": 0.8,
            "pass": bool(lo["oos_wf_sharpe"] >= 0.8) if not np.isnan(lo["oos_wf_sharpe"]) else False,
        },
        "G2_placebo_z_ge_3.0_matched_oos": {
            "value": placebo_z_lo_oos, "threshold": 3.0,
            "pass": bool(placebo_z_lo_oos >= 3.0) if not np.isnan(placebo_z_lo_oos) else False,
        },
        "G3_abs_beta_le_0.2": {
            "value": abs(lo["beta_vs_spy"]), "threshold": 0.2,
            "pass": bool(abs(lo["beta_vs_spy"]) <= 0.2) if np.isfinite(lo["beta_vs_spy"]) else False,
        },
        "G4_bear_sharpe_gt_0": {
            "value": lo["regime_analysis"]["bear"]["sharpe_mean"],
            "threshold": 0.0,
            "pass": bool(lo["regime_analysis"]["bear"]["sharpe_mean"] > 0),
        },
        "G5_turnover_le_0.15": {
            "value": lo["turnover_daily"], "threshold": 0.15,
            "pass": bool(lo["turnover_daily"] <= 0.15),
        },
    }
    n_pass = sum(1 for g in gates.values() if g["pass"])
    decision = "KEEP" if n_pass == len(gates) else "REJECT"

    print("\n" + "=" * 72)
    print(f"GATES ({n_pass}/{len(gates)} passed):")
    for k, v in gates.items():
        mark = "PASS" if v["pass"] else "FAIL"
        val = v["value"]
        if isinstance(val, float) and np.isnan(val):
            val_str = "NaN"
            mark = "FAIL"
        else:
            val_str = f"{val:.4f}"
        print(f"  {k}: {val_str} vs {v['threshold']}  [{mark}]")
    print(f"FE1: {json.dumps(fe1, default=str)}")
    print(f"DECISION: {decision}")
    print("=" * 72)

    result = {
        "experiment": "E030",
        "timestamp": deterministic_timestamp(),
        "pre_registered": {
            "method": "multi_asset_tsm",
            "source": "Moskowitz, Ooi & Pedersen (2012) 'Time Series Momentum', Journal of Financial Economics 104(2):228-250. Pure TSM engine identical to the repository equity flagship (strategies.time_series_momentum_pure + backtest.time_series_momentum_weights).",
            "universe": "16 liquid ETFs: " + ", ".join(ETF_TICKERS),
            "n_tickers": len(ETF_TICKERS),
            "data_integrity": fea.get("roll_artifact_note"),
            "primary_construction": "tsm_long_only (long positive-momentum ETFs, inv-vol weighted, monthly rebalance, gross 1.0)",
            "variant": "tsm_long_short (long positive / short negative momentum, inv-vol weighted, gross 1.0 / net 0)",
            "lookback": LOOKBACK,
            "skip": SKIP,
            "vol_window": VOL_WINDOW,
            "rebalance_freq": REBAL,
            "execution_convention": "close_to_close (primary convention v1.2.3)",
            "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
            "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP, "n_folds": len(splits)},
            "placebo": {"n_sim": N_PLACEBO, "kind": "i.i.d. standard-normal signals, identical engine"},
            "fe1": "mean|Spearman(signal[t], next-21d ret[t])| >= 0.03 AND >= 60% positive",
            "gates": {
                "G1": "OOS Sharpe (c2c, WF-mean) >= 0.8",
                "G2": "Placebo z (MATCHED OOS-WF null, same estimator) >= 3.0",
                "G3": "|beta vs SPY| <= 0.2",
                "G4": "Bear-market Sharpe > 0",
                "G5": "Turnover (daily) <= 0.15",
            },
        },
        "falsification": fe1,
        "feasibility": fea,
        "primary": lo,
        "variant_long_short": dn,
        "placebo": results["placebo"],
        "cost_sensitivity": cost_rows,
        "sensitivity": sens,
        "per_asset_decomposition": pad,
        "etf_correlation_matrix": corr_mat.round(4).to_dict(),
        "gates": gates,
        "n_gates_passed": n_pass,
        "decision": decision,
    }
    out_path = os.path.join("experiments", "e030_multiasset_tsm.json")
    os.makedirs("experiments", exist_ok=True)
    with open(out_path, "w") as f:
        jsonio.dump(result, f, indent=2, default=str)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
