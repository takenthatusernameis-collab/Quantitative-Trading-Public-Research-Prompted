"""E021: Pairs trading / statistical arbitrage (Gatev, Goetzmann & Rouwenhorst 2006).

Distance-method pairs on the large_liquid equity universe with pre-registered
gates, walk-forward evaluation, a pair-level placebo null, cost sweeps,
lookback sensitivity, per-pair decomposition and regime analysis.

Pre-registered gates (set before running, NOT moved after seeing results):
  - OOS Sharpe >= 0.8
  - pair-level placebo z >= 3
  - |equity_beta| <= 0.1
  - positive bear-market Sharpe
  - turnover <= 0.15
"""

import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import data, backtest, validation
from src.run_experiment import UNIVERSES, deterministic_timestamp
from src import pairs

UNIVERSE = UNIVERSES["large_liquid"]
TC_COST = 0.0005
SLIPPAGE = 0.0002
TRAIN = 504
TEST = 63
STEP = 63
REBAL = 21
FORMATION = 252
ENTRY_Z = 2.0
EXIT_Z = 0.0
VOL_WINDOW = 63
MAX_PAIRS = 20
PLACEBO_N = 50
SEED = 42

# Pre-registered gates
GATE_OOS = 0.8
GATE_Z = 3.0
GATE_BETA = 0.1
GATE_BEAR = 0.0
GATE_TURNOVER = 0.15


def load_data():
    df = data.download(UNIVERSE, start="2014-01-01")
    close = data.get_panel(df, "Close").dropna(how="all")
    open_ = data.get_panel(df, "Open").reindex(close.index).fillna(close)
    bm = data.download(["SPY"], start="2014-01-01")
    spy = data.get_panel(bm, "Close").dropna(how="all")["SPY"].reindex(close.index).ffill()
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
        "is_total_return": m.get("total_return"),
        "is_win_rate": m.get("win_rate"),
        "is_n_days": m.get("n_days"),
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


def main():
    print("=" * 70)
    print("E021: Pairs Trading / Statistical Arbitrage (Gatev et al. 2006)")
    print("=" * 70)

    close, open_, spy = load_data()
    spy_ret = spy.pct_change().fillna(0.0)
    splits = backtest.walk_forward_splits(len(close), TRAIN, TEST, STEP)
    print(f"Loaded {len(close)} days, {len(close.columns)} tickers; folds={len(splits)}")

    print("\n[1] Forming pairs (distance method, 252d formation, top-20)...")
    pairs_by_date = pairs.find_pairs_distance(
        close, formation_window=FORMATION, max_pairs=MAX_PAIRS
    )
    n_with_pairs = sum(1 for v in pairs_by_date.values() if v)
    print(f"    formation windows={len(pairs_by_date)}, with >=1 pair={n_with_pairs}")

    print("\n[2] Computing stateful pairs weights (entry_z=2.0, exit_z=0.0, monthly rebal)...")
    w = pairs.pairs_weights(
        close, pairs_by_date,
        formation_window=FORMATION, entry_z=ENTRY_Z, exit_z=EXIT_Z,
        vol_window=VOL_WINDOW, rebalance_freq=REBAL,
    )
    active_days = int((w.abs().sum(axis=1) > 1e-9).sum())
    print(f"    active days={active_days}/{len(w)}  gross exposure range="
          f"{w.abs().sum(axis=1).min():.3f}-{w.abs().sum(axis=1).max():.3f}")

    ret = backtest.portfolio_returns_rebalance_clean(
        w, close, open_, TC_COST, SLIPPAGE, rebalance_freq=REBAL
    )
    diag = market_diagnostics(ret, spy_ret)
    dd, uw = compute_dd(ret["net"])
    fm = walk_forward(ret, close, spy_ret)
    reg = regime_summary(fm)
    oos_sharpe = float(np.mean([m["sharpe"] for m in fm]))
    oos_std = float(np.std([m["sharpe"] for m in fm]))
    turnover = backtest.average_turnover(w)
    n_pos_folds = int(sum(1 for m in fm if m["sharpe"] > 0))
    print(f"    OOS Sharpe={oos_sharpe:.3f} (std {oos_std:.3f})  turnover={turnover:.4f}  "
          f"beta={diag['equity_beta']:.3f} corr={diag['corr_spy']:.3f} maxDD={dd:.3f} "
          f"pos_folds={n_pos_folds}/{len(fm)}")
    print(f"    regime: {reg}")

    # --- 3. Placebo null: random pair matching, same stateful rule ---
    print(f"\n[3] Pair-level placebo null ({PLACEBO_N} sims, random pair matching)...")
    placebo_w = pairs.pairs_placebo_weights(
        close, n_pairs=MAX_PAIRS, n_sim=PLACEBO_N, seed=SEED,
        formation_window=FORMATION, entry_z=ENTRY_Z, exit_z=EXIT_Z,
        vol_window=VOL_WINDOW, rebalance_freq=REBAL,
    )
    placebo_sharpes = []
    for pw in placebo_w:
        pr = backtest.portfolio_returns_rebalance_clean(
            pw, close, open_, TC_COST, SLIPPAGE, rebalance_freq=REBAL
        )
        placebo_sharpes.append(backtest.metrics(pr["net"]).get("sharpe", 0.0))
    pm = float(np.mean(placebo_sharpes))
    ps = float(np.std(placebo_sharpes))
    z_score = float((oos_sharpe - pm) / ps) if ps > 0 else float("nan")
    print(f"    placebo mean Sharpe={pm:.3f} std={ps:.3f}  z={z_score:.2f}")

    # --- 4. Cost sweep ---
    print("\n[4] Cost sweep...")
    cost_rows = []
    for tc, sl in [(0.0, 0.0), (0.0005, 0.0002), (0.0010, 0.0005), (0.0020, 0.0050)]:
        r = backtest.portfolio_returns_rebalance_clean(
            w, close, open_, tc_cost=tc, slippage=sl, rebalance_freq=REBAL
        )
        fm_c = walk_forward(r, close, spy_ret)
        npos = int(sum(1 for m in fm_c if m["sharpe"] > 0))
        cost_rows.append({
            "tc_cost": tc, "slippage": sl,
            "oos_sharpe": float(np.mean([m["sharpe"] for m in fm_c])),
            "turnover": backtest.average_turnover(w),
            "n_pos_folds": npos,
            "sharpe_std": float(np.std([m["sharpe"] for m in fm_c])),
        })
        print(f"    tc={tc:.4f} sl={sl:.4f}: OOS Sharpe={cost_rows[-1]['oos_sharpe']:.3f} "
              f"(std {cost_rows[-1]['sharpe_std']:.3f}) pos={npos}/{len(fm_c)}")

    # --- 5. Lookback / max-pairs sensitivity ---
    print("\n[5] Formation-window + max-pairs sensitivity...")
    sens_rows = []
    for form_w, mp in [(126, 10), (126, 20), (252, 10), (252, 20), (252, 30), (378, 20)]:
        pbd_s = pairs.find_pairs_distance(close, formation_window=form_w, max_pairs=mp)
        w_s = pairs.pairs_weights(
            close, pbd_s, formation_window=form_w, entry_z=ENTRY_Z, exit_z=EXIT_Z,
            vol_window=VOL_WINDOW, rebalance_freq=REBAL,
        )
        r_s = backtest.portfolio_returns_rebalance_clean(
            w_s, close, open_, TC_COST, SLIPPAGE, rebalance_freq=REBAL
        )
        fm_s = walk_forward(r_s, close, spy_ret)
        sh = float(np.mean([m["sharpe"] for m in fm_s]))
        sens_rows.append({
            "formation_window": form_w, "max_pairs": mp,
            "oos_sharpe": sh, "turnover": backtest.average_turnover(w_s),
            "n_pos_folds": int(sum(1 for m in fm_s if m["sharpe"] > 0)),
        })
        print(f"    form={form_w} max_pairs={mp}: OOS Sharpe={sh:.3f} "
              f"turnover={sens_rows[-1]['turnover']:.4f}")

    # --- 6. Bear-window analysis ---
    print("\n[6] Bear-market window analysis (2020-COVID, 2022-bear)...")
    for label, lo, hi in [("2020_covid", "2020-02-19", "2020-04-07"),
                          ("2022_bear", "2022-01-03", "2022-06-16")]:
        win_mask = (close.index >= lo) & (close.index <= hi)
        wret = ret.loc[ret.index[win_mask].intersection(ret.index), "net"]
        if len(wret) > 2:
            m = backtest.metrics(wret)
            print(f"    pairs {label}: Sharpe={m.get('sharpe',0):.3f} "
                  f"AnnRet={m.get('annual_return',0):.3f} MaxDD={m.get('max_drawdown',0):.3f}")

    # --- 7. Gate evaluation ---
    print("\n[7] Pre-registered gate evaluation...")
    gates = {
        "OOS Sharpe >= 0.8": oos_sharpe >= GATE_OOS,
        "placebo z >= 3.0": z_score >= GATE_Z,
        "|beta| <= 0.1": abs(diag["equity_beta"]) <= GATE_BETA,
        "bear Sharpe > 0": reg["bear"]["sharpe_mean"] > GATE_BEAR,
        "turnover <= 0.15": turnover <= GATE_TURNOVER,
    }
    n_pass = sum(gates.values())
    for k, v in gates.items():
        print(f"    [{'PASS' if v else 'FAIL'}] {k}")
    print(f"    {n_pass}/{len(gates)} gates passed")

    # --- 8. Save ---
    result = {
        "experiment": "E021",
        "timestamp": deterministic_timestamp(),
        "source": "Gatev, Goetzmann & Rouwenhorst (2006) \"Pairs Trading: Performance of "
                   "Relative-Value Arbitrage\", JFE 79(2):65-79. Distance method.",
        "universe": "large_liquid",
        "n_tickers": len(UNIVERSE),
        "specification": {
            "formation_window": FORMATION, "trading_window": None,
            "max_pairs": MAX_PAIRS, "entry_z": ENTRY_Z, "exit_z": EXIT_Z,
            "vol_window": VOL_WINDOW, "rebalance_freq_days": REBAL,
            "method": "distance (sum of squared normalized-price diffs), log-spread "
                      "z-score, stateful entry/exit, dollar-neutral per pair, "
                      "inverse-vol across pairs",
        },
        "costs": {"tc_cost": TC_COST, "slippage": SLIPPAGE},
        "walk_forward": {"train": TRAIN, "test": TEST, "step": STEP, "n_folds": len(splits)},
        "pre_registered": {
            "gates": {
                "oos_sharpe": GATE_OOS, "placebo_z": GATE_Z,
                "equity_beta_abs": GATE_BETA, "bear_sharpe": GATE_BEAR,
                "turnover": GATE_TURNOVER,
            },
            "gate_results": gates,
            "n_gates_passed": n_pass,
            "promoted": bool(n_pass == len(gates)),
        },
        "strategy": {
            "oos_sharpe": oos_sharpe,
            "oos_sharpe_std": oos_std,
            "turnover": turnover,
            "equity_beta": diag["equity_beta"],
            "corr_spy": diag["corr_spy"],
            "alpha_annual": diag["alpha_annual"],
            "is_sharpe": diag["is_sharpe"],
            "is_ann_return": diag["is_ann_return"],
            "is_ann_vol": diag["is_ann_vol"],
            "is_max_dd": diag["is_max_dd"],
            "max_drawdown": dd,
            "time_underwater_days": uw,
            "is_win_rate": diag["is_win_rate"],
            "active_days": active_days,
            "n_pos_folds": n_pos_folds,
            "regime_analysis": reg,
            "acf_lag1": float(validation.autocorrelation_test(ret["net"])["acf"][0]),
            "t_stat": float(validation.t_stat(oos_sharpe, TEST * len(fm))),
            "fold_metrics": fm,
        },
        "placebo": {"n_sim": PLACEBO_N, "mean_sharpe": pm, "std_sharpe": ps, "z_score": z_score},
        "cost_sensitivity": cost_rows,
        "sensitivity": sens_rows,
    }

    out_path = os.path.join("experiments", "e021_pairs_trading.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()