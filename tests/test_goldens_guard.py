import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import check_goldens_clean


class TestGoldensGuard(unittest.TestCase):
    def _repo(self, td):
        d = Path(td)
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
        p = d / "experiments" / "e001.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"experiment": "E001", "timestamp": "t"}))
        subprocess.run(["git", "add", "experiments/e001.json"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "add"], cwd=d, check=True)
        return d

    def test_clean_tree_passes(self):
        with tempfile.TemporaryDirectory() as td:
            d = self._repo(td)
            self.assertEqual(check_goldens_clean.main(root=d), 0)

    def test_modified_golden_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d = self._repo(td)
            (d / "experiments" / "e001.json").write_text(
                json.dumps({"experiment": "E001", "timestamp": "t2"}))
            self.assertNotEqual(check_goldens_clean.main(root=d), 0)

    def test_untracked_run_artifact_is_not_a_failure(self):
        with tempfile.TemporaryDirectory() as td:
            d = self._repo(td)
            (d / "experiments" / "e042_quick.json").write_text("{}")
            self.assertEqual(check_goldens_clean.main(root=d), 0)

    def test_modified_driver_source_is_not_a_baseline_failure(self):
        with tempfile.TemporaryDirectory() as td:
            d = self._repo(td)
            (d / "experiments" / "run_e001.py").write_text("# edited driver\n")
            subprocess.run(["git", "add", "experiments/run_e001.py"], cwd=d, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "driver"], cwd=d, check=True)
            (d / "experiments" / "run_e001.py").write_text("# edited driver again\n")
            self.assertEqual(check_goldens_clean.main(root=d), 0)

    def test_stale_snapshot_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d = self._repo(td)
            snap = d / check_goldens_clean.SNAPSHOT_DIRNAME
            snap.mkdir()
            (snap / check_goldens_clean.MARKER_NAME).write_text(
                json.dumps({"pid": 999999, "started": 0.0, "files": []}))
            self.assertNotEqual(check_goldens_clean.main(root=d), 0)

    def test_live_snapshot_passes(self):
        with tempfile.TemporaryDirectory() as td:
            d = self._repo(td)
            snap = d / check_goldens_clean.SNAPSHOT_DIRNAME
            snap.mkdir()
            (snap / check_goldens_clean.MARKER_NAME).write_text(
                json.dumps({"pid": os.getpid(), "started": 0.0, "files": []}))
            self.assertEqual(check_goldens_clean.main(root=d), 0)


if __name__ == "__main__":
    unittest.main()
