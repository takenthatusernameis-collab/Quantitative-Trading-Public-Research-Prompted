"""Probe: is the committed E042-lead /primary golden reproduced when the
exact active-set KKT solver (added in commit 309d289, "E050") is DISABLED?

Runs the driver's core path twice in-process:
  A) with exact_qp present      (current committed code)
  B) with exact_qp stubbed None (pre-309d289 behaviour)

Compares each to the committed golden.  Writes nothing under the repo.
"""
import json, os, sys, importlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'experiments'))

import numpy as np
import run_e042 as R
from src import portfolio_opt as P

GOLDEN = json.load(open(os.path.join(ROOT, 'experiments',
                                     'e042_lead_config_confirmatory.json')))

def run_primary(use_exact):
    """Return the /primary block produced by the lead config."""
    if not use_exact:
        # stub the exact solver -> SLSQP fallback path (pre-E050)
        orig = P.exact_qp
        P.exact_qp = lambda *a, **k: None
    try:
        comp = R.build_component_returns()
        cr = comp['returns']
        cols = R.SENS_SETS['macro_inclusive_3']
        sub = cr[cols]
        sub_bench = comp['spy_ret']
        sub_fb = comp['fut_index_ret']
        W = P.walk_forward_blend_weights(
            sub, benchmark_returns=sub_bench,
            futures_benchmark_returns=sub_fb,
            formation_window=R.FORMATION, rebalance_freq=63,
            beta_constraint=0.1, method='max_sharpe',
            seed=R.SEED, n_grid=0)
        gross, turnover, net = R.blend_series(sub, W, R.TC_EQUITY, R.SL_EQUITY)
        primary = R.evaluate_blend(net, sub.index, comp['spy_ret'],
                                   R.TC_EQUITY, R.SL_EQUITY, W)
    finally:
        if not use_exact:
            P.exact_qp = orig
    return primary

def cmp(label, got):
    g = GOLDEN['primary']
    keys = ['oos_sharpe', 'equity_beta', 'oos_equity_beta', 'turnover',
            'bear_sharpe', 'positive_folds', 'is_sharpe']
    print(f'--- {label} ---')
    worst = 0.0
    for k in keys:
        a, b = float(got[k]), float(g[k])
        d = abs(a - b)
        worst = max(worst, d)
        flag = 'OK ' if d < 1e-6 else 'DR '
        print(f'  {flag} {k:<16} got={a:<20.12f} golden={b:<20.12f} d={d:.3e}')
    print(f'  worst abs diff = {worst:.3e}')
    return worst

if __name__ == '__main__':
    w_exact = cmp('exact_qp ENABLED  (committed code)', run_primary(True))
    w_fallback = cmp('exact_qp DISABLED (pre-E050 SLSQP fallback)', run_primary(False))
    print()
    if w_exact < 1e-6:
        print('RESULT: committed code reproduces the golden /primary exactly.')
    else:
        print('RESULT: committed code does NOT reproduce /primary '
              f'(worst {w_exact:.3e}).')
    if w_fallback < 1e-6:
        print('RESULT: disabling exact_qp reproduces the golden -> the E050 '
              'solver change is the regression.')
    else:
        print('RESULT: disabling exact_qp also fails (worst {:.3e}) '
              '-> something else changed.'.format(w_fallback))