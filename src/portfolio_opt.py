"""Walk-forward portfolio optimization over validated component strategies.

E041: market-neutral portfolio construction from the five validated
components (equity TSM pure, equity dollar-neutral low-beta, futures
TSM 18m, futures realized-roll-yield carry, macro momentum).

The five components live on different universes (130-name equity panel,
16-contract de-seamed futures panel, 3 macro ETFs), so the blend is built
at the *return-stream* level: each component contributes a daily net
return series (close-to-close convention, class-appropriate base costs),
and the optimizer assigns non-negative weights to the five return streams
subject to market-neutrality constraints.

No look-ahead: at each rebalance date the optimizer sees only the trailing
``formation_window`` days of component returns. Ledoit-Wolf (2004)
shrinkage (scaled-identity target) conditions the covariance; a ridge
term guards against residual ill-conditioning. SLSQP solves the
constrained problem; a seeded Dirichlet grid is a deterministic
fallback/robustness layer if the solver struggles.
"""

import itertools
from typing import List, Optional

import numpy as np
import pandas as pd
from scipy.optimize import linprog, minimize


def ledoit_wolf_covariance(X: np.ndarray) -> np.ndarray:
    """Ledoit-Wolf (2004) shrunk covariance, scaled-identity target.

    Shrinks the sample covariance S toward ``mu * I`` (mu = average
    sample variance) with the closed-form shrinkage intensity of
    Ledoit & Wolf (2004, "Honey, I Shrunk the Sample Covariance
    Matrix"), Proposition 2. Deterministic; no randomness.
    """
    X = np.asarray(X, dtype=float)
    X = X - X.mean(axis=0)
    T, N = X.shape
    if T <= 1 or N == 0:
        return np.zeros((N, N))
    S = (X.T @ X) / T
    mu = float(np.trace(S)) / N
    X2 = X ** 2
    # Asymptotic variance of each sample-covariance entry (Prop. 2):
    # Var(S_ij) ~ (1/T) * (E[x_i^2 x_j^2] - S_ij^2).
    var_S = ((X2.T @ X2) / T - S ** 2) / T
    pi_hat = float(np.clip(var_S.sum(), 0.0, None))
    target = np.eye(N) * mu
    phi_hat = float(((S - target) ** 2).sum())
    if phi_hat <= 0.0:
        delta = 1.0
    else:
        delta = float(np.clip(pi_hat / phi_hat, 0.0, 1.0))
    return delta * target + (1.0 - delta) * S


def _beta_exposure(
    component_returns: pd.DataFrame,
    benchmark: pd.Series,
) -> Optional[np.ndarray]:
    """Per-component beta vs a benchmark over the formation window."""
    if benchmark is None:
        return None
    b = benchmark.reindex(component_returns.index)
    b = b.fillna(0.0)
    var_b = float(b.var())
    if var_b <= 0.0 or len(b) < 2:
        return None
    cov = component_returns.apply(lambda col: float(col.cov(b)))
    return (cov / var_b).to_numpy(dtype=float)


def _tangency_feasible(
    y: Optional[np.ndarray],
    mu_s: np.ndarray,
    A_ub_y: np.ndarray,
    tol: float = 1e-6,
) -> bool:
    """Numerical feasibility of a tangency-QP answer.

    ``scipy.optimize.minimize(method="SLSQP")`` can exit with "Positive
    directional derivative for linesearch" (status 8) *at* a constrained
    optimum while returning a point that satisfies every constraint to
    solver tolerance. The exit status is scipy-version dependent, so
    gating the tangency answer on ``res.success`` makes the optimized
    portfolio - and every artifact derived from it - environment
    dependent (the committed E042 lead artifact reproduces under some
    scipy builds and not under others).

    The answer is therefore validated against the *problem* (the QP
    constraints) rather than against the solver's status flag. A
    feasible point is only *offered* as a candidate: the candidate
    selection in ``optimize_portfolio_weights`` still keeps it only
    when its formation-window Sharpe beats the alternatives.
    """
    if y is None:
        return False
    y = np.asarray(y, dtype=float)
    if y.size == 0 or y.size != np.asarray(mu_s).size:
        return False
    if not np.all(np.isfinite(y)):
        return False
    if float(y.sum()) <= 1e-12:
        return False
    if float(np.min(y)) < -tol:
        return False
    if abs(float(mu_s @ y) - 1.0) > tol:
        return False
    if A_ub_y.size and float(np.max(A_ub_y @ y)) > tol:
        return False
    return True


def exact_qp(
    Q: np.ndarray,
    c: Optional[np.ndarray],
    A_ub: np.ndarray,
    b_ub: np.ndarray,
    A_eq: Optional[np.ndarray] = None,
    b_eq: Optional[np.ndarray] = None,
    tol: float = 1e-9,
) -> Optional[np.ndarray]:
    """Exact global optimum of a convex QP via active-set enumeration.

    Solves ``min 0.5 w'Qw + c'w`` subject to ``A_ub w <= b_ub``,
    ``A_eq w = b_eq`` and ``w >= 0`` by enumerating every active set of
    the inequality constraints, solving the resulting linear KKT
    system, and keeping the primal- and dual-feasible point with the
    lowest objective.

    Deterministic and environment independent: no iterative solver
    (SLSQP / HiGHS) is used, so the answer cannot depend on a
    build-dependent exit status or a BLAS thread count (ledger E049 /
    E050).  For the problem sizes met here (N = 2..5 components) the
    enumeration is exact and cheap: the QP is convex (Q is positive
    semidefinite), so every KKT point is a global optimum.

    Returns the optimal ``w`` or ``None`` if no KKT point is found.
    """
    Q = np.asarray(Q, dtype=float)
    N = Q.shape[0]
    if Q.shape != (N, N) or N == 0:
        return None
    c = np.zeros(N) if c is None else np.asarray(c, dtype=float)
    A_ub = np.asarray(A_ub, dtype=float)
    b_ub = np.asarray(b_ub, dtype=float)
    A_eq = (np.zeros((0, N)) if A_eq is None
            else np.asarray(A_eq, dtype=float))
    b_eq = (np.zeros(0) if b_eq is None
            else np.asarray(b_eq, dtype=float))
    if A_eq.size and A_eq.shape[1] != N:
        return None
    if A_ub.size and A_ub.shape[1] != N:
        return None

    # Inequality constraints in canonical form a_i'w <= beta_i:
    #   i in [0, N)       ->  -e_i'w <= 0        (w_i >= 0)
    #   i in [N, N+M)     ->  A_ub[i-N]'w <= b_ub[i-N]
    ineq = [(-np.eye(N)[i]) for i in range(N)]
    ineq_beta = [0.0] * N
    if A_ub.size:
        ineq += [A_ub[i] for i in range(A_ub.shape[0])]
        ineq_beta += [float(b_ub[i]) for i in range(A_ub.shape[0])]
    n_ineq = len(ineq)

    best_w: Optional[np.ndarray] = None
    best_obj = np.inf

    for r in range(0, n_ineq + 1):
        for combo in itertools.combinations(range(n_ineq), r):
            Act = np.array([ineq[i] for i in combo], dtype=float)
            Act_beta = np.array([ineq_beta[i] for i in combo], dtype=float)
            # Stack the equality constraints (A_eq w = b_eq) and the
            # active inequalities (Act w = Act_beta).  Either side may
            # be empty (no equalities, or no active inequalities) -
            # build the stacks from the non-empty parts only.
            parts = []
            b_parts = []
            if A_eq.size:
                parts.append(A_eq)
                b_parts.append(b_eq)
            if Act.size:
                parts.append(Act)
                b_parts.append(Act_beta)
            if not parts:
                # No constraints at all: S w = 0 => w = 0, which
                # cannot satisfy any nonzero equality, so skip.
                continue
            Astack = np.vstack(parts)
            bstack = np.concatenate(b_parts) if b_parts else np.zeros(0)
            # KKT system:
            #   [ Q   Astack^T ] [ w ]     [ -c ]
            #   [ Astack   0   ] [ l ]  =  [ bstack ]
            K = np.zeros((N + Astack.shape[0], N + Astack.shape[0]))
            K[:N, :N] = Q
            K[:N, N:] = Astack.T
            K[N:, :N] = Astack
            rhs = np.concatenate([-c, bstack])
            try:
                sol, *_ = np.linalg.lstsq(K, rhs, rcond=None)
            except np.linalg.LinAlgError:
                continue
            if sol.size != N + Astack.shape[0]:
                continue
            w = sol[:N]
            lam = sol[N:]
            # Primal feasibility
            if float(np.min(w)) < -tol:
                continue
            if A_ub.size and float(np.max(A_ub @ w - b_ub)) > tol:
                continue
            if A_eq.size and float(np.max(np.abs(A_eq @ w - b_eq))) > tol:
                continue
            # Dual feasibility: inequality multipliers >= 0
            if Act.size and np.min(lam[A_eq.shape[0]:]) < -tol:
                continue
            obj = 0.5 * float(w @ Q @ w) + float(c @ w)
            if best_w is None or obj < best_obj:
                best_obj = obj
                best_w = w.copy()
    return best_w


def exact_tangency_kkt(
    S_s: np.ndarray,
    mu_s: np.ndarray,
    A_ub_y: np.ndarray,
    tol: float = 1e-9,
) -> Optional[np.ndarray]:
    """Exact global optimum of the tangency QP via active-set enumeration.

    Thin wrapper over :func:`exact_qp` for the tangency problem
    ``min 0.5 y'Sy  s.t.  mu'y = 1,  y >= 0,  A_ub_y y <= 0``. Kept for
    backward compatibility with the E049/E050 call sites and tests.
    """
    S = np.asarray(S_s, dtype=float)
    N = S.shape[0]
    A = np.asarray(A_ub_y, dtype=float)
    if S.shape != (N, N) or A.size and A.shape[1] != N:
        return None
    return exact_qp(S, np.zeros(N), A, np.zeros(A.shape[0]),
                    A_eq=np.asarray(mu_s, dtype=float).reshape(1, -1),
                    b_eq=np.array([1.0]), tol=tol)


def _feasible(
    w: Optional[np.ndarray],
    beta_eq: Optional[np.ndarray],
    beta_fut: Optional[np.ndarray],
    beta_constraint: float,
) -> bool:
    if w is None:
        return False
    w = np.asarray(w, dtype=float)
    if not np.all(np.isfinite(w)) or np.any(w < -1e-9):
        return False
    if abs(float(w.sum()) - 1.0) > 1e-6:
        return False
    if beta_eq is not None and abs(float(beta_eq @ w)) > beta_constraint + 1e-6:
        return False
    if beta_fut is not None and abs(float(beta_fut @ w)) > beta_constraint + 1e-6:
        return False
    return True


def optimize_portfolio_weights(
    component_returns: pd.DataFrame,
    beta_constraint: float = 0.1,
    benchmark_returns: pd.Series = None,
    method: str = "max_sharpe",
    futures_benchmark_returns: pd.Series = None,
    seed: int = 42,
    ridge_lambda: float = 1e-4,
    n_grid: int = 2000,
) -> np.ndarray:
    """Optimal component weights on one formation window.

    Args:
        component_returns: (T, N) component net returns on the formation
            window (no look-ahead: trailing window ending at the rebalance
            date).
        beta_constraint: maximum absolute portfolio beta vs each benchmark.
        benchmark_returns: SPY returns (equity-beta constraint).
        method: "max_sharpe" (primary), "min_var", or "risk_parity".
        futures_benchmark_returns: equal-weight futures-index returns
            (futures-beta constraint).
        seed: seed for the deterministic Dirichlet grid fallback.
        ridge_lambda: ridge added to the shrunk covariance.
        n_grid: Dirichlet grid size (0 disables the grid layer).

    Returns:
        (N,) non-negative weight vector summing to 1.0. Falls back to
        equal weights if no feasible point is found.
    """
    R = component_returns.dropna(how="all")
    mu = R.mean().to_numpy(dtype=float)
    N = len(mu)
    if N == 0:
        return np.zeros(0)
    Sigma = ledoit_wolf_covariance(R.to_numpy(dtype=float))
    Sigma = Sigma + ridge_lambda * np.eye(N)

    beta_eq = (
        _beta_exposure(R, benchmark_returns) if benchmark_returns is not None else None
    )
    beta_fut = (
        _beta_exposure(R, futures_benchmark_returns)
        if futures_benchmark_returns is not None
        else None
    )

    def sharpe(w: np.ndarray) -> float:
        var = float(w @ Sigma @ w)
        if var <= 0.0:
            return -np.inf
        return float(w @ mu) / np.sqrt(var)

    # ---- Linear-constraint machinery (linprog form) ----
    # sum(w)=1, w>=0, |beta_eq'w|<=c, |beta_fut'w|<=c.
    betas = [b for b in (beta_eq, beta_fut) if b is not None]
    if betas:
        B = np.vstack([np.asarray(b, dtype=float) for b in betas])
    else:
        B = np.zeros((0, N))
    M = B.shape[0]
    A_ub = np.vstack([B, -B]) if M else np.zeros((0, N))
    b_ub = np.full(2 * M, float(beta_constraint))
    A_eq = np.ones((1, N))
    b_eq = np.array([1.0])
    bounds = [(0.0, 1.0)] * N

    # Phase I: feasibility via LP (HiGHS). The feasible region is a
    # convex polytope that lies in the tails of the simplex, so
    # random simplex sampling almost never finds it; an LP always
    # does (or proves infeasibility).
    phase1 = linprog(
        np.zeros(N), A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
        bounds=bounds, method="highs",
    )
    w_feas = np.asarray(phase1.x, dtype=float) if phase1.success else None

    def solve_qp(objective, init, eq_row=None, eq_val=None):
        """SLSQP on a (scaled) quadratic/linear objective.

        ``objective(w)`` returns the scalar to minimize. ``eq_row``
        adds an equality constraint ``eq_row'w = eq_val`` (used for
        the tangency normalization). Linear beta constraints are
        always attached.
        """
        cons = []
        if eq_row is not None:
            cons.append(
                {"type": "eq",
                 "fun": lambda w, r=eq_row, v=eq_val: float(r @ w) - v}
            )
        for row in A_ub:
            cons.append(
                {"type": "ineq",
                 "fun": lambda w, r=row: float(beta_constraint)
                 - float(r @ w)}
            )
            cons.append(
                {"type": "ineq",
                 "fun": lambda w, r=row: float(beta_constraint)
                 + float(r @ w)}
            )
        cons.append({"type": "eq", "fun": lambda w: float(w.sum()) - 1.0})
        res = minimize(
            objective,
            init,
            method="SLSQP",
            bounds=bounds,
            constraints=cons,
            options={"maxiter": 500, "ftol": 1e-12},
        )
        return res

    candidates: List[np.ndarray] = []
    if w_feas is not None:
        candidates.append(w_feas)

    if method == "min_var":
        # min 0.5 w'Sigma w  s.t.  sum(w)=1, w>=0, |B'w|<=c.
        w_opt = exact_qp(Sigma, np.zeros(N), A_ub, b_ub,
                          A_eq=A_eq, b_eq=b_eq)
        if w_opt is not None and _feasible(w_opt, beta_eq, beta_fut,
                                           beta_constraint):
            candidates.append(w_opt)
    elif method == "risk_parity":
        # Inverse-volatility risk budget; if it violates the beta
        # constraint, fall back to the exact min-variance solution as
        # the constrained risk-budgeted proxy.
        vols = np.sqrt(np.diag(Sigma))
        vols = np.where(vols > 0.0, vols, 1.0)
        w_ip = (1.0 / vols)
        w_ip = w_ip / w_ip.sum()
        if _feasible(w_ip, beta_eq, beta_fut, beta_constraint):
            candidates.append(w_ip)
        w_opt = exact_qp(Sigma, np.zeros(N), A_ub, b_ub,
                          A_eq=A_eq, b_eq=b_eq)
        if w_opt is not None and _feasible(w_opt, beta_eq, beta_fut,
                                           beta_constraint):
            candidates.append(w_opt)
    else:  # max_sharpe (primary)
        # Tangency portfolio via the standard QP reformulation:
        # max_w w'mu/sqrt(w'Sw) is invariant to scaling of mu and
        # Sigma, so solve  min_y y'Sy  s.t.  mu'y = 1, y >= 0,
        # |B'y| <= c * 1'y  (homogeneous linear constraints), then
        # normalize w = y / sum(y). The homogeneous form keeps the
        # beta constraints scale-invariant under the normalization.
        if w_feas is not None:
            sc_mu = float(np.max(np.abs(mu)))
            if sc_mu < 1e-12:
                sc_mu = 1e-12
            mu_s = mu / sc_mu
            sc_S = float(np.mean(np.diag(Sigma)))
            if sc_S < 1e-12:
                sc_S = 1e-12
            S_s = Sigma / sc_S
            # homogeneous beta constraints: (B - cJ)'y <= 0 and
            # (-B - cJ)'y <= 0 with J the all-ones matrix.
            J = np.ones_like(B)
            A_ub_y = np.vstack([B - beta_constraint * J,
                                  -B - beta_constraint * J]) if M else \
                np.zeros((0, N))
            # Exact active-set KKT enumeration (ledger E049/E050):
            # deterministic, environment independent, and globally
            # optimal for the convex QP.  SLSQP is retained only as a
            # fallback when the exact enumeration finds no KKT point
            # (it never adds a better answer than the exact solver,
            # so keeping it does not reintroduce the environment
            # dependence the exact branch removes).
            y_kkt = exact_qp(S_s, np.zeros(N), A_ub_y,
                             np.zeros(A_ub_y.shape[0]),
                             A_eq=mu_s.reshape(1, -1),
                             b_eq=np.array([1.0]))
            if _tangency_feasible(y_kkt, mu_s, A_ub_y):
                w_tan = y_kkt / float(y_kkt.sum())
                if _feasible(w_tan, beta_eq, beta_fut,
                               beta_constraint):
                    candidates.append(w_tan)
            else:
                y0 = w_feas / max(float(mu_s @ w_feas), 1e-12)
                cons_y = [
                    {"type": "eq",
                     "fun": lambda y: float(mu_s @ y) - 1.0}
                ]
                for row in A_ub_y:
                    cons_y.append(
                        {"type": "ineq",
                         "fun": lambda y, r=row: -float(r @ y)}
                    )
                res = minimize(
                    lambda y: 0.5 * float(y @ S_s @ y),
                    y0,
                    method="SLSQP",
                    bounds=[(0.0, None)] * N,
                    constraints=cons_y,
                    options={"maxiter": 500, "ftol": 1e-12},
                )
                y = np.asarray(res.x, dtype=float)
                # Validate the answer on the QP constraints, not on
                # the solver's exit status: an infeasible/garbage
                # answer is rejected here, a feasible one competes
                # on Sharpe with the LP fallback.
                if _tangency_feasible(y, mu_s, A_ub_y):
                    w_tan = y / float(y.sum())
                    if _feasible(w_tan, beta_eq, beta_fut,
                                   beta_constraint):
                        candidates.append(w_tan)

    best_w, best_s = None, -np.inf
    for w in candidates:
        if not _feasible(w, beta_eq, beta_fut, beta_constraint):
            continue
        s = sharpe(w)
        if s > best_s:
            best_s, best_w = s, w

    # Deterministic seeded Dirichlet grid: secondary robustness
    # layer (the feasible region is usually found by the LP/QP
    # phases; the grid bounds any residual SLSQP local-optimum
    # gap for very small N).
    rng = np.random.default_rng(seed)
    for _ in range(int(n_grid)):
        w = rng.dirichlet(np.ones(N))
        if _feasible(w, beta_eq, beta_fut, beta_constraint):
            s = sharpe(w)
            if s > best_s:
                best_s, best_w = s, w

    if best_w is not None:
        return np.asarray(best_w, dtype=float)

    # Infeasible constraint set (e.g. a component subset whose
    # every member carries beta above the cap): return the
    # minimum-violation portfolio - the LP that minimizes the
    # largest |beta| subject to sum(w)=1, w>=0. This is the
    # honest "constrained as tightly as achievable" answer.
    if M:
        # variables: [w (N), t (1)];  min t  s.t.  Bw - t <= c,
        # -Bw - t <= c, sum(w)=1, w>=0, t>=0.
        c_obj = np.concatenate([np.zeros(N), [1.0]])
        A_ub_r = np.hstack(
            [np.vstack([B, -B]), -np.ones((2 * M, 1))]
        )
        b_ub_r = np.full(2 * M, float(beta_constraint))
        A_eq_r = np.hstack([np.ones((1, N)), np.zeros((1, 1))])
        b_eq_r = np.array([1.0])
        bounds_r = [(0.0, 1.0)] * N + [(0.0, None)]
        relax = linprog(
            c_obj, A_ub=A_ub_r, b_ub=b_ub_r, A_eq=A_eq_r,
            b_eq=b_eq_r, bounds=bounds_r, method="highs",
        )
        if relax.success:
            return np.asarray(relax.x[:N], dtype=float)

    # Last resort: equal weights (violates the beta constraint;
    # flagged by the caller's feasibility diagnostics).
    return np.asarray(np.ones(N) / N, dtype=float)


def walk_forward_blend_weights(
    component_returns: pd.DataFrame,
    benchmark_returns: pd.Series = None,
    futures_benchmark_returns: pd.Series = None,
    formation_window: int = 504,
    rebalance_freq: int = 21,
    beta_constraint: float = 0.1,
    method: str = "max_sharpe",
    seed: int = 42,
    n_grid: int = 2000,
) -> pd.DataFrame:
    """Daily target component weights (walk-forward, no look-ahead).

    At each rebalance date (every ``rebalance_freq`` trading days, the
    same positional cadence as ``src.backtest._rebalance_weights``) the
    optimizer sees only the trailing ``formation_window`` days of component
    returns and returns a non-negative weight vector summing to 1.0.
    Before the first full formation window the equal-weight (1/N) default
    is used (it requires no history). Weights are held constant between
    rebalance dates.

    Note: the signature takes component *return streams* (not raw closes)
    because the five components live on different universes; the blend is
    defined at the return-stream level. Asset-level weights can be
    recovered with ``expand_to_asset_weights``.

    Returns a (T, N) DataFrame indexed like ``component_returns``.
    """
    R = component_returns.dropna(how="all")
    idx = R.index
    N = R.shape[1]
    cols = list(R.columns)
    W = pd.DataFrame(np.nan, index=idx, columns=cols)
    if N == 0:
        return W.fillna(0.0)
    equal = np.ones(N) / N
    n_days = len(idx)
    for pos in range(0, n_days, rebalance_freq):
        if pos >= formation_window:
            window = R.iloc[pos - formation_window:pos]
            w = optimize_portfolio_weights(
                window,
                beta_constraint=beta_constraint,
                benchmark_returns=benchmark_returns,
                method=method,
                futures_benchmark_returns=futures_benchmark_returns,
                seed=seed,
                n_grid=n_grid,
            )
        else:
            w = equal
        W.iloc[pos] = w
    return W.ffill().fillna(0.0)


def portfolio_placebo_weights(
    component_returns: pd.DataFrame,
    n_simulations: int = 50,
    seed: int = 42,
    rebalance_freq: int = 21,
) -> List[pd.DataFrame]:
    """Component-level placebo null (component-weight permutation).

    At each rebalance date (same positional cadence as the real
    walk-forward) component weights are drawn from a symmetric
    Dirichlet(1) on the simplex - random, long-only, fully invested -
    and held constant between rebalance dates. This preserves the
    rebalance/execution/cost structure of the real portfolio while
    destroying any timing or optimization content, so the real
    portfolio's OOS Sharpe can be scored against the null.

    Note: the input is the component *return stream* frame (its index
    defines the calendar and its width the number of components); the
    spec's ``component_weight_series`` list is interchangeable for this
    purpose since only the calendar and dimensionality are needed.

    Returns a list of (T, N) DataFrames indexed like
    ``component_returns``.
    """
    R = component_returns.dropna(how="all")
    idx = R.index
    N = R.shape[1]
    cols = list(R.columns)
    rng = np.random.default_rng(seed)
    out: List[pd.DataFrame] = []
    n_days = len(idx)
    for _ in range(int(n_simulations)):
        W = pd.DataFrame(np.nan, index=idx, columns=cols)
        for pos in range(0, n_days, rebalance_freq):
            W.iloc[pos] = rng.dirichlet(np.ones(N))
        out.append(W.ffill().fillna(0.0))
    return out


def project_onto_beta_cap(
    w0: np.ndarray,
    beta_eq: Optional[np.ndarray],
    beta_fut: Optional[np.ndarray],
    beta_constraint: float,
) -> np.ndarray:
    """Project a simplex point onto the beta-constrained feasible set.

    Solves ``min_w ||w - w0||^2`` subject to ``sum(w) = 1``,
    ``w >= 0`` and ``|beta'w| <= beta_constraint`` for each
    benchmark - the same constraint set
    ``optimize_portfolio_weights`` enforces. Used by the
    beta-constrained placebo null so random Dirichlet(1)
    component-weight draws respect the same market-neutrality
    cap as the real optimizer (E042 G2 pre-registration).

    Fallback chain if the QP fails or returns an infeasible
    point: LP phase-1 feasible point, LP minimum-violation
    point, equal weights.
    """
    w0 = np.asarray(w0, dtype=float)
    N = len(w0)
    if N == 0:
        return w0
    betas = [b for b in (beta_eq, beta_fut) if b is not None]
    if betas:
        B = np.vstack([np.asarray(b, dtype=float) for b in betas])
    else:
        B = np.zeros((0, N))
    M = B.shape[0]
    A_ub = np.vstack([B, -B]) if M else np.zeros((0, N))
    b_ub = np.full(2 * M, float(beta_constraint))
    bounds = [(0.0, 1.0)] * N

    if _feasible(w0, beta_eq, beta_fut, beta_constraint):
        return w0

    cons = [{"type": "eq",
             "fun": lambda w: float(w.sum()) - 1.0}]
    for row in A_ub:
        cons.append({"type": "ineq",
                     "fun": lambda w, r=row: float(beta_constraint)
                     - float(r @ w)})
        cons.append({"type": "ineq",
                     "fun": lambda w, r=row: float(beta_constraint)
                     + float(r @ w)})
    res = minimize(
        lambda w: float((w - w0) @ (w - w0)),
        w0,
        method="SLSQP",
        bounds=bounds,
        constraints=cons,
        options={"maxiter": 200, "ftol": 1e-12},
    )
    # As in the tangency branch: judge the answer by the constraints it
    # satisfies, not by the solver's exit status. SLSQP can report
    # failure at a constrained optimum while returning a feasible point;
    # discarding it would replace the projection by an unrelated LP
    # vertex and make the placebo null environment dependent.
    if _feasible(res.x, beta_eq, beta_fut, beta_constraint):
        return np.asarray(res.x, dtype=float)

    phase1 = linprog(
        np.zeros(N), A_ub=A_ub, b_ub=b_ub,
        A_eq=np.ones((1, N)), b_eq=np.array([1.0]),
        bounds=bounds, method="highs",
    )
    if phase1.success:
        w_feas = np.asarray(phase1.x, dtype=float)
        if _feasible(w_feas, beta_eq, beta_fut, beta_constraint):
            return w_feas

    if M:
        # Minimum-violation LP: min t s.t. Bw - t <= c,
        # -Bw - t <= c, sum(w)=1, w>=0, t>=0.
        c_obj = np.concatenate([np.zeros(N), [1.0]])
        A_ub_r = np.hstack(
            [np.vstack([B, -B]), -np.ones((2 * M, 1))]
        )
        b_ub_r = np.full(2 * M, float(beta_constraint))
        A_eq_r = np.hstack([np.ones((1, N)), np.zeros((1, 1))])
        b_eq_r = np.array([1.0])
        bounds_r = [(0.0, 1.0)] * N + [(0.0, None)]
        relax = linprog(
            c_obj, A_ub=A_ub_r, b_ub=b_ub_r, A_eq=A_eq_r,
            b_eq=b_eq_r, bounds=bounds_r, method="highs",
        )
        if relax.success:
            return np.asarray(relax.x[:N], dtype=float)

    return np.ones(N) / N


def portfolio_placebo_weights_beta_constrained(
    component_returns: pd.DataFrame,
    formation_window: int = 504,
    benchmark_returns: pd.Series = None,
    futures_benchmark_returns: pd.Series = None,
    beta_constraint: float = 0.05,
    n_simulations: int = 50,
    seed: int = 42,
    rebalance_freq: int = 21,
) -> List[pd.DataFrame]:
    """Beta-constrained component-level placebo null.

    Identical to ``portfolio_placebo_weights`` (symmetric
    Dirichlet(1) component-weight draws per rebalance, held
    constant between rebalance dates, same rebalance/execution
    structure) except that each draw is PROJECTED onto the
    beta-constrained feasible set (``project_onto_beta_cap``)
    using the same trailing formation-window beta exposures
    the real optimizer sees (no look-ahead). The null is
    therefore MATCHED to the market-neutrality constraint: a
    z-score computed against it measures the
    formation-window/timing content of the real optimizer,
    not the Sharpe cost of the constraint itself.

    Before the first full formation window the equal-weight
    (1/N) default is used, matching ``walk_forward_blend_weights``.
    """
    R = component_returns.dropna(how="all")
    idx = R.index
    N = R.shape[1]
    cols = list(R.columns)
    rng = np.random.default_rng(seed)
    n_days = len(idx)

    # Precompute the formation-window beta exposures at each
    # rebalance date (trailing window only - no look-ahead).
    exposures = {}
    for pos in range(0, n_days, rebalance_freq):
        if pos >= formation_window:
            win = R.iloc[pos - formation_window:pos]
            b_eq = (
                _beta_exposure(win, benchmark_returns)
                if benchmark_returns is not None else None
            )
            b_fut = (
                _beta_exposure(win, futures_benchmark_returns)
                if futures_benchmark_returns is not None else None
            )
        else:
            b_eq = b_fut = None
        exposures[pos] = (b_eq, b_fut)

    out: List[pd.DataFrame] = []
    for _ in range(int(n_simulations)):
        W = pd.DataFrame(np.nan, index=idx, columns=cols)
        for pos in range(0, n_days, rebalance_freq):
            b_eq, b_fut = exposures[pos]
            if b_eq is None and b_fut is None:
                W.iloc[pos] = np.ones(N) / N
                continue
            w0 = rng.dirichlet(np.ones(N))
            W.iloc[pos] = project_onto_beta_cap(
                w0, b_eq, b_fut, beta_constraint)
        out.append(W.ffill().fillna(0.0))
    return out


def expand_to_asset_weights(
    component_weights: pd.DataFrame,
    component_weight_series: List[pd.DataFrame],
) -> pd.DataFrame:
    """Expand component-level weights to asset-level target weights.

    Each component weight multiplies that component's asset-level weight
    series (pre-computed on its own universe, held constant intra-
    component-rebalance), producing the blended asset-level target
    weights:  W_asset(a, t) = sum_i comp_w_i(t) * comp_asset_w_i(a, t).
    Assets outside a component's universe contribute zero. Returns a
    DataFrame indexed like ``component_weights`` with the union of asset
    columns.
    """
    out = None
    for i, aws in enumerate(component_weight_series):
        if i >= component_weights.shape[1]:
            break
        scale = component_weights.iloc[:, i]
        contrib = aws.mul(scale, axis=0).fillna(0.0)
        if out is None:
            out = contrib
        else:
            out = out.add(contrib, fill_value=0.0)
    if out is None:
        return pd.DataFrame(index=component_weights.index)
    return out.reindex(component_weights.index).fillna(0.0)
