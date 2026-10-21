import json
from itertools import product
from src.run_experiment import run_strategy, STRATEGIES, UNIVERSES

UNIVERSE = "large_liquid"
universe = UNIVERSES[UNIVERSE]

top = ["reversal", "low_vol", "quality", "momentum_6m", "momentum"]

tc_vals = [0.0000, 0.0005, 0.0010, 0.0020]
sl_vals = [0.0000, 0.0002, 0.0005]

rows = []
for strat in top:
    try:
        base = run_strategy(strat, universe)
        turnover = base.get("turnover_avg", float('nan'))
        sharps = [f["sharpe"] for f in base["oos_folds"]]
        rows.append({
            "strategy": strat,
            "tc_cost": base["costs"]["tc_cost"],
            "slippage": base["costs"]["slippage"],
            "turnover_avg": turnover,
            "oos_sharpe": float(sum(sharps)/len(sharps)) if sharps else float('nan')
        })
    except Exception as e:
        print(f"ERR base {strat}: {e}")

    for tc, sl in product(tc_vals, sl_vals):
        if tc == 0.0005 and sl == 0.0002:
            continue  # already have base
        try:
            r = run_strategy(strat, universe, tc_cost=tc, slippage=sl)
            sharps = [f["sharpe"] for f in r["oos_folds"]]
            rows.append({
                "strategy": strat,
                "tc_cost": tc,
                "slippage": sl,
                "turnover_avg": r.get("turnover_avg", turnover),
                "oos_sharpe": float(sum(sharps)/len(sharps)) if sharps else float('nan')
            })
        except Exception as e:
            print(f"ERR {strat} tc={tc} sl={sl}: {e}")

with open("experiments/cost_sensitivity.json", "w") as f:
    json.dump(rows, f, indent=2, default=str)

print("done")
