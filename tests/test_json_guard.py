import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import check_json_artifacts


class TestJsonGuard(unittest.TestCase):
    def _run_in_temp(self, files):
        old_root = check_json_artifacts.ROOT
        try:
            with tempfile.TemporaryDirectory() as td:
                d = Path(td)
                subprocess.run(["git", "init", "-q"], cwd=d, check=True)
                subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=d, check=True)
                subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
                for rel, content in files.items():
                    p = d / rel
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(content)
                    subprocess.run(["git", "add", rel], cwd=d, check=True)
                subprocess.run(["git", "commit", "-q", "-m", "add"], cwd=d, check=True)
                check_json_artifacts.ROOT = d
                rc = check_json_artifacts.main()
                return rc
        finally:
            check_json_artifacts.ROOT = old_root

    def test_malformed_fails(self):
        rc = self._run_in_temp({"experiments/b.json": "{bad"})
        self.assertNotEqual(rc, 0)

    def test_missing_identifier_fails(self):
        rc = self._run_in_temp({"experiments/x.json": json.dumps({"timestamp": "t"})})
        self.assertNotEqual(rc, 0)

    def test_good_experiment_passes(self):
        rc = self._run_in_temp({"experiments/e.json": json.dumps({"experiment": "E1", "timestamp": "t"})})
        self.assertEqual(rc, 0)

    def test_unknown_structure_fails(self):
        rc = self._run_in_temp({"experiments/u.json": json.dumps({"foo": 1})})
        self.assertNotEqual(rc, 0)

    def test_missing_required_timestamp_fails(self):
        rc = self._run_in_temp({"experiments/e2.json": json.dumps({"experiment": "E2"})})
        self.assertNotEqual(rc, 0)

    def test_data_infeasibility_missing_decision_fails(self):
        rc = self._run_in_temp({"experiments/d.json": json.dumps({"data_feasibility_check": {}})})
        self.assertNotEqual(rc, 0)
        rc = self._run_in_temp({"experiments/d2.json": json.dumps({"experiment_id": "E3", "data_feasibility_check": {}})})
        self.assertNotEqual(rc, 0)

    def test_nondict_nonallowlisted_fails(self):
        rc = self._run_in_temp({"experiments/badlist.json": "[]"})
        self.assertNotEqual(rc, 0)

    def test_data_infeasibility_valid_passes(self):
        rc = self._run_in_temp({"experiments/d3.json": json.dumps({"experiment_id": "E3", "data_feasibility_check": {}, "decision": "REJECT"})})
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
