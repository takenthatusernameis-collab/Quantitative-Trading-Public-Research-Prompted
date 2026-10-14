#!/usr/bin/env python3
"""Fast offline guard for experiment-script reproducibility.

Invariant: every experiment driver under experiments/ that calls
``deterministic_timestamp()`` must import it from ``src.run_experiment``.
This catches the exact class of regression introduced when a timestamp
migration forgets the import (reproduced on E012/E023/E024/E027/E355),
which otherwise only fails at runtime when the script is re-run.

This check is AST-based (no execution, no data/network) so it stays in the
fast path of scripts/check.sh.
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = ROOT / "experiments"


def _imported_names(tree):
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "src.run_experiment":
            names |= {alias.name for alias in node.names}
    return names


def _defines_locally(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return True
    return False


def _calls(tree, name):
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == name):
            return True
    return False


def main():
    ok = True
    scripts = sorted(EXPERIMENTS.glob("run_e*.py"))
    for path in scripts:
        src = path.read_text()
        try:
            tree = ast.parse(src)
        except SyntaxError as exc:
            print(f"FAIL {path.name}: syntax error {exc}")
            ok = False
            continue
        calls = _calls(tree, "deterministic_timestamp")
        imported = "deterministic_timestamp" in _imported_names(tree)
        local_def = _defines_locally(tree, "deterministic_timestamp")
        if calls and not (imported or local_def):
            print(f"FAIL {path.name}: calls deterministic_timestamp() but does "
                  f"not import it from src.run_experiment")
            ok = False
        else:
            status = "calls+imports" if calls else "no-call"
            print(f"OK   {path.name}: {status}")
    print("ALL EXPERIMENT SCRIPT IMPORTS OK" if ok
          else "EXPERIMENT SCRIPT IMPORT CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
