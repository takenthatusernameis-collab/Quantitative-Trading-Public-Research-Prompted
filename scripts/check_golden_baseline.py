#!/usr/bin/env python3
"""Fast offline guard: the committed golden artifacts match their pinned fingerprint.

Why this exists
---------------
``scripts/check_goldens_clean.py`` answers "does the working tree still match
HEAD?". It cannot answer "is HEAD still the canonical baseline?", because a
*commit* that replaces an artifact is indistinguishable from a deliberate
baseline update once it lands. That gap has been exploited three times in this
repository:

  * ``d6042b0`` / ``9f20def`` - a checkpoint commit captured the output of an
    interrupted verification run (reverted in ``05b5353``);
  * ``1623923`` - an empty-message checkpoint commit replaced five committed
    artifacts with the output of a verification re-run (reverted in
    ``026d109``).

Every time, ``make check`` passed: the working tree matched HEAD, and HEAD was
simply the wrong baseline. This guard closes the gap by pinning a fingerprint
of the canonical artifacts. Any later commit that swaps an artifact has to
swap the fingerprint too, which puts the replacement in the diff where a
reviewer can see it.

Scope
-----
Every git-tracked JSON artifact under ``experiments/`` is pinned by SHA-256 in
``ledger/golden_baseline.json``. Driver sources (``experiments/*.py``) are
deliberately *not* pinned: they are code, reviewed through the ordinary diff,
and pinning them would turn every comment edit into a manifest update.

Deliberate updates
------------------
Re-pinning is an explicit act::

    python3 scripts/check_golden_baseline.py --update

which rewrites the manifest and prints what changed (added / changed /
removed paths) so the change is reviewable. Without ``--update`` the guard
only reads.

Interaction with a live verification run
----------------------------------------
``run_all_verification.py`` overwrites the artifacts while it re-runs the
drivers and restores them afterwards, so a digest check during a live run
would be meaningless. When the snapshot marker names a live pid the guard
reports that and exits 0 (same convention as ``check_goldens_clean.py``); a
*stale* marker (dead pid) fails, because the artifacts may hold run output.

Exit codes: 0 = baseline matches its fingerprint, 1 = baseline at risk.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "ledger" / "golden_baseline.json"
ARTIFACT_DIR = "experiments"
SNAPSHOT_DIRNAME = ".verify_snapshot"
MARKER_NAME = "ACTIVE.json"


def _git(root, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_artifacts(root):
    """Relative paths of the git-tracked JSON artifacts under experiments/."""
    res = _git(root, "ls-files", ARTIFACT_DIR)
    if res.returncode != 0:
        return None
    return sorted(rel for rel in res.stdout.split()
                  if rel.endswith(".json") and os.path.isfile(os.path.join(str(root), rel)))


def build_fingerprint(root):
    """Current fingerprint of the tracked JSON artifacts under experiments/."""
    root = Path(root)
    rels = tracked_artifacts(root)
    if rels is None:
        raise RuntimeError("git ls-files failed - not inside a git repository?")
    return {rel: _sha256(root / rel) for rel in rels}


def _read_marker(snapshot_dir):
    try:
        with open(os.path.join(str(snapshot_dir), MARKER_NAME)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


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


def _snapshot_state(root, snapshot_dir=None):
    """(state, pid) where state is 'live', 'stale' or 'none'."""
    snap = Path(snapshot_dir) if snapshot_dir is not None else Path(root) / SNAPSHOT_DIRNAME
    marker = _read_marker(snap)
    if marker is None:
        return "none", None
    pid = marker.get("pid")
    return ("live" if _pid_alive(pid) else "stale"), pid


def _load_manifest(path):
    try:
        text = Path(path).read_text()
    except OSError as exc:
        return None, f"cannot read manifest: {exc.strerror or exc}"
    try:
        data = json.loads(text)
    except ValueError as exc:
        return None, f"manifest is not valid JSON: {exc}"
    if not isinstance(data, dict) or not isinstance(data.get("files"), dict):
        return None, "manifest has no 'files' object"
    return data, None


def _update(root, manifest_path):
    root = Path(root)
    manifest_path = Path(manifest_path)
    old, err = _load_manifest(manifest_path)
    old_files = old["files"] if old else {}
    try:
        new_files = build_fingerprint(root)
    except RuntimeError as exc:
        print(f"FAIL {exc}")
        return 1

    added = sorted(set(new_files) - set(old_files))
    removed = sorted(set(old_files) - set(new_files))
    changed = sorted(rel for rel in set(new_files) & set(old_files)
                     if new_files[rel] != old_files[rel])

    payload = {
        "schema": "golden_baseline_fingerprint_v1",
        "algorithm": "sha256",
        "scope": "git-tracked JSON artifacts under experiments/",
        "note": ("Pinned fingerprint of the canonical golden artifacts. "
                 "Regenerate deliberately with: python3 scripts/check_golden_baseline.py --update "
                 "(a replacement of a committed artifact must be visible in the diff)."),
        "n_files": len(new_files),
        "files": new_files,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"updated {manifest_path} ({len(new_files)} artifact(s))")
    for rel in added:
        print(f"  + added    {rel}")
    for rel in changed:
        print(f"  ~ changed  {rel}")
    for rel in removed:
        print(f"  - removed  {rel}")
    if not (added or changed or removed):
        print("  (no change)")
    return 0


def check(root=None, manifest=None, snapshot_dir=None):
    root = Path(root) if root is not None else ROOT
    manifest_path = Path(manifest) if manifest is not None else DEFAULT_MANIFEST

    state, pid = _snapshot_state(root, snapshot_dir)
    if state == "live":
        print(f"verification run in progress (pid {pid}); the golden artifacts "
              "are temporarily modified by design - fingerprint check skipped")
        return 0
    if state == "stale":
        print(f"FAIL interrupted verification run: the snapshot is owned by pid "
              f"{pid}, which is no longer running")
        print("  the committed goldens in experiments/ may hold run output")
        print("  recover with: python3 run_all_verification.py --restore-only")
        print("  (or: git checkout -- experiments/)")
        return 1

    data, err = _load_manifest(manifest_path)
    if data is None:
        print(f"FAIL {err}: {manifest_path}")
        print("  the pinned baseline fingerprint is missing or unreadable")
        print("  regenerate with: python3 scripts/check_golden_baseline.py --update")
        return 1

    files = data["files"]
    missing, changed = [], []
    for rel, digest in sorted(files.items()):
        path = root / rel
        if not path.is_file():
            missing.append(rel)
            continue
        actual = _sha256(path)
        if actual != digest:
            changed.append((rel, digest, actual))

    if missing:
        print(f"FAIL {len(missing)} pinned artifact(s) missing from the working tree:")
        for rel in missing:
            print(f"  {rel}")
    if changed:
        print(f"FAIL {len(changed)} pinned artifact(s) differ from the pinned baseline:")
        for rel, digest, actual in changed:
            print(f"  {rel}")
            print(f"    pinned: {digest}")
            print(f"    actual: {actual}")
    if missing or changed:
        print("  the canonical baseline was replaced outside a deliberate update")
        print("  recover with: git checkout -- experiments/")
        print("  if the replacement is intended, re-pin it with:")
        print("    python3 scripts/check_golden_baseline.py --update")
        return 1

    unpinned = []
    rels = tracked_artifacts(root)
    if rels is None:
        print("NOTE git ls-files failed - skipped the unpinned-artifact scan")
    else:
        unpinned = [rel for rel in rels if rel not in files]
        if unpinned:
            print(f"NOTE {len(unpinned)} tracked artifact(s) under {ARTIFACT_DIR}/ are "
                  "not pinned (not a failure):")
            for rel in unpinned:
                print(f"  {rel}")
            print("  pin them with: python3 scripts/check_golden_baseline.py --update")

    print(f"ALL {len(files)} PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--update", action="store_true",
                    help="regenerate the pinned fingerprint from the working tree "
                         "(a deliberate act: re-pinning replaces the baseline)")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                    help=f"fingerprint manifest path (default: {DEFAULT_MANIFEST})")
    args = ap.parse_args(argv)
    if args.update:
        return _update(ROOT, args.manifest)
    return check(ROOT, args.manifest)


if __name__ == "__main__":
    sys.exit(main())
