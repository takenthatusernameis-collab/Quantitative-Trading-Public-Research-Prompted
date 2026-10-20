#!/usr/bin/env python3
"""Fast offline audit of the data-cache provenance.

Why this exists
---------------
A verification run compares a fresh driver output against a committed golden.
That comparison is only meaningful if both were computed from the *same*
input data. The input data is the cached parquet panel in ``data/``, keyed by
the download end date, and the repo pins that end date in
``data/vintages.json`` (``default_end_date``).

The 2026-10-19 session recorded the extended-suite divergences as
"floating-point drift". Direct measurement (2026-10-20, ledger entry E045)
shows they are not: several goldens were produced against a price panel that
ends *after* the pinned vintage, and some drivers read cache files that are
not committed at all, so they silently re-download from the network and pick
up revised adjusted prices. Both effects move the numbers far more than
floating-point noise.

This script makes the provenance visible without running any experiment:

  1. the pinned vintage and the end date it resolves to,
  2. an inventory of the cached panels (which end dates exist, which files are
     committed, which are untracked leftovers),
  3. for every driver input we can resolve statically, the cache file it
     needs and whether that file is committed - a driver whose input is not
     committed is not reproducible offline,
  4. a label/content integrity check on the committed panels (the last date
     inside a panel must not be after the end date in its filename),
  5. the last observation date of every cached FRED series (macro series get
     revised, so their vintage is part of the input provenance too).

Usage:
    python3 scripts/audit_data_vintage.py            # report (exit 0 unless an
                                                    # integrity check fails)
    python3 scripts/audit_data_vintage.py --strict   # also fail when a driver
                                                    # input is not committed

Exit codes: 0 = no integrity violation, 1 = integrity violation (or, with
--strict, an uncommitted driver input), 2 = usage/IO error.
"""
import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
VINTAGES = DATA_DIR / "vintages.json"

END_DATE_RE = re.compile(r"_(20\d{2}-\d{2}-\d{2})(\.parquet(\.adj\d\.act\d)?)?$")


# --- mirror of src/data.py::_cache_path (kept in sync by a unit test) -------
def cache_path(ticker_key, start, end, auto_adjust=True, actions=False):
    """Cache file name for a ticker key / start / end (see src/data.py)."""
    h = hashlib.sha256(str(ticker_key).encode()).hexdigest()[:16]
    safe = str(ticker_key)[:80].replace("/", "_").replace("^", "").replace("|", "_")
    suffix = "" if (auto_adjust and not actions) else f".adj{int(auto_adjust)}.act{int(actions)}"
    return f"{safe}_{h}_{start}_{end}.parquet{suffix}"


def _git_tracked(root, rel_path):
    """True when the path is tracked by git."""
    r = subprocess.run(["git", "ls-files", "--error-unmatch", "--", rel_path],
                       cwd=str(root), capture_output=True, text=True)
    return r.returncode == 0


def _git_tracked_set(root):
    r = subprocess.run(["git", "ls-files", "--", "data"],
                       cwd=str(root), capture_output=True, text=True)
    if r.returncode != 0:
        print(f"NOTE git ls-files failed ({r.stderr.strip() or 'git error'}); "
              f"treating every cached panel as uncommitted")
        return set()
    return {ln.strip() for ln in r.stdout.splitlines() if ln.strip()}


def pinned_end_date():
    """The end date pinned in data/vintages.json (None when absent)."""
    if not VINTAGES.exists():
        return None
    try:
        with open(VINTAGES) as f:
            return json.load(f).get("default_end_date")
    except (OSError, ValueError):
        return None


# --- static resolution of driver data inputs --------------------------------
class _ModuleSymbols(ast.NodeVisitor):
    """Collect module-level constant lists / strings for call resolution."""

    def __init__(self):
        self.symbols = {}

    def visit_Assign(self, node):
        if isinstance(node.value, (ast.List, ast.Constant)):
            value = self._literal(node.value)
            if value is not None:
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.symbols[target.id] = value
        self.generic_visit(node)

    @staticmethod
    def _literal(node):
        if isinstance(node, ast.Constant):
            return node.value if isinstance(node.value, (str, int, float)) else None
        if isinstance(node, ast.List):
            items = []
            for elt in node.elts:
                if not isinstance(elt, ast.Constant) or not isinstance(elt.value, str):
                    return None
                items.append(elt.value)
            return items
        return None


def _resolve(node, symbols):
    """Resolve a literal argument, or a module-level constant holding one."""
    value = _ModuleSymbols._literal(node)
    if value is not None:
        return value
    if isinstance(node, ast.Name):
        return symbols.get(node.id)
    return None


def _call_kwargs(call):
    return {kw.arg: kw.value for kw in call.keywords if kw.arg}


def driver_inputs(path, symbols, pinned):
    """Return the cache inputs a driver file requests (statically resolvable)."""
    try:
        tree = ast.parse(Path(path).read_text())
    except (OSError, SyntaxError):
        return []
    collector = _ModuleSymbols()
    collector.visit(tree)

    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
        if name not in ("download", "get_benchmark"):
            continue
        if not node.args:
            continue
        tickers = _resolve(node.args[0], collector.symbols)
        if isinstance(tickers, str):
            tickers = [tickers]
        if not isinstance(tickers, list) or not tickers:
            continue
        kwargs = _call_kwargs(node)
        start = _resolve(kwargs["start"], collector.symbols) if "start" in kwargs else None
        end = _resolve(kwargs["end"], collector.symbols) if "end" in kwargs else None
        auto_adjust = kwargs.get("auto_adjust")
        actions = kwargs.get("actions")
        auto_adjust = True if auto_adjust is None else bool(_resolve(auto_adjust, collector.symbols))
        actions = False if actions is None else bool(_resolve(actions, collector.symbols))
        if start is None:
            continue
        if end is None:
            end = pinned  # the driver inherits the resolved (pinned) end date
        if end is None:
            continue
        found.append({
            "file": Path(path).name,
            "tickers": tickers,
            "start": start,
            "end": end,
            "cache": cache_path("|".join(tickers), start, end, auto_adjust, actions),
        })
    return found


def _panel_last_date(path):
    """Last date inside a parquet panel (None when it cannot be read)."""
    try:
        import pandas as pd
        df = pd.read_parquet(path)
        if len(df) == 0:
            return None
        idx = pd.to_datetime(df.index, errors="coerce")
        return None if idx.isna().all() else idx.max().date().isoformat()
    except Exception:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when a driver input is not available from the "
                         "committed cache (the driver would need the network)")
    args = ap.parse_args(argv)

    if not DATA_DIR.exists():
        print(f"NOTE no data directory at {DATA_DIR} (cache miss - every driver "
              f"would download from the network)")
        return 0

    pinned = pinned_end_date()
    tracked = _git_tracked_set(ROOT)
    print("=" * 72)
    print("DATA VINTAGE AUDIT")
    print("=" * 72)
    print(f"pinned vintage (data/vintages.json default_end_date): {pinned}")
    print("note: yfinance 'end' is exclusive, so the panel ends at the last "
          "trading day before it\n")

    # --- 1. inventory --------------------------------------------------------
    panels = sorted(set(DATA_DIR.glob("*.parquet")) | set(DATA_DIR.glob("*.parquet.adj*")))
    price_panels = [p for p in panels if not p.name.startswith("fred_")]
    fred_panels = [p for p in panels if p.name.startswith("fred_")]

    by_end = {}
    for p in price_panels:
        m = END_DATE_RE.search(p.name)
        end = m.group(1) if m else "(no end date in name)"
        by_end.setdefault(end, []).append(p)

    print(f"[inventory] {len(price_panels)} price panel(s), {len(fred_panels)} FRED series")
    for end in sorted(by_end):
        files = by_end[end]
        committed = sum(1 for p in files if f"data/{p.name}" in tracked)
        flag = "" if committed == len(files) else \
            f"  <-- {len(files) - committed} NOT committed (network download)"
        print(f"  end={end}: {len(files)} file(s), {committed} committed{flag}")

    untracked_panels = [p for p in price_panels if f"data/{p.name}" not in tracked]
    if untracked_panels:
        print(f"  NOTE {len(untracked_panels)} untracked price panel(s) in data/: these "
              f"are session downloads\n       (not part of the committed baseline; a "
              f"driver that needs one is not reproducible offline)")

    # --- 2. label / content integrity ---------------------------------------
    print("\n[integrity] committed panels: last date inside the file vs the "
          "end date in its name")
    violations = 0
    for p in price_panels:
        if f"data/{p.name}" not in tracked:
            continue
        m = END_DATE_RE.search(p.name)
        if not m:
            continue
        labeled = m.group(1)
        last = _panel_last_date(p)
        if last is None:
            print(f"  SKIP {p.name} (not readable)")
            continue
        if last > labeled:
            print(f"  FAIL {p.name}: contains data through {last} but is labelled "
                  f"{labeled}")
            violations += 1
        else:
            print(f"  ok   {p.name}: last date {last} <= labelled {labeled}")
    if not violations:
        print("  all committed panels match their label")

    # --- 3. driver inputs ----------------------------------------------------
    print("\n[driver inputs] panels required by the drivers (committed = offline "
          "reproducible)")
    drivers = sorted(list((ROOT / "experiments").glob("run_e*.py")) +
                     list((ROOT / "src").glob("*.py")))
    needed = {}
    for drv in drivers:
        for inp in driver_inputs(drv, {}, pinned):
            entry = needed.setdefault(inp["cache"], {"end": inp["end"], "users": set()})
            entry["users"].add(inp["file"])
    missing = []
    for cache in sorted(needed):
        info = needed[cache]
        exists = (DATA_DIR / cache).exists()
        committed = f"data/{cache}" in tracked
        if committed:
            state = "committed"
        elif exists:
            state = "present but NOT committed (network download)"
            missing.append(cache)
        else:
            state = "ABSENT (network download)"
            missing.append(cache)
        print(f"  [{state}] end={info['end']} {cache}")
        print(f"      needed by: {', '.join(sorted(info['users']))}")
    if missing:
        print(f"\n  NOTE {len(missing)} required panel(s) are not available from the "
              f"committed cache.")
        print("       A driver reading such a panel re-downloads it from the "
              "network, and yfinance\n       revises adjusted prices as new "
              "corporate actions arrive, so its output\n       moves between "
              "sessions for reasons that have nothing to do with the code.")
        print("       This is the mechanism behind the divergences recorded in "
              "ledger/RESEARCH_LEDGER.md E045.")

    # --- 4. FRED vintage -----------------------------------------------------
    if fred_panels:
        print("\n[fred] last observation date per cached macro series")
        for p in fred_panels:
            last = _panel_last_date(p)
            series = p.name.split("_")[1] if "_" in p.name else p.name
            print(f"  {series:<12} last observation: {last}")

    print("\n" + "=" * 72)
    if violations:
        print(f"AUDIT FAILED: {violations} committed panel(s) contain data after "
              f"their label")
    elif args.strict and missing:
        print(f"AUDIT FAILED (--strict): {len(missing)} driver input(s) are not "
              f"committed")
    else:
        print("AUDIT PASSED: committed panels are internally consistent")
    print("=" * 72)
    return 1 if (violations or (args.strict and missing)) else 0


if __name__ == "__main__":
    sys.exit(main())
