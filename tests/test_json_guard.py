import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_json_artifacts as guard  # noqa: E402


def init_git_repo(d: Path):
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=d, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)


class TestJsonGuard(unittest.TestCase):
    def run_guard_on(self, files):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            init_git_repo(d)
            for rel, content in files.items():
                p = d / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
                subprocess.run(["git", "add", rel], cwd=d, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "add"], cwd=d, check=True)
            guard.ROOT = d
            # capture stdout
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = guard.main()
            return rc, buf.getvalue()

    def test_good_experiment_passes(self):
        content = json.dumps({"experiment": "E999", "timestamp": "2026-01-01", "decision": "REJECTED"})
        rc, out = self.run_guard_on({"experiments/e999.json": content})
        self.assertEqual(rc, 0, out)

    def test_malformed_json_fails(self):
        rc, out = self.run_guard_on({"experiments/bad.json": "{not json"})
        self.assertNotEqual(rc, 0)
        self.assertIn("JSONDecodeError", out)

    def test_missing_identifier_fails(self):
        content = json.dumps({"timestamp": "2026-01-01"})
        rc, out = self.run_guard_on({"experiments/noexp.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("unrecognized artifact structure", out)

    def test_unknown_structure_fails(self):
        content = json.dumps({"foo": 1, "bar": 2})
        rc, out = self.run_guard_on({"experiments/unknown.json": content})
        self.assertNotEqual(rc, 0)

    def test_list_artifact_not_allowlisted_fails(self):
        content = json.dumps([1, 2, 3])
        rc, out = self.run_guard_on({"experiments/listy.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("unexpected top-level list", out)


if __name__ == "__main__":
    unittest.main()
