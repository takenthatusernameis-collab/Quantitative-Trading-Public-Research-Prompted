"""Diagnostic: WHY exact_qp diverges from the SLSQP answer the committed
E042-lead golden was built from.

Calls optimize_portfolio_weights() on the first walk-forward formation
window with exact_qp ENABLED vs DISABLED, and reports the KKT objective,
the SLSQP objective, and the formation-window Sharpe each candidate would
be scored on.
"""
import os, sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'experiments'))

import run_e042 as R
from src import portfolio_opt as P

comp = R.build_component_returns()
cr = comp['returns']
cols = R.SENS_SETS['macro_inclusive_3']
sub = cr[cols]
sub_bench = comp['spy_ret']
sub_fb = comp['fut_index_ret']

FORM = R.FORMATION
pos = FORM  # first rebalance that actually optimizes
window = sub.iloc[pos - FORM:pos]
bench_w = sub_bench.iloc[pos - FORM:pos]
fut_w = sub_fb.iloc[pos - FORM:pos]

def solve(use_exact):
    if not use_exact:
        orig = P.exact_qp
        P.exact_qp = lambda *a, **k: None
    try:
        w = P.optimize_portfolio_weights(
            window, beta_constraint=0.1,
            benchmark_returns=bench_w,
            futures_benchmark_returns=fut_w,
            method='max_sharpe', seed=R.SEED, n_grid=0)
    finally:
        if not use_exact:
            P.exact_qp = orig
    return w

w_exact = solve(True)
w_slsqp = solve(False)
print('window rows:', len(window), 'cols:', list(window.columns))
print('exact_qp ENABLED  w =', w_exact)
print('exact_qp DISABLED  w =', w_slsqp)
print('weights identical:', np.allclose(w_exact, w_slsqp, atol=1e-12),
      ' max|d| =', float(np.max(np.abs(w_exact - w_slsqp))))

# Sharpe of each on the formation window (the criterion the selection loop
# actually maximises) - need the component return series and cost model.
gross, turnover, net = R.blend_series(sub, w_exact, R.TC_EQUITY, R.SL_EQUITY)
g2, t2, n2 = R.blend_series(sub, w_slsqp, R.TC_EQUITY, R.SL_EQUITY)
sh = lambda s: float(s.mean() / s.std()) if s.std() > 0 else float('nan')
print('formation-window Sharpe: exact=%+.6f  slsqp=%+.6f' % (sh(net), sh(n2)))