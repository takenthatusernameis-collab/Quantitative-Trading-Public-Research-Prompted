#!/usr/bin/env python3
"""Repoint generic canonical handoff pointers to the new durable handoff.

Only generic (stable-alias) names are touched. Any name carrying a timestamp
token (HH:MM:SS, HH-MM-SS, or HHMMSS), or matching the historical
HANDOFF_NEXT_SESSION_* / HANDOFF_2026* families, is left untouched so that
committed history is preserved.
"""
import os
import re
import sys

REPO = "/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted"
NEW = "handoff_2026-11-11T22-28-52Z_INITIAL_TASK.md"

# per-directory relative target for the new handoff
DIR_TARGETS = {
    ".": NEW,
    "handoff": "../" + NEW,
    "HANDOFFS": "../" + NEW,
    ".handoff": "../" + NEW,
    ".kilo": "../" + NEW,
    ".kilo/handoff": "../../" + NEW,
}

TS = re.compile(r"T\d{2}[:\-]\d{2}[:\-]\d{2}Z|T\d{6}Z")


def is_generic(name: str) -> bool:
    if TS.search(name):
        return False
    if name.startswith("HANDOFF_NEXT_SESSION_"):
        return False
    if name.startswith("HANDOFF_2026"):
        return False
    return True


def main() -> int:
    total = repointed = 0
    for d, target in DIR_TARGETS.items():
        try:
            entries = os.listdir(d)
        except FileNotFoundError:
            continue
        for name in entries:
            path = os.path.join(d, name)
            if not os.path.islink(path):
                continue
            if not is_generic(name):
                continue
            total += 1
            os.remove(path)
            os.symlink(target, path)
            repointed += 1
    print(f"generic pointers found: {total}  repointed: {repointed}")

    # verify
    bad = 0
    checked = 0
    for d, target in DIR_TARGETS.items():
        try:
            entries = os.listdir(d)
        except FileNotFoundError:
            continue
        for name in entries:
            path = os.path.join(d, name)
            if not os.path.islink(path) or not is_generic(name):
                continue
            checked += 1
            try:
                real = os.path.realpath(path)
            except OSError:
                bad += 1
                print(f"BAD (unresolvable): {path}")
                continue
            if not real.endswith("/" + NEW):
                bad += 1
                print(f"BAD: {path} -> {real}")
    print(f"checked={checked} bad={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())