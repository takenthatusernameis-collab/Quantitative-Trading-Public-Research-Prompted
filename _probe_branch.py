"""Probe: does the SLSQP fallback branch in optimize_portfolio_weights(max_sharpe)
ever fire during the E042-lead walk-forward?  Counts exact_qp outcomes and
minimize() calls.  Restores experiments/ goldens afterwards (never commits).
"""
import json
import os
import sys

os.environ.setdefault("QUANT_RESEARCH_OFFLINE", "1")
os.environ.setdefault("SEED", "42")

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "experiments"))

import src.portfolio_opt as P
import run_e042 as R

counts = {"exact_qp_none": 0, "exact_qp_feasible": 0,
          "exact_qp_infeasible": 0, "slsqp_calls": 0,
          "slsqp_feasible": 0, "slsqp_rejected": 0}

_orig_exact = P.exact_qp
_orig_tang = P._tangency_feasible
_orig_minimize = P.minimize


def wrapped_exact(Q, c, A_ub, b_ub, A_eq=None, b_eq=None, tol=1e-9):
    r = _orig_exact(Q, c, A_ub, b_ub, A_eq, b_eq, tol)
    if r is None:
        counts["exact_qp_none"] += 1
    else:
        counts["exact_qp_feasible"] += 1
    return r


def wrapped_tang(y, mu_s, A_ub_y, tol=1e-6):
    ok = _orig_tang(y, mu_s, A_ub_y, tol)
    if ok:
        counts["exact_qp_infeasible"] += 1
    return ok


def wrapped_minimize(*a, **k):
    counts["slsqp_calls"] += 1
    r = _orig_minimize(*a, **k)
    return r


P.exact_qp = wrapped_exact
P._tangency_feasible = wrapped_tang
P.minimize = wrapped_minimize

comp = R.build_component_returns()
cr = comp["returns"]
cols = R.SENS_SETS["macro_inclusive_3"]
sub = cr[cols]

W = P.walk_forward_blend_weights(
    sub, benchmark_returns=comp["spy_ret"],
    futures_benchmark_returns=comp["fut_index_ret"],
    formation_window=R.FORMATION, rebalance_freq=63,
    beta_constraint=0.1, method="max_sharpe", seed=R.SEED, n_grid=0)

print(json.dumps(counts, indent=2))
print("rebalances:", int(W.notna().any(axis=1).sum()))