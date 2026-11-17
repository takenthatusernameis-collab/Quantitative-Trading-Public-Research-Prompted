#!/usr/bin/env python3
"""Repair broken handoff symlinks that repoint_handoff.py leaves untouched.

repoint_handoff.py only touches generic (stable-alias) names; timestamped
pointers and HANDOFF_NEXT_SESSION_* / HANDOFF_2026* families are preserved as
history. When a session deletes its target artifact, those preserved pointers
go broken. This script repoints any *broken* symlink to the current durable
handoff using per-directory relative targets, leaving non-broken historical
pointers untouched.
"""
import os
import sys

REPO = "/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted"
NEW = sys.argv[1] if len(sys.argv) > 1 else "handoff_2026-11-17T03:23:18Z_INITIAL_TASK.md"

DIR_TARGETS = {
    ".": NEW,
    "HANDOFFS": "../" + NEW,
    "handoff": "../" + NEW,
    ".handoff": "../" + NEW,
    ".kilo": "../" + NEW,
    ".kilo/handoff": "../../" + NEW,
}


def main() -> int:
    repaired = 0
    still_bad = 0
    for d, target in DIR_TARGETS.items():
        try:
            entries = os.listdir(os.path.join(REPO, d))
        except FileNotFoundError:
            continue
        for name in entries:
            path = os.path.join(REPO, d, name)
            if not os.path.islink(path):
                continue
            if os.path.exists(path):
                continue  # already resolves; leave historical pointers alone
            os.remove(path)
            os.symlink(target, path)
            repaired += 1
            print(f"repaired: {os.path.relpath(path, REPO)} -> {target}")

    # verify
    for d, target in DIR_TARGETS.items():
        try:
            entries = os.listdir(os.path.join(REPO, d))
        except FileNotFoundError:
            continue
        for name in entries:
            path = os.path.join(REPO, d, name)
            if not os.path.islink(path):
                continue
            try:
                real = os.path.realpath(path)
            except OSError:
                still_bad += 1
                print(f"BAD (unresolvable): {os.path.relpath(path, REPO)}")
                continue
            if not real.endswith("/" + NEW):
                still_bad += 1
                print(f"BAD: {os.path.relpath(path, REPO)} -> {real}")
    print(f"repaired={repaired} still_bad={still_bad}")
    return 1 if still_bad else 0


if __name__ == "__main__":
    sys.exit(main())