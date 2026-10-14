#!/usr/bin/env python
"""E027: Idiosyncratic-Volatility Anomaly (Ang, Hodrick, Xing & Zhang 2006)

Pre-registered specification:
- Source: Ang, A., Hodrick, R.J., Xing, Y. & Zhang, X. (2006),
  "The Cross-Section of Volatility and Expected Returns",
  Journal of Financial Economics 82(1): 259-292.
- Factor model: CAPM (daily stock return ~ SPY return), trailing 252 trading days
- IVOL = residual standard deviation from the regression (annualized)
- Monthly (21d) rebalance, dollar-neutral long-short
- Long bottom quintile (low IVOL), short top quintile (high IVOL)
- Inverse-vol weighted across active names
- Close-to-close execution convention (primary per v1.2.3)
- Costs: tc=0.5bps + slippage=0.2bps
- Universe: large_liquid, walk-forward 504/63/63, 42 OOS folds

Falsification expectations (FE, v1.2.2 requirement):
- FE1 (within-sample predictive content): mean |Spearman(IVOL[t], next-month return[t])| >= 0.03
  AND >= 60% negative (high IVOL -> lower next-month return).
  If FE1 fails, the IVOL mechanism has no within-sample evidence on this universe/sample.

Gates (promote if all satisfied):
- G1: OOS Sharpe (c2c) >= 0.8
- G2: Placebo z >= 3.0
- G3: |beta vs SPY| <= 0.2
- G4: Bear-market Sharpe > 0
- G5: Turnover (daily) <= 0.15

Implementation gaps vs paper (recorded, not hidden):
- Paper: 1963-2000 US equities, CRSP, FF3 factor model, value-weighted quintiles,
  equal-weight within quintile, monthly rebalance.
- This test: 2014-2026 large_liquid (130 mega-caps), CAPM only (SPY), inverse-vol
  weighting, dollar-neutral, monthly rebalance, close-to-close convention.
- The IVOL anomaly is widely reported as era-dependent (strong pre-2000,
  weak/absent post-2000); FE1 screens this before full walk-forward.
"""

import json
import os
from datetime import datetime
from typing import Dict, List

import numpy as np
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data, backtest, ivol
from src.run_experiment import deterministic_timestamp

SEED = 42
np.random.seed(SEED)

UNIVERSE = [
    "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
    "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
    "BAC","BK","BKNG","BMY","BRK-B","BSX","C","CAT","CCI","CDNS",
    "CHTR","CI","CL","CMCSA","CME","COF","COP","COST","CRM","CSCO",
    "CSX","CVS","CVX","DE","DHR","DIS","DOW","DXCM","EMR","EOG",
    "EQIX","ETN","EXC","FDX","FIS","FTNT","GD","GE","GILD","GM",
    "GOOG","GOOGL","GS","HD","HON","IBM","ICE","INTC","INTU","ISRG",
    "JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LLY","LMT","LOW",
    "LRCX","MA","MCD","MDLZ","MDT","META","MET","MMM","MO","MRK",
    "MS","MSFT","MU","NFLX","NKE","NOW","NVDA","ORCL","PCAR","PEP",
    "PFE","PG","PLD","PM","PNC","PYPL","QCOM","REGN","ROST","RTX",
    "SBUX","SCHW","SLB","SO","SPG","T","TGT","TJX","TMO","TMUS",
    "TSLA","TXN","UNH","UNP","UPS","USB","V","VZ","WBA","WFC",
    "WMT","XOM"
]

FORMATION_WINDOW = 252
VOL_WINDOW = 63
TOP_FRAC = 0.2
REBALANCE_FREQ = 21
TC_COST = 0.0005
SLIPPAGE = 0.0002

def main():
    # Download data
    df = data.download(UNIVERSE, start="2014-01-01")
    close = data.get_panel(df, "Close")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)

    close = close.dropna(how="all")
    open_ = open_.reindex(close.index).fillna(close)

    # Benchmark
    bm = data.get_benchmark("SPY", start="2014-01-01")
    spy = bm["close"].reindex(close.index).ffill()

    # Compute IVOL signal
    ivol_signal = ivol.idiosyncratic_vol_signal(
        close, spy, window=FORMATION_WINDOW, skip=1
    )

    # Falsification expectation (FE1) - computed BEFORE walk-forward
    falsification = ivol.compute_falsification(close, spy, ivol_signal, window=FORMATION_WINDOW)

    print("Falsification (FE1):", json.dumps(falsification, indent=2, default=str))

    # Compute weights
    weights = ivol.ivol_weights(
        ivol_signal, close, vol_window=VOL_WINDOW, top_frac=TOP_FRAC
    )

    # Returns (close-to-close convention, primary per v1.2.3)
    rets = backtest.portfolio_returns_close_to_close(
        weights, close, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBALANCE_FREQ
    )

    turnover_avg = backtest.average_turnover(weights)

    # Benchmark returns
    bm_ret = spy.pct_change().fillna(0.0)
    common = rets.index.intersection(bm_ret.index)
    rets = rets.loc[common]
    bm_ret = bm_ret.loc[common]

    strat_metrics = backtest.metrics(rets["net"])

    # Beta vs SPY
    net = rets["net"]
    n = len(net)
    if n > 2 and bm_ret.std() > 0:
        A = np.vstack([np.ones(n), bm_ret.values]).T
        alpha, beta_coef = np.linalg.lstsq(A, net.values, rcond=None)[0]
        corr = float(np.corrcoef(net.values, bm_ret.values)[0, 1])
    else:
        alpha, beta_coef, corr = np.nan, np.nan, np.nan

    # Walk-forward OOS
    splits = backtest.walk_forward_splits(len(close), 504, 63, 63)
    oos_results = []
    for i, (tr_s, tr_e, te_s, te_e) in enumerate(splits):
        test_idx = close.index[te_s:te_e]
        test_rets = rets.loc[rets.index.intersection(test_idx)]
        if len(test_rets) > 0:
            m = backtest.metrics(test_rets["net"])
            m["fold"] = i
            oos_results.append(m)

    oos_sharpe = float(np.mean([m["sharpe"] for m in oos_results])) if oos_results else np.nan

    # Placebo null
    placebo_weights_list = ivol.ivol_placebo_weights(
        ivol_signal, close, vol_window=VOL_WINDOW, top_frac=TOP_FRAC,
        seed=SEED, n_sim=50
    )
    placebo_sharpes = []
    for pw in placebo_weights_list:
        pr = backtest.portfolio_returns_close_to_close(
            pw, close, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBALANCE_FREQ
        )
        pr = pr.loc[common]
        pm = backtest.metrics(pr["net"])
        placebo_sharpes.append(pm["sharpe"])

    placebo_mean = float(np.mean(placebo_sharpes)) if placebo_sharpes else 0.0
    placebo_std = float(np.std(placebo_sharpes, ddof=0)) if len(placebo_sharpes) > 0 else 1.0
    placebo_z = (oos_sharpe - placebo_mean) / placebo_std if placebo_std > 0 else np.nan

    # Regime analysis: bear folds (SPY return < -2% over test period)
    bear_sharpes = []
    for m in oos_results:
        # Get SPY return for this fold
        test_idx = close.index[m["fold"] * 63 + 504 : m["fold"] * 63 + 504 + 63]
        if len(test_idx) > 0:
            spy_fold = spy.loc[spy.index.intersection(test_idx)]
            if len(spy_fold) > 1:
                spy_ret = spy_fold.iloc[-1] / spy_fold.iloc[0] - 1
                if spy_ret < -0.02:
                    bear_sharpes.append(m["sharpe"])

    bear_sharpe = float(np.mean(bear_sharpes)) if bear_sharpes else np.nan

    # Cost sensitivity
    cost_scenarios = [
        (0.0, 0.0),
        (TC_COST, SLIPPAGE),
        (0.0010, 0.0005),
        (0.0020, 0.0005),
    ]
    cost_sensitivity = {}
    for tc, sl in cost_scenarios:
        r = backtest.portfolio_returns_close_to_close(
            weights, close, tc_cost=tc, slippage=sl, rebalance_freq=REBALANCE_FREQ
        )
        r = r.loc[common]
        m = backtest.metrics(r["net"])
        cost_sensitivity[f"tc{tc}_sl{sl}"] = m["sharpe"]

    # Sensitivity grid (top_frac only for primary run)
    sensitivity = {}
    for tf in [0.10, 0.20, 0.30]:
        w = ivol.ivol_weights(
            ivol_signal, close, vol_window=VOL_WINDOW, top_frac=tf
        )
        r = backtest.portfolio_returns_close_to_close(
            w, close, tc_cost=TC_COST, slippage=SLIPPAGE, rebalance_freq=REBALANCE_FREQ
        )
        r = r.loc[common]
        m = backtest.metrics(r["net"])
        sensitivity[f"top_frac_{tf}"] = m["sharpe"]

    # Compile result
    result = {
        "experiment": "E027",
        "timestamp": deterministic_timestamp(),
        "pre_registered": {
            "source": "Ang, Hodrick, Xing & Zhang (2006) JFE",
            "factor_model": "CAPM (SPY)",
            "formation_window": FORMATION_WINDOW,
            "vol_window": VOL_WINDOW,
            "top_frac": TOP_FRAC,
            "rebalance_freq": REBALANCE_FREQ,
            "execution_convention": "close_to_close",
            "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
            "gates": {
                "G1_oos_sharpe_c2c": 0.8,
                "G2_placebo_z": 3.0,
                "G3_abs_beta": 0.2,
                "G4_bear_sharpe_gt_0": True,
                "G5_turnover": 0.15,
            },
            "falsification_expectation": {
                "FE1_mean_abs_spearman_ge_0_03": 0.03,
                "FE1_frac_negative_ge_0_60": 0.60,
            },
        },
        "falsification": falsification,
        "in_sample": strat_metrics,
        "oos_folds": oos_results,
        "oos_sharpe": oos_sharpe,
        "beta_vs_spy": float(beta_coef) if np.isfinite(beta_coef) else np.nan,
        "corr_spy": corr,
        "turnover_avg": turnover_avg,
        "placebo_sharpes": placebo_sharpes,
        "placebo_mean": placebo_mean,
        "placebo_std": placebo_std,
        "placebo_z": placebo_z,
        "bear_sharpe": bear_sharpe,
        "cost_sensitivity": cost_sensitivity,
        "sensitivity": sensitivity,
        "n_folds": len(oos_results),
    }

    # Gate evaluation
    gates = {
        "G1_oos_sharpe": oos_sharpe >= 0.8 if not np.isnan(oos_sharpe) else False,
        "G2_placebo_z": placebo_z >= 3.0 if not np.isnan(placebo_z) else False,
        "G3_beta": abs(beta_coef) <= 0.2 if np.isfinite(beta_coef) else False,
        "G4_bear_sharpe": bear_sharpe > 0 if not np.isnan(bear_sharpe) else False,
        "G5_turnover": turnover_avg <= 0.15,
    }
    result["gates"] = gates
    result["gates_passed"] = sum(gates.values())
    result["gates_total"] = len(gates)
    result["promoted"] = all(gates.values())

    out_path = "experiments/e027_ivol_anomaly.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(json.dumps({
        "oos_sharpe": oos_sharpe,
        "placebo_z": placebo_z,
        "beta": float(beta_coef) if np.isfinite(beta_coef) else np.nan,
        "bear_sharpe": bear_sharpe,
        "turnover": turnover_avg,
        "gates": gates,
        "promoted": result["promoted"],
        "falsification": falsification,
    }, indent=2, default=str))


if __name__ == "__main__":
    main()