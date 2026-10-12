"""E029 feasibility gate: yfinance fundamental accounting coverage for large_liquid.

Records the decisive evidence for the E029 fundamental-factors task:
- field availability (Revenue, Cost Of Revenue, Gross Profit, Total Assets)
- history depth (earliest quarterly / annual period end per name)
- whether a 2014-2026 walk-forward is possible with this data source.
"""

import json
import os
import time
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf

UNIVERSE = [
    "AAPL","ABBV","ABT","ACN","ADBE","ADI","ADM","ADP","ADSK","AEP",
    "AIG","ALL","AMAT","AMD","AMGN","AMT","AMZN","AVGO","AXP","BA",
    "BAC","BK","BKNG","BMY","BSX","C","CAT","CCI","CDNS",
    "CHTR","CI","CL","CMCSA","CME","COF","COP","COST","CRM","CSCO",
    "CSX","CVS","CVX","DE","DHR","DIS","DOW","DXCM","EMR","EOG",
    "EQIX","ETN","EXC","FDX","FIS","FTNT","GD","GE","GILD","GM",
    "GOOG","GOOGL","GS","HD","HON","IBM","ICE","INTU","ISRG",
    "JNJ","JPM","KDP","KHC","KLAC","KO","LIN","LLY","LMT","LOW",
    "LRCX","MA","MCD","MDLZ","MDT","META","MET","MMM","MO","MRK",
    "MS","MSFT","MU","NFLX","NKE","NOW","NVDA","ORCL","PCAR","PEP",
    "PFE","PG","PLD","PM","PNC","PYPL","QCOM","REGN","ROST","RTX",
    "SBUX","SCHW","SLB","SO","SPG","T","TGT","TJX","TMO","TMUS",
    "TSLA","TXN","UNH","UNP","UPS","USB","V","VZ","WBA","WFC",
    "WMT","XOM",
]

QF_FIELDS = ["Total Revenue", "Cost Of Revenue", "Gross Profit"]
BS_FIELDS = ["Total Assets"]


def main():
    rows = {}
    t0 = time.time()
    for i, t in enumerate(UNIVERSE):
        try:
            tk = yf.Ticker(t)
            qf = tk.quarterly_financials
            bs = tk.balancesheet
            row = {
                "qf_n_periods": int(len(qf.columns)),
                "bs_n_periods": int(len(bs.columns)),
                "qf_earliest": str(qf.columns[-1].date()) if len(qf.columns) else None,
                "bs_earliest": str(bs.columns[-1].date()) if len(bs.columns) else None,
                "qf_has_revenue": bool("Total Revenue" in qf.index),
                "qf_has_cogs": bool("Cost Of Revenue" in qf.index),
                "qf_has_gross_profit": bool("Gross Profit" in qf.index),
                "bs_has_total_assets": bool("Total Assets" in bs.index),
            }
            rows[t] = row
        except Exception as e:
            rows[t] = {"error": str(e)}
        if (i + 1) % 25 == 0:
            print(f"  probed {i+1}/{len(UNIVERSE)}")
        time.sleep(0.05)

    n = len(rows)
    has_rev = sum(1 for r in rows.values() if r.get("qf_has_revenue"))
    has_cogs = sum(1 for r in rows.values() if r.get("qf_has_cogs"))
    has_gp = sum(1 for r in rows.values() if r.get("qf_has_gross_profit"))
    has_ta = sum(1 for r in rows.values() if r.get("bs_has_total_assets"))
    full = sum(1 for r in rows.values()
               if r.get("qf_has_revenue") and r.get("qf_has_cogs")
               and r.get("qf_has_gross_profit") and r.get("bs_has_total_assets"))

    earliest_q = sorted({r["qf_earliest"] for r in rows.values() if r.get("qf_earliest")})
    earliest_b = sorted({r["bs_earliest"] for r in rows.values() if r.get("bs_earliest")})

    result = {
        "experiment": "E029_fundamental_factors_feasibility",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "n_universe": n,
        "n_with_revenue": has_rev,
        "n_with_cogs": has_cogs,
        "n_with_gross_profit": has_gp,
        "n_with_total_assets": has_ta,
        "n_with_all_fields": full,
        "coverage_frac_all_fields": full / n,
        "qf_earliest_periods": earliest_q,
        "bs_earliest_periods": earliest_b,
        "per_name": rows,
        "elapsed_s": round(time.time() - t0, 1),
        "verdict": (
            "FEASIBLE" if full / n >= 0.5 else "INFEASIBLE"
        ),
    }
    print(json.dumps({k: v for k, v in result.items() if k != "per_name"}, indent=2, default=str))
    os.makedirs("experiments", exist_ok=True)
    with open("experiments/e029_fundamental_feasibility.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    print("Saved experiments/e029_fundamental_feasibility.json")


if __name__ == "__main__":
    main()