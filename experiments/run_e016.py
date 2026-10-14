"""E016: Time-series momentum + carry on a properly-rolled futures universe.

Follows up the E015 handoff:
  Part 1 - Roll methodology: detect roll seams in yfinance front-month
           continuous futures (data-driven: futures-vs-spot excess
           overnight gaps inside expected roll windows, plus outlier
           days), build de-seamed return indices, and quantify how
           much the raw stitched series distorts TSM (raw vs de-seamed).
  Part 2 - Carry signal: basis carry (Koijen, Moskowitz, Pedersen &
           Vrugt 2018), carry = (S - F)/S, using paired spot ETFs
           (physical gold/silver, equity, bond and FX trusts; futures-
           based USO/UNG as commodity proxies whose NAV embeds the
           rolled curve). Dollar-neutral, inverse-vol weighted.
  Part 3 - TSM + Carry blend: 50/50, walk-forward OOS, placebo null
           (random TSM + random carry), cost sweep, regime analysis.

Design:
  - Universe: 12 liquid futures contracts across equities, bonds,
    commodities and FX, each paired with a spot ETF.
  - Walk-forward 504/63/63 (~41 OOS folds), monthly (21d) rebalance,
    next-day-open execution (close-to-close for the de-seamed index,
    whose open prices are not observable), tc=0.5bps + slippage=0.2bps.
  - TSM: 12-month lookback, 1-month skip, inverse-vol (63d), symmetric
    long/short (futures allow shorting as cheaply as longing).
  - Carry: dollar-neutral top/bottom-half sort, inverse-vol weighted.
  - Pre-registered promotion gates: OOS Sharpe >= 1.5, |beta| <= 0.2,
    maxDD >= -0.15, positive bear-market Sharpe, placebo z >= 3.
"""

import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, strategies, futures
from src.run_experiment import deterministic_timestamp

TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
SEED = 42
PLACEBO_N_SIM = 50

START = "2014-01-01"

# Futures ticker -> (paired spot ETF, roll cadence).
FUTURES_UNIVERSE = {
    "ES=F": ("SPY", "quarterly"),
    "NQ=F": ("QQQ", "quarterly"),
    "YM=F": ("DIA", "quarterly"),
    "RTY=F": ("IWM", "quarterly"),
    "ZB=F": ("TLT", "quarterly"),
    "ZN=F": ("IEF", "quarterly"),
    "GC=F": ("GLD", "monthly"),
    "SI=F": ("SLV", "monthly"),
    "CL=F": ("USO", "monthly"),
    "NG=F": ("UNG", "monthly"),
    "6E=F": ("FXE", "quarterly"),
    "6B=F": ("FXF", "quarterly"),
    "6J=F": ("FXY", "quarterly"),
}


def load_panels():
    """Download and build raw / de-seamed / carry panels."""
    fut_tickers = list(FUTURES_UNIVERSE.keys())
    spot_tickers = [v[0] for v in FUTURES_UNIVERSE.values()]
    tickers = sorted(set(fut_tickers + spot_tickers + ["SPY"]))
    df = data.download(tickers, start=START)

    raw_fut, raw_spot, raw_open = {}, {}, {}
    for ft, (st, cad) in FUTURES_UNIVERSE.items():
        f = data.wide_close(df, ft)
        s = data.wide_close(df, st)
        o = data.get_panel(df, "Open")[ft]
        # Spot panel is keyed by the futures ticker so the two
        # panels share columns (each futures contract has exactly
        # one paired spot ETF).
        raw_fut[ft] = f["close"]
        raw_spot[ft] = s["close"]
        raw_open[ft] = o

    fut_close = pd.DataFrame(raw_fut).dropna(axis=1, how="all")
    spot_close = pd.DataFrame(raw_spot).reindex(columns=fut_close.columns).ffill()
    fut_open = pd.DataFrame(raw_open).reindex(columns=fut_close.columns).ffill()

    # Align all series to common trading dates.
    common = fut_close.dropna().index
    for col in spot_close.columns:
        common = common.intersection(spot_close[col].dropna().index)
    common = common.intersection(fut_open.dropna().index)
    fut_close = fut_close.loc[common]
    spot_close = spot_close.loc[common].ffill()
    fut_open = fut_open.loc[common].ffill()

    # De-seamed indices and seam diagnostics.
    idx = {}
    seams = {}
    seam_stats = {}
    for ft, (st, cad) in FUTURES_UNIVERSE.items():
        f = fut_close[ft]
        s = spot_close[ft]
        detected = futures.detect_seams(f, s, cadence=cad)
        clean_ret = futures.deseam_returns(f, s, detected)
        idx[ft] = futures.deseam_index(clean_ret)
        seams[ft] = pd.DatetimeIndex(detected)

        # Excess-gap magnitudes at detected seams (the removed artifacts).
        r_fut = f.pct_change()
        r_spot = s.reindex(f.index).ffill().pct_change()
        excess = (r_fut - r_spot).reindex(pd.DatetimeIndex(detected))
        seam_stats[ft] = {
            "cadence": cad,
            "n_seams": int(len(detected)),
            "median_excess_gap": float(np.nanmedian(excess.abs())) if len(excess) else 0.0,
            "max_excess_gap": float(np.nanmax(excess.abs())) if len(excess) else 0.0,
            "max_seam_date": str(excess.abs().idxmax().date()) if len(excess) and np.isfinite(excess.abs().max()) else None,
        }

    de_index = pd.DataFrame(idx).loc[common]
    carry = strategies.carry_signal(fut_close, spot_close)
    # Secondary carry variant: trailing realized roll yield from seam gaps.
    carry_rroll = pd.DataFrame(index=fut_close.index, columns=fut_close.columns, dtype=float)
    for ft, (st, cad) in FUTURES_UNIVERSE.items():
        carry_rroll[ft] = futures.realized_roll_yield(
            fut_close[ft], spot_close[ft], seams[ft]
        )

    bm = data.download(["SPY"], start=START)
    spy = data.get_panel(bm, "Close")["SPY"].reindex(common).ffill()

    return {
        "fut_close": fut_close,
        "fut_open": fut_open,
        "spot_close": spot_close,
        "de_index": de_index,
        "carry": carry,
        "carry_rroll": carry_rroll,
        "spy": spy,
        "seams": {k: [str(d.date()) for d in v] for k, v in seams.items()},
        "seam_stats": seam_stats,
    }


def market_diagnostics(ret, spy_ret):
    """Full-sample metrics + market-neutrality diagnostics (equity beta, corr)."""
    net = ret["net"].dropna()
    m = backtest.metrics(net)
    common = net.index.intersection(spy_ret.index)
    y = net.loc[common].values
    x = spy_ret.loc[common].values
    if len(y) > 2 and np.std(x) > 0:
        A = np.vstack([np.ones(len(x)), x]).T
        coef = np.linalg.lstsq(A, y, rcond=None)[0]
        alpha, beta_coef = float(coef[0]), float(coef[1])
        corr = float(np.corrcoef(y, x)[0, 1])
    else:
        alpha, beta_coef, corr = float("nan"), float("nan"), float("nan")
    return {
        "sharpe": m.get("sharpe"),
        "annual_return": m.get("annual_return"),
        "annual_vol": m.get("annual_vol"),
        "max_drawdown": m.get("max_drawdown"),
        "total_return": m.get("total_return"),
        "n_days": m.get("n_days"),
        "equity_beta": beta_coef,
        "alpha_annual": alpha * 252,
        "corr_spy": corr,
    }


def walk_forward(ret, close, spy_ret):
    """Walk-forward OOS fold metrics with regime classification."""
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    fold_metrics = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = ret.loc[ret.index.intersection(test_idx)]
        m = backtest.metrics(test_rets["net"])
        m["fold"] = i
        spy_win = spy_ret.loc[spy_ret.index.intersection(test_idx)]
        spy_win_ret = float(spy_win.sum()) if len(spy_win) else float("nan")
        if spy_win_ret > 0.02:
            regime = "bull"
        elif spy_win_ret < -0.02:
            regime = "bear"
        else:
            regime = "sideways"
        m["regime"] = regime
        m["spy_test_return"] = spy_win_ret
        fold_metrics.append(m)
    return fold_metrics, splits


def regime_summary(fold_metrics):
    out = {}
    for regime in ["bull", "bear", "sideways"]:
        rows = [m for m in fold_metrics if m.get("regime") == regime]
        sharps = [m["sharpe"] for m in rows
                  if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        out[regime] = {
            "n_folds": len(rows),
            "sharpe_mean": float(np.mean(sharps)) if sharps else float("nan"),
            "sharpe_pos": int(sum(1 for s in sharps if s > 0)) if sharps else 0,
        }
    return out


def compute_drawdown(ret):
    ret = ret.dropna()
    if len(ret) == 0:
        return 0.0, 0
    cum = (1.0 + ret).cumprod()
    roll = cum.cummax()
    dd = cum / roll - 1.0
    underwater = int((dd < 0).sum())
    return float(dd.min()), underwater


def evaluate(close, open_, spy, weights, label):
    """Full evaluation of a weight panel: OOS, beta, turnover, DD, regime."""
    ret = backtest.portfolio_returns_rebalance_clean(
        weights, close, open_, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
    )
    spy_ret = spy.pct_change().fillna(0.0)
    diag = market_diagnostics(ret, spy_ret)
    fm, splits = walk_forward(ret, close, spy_ret)
    sharpes = [m["sharpe"] for m in fm
               if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
    oos_sharpe = float(np.mean(sharpes)) if sharpes else float("nan")
    oos_std = float(np.std(sharpes)) if sharpes else float("nan")
    turn = backtest.average_turnover(weights)
    dd, uw = compute_drawdown(ret["net"])
    reg = regime_summary(fm)
    n_pos = int(sum(1 for m in fm if m.get("sharpe") is not None and m.get("sharpe", 0) > 0))
    return {
        "label": label,
        "is_sharpe": diag["sharpe"],
        "is_ann_return": diag["annual_return"],
        "is_ann_vol": diag["annual_vol"],
        "oos_sharpe": oos_sharpe,
        "oos_sharpe_std": oos_std,
        "turnover": turn,
        "equity_beta": diag["equity_beta"],
        "corr_spy": diag["corr_spy"],
        "alpha_annual": diag["alpha_annual"],
        "max_drawdown": dd,
        "time_underwater_days": uw,
        "positive_folds": n_pos,
        "n_folds": len(splits),
        "n_tickers": int(close.shape[1]),
        "regime_analysis": reg,
    }, fm


def blended_placebo(de_index, spy, n_sim=PLACEBO_N_SIM):
    """Placebo null: random TSM + random carry, blended 50/50."""
    rng = np.random.default_rng(SEED)
    spy_ret = spy.pct_change().fillna(0.0)
    sharps = []
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    for _ in range(n_sim):
        tsm_sig = pd.DataFrame(
            rng.standard_normal(size=de_index.shape),
            index=de_index.index, columns=de_index.columns,
        )
        tsm_w = backtest.time_series_momentum_weights(
            tsm_sig, de_index, long_only=False, vol_window=63
        )
        carry_sig = pd.DataFrame(
            rng.standard_normal(size=de_index.shape),
            index=de_index.index, columns=de_index.columns,
        )
        carry_w = backtest.carry_weights(carry_sig, vol)
        bw = 0.5 * tsm_w + 0.5 * carry_w
        r = backtest.portfolio_returns_rebalance_clean(
            bw, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        fm, _ = walk_forward(r, de_index, spy_ret)
        s = [m["sharpe"] for m in fm
             if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        sharps.append(float(np.mean(s)) if s else 0.0)
    return float(np.mean(sharps)), float(np.std(sharps))


def cost_sweep(weights, close, open_, spy):
    """Net Sharpe under base vs high cost assumptions."""
    spy_ret = spy.pct_change().fillna(0.0)
    out = {}
    for name, tc, sl in [("base_0.5_0.2bps", 0.0005, 0.0002),
                         ("high_20_5bps", 0.0020, 0.0005),
                         ("zero_cost", 0.0, 0.0)]:
        ret = backtest.portfolio_returns_rebalance_clean(
            weights, close, open_, tc_cost=tc, slippage=sl, rebalance_freq=REBAL
        )
        fm, _ = walk_forward(ret, close, spy_ret)
        sharpes = [m["sharpe"] for m in fm
                   if m.get("sharpe") is not None and not np.isnan(m.get("sharpe", float("nan")))]
        out[name] = {
            "tc_cost": tc,
            "slippage": sl,
            "oos_sharpe": float(np.mean(sharpes)) if sharpes else float("nan"),
        }
    return out


def validation_extras(de_index, spy):
    """Supplementary validation: per-contract standalone TSM OOS Sharpe
    and TSM lookback sensitivity (guards against a single-contract or
    single-lookback driving the book result)."""
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(de_index), TRAIN, TEST, STEP)

    per_contract = {}
    for col in de_index.columns:
        sig = strategies.time_series_momentum_pure(de_index[[col]], lookback=12, skip=1)
        w = backtest.time_series_momentum_weights(
            sig, de_index[[col]], long_only=False, vol_window=63
        )
        r = backtest.portfolio_returns_rebalance_clean(
            w, de_index[[col]], de_index[[col]],
            tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        sh = [backtest.metrics(r.loc[r.index.intersection(de_index.index[c:d])]["net"])["sharpe"]
              for (_, _, c, d) in splits]
        sh = [s for s in sh if s == s]
        per_contract[col] = {
            "oos_sharpe": float(np.mean(sh)) if sh else float("nan"),
            "positive_folds": int(sum(1 for s in sh if s > 0)),
            "n_folds": len(sh),
        }

    lookbacks = {}
    for lb in [3, 6, 9, 12, 18]:
        sig = strategies.time_series_momentum_pure(de_index, lookback=lb, skip=1)
        w = backtest.time_series_momentum_weights(
            sig, de_index, long_only=False, vol_window=63
        )
        r = backtest.portfolio_returns_rebalance_clean(
            w, de_index, de_index, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBAL
        )
        sh = [backtest.metrics(r.loc[r.index.intersection(de_index.index[c:d])]["net"])["sharpe"]
              for (_, _, c, d) in splits]
        sh = [s for s in sh if s == s]
        lookbacks[f"{lb}m"] = {
            "lookback_months": lb,
            "oos_sharpe": float(np.mean(sh)) if sh else float("nan"),
            "positive_folds": int(sum(1 for s in sh if s > 0)),
            "n_folds": len(sh),
        }
    return {"per_contract_tsm": per_contract, "tsm_lookback_sensitivity": lookbacks}


def main():
    print("=" * 72)
    print("E016: TSM + Carry on a Properly-Rolled Futures Universe")
    print("=" * 72)

    panels = load_panels()
    fut_close = panels["fut_close"]
    fut_open = panels["fut_open"]
    spot_close = panels["spot_close"]
    de_index = panels["de_index"]
    carry = panels["carry"]
    carry_rroll = panels["carry_rroll"]
    spy = panels["spy"]
    seam_stats = panels["seam_stats"]

    print(f"\nLoaded: {len(de_index)} common trading days, {de_index.shape[1]} futures contracts")
    print(f"  Futures: {list(de_index.columns)}")
    print(f"  Period: {de_index.index[0].date()} to {de_index.index[-1].date()}")

    # ---- Part 1: roll-seam diagnostics ----
    print("\n" + "-" * 72)
    print("Part 1: Roll-seam detection (raw continuous contracts)")
    print("-" * 72)
    for ft, (st, cad) in FUTURES_UNIVERSE.items():
        s = seam_stats[ft]
        print(f"  {ft:<6} (vs {st:<4}) seams={s['n_seams']:<3} "
              f"median_gap={s['median_excess_gap']*100:.3f}%  "
              f"max_gap={s['max_excess_gap']*100:.2f}%  at {s['max_seam_date']}")

    # CL April-2020 case study: raw vs de-seamed returns.
    cl_raw_ret = fut_close["CL=F"].pct_change()
    r_spot = spot_close["CL=F"].reindex(fut_close.index).ffill().pct_change()
    case = {}
    for d in ["2020-04-20", "2020-04-21"]:
        ts = pd.Timestamp(d)
        if ts in cl_raw_ret.index:
            case[d] = {
                "raw_cl_return": float(cl_raw_ret.loc[ts]),
                "uso_return": float(r_spot.loc[ts]),
                "deseamed_return": float(r_spot.loc[ts]),
            }
    print("\n  CL=F April-2020 roll-wedge case study (raw vs de-seamed):")
    for d, v in case.items():
        print(f"    {d}: raw CL return {v['raw_cl_return']*100:+.1f}%  "
              f"-> de-seamed (USO proxy) {v['deseamed_return']*100:+.1f}%")

    # ---- Part 2: strategies ----
    print("\n" + "-" * 72)
    print("Part 2: Strategy construction")
    print("-" * 72)

    # TSM on RAW stitched futures (uncorrected baseline).
    tsm_sig_raw = strategies.time_series_momentum_pure(fut_close, lookback=12, skip=1)
    w_tsm_raw = backtest.time_series_momentum_weights(
        tsm_sig_raw, fut_close, long_only=False, vol_window=63
    )

    # TSM on de-seamed indices (roll-corrected).
    tsm_sig = strategies.time_series_momentum_pure(de_index, lookback=12, skip=1)
    w_tsm = backtest.time_series_momentum_weights(
        tsm_sig, de_index, long_only=False, vol_window=63
    )

    # Carry: dollar-neutral top/bottom half, inverse-vol.
    vol = de_index.pct_change().rolling(63).std().replace(0, np.nan)
    w_carry = backtest.carry_weights(carry, vol)

    # Secondary carry variant: realized roll yield (trailing seam gaps).
    w_carry_rroll = backtest.carry_weights(carry_rroll, vol)

    # 50/50 blend.
    w_blend = 0.5 * w_tsm + 0.5 * w_carry

    results = {}
    fold_metrics = {}

    print("\n  Evaluating strategies (walk-forward 504/63/63, monthly rebal, base costs)...")
    for label, weights, cl, op in [
        ("tsm_raw_stitched", w_tsm_raw, fut_close, fut_open),
        ("tsm_deseamed", w_tsm, de_index, de_index),
        ("carry_normalized_basis", w_carry, de_index, de_index),
        ("carry_realized_rollyield", w_carry_rroll, de_index, de_index),
        ("blend_tsm_carry_50_50", w_blend, de_index, de_index),
    ]:
        res, fm = evaluate(cl, op, spy, weights, label)
        results[label] = res
        fold_metrics[label] = fm
        bear = res["regime_analysis"]["bear"]["sharpe_mean"]
        print(f"    {label:<28} OOS_Sharpe={res['oos_sharpe']:.3f}  "
              f"beta={res['equity_beta']:+.3f}  corr={res['corr_spy']:+.3f}  "
              f"maxDD={res['max_drawdown']:.3f}  bear_Sh={bear:+.3f}  "
              f"turn={res['turnover']:.4f}  pos={res['positive_folds']}/{res['n_folds']}")

    # Correlation between the two carry signals (information overlap).
    c_corr = float(carry.stack().corr(carry_rroll.stack()))
    print(f"\n  Carry signal correlation (normalized basis vs realized roll yield): {c_corr:.3f}")
    results["carry_signal_correlation"] = c_corr

    # ---- Part 3: placebo validation ----
    print("\n  Blended placebo null (50 random TSM + random carry, 50/50)...")
    pm, ps = blended_placebo(de_index, spy)
    print(f"    Placebo: mean Sharpe={pm:.3f}  std={ps:.3f}  n_sim={PLACEBO_N_SIM}")
    for label in ["tsm_deseamed", "carry_normalized_basis",
                  "carry_realized_rollyield", "blend_tsm_carry_50_50"]:
        z = (results[label]["oos_sharpe"] - pm) / ps if ps > 0 else float("nan")
        results[label]["placebo_z"] = float(z)
        results[label]["placebo_mean"] = pm
        results[label]["placebo_std"] = ps
        print(f"    {label:<28} placebo z={z:.2f}")

    # ---- Part 4: cost sweep on the blend ----
    print("\n  Cost sweep (blend):")
    cs = cost_sweep(w_blend, de_index, de_index, spy)
    for name, v in cs.items():
        print(f"    {name:<16} OOS Sharpe={v['oos_sharpe']:.3f}")
    results["blend_tsm_carry_50_50"]["cost_sweep"] = cs

    # ---- Promotion gates (pre-registered) ----
    blend = results["blend_tsm_carry_50_50"]
    gates = {
        "oos_sharpe_gte_1.5": bool(blend["oos_sharpe"] >= 1.5),
        "abs_beta_lte_0.2": bool(abs(blend["equity_beta"]) <= 0.2),
        "maxdd_gte_-0.15": bool(blend["max_drawdown"] >= -0.15),
        "bear_sharpe_positive": bool(blend["regime_analysis"]["bear"]["sharpe_mean"] > 0),
        "placebo_z_gte_3": bool(blend.get("placebo_z", 0) >= 3),
    }
    print("\n  Pre-registered promotion gates (blend):")
    for g, ok in gates.items():
        print(f"    {g:<28} {'PASS' if ok else 'FAIL'}")
    gates["all_passed"] = all(v for k, v in gates.items() if k != "all_passed")

    # ---- Supplementary validation ----
    print("\n  Supplementary validation (per-contract TSM + lookback sensitivity)...")
    validation = validation_extras(de_index, spy)
    for col, v in validation["per_contract_tsm"].items():
        print(f"    {col:<6} standalone OOS Sharpe={v['oos_sharpe']:+.3f}  "
              f"pos={v['positive_folds']}/{v['n_folds']}")
    for lb, v in validation["tsm_lookback_sensitivity"].items():
        print(f"    lookback {lb:<4} OOS Sharpe={v['oos_sharpe']:+.3f}  "
              f"pos={v['positive_folds']}/{v['n_folds']}")

    # ---- Summary ----
    print("\n" + "=" * 72)
    print("E016 Summary")
    print("=" * 72)
    best = max(["tsm_deseamed", "carry_normalized_basis",
                "carry_realized_rollyield", "blend_tsm_carry_50_50"],
               key=lambda k: results[k]["oos_sharpe"])
    print(f"  Best de-seamed strategy: {best} "
          f"(OOS Sharpe={results[best]['oos_sharpe']:.3f}, z={results[best].get('placebo_z', float('nan')):.2f})")
    print(f"  Roll-methodology impact (TSM raw vs de-seamed): "
          f"{results['tsm_raw_stitched']['oos_sharpe']:.3f} -> {results['tsm_deseamed']['oos_sharpe']:.3f}")
    print(f"  Promotion gates: {'ALL PASSED' if gates['all_passed'] else 'NOT all passed'}")

    # ---- Save ----
    result = {
        "experiment": "E016",
        "timestamp": deterministic_timestamp(),
        "description": "TSM + carry on a properly-rolled 12-contract futures universe.",
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP},
        "rebalance_freq_days": REBAL,
        "universe": {
            "futures": list(FUTURES_UNIVERSE.keys()),
            "pairs": {k: v[0] for k, v in FUTURES_UNIVERSE.items()},
            "n_days": int(len(de_index)),
            "start": str(de_index.index[0].date()),
            "end": str(de_index.index[-1].date()),
        },
        "roll_methodology": {
            "detector": "futures-vs-spot excess overnight gap: calendar windows (bd 1-18 of roll month; monthly for commodities, Mar/Jun/Sep/Dec for financials) with 15bps threshold + 50% outlier rule",
            "correction": "seam-day futures returns replaced by paired spot ETF return (proxy for true underlying move); synthetic index rebuilt from de-seamed returns",
            "seam_stats": seam_stats,
            "cl_april_2020_case": case,
        },
        "tsm_config": {"lookback_months": 12, "skip_months": 1, "vol_window": 63, "long_only": False},
        "carry_config": {
            "primary": "normalized basis carry: 1 - (F/S)_t / median(F/S)_{t-252..t-1}, KMPV 2018 sign convention, cap 0.35",
            "secondary": "realized roll yield: negative trailing 252d sum of seam excess gaps (futures-vs-spot)",
            "top_frac": 0.5,
            "vol_window": 63,
        },
        "placebo": {"mean": pm, "std": ps, "n_sim": PLACEBO_N_SIM,
                    "type": "random TSM + random carry, 50/50 blend"},
        "results": results,
        "validation": validation,
        "promotion_gates": gates,
        "best_strategy": best,
    }

    out_path = os.path.join("experiments", "e016_futures_tsm_carry.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
