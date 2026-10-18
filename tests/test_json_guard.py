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

    # --- SENSITIVITY_GRID schema ---

    def test_sensitivity_grid_passes(self):
        content = json.dumps({
            "experiment": "E042",
            "grid": {"a": 1},
            "n_configs": 96,
            "decision": "PARTIAL",
        })
        rc, out = self.run_guard_on({"experiments/e042_grid.json": content})
        self.assertEqual(rc, 0, out)

    def test_sensitivity_grid_missing_grid_fails(self):
        # `experiment` + `n_configs` without `grid` does not match any
        # structural class, so the guard rejects it as unrecognized (still a
        # non-zero failure; the specific message is "unrecognized artifact
        # structure" rather than the missing-field hint).
        content = json.dumps({"experiment": "E042", "n_configs": 96})
        rc, out = self.run_guard_on({"experiments/e042_grid.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("unrecognized artifact structure", out)

    def test_sensitivity_grid_missing_n_configs_fails(self):
        content = json.dumps({"experiment": "E042", "grid": {}})
        rc, out = self.run_guard_on({"experiments/e042_grid.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("unrecognized artifact structure", out)

    def test_sensitivity_grid_missing_identifier_fails(self):
        content = json.dumps({"grid": {}, "n_configs": 96})
        rc, out = self.run_guard_on({"experiments/e042_grid.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("missing identifier field", out)

    # --- STRATEGY_EVAL schema ---

    def test_strategy_eval_passes(self):
        content = json.dumps({
            "strategy": "mom",
            "benchmark": "sp500",
            "oos_sharpe": 0.5,
        })
        rc, out = self.run_guard_on({"experiments/mom_large_liquid.json": content})
        self.assertEqual(rc, 0, out)

    def test_strategy_eval_missing_oos_sharpe_fails(self):
        content = json.dumps({"strategy": "mom", "benchmark": "sp500"})
        rc, out = self.run_guard_on({"experiments/mom_large_liquid.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("STRATEGY_EVAL missing required field 'oos_sharpe'", out)

    # --- DATA_INFEASIBILITY schema ---

    def test_data_infeasibility_passes(self):
        content = json.dumps({
            "experiment": "E026",
            "data_feasibility_check": {"feasible": False},
            "decision": "REJECTED",
            "status": "DATA_INFEASIBLE",
        })
        rc, out = self.run_guard_on({"experiments/e026_div.json": content})
        self.assertEqual(rc, 0, out)

    def test_data_infeasibility_missing_decision_fails(self):
        content = json.dumps({
            "experiment": "E026",
            "data_feasibility_check": {"feasible": False},
        })
        rc, out = self.run_guard_on({"experiments/e026_div.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("DATA_INFEASIBILITY missing required field 'decision'", out)

    # --- EXPERIMENT_ID_DRIVER schema ---

    def test_experiment_id_driver_passes(self):
        content = json.dumps({"experiment_id": "E999", "decision": "REJECTED"})
        rc, out = self.run_guard_on({"experiments/e999.json": content})
        self.assertEqual(rc, 0, out)

    def test_experiment_id_driver_missing_decision_fails(self):
        content = json.dumps({"experiment_id": "E999"})
        rc, out = self.run_guard_on({"experiments/e999.json": content})
        self.assertNotEqual(rc, 0)
        self.assertIn("EXPERIMENT_ID_DRIVER missing required field 'decision'", out)

    # --- E024_PART schema ---

    def test_e024_part_passes(self):
        content = json.dumps({"part_a": {}, "part_b": {}, "part_c": {}})
        rc, out = self.run_guard_on({"experiments/e024_part_a.json": content})
        self.assertEqual(rc, 0, out)

    # --- NON_EXPERIMENT allowlist ---

    def test_non_experiment_allowlisted_passes(self):
        content = json.dumps({"a": 1})
        rc, out = self.run_guard_on({"summary.json": content})
        self.assertEqual(rc, 0, out)

    def test_non_experiment_allowlisted_root_vintages(self):
        content = json.dumps({"vintages": []})
        rc, out = self.run_guard_on({"data/vintages.json": content})
        self.assertEqual(rc, 0, out)

    def test_non_experiment_untracked_not_flagged(self):
        # An untracked JSON file must not be flagged: the guard only inspects
        # git-tracked files. Verify by leaving the file out of the index.
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            init_git_repo(d)
            (d / "experiments" / "untracked.json").parent.mkdir(parents=True, exist_ok=True)
            (d / "experiments" / "untracked.json").write_text("{not json")
            # commit an unrelated good file so the repo is non-empty
            good = json.dumps({"experiment": "E000", "timestamp": "t"})
            (d / "experiments" / "good.json").write_text(good)
            subprocess.run(["git", "add", "experiments/good.json"], cwd=d, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "add"], cwd=d, check=True)
            guard.ROOT = d
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = guard.main()
            self.assertEqual(rc, 0, buf.getvalue())


if __name__ == "__main__":
    unittest.main()
