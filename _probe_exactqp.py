"""Instrument exact_qp to see what it returns for the E042-lead tangency QP."""
import sys, json, numpy as np, shutil
sys.path.insert(0, "src")
sys.path.insert(0, "experiments")
import portfolio_opt as po

_calls = []
_orig = po.exact_qp

def _logged(Q, c, A_ub, b_ub, A_eq=None, b_eq=None, tol=1e-9):
    r = _orig(Q, c, A_ub, b_ub, A_eq=A_eq, b_eq=b_eq, tol=tol)
    if A_eq is not None and getattr(A_eq, "size", 0) and np.asarray(b_eq).size:
        Qa = np.asarray(Q, float)
        _calls.append({
            "N": Qa.shape[0],
            "cond": float(np.linalg.cond(Qa)) if Qa.shape[0] else float("nan"),
            "returned": None if r is None else [float(x) for x in np.asarray(r).ravel()],
        })
    return r

po.exact_qp = _logged

import experiments.run_e042_lead as driver
driver.portfolio_opt.exact_qp = _logged

shutil.copy("experiments/e042_lead_config_confirmatory.json", "/tmp/gold_before_probe.json")
driver.main()
shutil.copy("experiments/e042_lead_config_confirmatory.json", "/tmp/gold_after_probe.json")
shutil.copy("/tmp/gold_before_probe.json", "experiments/e042_lead_config_confirmatory.json")

print("\n=== exact_qp tangency calls ===")
for i, c in enumerate(_calls):
    print(i, "N=", c["N"], "cond=", f"{c['cond']:.3e}", "returned=", c["returned"])

d = json.load(open("/tmp/gold_after_probe.json"))
print("\nprimary equity_beta:", d["primary"]["equity_beta"])
print("primary oos_sharpe:", d["primary"]["oos_sharpe"])