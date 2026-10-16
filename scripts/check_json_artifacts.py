#!/usr/bin/env python3
"""Fast offline guard for committed experiment artifacts.

Invariant: every committed JSON artifact under experiments/ (and the repo
root, where applicable) must parse as valid JSON. A malformed artifact breaks
the repository's reproducibility claim — any bulk loader, the convention
verification script, or a future agent re-reading results would crash.

This check is pure file I/O (no execution, no data/network) so it stays in the
fast path of scripts/check.sh.

Catches the exact class of regression found in experiments/
e031_accruals_feasibility.json, where the data_feasibility_check dict was closed
with a stray `]` instead of `}`, leaving the only malformed file among all 106
committed JSON artifacts.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    files = subprocess.check_output(["git", "ls-files"], cwd=ROOT).decode().split()
    bad = []
    n = 0
    for rel in files:
        if not rel.endswith(".json"):
            continue
        n += 1
        path = ROOT / rel
        try:
            text = path.read_text()
        except OSError as exc:
            bad.append((rel, "read error", str(exc).splitlines()[0]))
            continue
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            bad.append((rel, "JSONDecodeError", str(exc).splitlines()[0]))

    for rel, kind, msg in bad:
        print(f"FAIL {rel}: {kind}: {msg}")
    print(f"checked {n} committed JSON artifacts")
    if bad:
        print(f"JSON ARTIFACT CHECKS FAILED ({len(bad)} malformed)")
        return 1
    print("ALL COMMITTED JSON ARTIFACTS PARSE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())