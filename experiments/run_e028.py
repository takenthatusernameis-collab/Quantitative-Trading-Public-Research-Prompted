#!/usr/bin/env python
"""E028: Crypto cross-asset momentum (BTC, ETH via yfinance)

Four consecutive fundamental-style equity strategies failed on 2014-2026
large_liquid (E021 distance pairs, E025 cointegration pairs, E026 equity carry,
E027 IVOL).  The next candidate per the E026/E027 handoff search order and
prioritization v1.2.3 is crypto cross-asset signals: time-series momentum
(Moskowitz, Ooi & Pedersen 2012) and cross-sectional momentum applied to
Bitcoin and Ethereum.

Pre-registered specification (primary = TSM long-only):
- Universe: BTC-USD, ETH-USD (yfinance, daily, auto_adjust=True for price
  consistency with the repo's adjusted-close convention).
- Calendar alignment: crypto trades 24/7; reindexed to the SPY business-day
  calendar (forward-fill crypto close) so walk-forward splits and SPY-beta
  comparison are meaningful.  Weekend/holiday returns are captured in the
  next business-day close (correct for a close-to-close convention).
- Signal: 12-month (252 trading-day) past total return, lagged 1 month
  (21 trading days) to avoid look-ahead.  Cross-sectionally winsorized 1/99
  and z-scored per day.
- Construction PRIMARY: long-only — long assets with positive signal,
  inverse-realized-vol (63d) weighted.
- Variant: dollar-neutral cross-sectional momentum — long top-50% by signal,
  short bottom-50%, each side inverse-vol weighted and scaled to 0.5 gross.
  With 2 tickers this is long the stronger-momentum name, short the weaker.
- Monthly (21d) rebalance, weights held constant between rebalances via the
  backtest engine's rebalance_freq.  Close-to-close execution (primary
  convention per v1.2.3).
- Costs: base tc=0.5bps + slippage=0.2bps.
  Crypto-specific premium: +5bps/day short borrowing cost applied as a
  measurement stress (modelled as additional tc on the short leg of the DN
  variant only).
- Walk-forward: 504-day formation / 63-day test / 63-day step on the aligned
  calendar.
- SEED=42.

Pre-registered primary gates:
  G1: OOS Sharpe (c2c, WF-mean)        >= 0.8
  G2: Placebo z (cross-section null)  >= 3.0
  G3: |beta vs SPY|                    <= 0.3
  G4: Bear-market Sharpe              > 0
  G5: Turnover (daily)                <= 0.15

Falsification expectation (v1.2.2):
  FE1 (within-sample predictive content): mean |Spearman(TSM signal[t],
        next-21d return[t])| >= 0.03 AND >= 60% of dates positive
        (high signal -> higher next-month return).  If this fails, there is
        no within-sample momentum mechanism on this crypto sample.

Sensitivity grid (reported, not gated):
  lookback {126, 252, 378} x {long_only, dollar_neutral} x
  cost {0, base, +10bps/+5bps, +20bps/+5bps, +5bps short-premium}

Implementation gaps vs paper (recorded, not hidden):
- Moskowitz et al. (2012) is 1990s-2010 global futures/cross-section; this
  test is 2017-2026 BTC+ETH spot.  Crypto momentum is documented in the
  literature (Corbet et al. 2018; Bucchino et al. 2022) but the strong trend
  regime of 2017-2021 may not persist; FE1 screens directional predictability.
- Carry/funding-rate (the third handoff item) is NOT testable: yfinance spot
  has no funding-rate column.  A degenerate price-based carry proxy would
  be conflated with momentum.
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.run_experiment import deterministic_timestamp
from src import data, backtest, crypto, validation

SEED = 42
np.random.seed(SEED)

CRYPTO_TICKERS = ["BTC-USD", "ETH-USD"]
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
VOL_WINDOW = 63
TOP_FRAC = 0.5
LOOKBACK = 252
SKIP = 21
TC_COST = 0.0005
SLIPPAGE = 0.0002
N_PLACEBO = 50

# Crypto-specific: +5bps/day short borrowing premium (measurement only)
SHORT_PREMIUM = 0.0005


def load_data():
    """Download and align crypto to the SPY business-day calendar."""
    df = data.download(CRYPTO_TICKERS, start="2014-01-01", end="2026-10-11")
    close_raw = data.get_panel(df, "Close")
    close_raw = close_raw.dropna(how="all")

    bm = data.get_benchmark("SPY", start="2014-01-01")
    equity_calendar = bm["close"].index

    # Forward-fill crypto close to business days (weekend/holiday returns
    # are captured in the next business-day close)
    close = close_raw.reindex(equity_calendar).ffill().dropna(how="all")
    spy = bm["close"].reindex(close.index).ffill()

    return close, spy


def feasibility_check():
    """Pre-implementation data-integrity screen for BTC-USD, ETH-USD."""
    print("[FEASIBILITY] Downloading BTC-USD, ETH-USD from yfinance...")
    df = data.download(CRYPTO_TICKERS, start="2014-01-01", end="2026-10-11")
    close = data.get_panel(df, "Close")

    bm = data.get_benchmark("SPY", start="2014-01-01")
    spy = bm["close"]
    equity_calendar = spy.index

    report = {}
    for t in CRYPTO_TICKERS:
        if t not in close.columns:
            report[t] = {"status": "MISSING", "reason": f"{t} not found in download"}
            continue
        s = close[t].dropna()
        n_days = len(s)
        first_date = str(s.index[0].date())
        last_date = str(s.index[-1].date())
        nan_count = int(close[t].isna().sum())
        nan_frac = close[t].isna().mean()

        # Weekend coverage check: crypto trades 24/7
        weekdays = s.index.dayofweek
        weekend_frac = (weekdays >= 5).mean()

        report[t] = {
            "n_trading_days": n_days,
            "first_date": first_date,
            "last_date": last_date,
            "nan_frac_in_panel": float(nan_frac),
            "weekend_data_frac": float(weekend_frac),
            "weekend_presence": bool(weekend_frac > 0.1),
            "price_range": [float(s.min()), float(s.max())],
        }

    # Calendar alignment check
    aligned = close.reindex(equity_calendar).ffill()
    aligned_nonan = aligned.dropna(how="all")
    report["calendar_alignment"] = {
        "equity_business_days": len(equity_calendar),
        "aligned_business_days": len(aligned_nonan),
        "ffill_fraction": float(aligned_nonan.isna().sum().sum() / (aligned_nonan.shape[0] * aligned_nonan.shape[1])),
    }

    feasible = all(
        r.get("n_trading_days", 0) > 500
        for r in report.values() if isinstance(r, dict) and "n_trading_days" in r
    )
    report["feasible"] = feasible
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
                 "total_return": float("nan"), "win_rate": float("nan"), "n_days": 0}
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


def analyze(weights: pd.DataFrame, close: pd.DataFrame, spy_ret: pd.Series, label: str):
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
    # Bear windows: crypto severe drawdowns
    bear_windows = {}
    for lab, lo, hi in [("crypto_bear_2018", "2018-01-01", "2018-12-31"),
                        ("covid_crash", "2020-02-19", "2020-04-15"),
                        ("crypto_bear_2022", "2022-01-01", "2022-12-31")]:
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
    return {
        "contributors": {k: float(v) for k, v in contrib.items()},
    }


def main():
    print("=" * 72)
    print("E028: Crypto cross-asset momentum (BTC, ETH via yfinance)")
    print("=" * 72)

    # --- Feasibility check (gate before implementation) ---
    print("\n[0] Feasibility check (data-integrity screen)...")
    fea = feasibility_check()
    print(json.dumps(fea, indent=2, default=str))
    if not fea.get("feasible", False):
        print("FEASIBILITY FAILED: data not sufficient. Aborting.")
        return

    # --- Load aligned data ---
    close, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    print(f"\nLoaded: {close.shape[0]} business days, {close.shape[1]} tickers "
          f"({close.index[0].date()} to {close.index[-1].date()}); folds={len(splits)}")

    # --- Compute signal ---
    print("\n[1] Computing TSM signal (252d lookback, 21d skip, winsorize 1/99, z-score)...")
    sig = crypto.crypto_tsm_signal(close, lookback_days=LOOKBACK, skip=SKIP, winsorize=True)
    print(f"    signal non-NaN cells: {int(sig.notna().sum().sum())} / {sig.size}")

    # --- FE1 (falsification, computed BEFORE walk-forward) ---
    print("\n[2] Falsification FE1 (predictive content)...")
    fe1 = crypto.compute_falsification(sig, close, forward_window=21)
    print(f"    mean|Spearman|={fe1['fe1_mean_abs_spearman']:.4f}  "
          f"frac_positive={fe1['fe1_frac_positive']:.3f}  (n={fe1['fe1_n_dates']})")

    results = {}

    # --- Primary: TSM long-only ---
    print("\n[3] PRIMARY: TSM long-only (long positive-momentum crypto, inv-vol weighted)...")
    w_lo = crypto.crypto_weights(sig, close, vol_window=VOL_WINDOW, top_frac=1.0, long_only=True)
    lo = analyze(w_lo, close, spy_ret, "tsm_long_only_primary")
    results["primary"] = lo
    print(f"    OOS Sharpe(WF)={lo['oos_wf_sharpe']:.3f}  beta={lo['beta_vs_spy']:.3f}  "
          f"corr_spy={lo['corr_spy']:.3f}  turn={lo['turnover_daily']:.4f}  "
          f"maxDD={lo['max_drawdown']:.3f}  pos={lo['n_pos_folds']}/{lo['n_folds']}")
    print(f"    regime bear: {lo['regime_analysis']['bear']}")

    # --- Variant: Dollar-neutral XSM ---
    print("\n[4] VARIANT: Dollar-neutral cross-sectional momentum (long high, short low)...")
    w_dn = crypto.crypto_weights(sig, close, vol_window=VOL_WINDOW, top_frac=TOP_FRAC, long_only=False)
    dn = analyze(w_dn, close, spy_ret, "dn_xsm_variant")
    results["variant_dn"] = dn
    print(f"    OOS Sharpe(WF)={dn['oos_wf_sharpe']:.3f}  beta={dn['beta_vs_spy']:.3f}  "
          f"corr_spy={dn['corr_spy']:.3f}  turn={dn['turnover_daily']:.4f}  "
          f"maxDD={dn['max_drawdown']:.3f}  pos={dn['n_pos_folds']}/{dn['n_folds']}")

    # --- Placebo null (50 sims, long-only, random signal) ---
    print(f"\n[5] Placebo null ({N_PLACEBO} sims, long-only, random signal)...")
    placebo_weights_list = crypto.crypto_placebo_weights(
        sig, close, vol_window=VOL_WINDOW, top_frac=1.0, long_only=True,
        seed=SEED, n_sim=N_PLACEBO
    )
    placebo_sharpes = []
    for pw in placebo_weights_list:
        pr = portfolio_ret(pw, close)
        pm = backtest.metrics(pr["net"].dropna())
        placebo_sharpes.append(pm.get("sharpe", 0.0))
    pm_val = float(np.mean(placebo_sharpes)) if placebo_sharpes else 0.0
    ps_val = float(np.std(placebo_sharpes, ddof=0)) if len(placebo_sharpes) > 1 else 1.0
    placebo_z = (lo["oos_wf_sharpe"] - pm_val) / ps_val if ps_val > 0 else float("nan")
    print(f"    placebo mean={pm_val:.4f} std={ps_val:.4f}  z={placebo_z:.3f}")

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

    # --- DN short-premium stress (measurement only) ---
    print("\n[6b] DN short-premium stress (+5bps/day short borrowing, measurement only)...")
    # Approximate: add SHORT_PREMIUM to tc_cost to stress DN short leg
    dn_stress_ret = portfolio_ret(w_dn, close, tc=TC_COST + SHORT_PREMIUM, sl=SLIPPAGE)
    dn_stress_wf = walk_forward(dn_stress_ret, close, spy_ret)
    dn_stress_sharpe = float(np.mean([m["sharpe"] for m in dn_stress_wf])) if dn_stress_wf else float("nan")
    results["variant_dn_short_premium"] = {
        "label": "dn_xsm_short_premium_stress",
        "oos_wf_sharpe": dn_stress_sharpe,
        "cost_applied": {"tc_cost": TC_COST + SHORT_PREMIUM, "slippage": SLIPPAGE},
        "short_premium_applied": SHORT_PREMIUM,
        "note": "Approximate: SHORT_PREMIUM added to tc_cost for all DN positions (short-leg borrowing proxy)",
        "n_pos_folds": int(sum(1 for m in dn_stress_wf if m["sharpe"] > 0)),
        "n_folds": len(dn_stress_wf),
    }
    print(f"    DN stress Sharpe={dn_stress_sharpe:.3f} pos={results['variant_dn_short_premium']['n_pos_folds']}/{len(dn_stress_wf)}")

    # --- Sensitivity grid ---
    print("\n[7] Sensitivity grid (lookback x construction)...")
    sens = []
    for lb in [126, 252, 378]:
        sig_s = crypto.crypto_tsm_signal(close, lookback_days=lb, skip=SKIP, winsorize=True)
        for tf, lo_flag, tag in [(1.0, True, "tsm_long_only"), (0.5, False, "dn_xsm")]:
            w = crypto.crypto_weights(sig_s, close, vol_window=VOL_WINDOW, top_frac=tf, long_only=lo_flag)
            ret = portfolio_ret(w, close)
            fm = walk_forward(ret, close, spy_ret)
            beta_s, _, _ = beta_vs_benchmark(ret["net"], spy_ret)
            turn_s = executed_turnover(w)
            shr = float(np.mean([m["sharpe"] for m in fm])) if fm else float("nan")
            sens.append({
                "lookback": lb, "top_frac": tf, "construction": tag,
                "oos_sharpe": shr, "beta_vs_spy": beta_s, "turnover": turn_s,
            })
            print(f"    lookback={lb} {tag}: Sharpe={shr:.3f} beta={beta_s:.3f} turn={turn_s:.4f}")
    results["sensitivity"] = sens

    # --- FE1 (predictive content) ---
    print("\n[8] Falsification FE1 (predictive content)...")
    # Already computed in step 2
    print(f"    mean|Spearman|={fe1['fe1_mean_abs_spearman']:.4f}  "
          f"frac_positive={fe1['fe1_frac_positive']:.3f}  "
          f"(n={fe1['fe1_n_dates']})")

    # --- Gates + decision (primary) ---
    gates = {
        "G1_oos_sharpe_ge_0.8": {
            "value": lo["oos_wf_sharpe"], "threshold": 0.8,
            "pass": bool(lo["oos_wf_sharpe"] >= 0.8) if not np.isnan(lo["oos_wf_sharpe"]) else False,
        },
        "G2_placebo_z_ge_3.0": {
            "value": placebo_z, "threshold": 3.0,
            "pass": bool(placebo_z >= 3.0) if not np.isnan(placebo_z) else False,
        },
        "G3_abs_beta_le_0.3": {
            "value": abs(lo["beta_vs_spy"]), "threshold": 0.3,
            "pass": bool(abs(lo["beta_vs_spy"]) <= 0.3) if np.isfinite(lo["beta_vs_spy"]) else False,
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
        "experiment": "E028",
        "timestamp": deterministic_timestamp(),
        "pre_registered": {
            "method": "crypto_tsm_xsm",
            "source": "Moskowitz, Ooi & Pedersen (2012) 'Time Series Momentum', JFE; applied to BTC/ETH spot via yfinance. Crypto momentum context: Corbet et al. (2018), Bucchino et al. (2022).",
            "universe": "BTC-USD, ETH-USD",
            "n_tickers": 2,
            "calendar_alignment": "crypto 24/7 reindexed to SPY business-day calendar (forward-fill)",
            "primary_construction": "tsm_long_only (long positive-momentum, inv-vol weighted, monthly rebalance)",
            "variant": "dollar_neutral_xsm (long high-momentum, short low-momentum, inv-vol weighted)",
            "lookback": LOOKBACK,
            "skip": SKIP,
            "top_frac": TOP_FRAC,
            "vol_window": VOL_WINDOW,
            "rebalance_freq": REBAL,
            "execution_convention": "close_to_close (primary convention v1.2.3)",
            "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
            "short_premium_stress": SHORT_PREMIUM,
            "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP, "n_folds": len(splits)},
            "placebo": {"n_sim": N_PLACEBO},
            "fe1": "mean|Spearman(signal[t], next-21d ret[t])| >= 0.03 AND >= 60% positive",
            "gates": {
                "G1": "OOS Sharpe (c2c, WF-mean) >= 0.8",
                "G2": "Placebo z >= 3.0",
                "G3": "|beta vs SPY| <= 0.3",
                "G4": "Bear-market Sharpe > 0",
                "G5": "Turnover (daily) <= 0.15",
            },
        },
        "falsification": fe1,
        "feasibility": fea,
        "primary": lo,
        "variant_dn": dn,
        "placebo": {"n_sim": N_PLACEBO, "mean_sharpe": pm_val, "std_sharpe": ps_val,
                    "sharpe_list": placebo_sharpes, "placebo_z": placebo_z},
        "cost_sensitivity": cost_rows,
        "sensitivity": sens,
        "per_asset_decomposition": per_asset_decomp(w_lo, close),
        "gates": gates,
        "n_gates_passed": n_pass,
        "decision": decision,
    }
    out_path = os.path.join("experiments", "e028_crypto_momentum.json")
    os.makedirs("experiments", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
