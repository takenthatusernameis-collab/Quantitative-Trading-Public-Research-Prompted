"""Regression tests for the optimizer's solver-answer validation.

Invariant under test: a solver answer is judged by the constraints it
satisfies, not by the solver's exit status.

``scipy.optimize.minimize(method="SLSQP")`` can exit with "Positive
directional derivative for linesearch" (status 8) at a constrained
optimum while returning a point that satisfies every constraint to
solver tolerance.  The shipped code used to gate the answer on
``res.success``, which silently discarded such a point and replaced it
with an unrelated LP vertex.  Because the exit status is scipy-build
dependent, that made the tangency portfolio - and every committed
artifact derived from it - environment dependent.

The tests below pin the fixed behaviour:
  1. the same answer is produced whether or not the solver reports
     success (the exit status must not change the result);
  2. an infeasible answer is rejected and a feasible portfolio is
     returned instead;
  3. the projection path behaves the same way.
"""

import unittest

import numpy as np
import pandas as pd

from src import portfolio_opt as P


def _components(seed=42, days=300):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2018-01-01", periods=days)
    x = rng.standard_normal((days, 2)) * 0.01
    x[:, 0] += 0.0006
    x[:, 1] += 0.0004
    return pd.DataFrame(x, index=idx, columns=["a", "b"])


class _FakeResult:
    def __init__(self, x, success, message="synthetic"):
        self.x = np.asarray(x, dtype=float)
        self.success = success
        self.message = message
        self.fun = float("nan")


class TestTangencyAnswerValidation(unittest.TestCase):
    def test_exit_status_does_not_change_the_answer(self):
        """The tangency answer is the same whether or not SLSQP says success."""
        R = _components()
        baseline = P.optimize_portfolio_weights(R, beta_constraint=1.0,
                                                method="max_sharpe", n_grid=0)
        original = P.minimize
        seen = {}

        def failing_minimize(*a, **k):
            res = original(*a, **k)
            seen["x"] = np.asarray(res.x, dtype=float)
            return _FakeResult(seen["x"], success=False)

        P.minimize = failing_minimize
        try:
            w = P.optimize_portfolio_weights(R, beta_constraint=1.0,
                                             method="max_sharpe", n_grid=0)
        finally:
            P.minimize = original
        self.assertIn("x", seen, "the solver was never called")
        self.assertTrue(np.allclose(w, baseline, atol=1e-10),
                        f"exit status changed the answer: {w} != {baseline}")

    def test_infeasible_answer_is_rejected(self):
        """An infeasible answer is discarded and a feasible one returned."""
        R = _components()
        original = P.minimize
        P.minimize = lambda *a, **k: _FakeResult(
            np.array([1e12, 1e12]), success=False)
        try:
            w = P.optimize_portfolio_weights(R, beta_constraint=1.0,
                                             method="max_sharpe", n_grid=0)
        finally:
            P.minimize = original
        self.assertTrue(np.all(np.isfinite(w)))
        self.assertAlmostEqual(float(w.sum()), 1.0, places=6)
        self.assertTrue(np.all(w >= -1e-9))

    def test_result_is_always_feasible(self):
        """Whatever the solver returns, the portfolio stays feasible."""
        R = _components(seed=7)
        for answer, success in [([0.5, 0.5], True), ([0.5, 0.5], False),
                                ([np.nan, 1.0], False), ([-1.0, 2.0], False),
                                ([1e12, 1e12], False)]:
            original = P.minimize

            def fake(*a, _ans=answer, _ok=success, **k):
                return _FakeResult(_ans, success=_ok)

            P.minimize = fake
            try:
                w = P.optimize_portfolio_weights(R, beta_constraint=0.5,
                                                 method="max_sharpe", n_grid=0)
            finally:
                P.minimize = original
            self.assertTrue(np.all(np.isfinite(w)), f"answer={answer}")
            self.assertAlmostEqual(float(w.sum()), 1.0, places=6)
            self.assertTrue(np.all(w >= -1e-9), f"answer={answer}")


class TestProjectionAnswerValidation(unittest.TestCase):
    # beta = [0.5, -0.5] with sum(w) = 1 gives beta'w = 0.5 - w0, so the
    # cap |beta'w| <= 0.1 is satisfiable and the projection is well posed.
    BETA = np.array([0.5, -0.5])

    def test_feasible_projection_kept_when_solver_reports_failure(self):
        """A feasible projection survives a failure status."""
        w0 = np.array([0.9, 0.1])            # beta'w0 = 0.4 -> infeasible
        proj = np.array([0.45, 0.55])        # beta'proj = -0.05 -> feasible
        self.assertFalse(P._feasible(w0, self.BETA, None, 0.1))
        self.assertTrue(P._feasible(proj, self.BETA, None, 0.1))
        original = P.minimize
        P.minimize = lambda *a, **k: _FakeResult(proj, success=False)
        try:
            out = P.project_onto_beta_cap(w0, self.BETA, None, 0.1)
        finally:
            P.minimize = original
        self.assertTrue(np.allclose(out, proj),
                        f"expected the projection {proj}, got {out}")

    def test_infeasible_projection_is_rejected(self):
        """An infeasible projection is discarded; the result stays feasible."""
        w0 = np.array([0.9, 0.1])
        bad = np.array([0.0, 1.0])           # beta'bad = -0.5 -> infeasible
        self.assertFalse(P._feasible(bad, self.BETA, None, 0.1))
        original = P.minimize
        P.minimize = lambda *a, **k: _FakeResult(bad, success=False)
        try:
            out = P.project_onto_beta_cap(w0, self.BETA, None, 0.1)
        finally:
            P.minimize = original
        self.assertTrue(P._feasible(out, self.BETA, None, 0.1),
                        f"returned an infeasible projection {out}")


if __name__ == "__main__":
    unittest.main()
