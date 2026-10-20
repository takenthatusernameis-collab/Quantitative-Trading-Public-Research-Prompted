import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import check_golden_baseline as CGB


class TestGoldenBaselineGuard(unittest.TestCase):
    def _repo(self, td):
        """A tiny git repo with one golden artifact and a pinned manifest."""
        d = Path(td)
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
        art = d / "experiments"
        art.mkdir(parents=True, exist_ok=True)
        (art / "e001.json").write_text(
            json.dumps({"experiment": "E001", "timestamp": "t"}))
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "add"], cwd=d, check=True)
        manifest = d / "ledger" / "golden_baseline.json"
        with contextlib.redirect_stdout(io.StringIO()):
            rc = CGB._update(d, manifest)
        self.assertEqual(rc, 0)
        return d, manifest

    def _commit_all(self, d, msg="replace artifact"):
        subprocess.run(["git", "add", "-A"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-q", "-m", msg], cwd=d, check=True)

    def _quiet(self, fn, *a, **kw):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = fn(*a, **kw)
        return rc, buf.getvalue()

    def test_clean_repo_passes(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            rc, _ = self._quiet(CGB.check, d, manifest)
            self.assertEqual(rc, 0)

    def test_replaced_artifact_committed_fails(self):
        """The regression this guard exists for: a commit swaps the artifact.

        check_goldens_clean.py cannot see it (working tree == HEAD), so the
        pinned fingerprint has to.
        """
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            (d / "experiments" / "e001.json").write_text(
                json.dumps({"experiment": "E001", "timestamp": "regenerated"}))
            self._commit_all(d)
            rc, out = self._quiet(CGB.check, d, manifest)
            self.assertNotEqual(rc, 0)
            self.assertIn("e001.json", out)

    def test_modified_artifact_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            (d / "experiments" / "e001.json").write_text(
                json.dumps({"experiment": "E001", "timestamp": "t2"}))
            rc, _ = self._quiet(CGB.check, d, manifest)
            self.assertNotEqual(rc, 0)

    def test_deleted_artifact_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            os.remove(d / "experiments" / "e001.json")
            rc, out = self._quiet(CGB.check, d, manifest)
            self.assertNotEqual(rc, 0)
            self.assertIn("missing", out)

    def test_unpinned_artifact_is_a_note_not_a_failure(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            (d / "experiments" / "e002.json").write_text(
                json.dumps({"experiment": "E002", "timestamp": "t"}))
            self._commit_all(d, "add artifact")
            rc, out = self._quiet(CGB.check, d, manifest)
            self.assertEqual(rc, 0)
            self.assertIn("not pinned", out)

    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            os.remove(manifest)
            rc, out = self._quiet(CGB.check, d, manifest)
            self.assertNotEqual(rc, 0)
            self.assertIn("--update", out)

    def test_live_snapshot_skips_the_digest_check(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            snap = d / CGB.SNAPSHOT_DIRNAME
            snap.mkdir()
            (snap / CGB.MARKER_NAME).write_text(
                json.dumps({"pid": os.getpid(), "started": 0.0, "files": []}))
            rc, out = self._quiet(CGB.check, d, manifest)
            self.assertEqual(rc, 0)
            self.assertIn("in progress", out)

    def test_stale_snapshot_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            snap = d / CGB.SNAPSHOT_DIRNAME
            snap.mkdir()
            (snap / CGB.MARKER_NAME).write_text(
                json.dumps({"pid": 999999, "started": 0.0, "files": []}))
            rc, out = self._quiet(CGB.check, d, manifest)
            self.assertNotEqual(rc, 0)
            self.assertIn("interrupted verification run", out)

    def test_update_repins_and_then_passes(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            (d / "experiments" / "e001.json").write_text(
                json.dumps({"experiment": "E001", "timestamp": "t2"}))
            rc, out = self._quiet(CGB._update, d, manifest)
            self.assertEqual(rc, 0)
            self.assertIn("changed", out)
            rc, _ = self._quiet(CGB.check, d, manifest)
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
