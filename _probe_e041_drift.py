"""Measure E041 drift vs committed golden WITHOUT overwriting it.

Runs the driver as a subprocess inside a sandbox CWD (symlinks to the real
repo's src/ledger/data/tests/scripts, temp experiments/ seeded from the
goldens), diffs the new outputs against the committed goldens, and reports:
# diffs, # structural (non-numeric), max relative drift, worst drift as a
multiple of the 1e-4 tolerance, and whether decision / gates_passed_count /
gate flags are unchanged.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))

tmp = tempfile.mkdtemp()
for name in ["src", "ledger", "data", "tests", "scripts", "experiments"]:
    src = os.path.join(ROOT, name)
    if os.path.isdir(src) or os.path.isfile(src):
        os.symlink(src, os.path.join(tmp, name))
exp_tmp = os.path.join(tmp, "experiments")
if os.path.isdir(exp_tmp):
    os.remove(exp_tmp)
os.makedirs(exp_tmp)
for f in ["e041_market_neutral_portfolio.json", "e041_sensitivity_grid.json"]:
    shutil.copy2(os.path.join(ROOT, "experiments", f), os.path.join(exp_tmp, f))

env = dict(os.environ, QUANT_RESEARCH_OFFLINE="1", SEED="42")
r = subprocess.run([sys.executable, "experiments/run_e041.py"],
                   cwd=tmp, env=env, capture_output=True, text=True)
print("driver rc:", r.returncode)
if r.returncode != 0:
    print(r.stdout[-3000:])
    print(r.stderr[-3000:])
    sys.exit(1)

for f in ["e041_market_neutral_portfolio.json", "e041_sensitivity_grid.json"]:
    new = json.load(open(os.path.join(exp_tmp, f)))
    gold = json.load(open(os.path.join(ROOT, "experiments", f)))

    def walk(a, b, path=""):
        diffs = []
        if isinstance(a, dict) and isinstance(b, dict):
            for k in set(a) | set(b):
                diffs += walk(a.get(k), b.get(k), path + "/" + str(k))
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                diffs.append((path, "STRUCT len", len(a), len(b)))
            else:
                for i, (x, y) in enumerate(zip(a, b)):
                    diffs += walk(x, y, path + "[%d]" % i)
        else:
            if type(a) is not type(b):
                diffs.append((path, "STRUCT type", type(a).__name__, type(b).__name__))
            elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                if a != b:
                    denom = max(abs(b), 1e-300)
                    rel = abs(a - b) / denom
                    diffs.append((path, "num", a, b, rel))
            elif a != b:
                diffs.append((path, "STRUCT val", str(a)[:60], str(b)[:60]))
        return diffs

    d = walk(new, gold)
    num = [x for x in d if x[1] == "num"]
    struct = [x for x in d if x[1] != "num"]
    maxrel = max((x[4] for x in num), default=0.0)
    worst_mult = maxrel / 1e-4
    print(f"\n=== {f} ===")
    print(f"total diffs: {len(d)}  numeric: {len(num)}  structural: {len(struct)}")
    print(f"max relative drift: {maxrel:.3e}  ({worst_mult:.1f}x the 1e-4 tolerance)")
    if struct:
        print("structural examples:", struct[:5])
    if num:
        worst = max(num, key=lambda x: x[4])
        print("worst numeric:", worst[0], worst[2], "->", worst[3], "rel", worst[4])
    for key in ["decision", "gates_passed_count", "gates_total"]:
        if key in new and key in gold:
            print(f"{key}: new={new[key]} gold={gold[key]} same={new[key]==gold[key]}")
    if "gates" in new and "gates" in gold:
        print(f"gates flags identical: {new['gates'] == gold['gold']}")
    if "promotion_gates" in new and "promotion_gates" in gold:
        pg_new = {g.get("name"): g.get("passed") for g in new["promotion_gates"] if isinstance(g, dict)}
        pg_gold = {g.get("name"): g.get("passed") for g in gold["promotion_gates"] if isinstance(g, dict)}
        print(f"promotion_gates flags identical: {pg_new == pg_gold}")

shutil.rmtree(tmp)