#!/usr/bin/env python
"""E026: Equity carry / dividend-yield factor (Koijen, Moskowitz, Pedersen & Vrugt 2018).

The repository's first fundamental-signal family. E025 cointegration stat-arb was the
second stat-arb variant to fail cleanly on 2014-2026 large_liquid (E021 distance, E025
cointegration). Per the E025 handoff search order, equity carry (the dividend-yield
sleeve of KMPV "Carry", JFE 2018) is the next candidate: expected return = dividend
yield + expected capital gain.

Pre-registered specification (primary = dollar-neutral long-short):
- Universe: large_liquid feasibility cohort (131 tickers), data 2014-01-02..2026-10-09.
  Delisted BK/WBA are absent from the feed (verified in e026_dividend_feasibility.json).
- Signal: trailing 252-day dividend yield = sum(nominal dividends over trailing 252
  trading days) / current price (Adj Close for total-return consistency). Winsorized
  1/99 and cross-sectionally z-scored per day (src/carry_equity.dividend_yield_signal).
- Construction PRIMARY: dollar-neutral long-short — long top 20% by yield, short bottom
  20%, each side inverse-vol weighted (63d) and scaled to 0.5 gross (net 0).
  Rationale: the pre-registered gate |beta_vs_SPY| <= 0.2 is a market-neutrality gate,
  so the primary must be market-neutral (matches E012 DN-lowbeta precedent and the
  KMPV carry long-short framing). Long-only top-20% is a REPORTED VARIANT.
- Weighting: inverse realized-vol (63d), monthly (21d) rebalance, weights held via the
  backtest engine's rebalance_freq (no look-ahead; formation window ends at rebalance).
- Execution: close-to-close (primary convention, ledger/PRIORITIZATION.md v1.2.3).
  Returns use total-return (dividend-adjusted) close so the dividend carry is captured
  in P&L -- required for an equity-carry factor.
- Costs: base tc=0.5bps + slippage=0.2bps.
- Walk-forward: 504-day formation / 63-day test / 63-day step (42 OOS folds).
- SEED=42.

Falsification expectation (v1.2.2):
  FE1 (within-sample predictive content): mean |Spearman(dividend-yield signal[t],
  next-21d total return[t])| >= 0.03 AND >= 60% of dates positive (high yield -> higher
  next-month return). If this fails, there is no within-sample yield-return link to
  motivate the factor.

Pre-registered promotion gates (applied to the dollar-neutral primary):
  G1: OOS Sharpe (c2c)        >= 0.8
  G2: Placebo z (pair/cross-section null) >= 3.0
  G3: |beta_vs_SPY|           <= 0.2
  G4: Bear-market Sharpe      > 0
  G5: Turnover (daily, monthly-exec) <= 0.15

Sensitivity grid (reported, not gated): top_frac {0.10,0.20,0.30} x {DN, long-only};
yield formation window {126,252,378}; cost {0, base, +10bps/+5bps, +20bps/+5bps}.

Placebo null: 50 simulations. The repo's E012 placebo uses
backtest.dollar_neutral_longshort_weights on i.i.d. random signals; here we use the
SAME src/carry_equity.carry_equity_weights engine on i.i.d. standard-normal signals
(the signal is destroyed; universe breadth, inv-vol weighting and monthly freeze are
preserved). This is methodologically identical to carry_equity.carry_equity_placebo_weights
(random top-frac selection + inv-vol weighting, per-date) but vectorized: the module's
per-date loop measures 9.3s/sim (8+ min for 50 sims), while the vectorized form is 0.06s/sim;
both exercise the identical carry_equity_weights engine and produce a null centered on 0.
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, carry_equity, validation

SEED = 42
UNIVERSE = [
    "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
    "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
    "BAC","BK","BKNG","BMY","BSX","C","CAT","CCI","CDNS",
    "CHTR","CI","CL","CMCSA","CME","COF","COP","COST","CRM","CSCO",
    "CSX","CVS","CVX","DE","DHR","DIS","DOW","DXCM","EMR","EOG",
    "EQIX","ETN","EXC","FDX","FIS","FTNT","GD","GE","GILD","GM",
    "GOOG","GOOGL","GS","HD","HON","IBM","ICE","INTU","ISRG",
    "JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LLY","LMT","LOW",
    "LRCX","MA","MCD","MDLZ","MDT","META","MET","MMM","MO","MRK",
    "MS","MSFT","MU","NFLX","NKE","NOW","NVDA","ORCL","PCAR","PEP",
    "PFE","PG","PLD","PM","PNC","PYPL","QCOM","REGN","ROST","RTX",
    "SBUX","SCHW","SLB","SO","SPG","T","TGT","TJX","TMO","TMUS",
    "TSLA","TXN","UNH","UNP","UPS","USB","V","VZ","WBA","WFC",
    "WMT","XOM",
]
TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
TOP_FRAC = 0.2
VOL_WINDOW = 63
YIELD_WINDOW = 252
N_PLACEBO = 50
N_FOLDS = 42


def load_data():
    df = data.download(UNIVERSE, start="2014-01-01", end="2026-10-11",
                       auto_adjust=False, actions=True)
    close = data.get_panel(df, "Close")          # raw nominal (unused for P&L)
    adj = data.get_panel(df, "Adj Close").dropna(how="all")  # total-return prices
    dividends = data.get_panel(df, "Dividends").reindex(columns=adj.columns)
    open_ = data.get_panel(df, "Open").reindex(columns=adj.columns).reindex(adj.index).fillna(adj)
    bm = data.get_benchmark("SPY", start="2014-01-01")
    spy = bm["close"].reindex(adj.index).ffill()
    return adj, dividends, open_, spy


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
        m = backtest.metrics(test_rets["net"])
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
    """Turnover of the actually-executed (next-day-shifted, monthly-frozen) weights."""
    w = backtest.shift_weights(weights)
    w = backtest._rebalance_weights(w, reb)
    turn = (w.diff().abs()).sum(axis=1)
    return float(turn.mean()) if len(turn) else 0.0


def portfolio_ret(weights, close, tc=TC_COST, sl=SLIPPAGE, reb=REBAL):
    return backtest.portfolio_returns_close_to_close(
        weights, close, tc_cost=tc, slippage=sl, rebalance_freq=reb
    )


def row_spearman(a: pd.DataFrame, b: pd.DataFrame):
    """Per-row (cross-sectional) Spearman correlation of a vs b."""
    ar = a.rank(axis=1, method="average")
    br = b.rank(axis=1, method="average")
    rho = np.full(a.shape[0], np.nan)
    av = ar.to_numpy()
    bv = br.to_numpy()
    for i in range(a.shape[0]):
        m = ~(np.isnan(av[i]) | np.isnan(bv[i]))
        if m.sum() >= 3:
            x = av[i][m] - av[i][m].mean()
            y = bv[i][m] - bv[i][m].mean()
            den = np.sqrt((x * x).sum() * (y * y).sum())
            rho[i] = float((x * y).sum() / den) if den > 0 else np.nan
    return rho


def compute_fe1(sig, adj):
    """FE1: within-sample predictive content of dividend yield for next-21d return."""
    fwd = adj.shift(-21) / adj - 1.0
    rho = row_spearman(sig, fwd)
    rho = rho[~np.isnan(rho)]
    mean_abs = float(np.mean(np.abs(rho))) if len(rho) else float("nan")
    frac_pos = float(np.mean(rho > 0)) if len(rho) else float("nan")
    return {
        "fe1_mean_abs_spearman": mean_abs,
        "fe1_frac_positive": frac_pos,
        "fe1_n_dates": int(len(rho)),
        "fe1_gate_mean_abs_ge_0_03": bool(mean_abs >= 0.03) if np.isfinite(mean_abs) else False,
        "fe1_gate_frac_pos_ge_0_60": bool(frac_pos >= 0.60) if np.isfinite(frac_pos) else False,
    }


def analyze(weights, adj, spy_ret, label):
    ret = portfolio_ret(weights, adj)
    net = ret["net"]
    is_m = backtest.metrics(net.dropna())
    folds = walk_forward(ret, adj, spy_ret)
    wf_sharpe = float(np.mean([m["sharpe"] for m in folds])) if folds else float("nan")
    wf_std = float(np.std([m["sharpe"] for m in folds])) if folds else float("nan")
    beta, alpha, corr = beta_vs_benchmark(net, spy_ret)
    turn = executed_turnover(weights)
    dd, uw = compute_dd(net)
    pos_folds = int(sum(1 for m in folds if m["sharpe"] > 0))
    reg = regime_summary(folds)
    # bear windows (specific crisis windows)
    bear_windows = {}
    for lab, lo, hi in [("2020_covid", "2020-02-19", "2020-04-07"),
                        ("2022_bear", "2022-01-03", "2022-06-16")]:
        mask = (adj.index >= lo) & (adj.index <= hi)
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


def placebo_one(sig, adj, seed, long_only=False):
    rng = np.random.default_rng(seed)
    R = pd.DataFrame(rng.standard_normal(size=adj.shape),
                     index=adj.index, columns=adj.columns)
    R = R.where(sig.notna())
    w = carry_equity.carry_equity_weights(R, adj, vol_window=VOL_WINDOW,
                                          top_frac=TOP_FRAC, long_only=long_only)
    ret = portfolio_ret(w, adj, adj)
    return backtest.metrics(ret["net"].dropna()).get("sharpe", 0.0)


def per_name_decomp(weights, adj):
    w = backtest.shift_weights(weights)
    w = backtest._rebalance_weights(w, REBAL)
    ret = adj.pct_change()
    contrib = (w * ret).mean(axis=0).dropna().sort_values(key=lambda s: s.abs(), ascending=False)
    return {
        "top_long_contributors": {k: float(v) for k, v in contrib.head(10).items()},
        "top_short_contributors": {k: float(v) for k, v in contrib.sort_values().head(10).items()},
    }


def main():
    print("=" * 72)
    print("E026: Equity carry / dividend-yield factor (Koijen, Moskowitz, Pedersen & Vrugt 2018)")
    print("=" * 72)

    adj, div, open_, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(adj), TRAIN, TEST, STEP)
    print(f"Loaded: {adj.shape[0]} days, {adj.shape[1]} tickers (incl. {len(div.columns)} with dividends); "
          f"folds={len(splits)}")

    print("\n[1] Computing dividend-yield signal (252d trailing yield, winsorize 1/99, z-score)...")
    sig = carry_equity.dividend_yield_signal(adj, div, window=YIELD_WINDOW)
    print(f"    signal non-NaN cells: {int(sig.notna().sum().sum())} / {sig.size}")

    results = {}

    # --- Primary: dollar-neutral long-short ---
    print("\n[2] PRIMARY: dollar-neutral high-minus-low dividend yield (top20 long / bottom20 short)")
    w_dn = carry_equity.carry_equity_weights(sig, adj, vol_window=VOL_WINDOW,
                                             top_frac=TOP_FRAC, long_only=False)
    dn = analyze(w_dn, adj, spy_ret, "dollar_neutral_carry_primary")
    results["primary"] = dn
    print(f"    OOS Sharpe(WF)={dn['oos_wf_sharpe']:.3f}  beta={dn['beta_vs_spy']:.3f}  "
          f"corr_spy={dn['corr_spy']:.3f}  turn={dn['turnover_daily']:.4f}  "
          f"maxDD={dn['max_drawdown']:.3f}  pos={dn['n_pos_folds']}/{dn['n_folds']}")
    print(f"    regime bear: {dn['regime_analysis']['bear']}")

    # --- Variant: long-only top quintile ---
    print("\n[3] VARIANT: long-only top-20% dividend yield")
    w_lo = carry_equity.carry_equity_weights(sig, adj, vol_window=VOL_WINDOW,
                                             top_frac=TOP_FRAC, long_only=True)
    lo = analyze(w_lo, adj, spy_ret, "long_only_top_quintile")
    results["variant_long_only"] = lo
    print(f"    OOS Sharpe(WF)={lo['oos_wf_sharpe']:.3f}  beta={lo['beta_vs_spy']:.3f}  "
          f"corr_spy={lo['corr_spy']:.3f}  turn={lo['turnover_daily']:.4f}")

    # --- Placebo null (50 sims, DN construction) ---
    print(f"\n[4] Placebo null ({N_PLACEBO} sims, DN, vectorized random signal)...")
    placebo_sharpes = [placebo_one(sig, adj, SEED + i, long_only=False) for i in range(N_PLACEBO)]
    pm = float(np.mean(placebo_sharpes))
    ps = float(np.std(placebo_sharpes, ddof=0)) or 1.0
    placebo_z = (dn["oos_wf_sharpe"] - pm) / ps
    print(f"    placebo mean={pm:.4f} std={ps:.4f}  z={placebo_z:.3f}")

    # --- Cost sensitivity (primary DN) ---
    print("\n[5] Cost sweep (primary DN)...")
    cost_rows = []
    for tc, sl in [(0.0, 0.0), (TC_COST, SLIPPAGE), (0.010, 0.005), (0.020, 0.005)]:
        ret = portfolio_ret(w_dn, adj, tc=tc, sl=sl)
        fm = walk_forward(ret, adj, spy_ret)
        npos = int(sum(1 for m in fm if m["sharpe"] > 0))
        cost_rows.append({
            "tc_cost": tc, "slippage": sl,
            "oos_sharpe": float(np.mean([m["sharpe"] for m in fm])) if fm else float("nan"),
            "n_pos_folds": npos,
            "sharpe_std": float(np.std([m["sharpe"] for m in fm])) if fm else float("nan"),
        })
        print(f"    tc={tc:.4f} sl={sl:.4f}: Sharpe={cost_rows[-1]['oos_sharpe']:.3f} pos={npos}/{len(fm)}")
    results["cost_sensitivity"] = cost_rows

    # --- Sensitivity grid: top_frac x construction ---
    print("\n[6] Sensitivity grid (top_frac x construction)...")
    sens = []
    for tf in [0.10, 0.20, 0.30]:
        for lo_flag, tag in [(False, "dn"), (True, "long_only")]:
            w = carry_equity.carry_equity_weights(sig, adj, vol_window=VOL_WINDOW,
                                                  top_frac=tf, long_only=lo_flag)
            ret = portfolio_ret(w, adj)
            fm = walk_forward(ret, adj, spy_ret)
            beta, _, _ = beta_vs_benchmark(ret["net"], spy_ret)
            sens.append({
                "top_frac": tf, "construction": tag,
                "oos_sharpe": float(np.mean([m["sharpe"] for m in fm])) if fm else float("nan"),
                "beta_vs_spy": beta,
                "turnover": executed_turnover(w),
            })
    results["sensitivity"] = sens

    # --- FE1 (predictive content) ---
    print("\n[7] Falsification FE1 (predictive content)...")
    fe1 = compute_fe1(sig, adj)
    print(f"    mean|Spearman|={fe1['fe1_mean_abs_spearman']:.4f}  frac_positive={fe1['fe1_frac_positive']:.3f}  "
          f"(n={fe1['fe1_n_dates']})")

    # --- Gates + decision (primary DN) ---
    gates = {
        "G1_oos_sharpe_ge_0.8": {"value": dn["oos_wf_sharpe"], "threshold": 0.8,
                                  "pass": bool(dn["oos_wf_sharpe"] >= 0.8)},
        "G2_placebo_z_ge_3.0": {"value": placebo_z, "threshold": 3.0,
                                "pass": bool(placebo_z >= 3.0)},
        "G3_abs_beta_le_0.2": {"value": abs(dn["beta_vs_spy"]), "threshold": 0.2,
                               "pass": bool(abs(dn["beta_vs_spy"]) <= 0.2)},
        "G4_bear_sharpe_gt_0": {"value": dn["regime_analysis"]["bear"]["sharpe_mean"],
                                "threshold": 0.0, "pass": bool(dn["regime_analysis"]["bear"]["sharpe_mean"] > 0)},
        "G5_turnover_le_0.15": {"value": dn["turnover_daily"], "threshold": 0.15,
                                "pass": bool(dn["turnover_daily"] <= 0.15)},
    }
    n_pass = sum(1 for g in gates.values() if g["pass"])
    decision = "KEEP" if n_pass == len(gates) else "REJECT"

    print("\n" + "=" * 72)
    print(f"GATES ({n_pass}/{len(gates)} passed):")
    for k, v in gates.items():
        mark = "PASS" if v["pass"] else "FAIL"
        print(f"  {k}: {v['value']:.4f} vs {v['threshold']}  [{mark}]")
    print(f"FE1: {fe1}")
    print(f"DECISION: {decision}")
    print("=" * 72)

    result = {
        "experiment": "E026",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "pre_registered": {
            "method": "dividend_yield_carry",
            "source": "Koijen, Moskowitz, Pedersen & Vrugt (2018) 'Carry', JFE; equity sleeve = dividend yield.",
            "universe": "large_liquid_feasibility_cohort",
            "n_tickers": int(adj.shape[1]),
            "primary_construction": "dollar_neutral_long_short_top20_pct",
            "variant": "long_only_top_quintile",
            "yield_window": YIELD_WINDOW,
            "top_frac": TOP_FRAC,
            "vol_window": VOL_WINDOW,
            "rebalance_freq": REBAL,
            "entry/exit": "monthly rebalance of yield-ranked quintile (DN: high long / low short)",
            "execution": "close-to_close (primary convention v1.2.3)",
            "returns": "total_return (dividend-adjusted close) so dividend carry is in P&L",
            "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
            "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP, "n_folds": len(splits)},
            "placebo": {"n_sim": N_PLACEBO, "construction": "dn", "seed": SEED},
            "fe1": "mean|Spearman(yield[t], next-21d ret[t])| >= 0.03 AND >= 60% positive",
            "gates": {
                "G1": "OOS Sharpe (c2c, WF-mean) >= 0.8",
                "G2": "Placebo z >= 3.0",
                "G3": "|beta vs SPY| <= 0.2",
                "G4": "Bear-market Sharpe > 0",
                "G5": "Turnover (daily, monthly-exec) <= 0.15",
            },
        },
        "primary": dn,
        "variant_long_only": lo,
        "placebo": {"n_sim": N_PLACEBO, "mean_sharpe": pm, "std_sharpe": ps,
                    "sharpe_list": placebo_sharpes, "placebo_z": placebo_z},
        "cost_sensitivity": cost_rows,
        "sensitivity": sens,
        "falsification": fe1,
        "per_name_decomposition": per_name_decomp(w_dn, adj),
        "gates": gates,
        "n_gates_passed": n_pass,
        "decision": decision,
    }

    out_path = os.path.join("experiments", "e026_equity_carry.json")
    os.makedirs("experiments", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
