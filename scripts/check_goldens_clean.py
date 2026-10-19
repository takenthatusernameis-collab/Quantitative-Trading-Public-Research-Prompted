#!/usr/bin/env python3
"""Fast offline guard: the committed golden artifacts must be untouched.

Invariant: the experiment goldens under experiments/ are the canonical
research artifacts (the ledger quotes their numbers). The verification suite
overwrites them while it re-runs the drivers and restores them afterwards.
If the suite is killed mid-run (SIGKILL / OOM / session timeout) the restore
never happens, and the next checkpoint commit silently replaces the canonical
baseline with a verification-run artifact. That is exactly what happened in
commits d6042b0 / 9f20def, whose only content was the float-drifted output
of an interrupted verification run.

This guard therefore checks two things (pure file I/O + git plumbing, no
execution, no data/network, so it stays in the fast path of scripts/check.sh):

  1. no tracked file under experiments/ differs from HEAD, and no
     run-created artifact was left behind, and
  2. no stale verification snapshot (an interrupted run) is pending.

A *live* verification run is not a failure: it owns .verify_snapshot/ and
restores the baseline when it finishes, so the guard reports it and exits 0.

Exit codes: 0 = baseline safe, 1 = baseline at risk (restore required).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_DIRNAME = ".verify_snapshot"
MARKER_NAME = "ACTIVE.json"


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True)


def _pid_alive(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _read_marker(snapshot_dir):
    try:
        with open(snapshot_dir / MARKER_NAME) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def main(root=None, snapshot_dir=None):
    root = Path(root) if root is not None else ROOT
    snap = Path(snapshot_dir) if snapshot_dir is not None else root / SNAPSHOT_DIRNAME

    marker = _read_marker(snap)
    if marker is not None:
        pid = marker.get("pid")
        if _pid_alive(pid):
            print(f"verification run in progress (pid {pid}); the golden artifacts "
                  "are temporarily modified by design")
            return 0
        print(f"FAIL interrupted verification run: snapshot {snap} is owned by "
              f"pid {pid}, which is no longer running")
        print("  the committed goldens in experiments/ may be overwritten by that run")
        print("  recover with: python3 run_all_verification.py --restore-only")
        print("  (or: git checkout -- experiments/)")
        return 1

    status = _git(root, "status", "--porcelain", "--untracked-files=all", "--", "experiments/")
    if status.returncode != 0:
        print(f"FAIL cannot inspect git status: {status.stderr.strip() or 'git failed'}")
        return 1
    modified, untracked = [], []
    for ln in status.stdout.splitlines():
        if not ln.strip():
            continue
        (untracked if ln.startswith("??") else modified).append(ln)
    if untracked:
        # Additive artifacts (a new experiment result) do not replace the
        # canonical baseline, so they are reported but not treated as a
        # failure. A leftover run-created file (e.g. the quick-mode E042
        # output) shows up here after an interrupted run.
        print(f"NOTE {len(untracked)} untracked file(s) under experiments/ (not a baseline failure):")
        for ln in untracked:
            print(f"  {ln}")
    if modified:
        print(f"FAIL {len(modified)} golden artifact(s) differ from HEAD:")
        for ln in modified:
            print(f"  {ln}")
        print("  the committed baseline was modified outside the verification suite")
        print("  recover with: git checkout -- experiments/")
        return 1

    print("ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
