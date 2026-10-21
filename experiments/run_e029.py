#!/usr/bin/env python
"""E029: Fundamental accounting factors -- profitability (Novy-Marx 2013) and investment
(Titman, Wei & Xing 2008).

The E028 handoff selected fundamental factors as the next family after E026 (equity
carry / dividend yield) failed its promotion gates.  This driver implements the two
best-known fundamental-factor signals and evaluates them over the window the data
source actually supports.

DATA-SOURCE REALITY (recorded in experiments/e029_fundamental_feasibility.json):
the repo's only public fundamental source is yfinance, whose quarterly income
statements start ~2025-01-31 and balance sheets start ~2021-10-31.  A 2014-2026
walk-forward with a 504-day formation window is therefore NOT possible.  This driver
does the honest thing: it (1) reports the available window, (2) runs an in-sample
mechanism test over the window, and (3) runs a SHORT out-of-sample tail (the last
63 trading days) as the only OOS evidence.  No OOS Sharpe gate is evaluated on data
the source cannot provide; the pre-registered gates are reported as NOT-APPLICABLE
rather than silently skipped.

Pre-registered specification:
- Universe: large_liquid feasibility cohort (130 tickers), data 2014-2026.
- Signals (src/fundamentals):
  * Gross profitability (Novy-Marx 2013): TTM (Revenue - Cost Of Revenue) / Total Assets.
  * Asset growth (Titman et al. 2008): (TA_t - TA_{t-4Q}) / TA_{t-4Q}, sign flipped so
    low investment -> high signal.
  Both winsorized 1/99 and cross-sectionally z-scored per day.
- Construction PRIMARY: dollar-neutral long-short -- long top 20% by signal, short
  bottom 20%, each side inverse-vol weighted (63d) and scaled to 0.5 gross (net 0).
  Long-only top-20% is a REPORTED VARIANT.
- Weighting: inverse realized-vol (63d), monthly (21d) rebalance.
- Execution: close-to-close (primary convention v1.2.3), total-return (dividend-adjusted)
  close so dividend policy is in P&L.
- Costs: base tc=0.5bps + slippage=0.2bps.
- SEED=42.

Falsification expectation:
  FE1 (within-sample predictive content): mean |Spearman(signal[t], next-21d return[t])|
  >= 0.03 AND >= 60% of dates in the expected direction (high GP -> positive; low AG
  -> positive).  If this fails there is no within-sample signal-return link to
  motivate the factor.

Reported (NOT gated, because the window is too short for a credible OOS Sharpe):
  G1: OOS Sharpe (c2c, short tail)      >= 0.8
  G2: Placebo z (pair/cross-section)    >= 3.0
  G3: |beta_vs_SPY|                     <= 0.2
  G4: Bear-market Sharpe                > 0
  G5: Turnover (daily, monthly-exec)    <= 0.15
"""

import json
import os
import sys
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest
from src import jsonio
from src.run_experiment import deterministic_timestamp
from src import fundamentals as F

SEED = 42
UNIVERSE = [
    "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
    "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
    "BAC","BKNG","BMY","BSX","C","CAT","CCI","CDNS",
    "CHTR","CI","CL","CMCSA","CME","COF","COP","COST","CRM","CSCO",
    "CSX","CVS","CVX","DE","DHR","DIS","DOW","DXCM","EMR","EOG",
    "EQIX","ETN","EXC","FDX","FIS","FTNT","GD","GE","GILD","GM",
    "GOOG","GOOGL","GS","HD","HON","IBM","ICE","INTU","ISRG",
    "JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LLY","LMT","LOW",
    "LRCX","MA","MCD","MDLZ","MDT","META","MET","MMM","MO","MRK",
    "MS","MSFT","MU","NFLX","NKE","NOW","NVDA","ORCL","PCAR","PEP",
    "PFE","PG","PLD","PM","PNC","PYPL","QCOM","REGN","ROST","RTX",
    "SBUX","SCHW","SLB","SO","SPG","T","TGT","TJX","TMO","TMUS",
    "TSLA","TXN","UNH","UNP","UPS","USB","V","VZ","WFC",
    "WMT","XOM",
]
# WBA and BK were removed from the yfinance feed (delisted) as of 2026-10;
# they are excluded so the price panel is complete.
TC_COST = 0.0005
SLIPPAGE = 0.0002
REBAL = 21
TOP_FRAC = 0.2
VOL_WINDOW = 63
N_PLACEBO = 50

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


def portfolio_ret(weights, close, tc=TC_COST, sl=SLIPPAGE, reb=REBAL):
    return backtest.portfolio_returns_close_to_close(
        weights, close, tc_cost=tc, slippage=sl, rebalance_freq=reb
    )


def executed_turnover(weights, reb=REBAL):
    w = backtest.shift_weights(weights)
    w = backtest._rebalance_weights(w, reb)
    turn = (w.diff().abs()).sum(axis=1)
    return float(turn.mean()) if len(turn) else 0.0


def compute_dd(ret):
    ret = ret.dropna()
    if len(ret) == 0:
        return 0.0, 0
    cum = (1.0 + ret).cumprod()
    dd = cum / cum.cummax() - 1.0
    return float(dd.min()), int((dd < 0).sum())


def analyze(weights, adj, spy_ret, label):
    ret = portfolio_ret(weights, adj)
    net = ret["net"]
    is_m = backtest.metrics(net.dropna())
    beta, alpha, corr = beta_vs_benchmark(net, spy_ret)
    turn = executed_turnover(weights)
    dd, uw = compute_dd(net)
    return {
        "label": label,
        "in_sample": is_m,
        "beta_vs_spy": beta,
        "alpha_annual": alpha,
        "corr_spy": corr,
        "turnover_daily": turn,
        "max_drawdown": dd,
        "time_underwater_days": uw,
    }


def placebo_one(sig, adj, seed, long_only=False):
    rng = np.random.default_rng(seed)
    R = pd.DataFrame(rng.standard_normal(size=adj.shape),
                     index=adj.index, columns=adj.columns)
    R = R.where(sig.notna())
    w = backtest.dollar_neutral_longshort_weights(R, top_frac=TOP_FRAC)
    ret = portfolio_ret(w, adj)
    return backtest.metrics(ret["net"].dropna()).get("sharpe", 0.0)


def main():
    print("=" * 72)
    print("E029: Fundamental factors -- profitability (Novy-Marx 2013) & investment (Titman et al. 2008)")
    print("=" * 72)

    adj = data.download(UNIVERSE, start="2014-01-01", end="2026-10-11",
                        auto_adjust=True)
    adj = data.get_panel(adj, "Close").dropna(how="all")
    spy = data.get_benchmark("SPY", start="2014-01-01")["close"].reindex(adj.index).ffill()
    spy_ret = spy.pct_change().fillna(0.0)

    print(f"Loaded: {adj.shape[0]} days, {adj.shape[1]} tickers; SPY range {spy.index.min().date()}..{spy.index.max().date()}")

    print("\n[1] Fetching yfinance quarterly fundamentals (Revenue, Cost Of Revenue, Total Assets)...")
    rev, cogs, ta = F.fetch_fundamentals(UNIVERSE)
    print(f"    revenue panel: {rev.shape}, cogs: {cogs.shape}, total assets: {ta.shape}")

    # ---- feasibility gate -------------------------------------------------
    n_rev4 = int((rev.notna().sum() >= 4).sum())
    n_ta4 = int((ta.notna().sum() >= 4).sum())
    coverage = min(n_rev4, n_ta4) / len(UNIVERSE)
    earliest_rev = rev.index.min()
    earliest_ta = ta.index.min()
    latest = max(rev.index.max(), ta.index.max())
    print(f"    names with >=4 revenue quarters: {n_rev4}/{len(UNIVERSE)}")
    print(f"    names with >=4 total-assets quarters: {n_ta4}/{len(UNIVERSE)}")
    print(f"    earliest revenue report: {earliest_rev.date()}; earliest balance sheet: {earliest_ta.date()}")
    print(f"    latest report in panel: {latest.date()}")
    print(f"    signal available from ~{earliest_rev.date()} (needs 4 quarters of history); " +
          f"latest signal date ~{latest.date()}")

    # ---- signals ----------------------------------------------------------
    print("\n[2] Computing fundamental signals...")
    sig_gp = F.gross_profit_signal(rev, cogs, ta, adj)
    sig_ag = F.asset_growth_signal(ta, adj)
    sig = sig_gp * 0.5 + sig_ag * 0.5
    for name, s in (("gross_profitability", sig_gp), ("asset_growth", sig_ag), ("blend", sig)):
        nz = int(s.notna().sum().sum())
        print(f"    {name}: {s.shape[0]}d x {s.shape[1]} names, {nz} non-NaN signal cells, " +
              f"first signal date {s.dropna(how='all').index.min().date() if nz else 'n/a'}")

    # ---- primary: dollar-neutral long-short --------------------------------
    print("\n[3] PRIMARY: dollar-neutral long-short (top 20% long / bottom 20% short)")

    results = {}
    for tag, s in (("gross_profitability", sig_gp), ("asset_growth", sig_ag), ("blend", sig)):
        w = backtest.dollar_neutral_longshort_weights(s, top_frac=TOP_FRAC)
        res = analyze(w, adj, spy_ret, f"dn_{tag}")
        results[f"primary_{tag}"] = res
        print(f"    {tag}: IS Sharpe={res['in_sample']['sharpe']:.3f}  " +
              f"beta={res['beta_vs_spy']:.3f}  turn={res['turnover_daily']:.4f}  " +
              f"maxDD={res['max_drawdown']:.3f}")

    # ---- short OOS tail (last 63 trading days) -----------------------------
    print("\n[4] SHORT OOS tail: last 63 trading days (only OOS evidence available)")
    tail_start = adj.index[-63]
    oos_rows = []
    for tag, s in (("gross_profitability", sig_gp), ("asset_growth", sig_ag), ("blend", sig)):
        w = backtest.dollar_neutral_longshort_weights(s, top_frac=TOP_FRAC)
        ret = portfolio_ret(w, adj)
        net = ret["net"].loc[ret.index >= tail_start].dropna()
        m = backtest.metrics(net)
        beta, alpha, corr = beta_vs_benchmark(net, spy_ret.loc[spy_ret.index >= tail_start])
        oos_rows.append({
            "signal": tag,
            "tail_start": str(tail_start.date()),
            "n_days": int(len(net)),
            "sharpe": m.get("sharpe", float("nan")),
            "annual_return": m.get("annual_return", float("nan")),
            "max_drawdown": m.get("max_drawdown", float("nan")),
            "beta_vs_spy": beta,
            "turnover_daily": executed_turnover(w),
        })
        print(f"    {tag}: OOS Sharpe={oos_rows[-1]['sharpe']:.3f}  " +
              f"beta={beta:.3f}  n_days={oos_rows[-1]['n_days']}")
    results["oos_short_tail"] = oos_rows

    # ---- placebo null (50 sims) --------------------------------------------
    print(f"\n[5] Placebo null ({N_PLACEBO} sims, DN, i.i.d. random signal)...")
    placebo_rows = {}
    for tag, s in (("gross_profitability", sig_gp), ("asset_growth", sig_ag), ("blend", sig)):
        sh = [placebo_one(s, adj, SEED + i) for i in range(N_PLACEBO)]
        pm = float(np.mean(sh))
        ps = float(np.std(sh, ddof=0)) or 1.0
        real = results[f"primary_{tag}"]["in_sample"]["sharpe"]
        z = (real - pm) / ps
        placebo_rows[tag] = {"mean_sharpe": pm, "std_sharpe": ps, "placebo_z": z,
                             "sharpe_list": sh}
        print(f"    {tag}: placebo mean={pm:.4f} std={ps:.4f}  z={z:.3f}")

    # ---- FE1: within-sample predictive content --------------------------------
    print("\n[6] Falsification FE1 (within-sample predictive content)...")
    fwd = adj.shift(-21) / adj - 1.0
    fe1 = {}
    for tag, s in (("gross_profitability", sig_gp), ("asset_growth", sig_ag), ("blend", sig)):
        rho = F.row_spearman(s, fwd)
        rho = rho[~np.isnan(rho)]
        mean_abs = float(np.mean(np.abs(rho))) if len(rho) else float("nan")
        # expected direction: GP high -> positive; AG low (signal high) -> positive
        frac_pos = float(np.mean(rho > 0)) if len(rho) else float("nan")
        fe1[tag] = {
            "fe1_mean_abs_spearman": mean_abs,
            "fe1_frac_positive": frac_pos,
            "fe1_n_dates": int(len(rho)),
            "fe1_gate_mean_abs_ge_0_03": bool(mean_abs >= 0.03) if np.isfinite(mean_abs) else False,
            "fe1_gate_frac_pos_ge_0_60": bool(frac_pos >= 0.60) if np.isfinite(frac_pos) else False,
        }
        print(f"    {tag}: mean|Spearman|={mean_abs:.4f}  frac_positive={frac_pos:.3f}  " +
              f"(n={len(rho)})")
    results["falsification"] = fe1

    # ---- reported gates (NOT gated: window too short for a credible OOS Sharpe) -
    print("\n[7] Reported promotion gates (NOT APPLICABLE as OOS gates; reported for completeness)")
    gates = {}
    for tag in ["gross_profitability", "asset_growth", "blend"]:
        real_sh = results[f"primary_{tag}"]["in_sample"]["sharpe"]
        z = placebo_rows[tag]["placebo_z"]
        beta = results[f"primary_{tag}"]["beta_vs_spy"]
        turn = results[f"primary_{tag}"]["turnover_daily"]
        oos_sh = next(r["sharpe"] for r in results["oos_short_tail"] if r["signal"] == tag)
        gates[tag] = {
            "G1_oos_sharpe_ge_0.8": {"value": oos_sh, "threshold": 0.8,
                                      "pass": bool(oos_sh >= 0.8)},
            "G2_placebo_z_ge_3.0": {"value": z, "threshold": 3.0,
                                     "pass": bool(z >= 3.0)},
            "G3_abs_beta_le_0.2": {"value": abs(beta), "threshold": 0.2,
                                   "pass": bool(abs(beta) <= 0.2)},
            "G5_turnover_le_0.15": {"value": turn, "threshold": 0.15,
                                     "pass": bool(turn <= 0.15)},
        }
        n_pass = sum(1 for g in gates[tag].values() if g["pass"])
        print(f"    {tag}: {n_pass}/4 reported gates pass (G4 bear not evaluable on this window)")
    results["gates"] = gates

    # ---- decision -----------------------------------------------------------
    # The honest decision rule for E029: the data source cannot support the
    # pre-registered 2014-2026 walk-forward, so no factor can be promoted on OOS
    # evidence.  The decision is therefore DATA-INFEASIBLE unless FE1 (the
    # within-sample mechanism test) passes, which is the only credible evidence
    # this source can provide.
    fe1_pass = all(
        fe1[t]["fe1_gate_mean_abs_ge_0_03"] and fe1[t]["fe1_gate_frac_pos_ge_0_60"]
        for t in ("gross_profitability", "asset_growth", "blend")
    )
    decision = "DATA-INFEASIBLE"
    if fe1_pass:
        decision = "FE1_PASS_NO_OOS_PROMOTION"
    print(f"\nFE1 passes for all three signals: {fe1_pass}")
    print(f"DECISION: {decision}")
    print("    (yfinance fundamentals cannot support a 2014-2026 walk-forward; " +
          "no OOS Sharpe gate is evaluated.  See experiments/e029_fundamental_feasibility.json.)")

    result = {
        "experiment": "E029",
        "timestamp": deterministic_timestamp(),
        "data_source": "yfinance (only public fundamental source available in this repo)",
        "feasibility": {
            "n_universe": len(UNIVERSE),
            "n_with_4_rev_quarters": n_rev4,
            "n_with_4_ta_quarters": n_ta4,
            "coverage_frac": coverage,
            "earliest_revenue_report": str(earliest_rev.date()),
            "earliest_balance_sheet": str(earliest_ta.date()),
            "latest_report_in_panel": str(latest.date()),
            "verdict": "DATA-INFEASIBLE_FOR_2014_2026_WALK_FORWARD",
            "detail": "yfinance quarterly income statements start ~2025-01-31 and " +
                       "balance sheets start ~2021-10-31; a 504-day formation window " +
                       "before the first OOS fold is not available.  Only an in-sample " +
                       "mechanism test plus a short 63-day OOS tail is possible.",
        },
        "pre_registered": {
            "signals": ["gross_profitability_novy_marx_2013", "asset_growth_titman_wei_xing_2008"],
            "primary_construction": "dollar_neutral_long_short_top20_pct",
            "variant": "long_only_top_quintile (REPORTED, not run: DN is the primary)",
            "vol_window": VOL_WINDOW,
            "rebalance_freq": REBAL,
            "execution": "close_to_close (primary convention v1.2.3)",
            "returns": "total_return (dividend-adjusted close)",
            "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
            "placebo": {"n_sim": N_PLACEBO, "seed": SEED},
            "fe1": "mean|Spearman(signal[t], next-21d ret[t])| >= 0.03 AND >= 60% positive",
            "gates_reported_not_gated": [
                "G1: OOS Sharpe (c2c, short 63d tail) >= 0.8 -- NOT APPLICABLE",
                "G2: Placebo z >= 3.0 -- reported only",
                "G3: |beta vs SPY| <= 0.2 -- reported only",
                "G4: Bear-market Sharpe > 0 -- NOT EVALUABLE on this window",
                "G5: Turnover (daily, monthly-exec) <= 0.15 -- reported only",
            ],
        },
        "primary": {k: v for k, v in results.items() if k.startswith("primary_")},
        "oos_short_tail": results["oos_short_tail"],
        "placebo": placebo_rows,
        "falsification": results["falsification"],
        "gates": results["gates"],
        "decision": decision,
    }

    out_path = os.path.join("experiments", "e029_fundamental_factors.json")
    os.makedirs("experiments", exist_ok=True)
    with open(out_path, "w") as f:
        jsonio.dump(result, f, indent=2, default=str)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
