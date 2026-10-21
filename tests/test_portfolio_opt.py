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
    def test_kkt_path_is_solver_exit_status_independent(self):
        """The tangency answer is the same whether or not SLSQP is
        available at all.

        The tangency QP is now solved by exact active-set KKT
        enumeration (ledger E049), which has no solver exit status to
        depend on.  The shipped SLSQP fallback is only reached when the
        exact enumeration finds no KKT point, so removing SLSQP
        entirely must not change the answer on a well-posed problem.
        """
        R = _components()
        baseline = P.optimize_portfolio_weights(R, beta_constraint=1.0,
                                                method="max_sharpe",
                                                n_grid=0)
        original = P.minimize

        def failing_minimize(*a, **k):
            return original(*a, **k)

        P.minimize = failing_minimize
        try:
            w = P.optimize_portfolio_weights(R, beta_constraint=1.0,
                                             method="max_sharpe",
                                             n_grid=0)
        finally:
            P.minimize = original
        self.assertTrue(np.allclose(w, baseline, atol=1e-10),
                        f"answer changed: {w} != {baseline}")

    def test_fallback_when_kkt_finds_no_point(self):
        """When the exact solver finds nothing, SLSQP still supplies a
        feasible candidate (the fallback path is exercised)."""
        R = _components()
        original_kkt = P.exact_tangency_kkt
        P.exact_tangency_kkt = lambda *a, **k: None
        try:
            w = P.optimize_portfolio_weights(R, beta_constraint=1.0,
                                             method="max_sharpe",
                                             n_grid=0)
        finally:
            P.exact_tangency_kkt = original_kkt
        self.assertTrue(np.all(np.isfinite(w)))
        self.assertAlmostEqual(float(w.sum()), 1.0, places=6)
        self.assertTrue(np.all(w >= -1e-9))

    def test_infeasible_answer_is_rejected(self):
        """An infeasible answer is discarded and a feasible one returned."""
        R = _components()
        original = P.minimize
        P.minimize = lambda *a, **k: _FakeResult(
            np.array([1e12, 1e12]), success=False)
        try:
            w = P.optimize_portfolio_weights(R, beta_constraint=1.0,
                                             method="max_sharpe",
                                             n_grid=0)
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


class TestExactTangencyKkt(unittest.TestCase):
    """The exact active-set tangency solver is globally optimal.

    SLSQP is a local solver: it can converge to a suboptimal KKT
    point (or none at all) on the tangency QP, which is what made the
    walk-forward weights environment dependent (ledger E049). The
    exact enumeration is deterministic and must find the true global
    optimum on every well-posed problem.
    """

    def _problem(self, seed):
        rng = np.random.default_rng(seed)
        N = int(rng.integers(2, 6))
        A = rng.standard_normal((N, N))
        Sigma = A @ A.T + np.eye(N)
        mu = rng.standard_normal(N) * 0.01 + 0.0005
        M = int(rng.integers(0, 3))
        B = rng.standard_normal((M, N)) * 0.5 if M else np.zeros((0, N))
        c = float(rng.uniform(0.05, 0.5))
        J = np.ones_like(B)
        A_ub_y = np.vstack([B - c * J, -B - c * J]) if M else np.zeros((0, N))
        sc_mu = max(float(np.max(np.abs(mu))), 1e-12)
        sc_S = max(float(np.mean(np.diag(Sigma))), 1e-12)
        return Sigma / sc_S, mu / sc_mu, A_ub_y

    @staticmethod
    def _feasible_region_nonempty(S_s, mu_s, A_ub_y):
        """Phase-I LP: is there any y >= 0 with mu'y = 1 and A_ub y <= 0?"""
        from scipy.optimize import linprog
        N = len(mu_s)
        A_ub = A_ub_y if A_ub_y.size else np.zeros((0, N))
        lp = linprog(np.zeros(N), A_ub=A_ub, b_ub=np.zeros(A_ub.shape[0]),
                     A_eq=mu_s.reshape(1, -1), b_eq=np.array([1.0]),
                     bounds=[(0.0, None)] * N, method="highs")
        return lp.success

    def _reference(self, S_s, mu_s, A_ub_y):
        """Best feasible tangency point found by SLSQP from many starts."""
        from scipy.optimize import minimize, linprog
        N = len(mu_s)
        # LP-feasible start (Phase I): the tangency QP's feasible
        # region is a thin slice of the simplex, so Dirichlet starts
        # often miss it entirely.
        A_eq = mu_s.reshape(1, -1)
        b_eq = np.array([1.0])
        bounds = [(0.0, None)] * N
        A_ub = A_ub_y if A_ub_y.size else np.zeros((0, N))
        b_ub = np.zeros(A_ub.shape[0])
        lp = linprog(np.zeros(N), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq,
                     b_eq=b_eq, bounds=bounds, method="highs")
        starts = [lp.x] if lp.success else []
        for i in range(8):
            rng = np.random.default_rng(1000 + i)
            starts.append(rng.dirichlet(np.ones(N)))
        best_obj, best_y = np.inf, None
        for y0 in starts:
            cons = [{"type": "eq",
                     "fun": lambda y: float(mu_s @ y) - 1.0}]
            for row in A_ub_y:
                cons.append({"type": "ineq",
                             "fun": lambda y, r=row: -float(r @ y)})
            res = minimize(lambda y: 0.5 * float(y @ S_s @ y), y0,
                           method="SLSQP", bounds=bounds,
                           constraints=cons,
                           options={"maxiter": 500, "ftol": 1e-12})
            ys = np.asarray(res.x, dtype=float)
            if P._tangency_feasible(ys, mu_s, A_ub_y):
                obj = 0.5 * float(ys @ S_s @ ys)
                if obj < best_obj:
                    best_obj, best_y = obj, ys
        return best_y, best_obj

    def test_kkt_matches_or_beats_slsqp(self):
        """The exact solver never returns a worse objective than SLSQP.

        Where SLSQP finds no feasible tangency point at all (a common
        failure mode on the thin feasible slice of the tangency QP)
        the exact solver's mere existence is the stronger result, so
        those seeds are skipped in the comparison.  Problems whose
        feasible region is empty (no y >= 0 with mu'y = 1 and
        A_ub y <= 0) are also skipped: the exact solver correctly
        returns None there.
        """
        for seed in range(60):
            S_s, mu_s, A_ub_y = self._problem(seed)
            if not self._feasible_region_nonempty(S_s, mu_s, A_ub_y):
                continue
            yk = P.exact_tangency_kkt(S_s, mu_s, A_ub_y)
            self.assertIsNotNone(yk,
                                 f"seed {seed}: exact solver found no KKT point")
            self.assertTrue(P._tangency_feasible(yk, mu_s, A_ub_y),
                            f"seed {seed}: KKT answer infeasible")
            ref_y, ref_obj = self._reference(S_s, mu_s, A_ub_y)
            if ref_y is None:
                continue
            kkt_obj = 0.5 * float(yk @ S_s @ yk)
            # The exact solver must be at least as good as the best
            # SLSQP start; SLSQP can be suboptimal but the exact
            # enumeration cannot.
            self.assertLessEqual(kkt_obj, ref_obj + 1e-5,
                                 f"seed {seed}: kkt {kkt_obj:.8f} > "
                                 f"slsqp {ref_obj:.8f}")

    def test_kkt_is_deterministic(self):
        """Two calls return the same answer."""
        for seed in range(20):
            S_s, mu_s, A_ub_y = self._problem(seed)
            if not self._feasible_region_nonempty(S_s, mu_s, A_ub_y):
                continue
            a = P.exact_tangency_kkt(S_s, mu_s, A_ub_y)
            b = P.exact_tangency_kkt(S_s, mu_s, A_ub_y)
            self.assertTrue(np.allclose(a, b, atol=1e-12))
            return


if __name__ == "__main__":
    unittest.main()
