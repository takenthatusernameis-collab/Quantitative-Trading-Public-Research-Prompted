"""Scan every walk-forward rebalance fold: find which ones produce
different weights under exact_qp ENABLED vs DISABLED, and for those,
compare the KKT objective to the SLSQP objective.
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
idx = sub.index
n_days = len(idx)

def solve_at(pos, use_exact):
    if not use_exact:
        orig = P.exact_qp
        P.exact_qp = lambda *a, **k: None
    try:
        window = sub.iloc[pos - FORM:pos]
        bench_w = sub_bench.iloc[pos - FORM:pos]
        fut_w = sub_fb.iloc[pos - FORM:pos]
        w = P.optimize_portfolio_weights(
            window, beta_constraint=0.1,
            benchmark_returns=bench_w,
            futures_benchmark_returns=fut_w,
            method='max_sharpe', seed=R.SEED, n_grid=0)
    finally:
        if not use_exact:
            P.exact_qp = orig
    return w

divergent = []
for pos in range(FORM, n_days, 63):
    we = solve_at(pos, True)
    ws = solve_at(pos, False)
    d = float(np.max(np.abs(we - ws)))
    if d > 1e-9:
        divergent.append((pos, d, we, ws, str(idx[pos])[:10]))

print('total rebalance dates:', len(range(FORM, n_days, 63)))
print('divergent folds:', len(divergent))
for pos, d, we, ws, date in divergent[:12]:
    print(f'  pos={pos} date={date} max|d|={d:.3e}')
    print(f'    exact w={we}')
    print(f'    slsqp w={ws}')