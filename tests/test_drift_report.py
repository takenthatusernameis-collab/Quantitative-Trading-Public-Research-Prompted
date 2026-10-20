"""Unit tests for the extended-block drift report.

The report is reporting only: it must never change what the verification
suite accepts or rejects. These tests therefore pin down three things:

  1. ``deep_compare`` still emits exactly the same difference messages as
     before the structured collector was introduced,
  2. the structured collector classifies differences the way the report
     claims (numeric vs structural) and never relaxes a structural one, and
  3. the report itself is deterministic, strict JSON, written outside the
     canonical ``experiments/`` directory and gitignored.
"""
import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import run_all_verification as RAV
from scripts import diff_golden


ROOT = Path(__file__).resolve().parent.parent


def _quiet(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = fn(*args, **kwargs)
    return result, buf.getvalue()


class TestDeepCompareParity(unittest.TestCase):
    """The message format of deep_compare is part of the suite's contract."""

    def test_messages_match_the_historical_format(self):
        golden = {"a": 1, "b": [1, 2, 3], "c": {"d": 1.5}, "s": "x", "t": True}
        fresh = {"a": 2, "b": [1, 2, 3, 4], "c": {"d": 2.5}, "s": "y", "u": 3}
        diffs = RAV.deep_compare(golden, fresh, numeric_tol=1e-9)
        self.assertEqual(sorted(diffs), sorted([
            "/a: 1 -> 2",
            "/b: list length 3 -> 4",
            "/c/d: 1.5 -> 2.5",
            "/s: 'x' -> 'y'",
            "/t: present in golden, absent in fresh",
            "/u: absent in golden, added in fresh",
        ]))

    def test_type_change_is_reported(self):
        diffs = RAV.deep_compare({"a": [1, 2]}, {"a": {"b": 1}})
        self.assertEqual(len(diffs), 1)
        self.assertTrue(diffs[0].startswith("/a: "))

    def test_nan_equals_nan(self):
        self.assertEqual(RAV.deep_compare({"a": float("nan")}, {"a": float("nan")}), [])

    def test_drift_within_tolerance_is_not_reported(self):
        self.assertEqual(RAV.deep_compare({"a": 1.0}, {"a": 1.0000001}, numeric_tol=1e-4), [])

    def test_structural_difference_is_never_relaxed(self):
        """A large numeric tolerance must not accept a string change."""
        diffs = RAV.deep_compare({"a": "8 of 96"}, {"a": "7 of 96"}, numeric_tol=1e-4)
        self.assertEqual(diffs, ["/a: '8 of 96' -> '7 of 96'"])


class TestDriftClassification(unittest.TestCase):
    def test_numeric_and_structural_are_separated(self):
        golden = {"num": 1.0, "lst": [1, 2], "txt": "a"}
        fresh = {"num": 2.0, "lst": [1], "txt": "b"}
        records = RAV._collect_diffs(golden, fresh, numeric_tol=1e-9)
        kinds = {r["path"]: r["kind"] for r in records}
        self.assertEqual(kinds, {"/num": "numeric", "/lst": "structural", "/txt": "structural"})

    def test_numeric_record_carries_the_deltas(self):
        records = RAV._collect_diffs({"a": 1.0}, {"a": 1.5}, numeric_tol=1e-9)
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertAlmostEqual(rec["abs_delta"], 0.5)
        self.assertAlmostEqual(rec["rel_delta"], 0.5 / 1.5)
        self.assertEqual(rec["message"], "/a: 1.0 -> 1.5")

    def test_rel_delta_matches_the_standalone_diff_tool(self):
        """scripts/diff_golden.py and the suite must agree on relative drift."""
        pairs = [(1.0, 1.5), (0.06427111431948639, 0.06427110931499598),
                 (-2.0, -1.0), (0.0, 0.0), (1e-9, 2e-9), (3.0, 0.0)]
        for g, f in pairs:
            self.assertEqual(RAV._rel_delta(g, f), diff_golden._rel_delta(g, f),
                             msg=f"rel_delta mismatch for {g} -> {f}")

    def test_summary_counts_and_worst_case(self):
        records = RAV._collect_diffs(
            {"a": 1.0, "b": 2.0, "c": "x", "d": "y"},
            {"a": 1.5, "b": 2.05, "c": "z", "e": 1},
            numeric_tol=1e-9,
        )
        summary = RAV.summarize_drift(records, numeric_tol=1e-4)
        self.assertEqual(summary["n_diffs"], 5)
        self.assertEqual(summary["n_numeric"], 2)
        self.assertEqual(summary["n_structural"], 3)
        self.assertAlmostEqual(summary["max_abs_delta"], 0.5)
        self.assertEqual(summary["max_abs_delta_path"], "/a")
        self.assertAlmostEqual(summary["max_rel_delta"], 0.5 / 1.5)
        self.assertEqual(summary["max_rel_delta_path"], "/a")
        # the worst relative drift is ~3333x the accepted tolerance
        self.assertAlmostEqual(summary["worst_tol_ratio"], (0.5 / 1.5) / 1e-4)
        self.assertEqual(summary["worst_tol_ratio_path"], "/a")

    def test_summary_of_a_clean_artifact_is_empty(self):
        summary = RAV.summarize_drift([], numeric_tol=1e-4)
        self.assertEqual(summary["n_diffs"], 0)
        self.assertIsNone(summary["max_abs_delta"])
        self.assertIsNone(summary["max_rel_delta"])
        self.assertIsNone(summary["worst_tol_ratio"])


class TestComparePatternsFloatReporting(unittest.TestCase):
    def _tree(self, root, name, payload):
        art = Path(root) / "experiments"
        art.mkdir(parents=True, exist_ok=True)
        (art / name).write_text(json.dumps(payload))
        return str(root)

    def test_records_are_collected_for_a_clean_match(self):
        with tempfile.TemporaryDirectory() as td:
            golden = self._tree(Path(td) / "golden", "e001.json", {"experiment": "E001", "v": 1.0})
            fresh = self._tree(Path(td) / "fresh", "e001.json", {"experiment": "E001", "v": 1.0})
            records_out = {}
            ok, _ = _quiet(RAV.compare_patterns_float, golden, fresh,
                           ["experiments/e001.json"], numeric_tol=1e-4,
                           records_out=records_out)
            self.assertTrue(ok)
            self.assertEqual(list(records_out), ["experiments/e001.json"])
            self.assertEqual(records_out["experiments/e001.json"], [])

    def test_records_quantify_a_failing_numeric_drift(self):
        with tempfile.TemporaryDirectory() as td:
            golden = self._tree(Path(td) / "golden", "e001.json", {"experiment": "E001", "v": 1.0})
            fresh = self._tree(Path(td) / "fresh", "e001.json", {"experiment": "E001", "v": 1.5})
            records_out = {}
            ok, _ = _quiet(RAV.compare_patterns_float, golden, fresh,
                           ["experiments/e001.json"], numeric_tol=1e-4,
                           records_out=records_out)
            self.assertFalse(ok)
            records = records_out["experiments/e001.json"]
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["kind"], "numeric")
            summary = RAV.summarize_drift(records, numeric_tol=1e-4)
            self.assertEqual(summary["n_numeric"], 1)
            self.assertAlmostEqual(summary["max_rel_delta"], 0.5 / 1.5)

    def test_documented_e022_vintage_drift_is_still_filtered(self):
        """The E022 allowlist must keep working exactly as before."""
        payload = {
            "strategy": {"active_days": 100, "fold_metrics": [0.0] * 29},
            "placebo": {"z_score": 1.0, "std_sharpe": 2.0, "mean_sharpe": 3.0},
        }
        drifted = json.loads(json.dumps(payload))
        drifted["strategy"]["active_days"] = 101
        drifted["strategy"]["fold_metrics"][28] = 0.5
        drifted["placebo"]["z_score"] = 1.1
        drifted["placebo"]["std_sharpe"] = 2.1
        drifted["placebo"]["mean_sharpe"] = 3.1

        with tempfile.TemporaryDirectory() as td:
            golden = self._tree(Path(td) / "golden", "e022_macro_momentum.json", payload)
            fresh = self._tree(Path(td) / "fresh", "e022_macro_momentum.json", drifted)
            records_out = {}
            ok, _ = _quiet(RAV.compare_patterns_float, golden, fresh,
                           ["experiments/e022_macro_momentum.json"], numeric_tol=1e-4,
                           records_out=records_out)
            self.assertTrue(ok)
            self.assertEqual(records_out["experiments/e022_macro_momentum.json"], [])

            # a difference outside the allowlist must still fail
            drifted["strategy"]["fold_metrics"][3] = 9.0
            fresh = self._tree(Path(td) / "fresh2", "e022_macro_momentum.json", drifted)
            ok, _ = _quiet(RAV.compare_patterns_float, golden, fresh,
                           ["experiments/e022_macro_momentum.json"], numeric_tol=1e-4)
            self.assertFalse(ok)


class TestExtendedBlockIntegration(unittest.TestCase):
    """Exercise the real --extended code path with a fake driver."""

    FAKE_DRIVER = (
        "import argparse, json\n"
        "ap = argparse.ArgumentParser()\n"
        "ap.add_argument('--out', required=True)\n"
        "ap.add_argument('--value', type=float, default=1.0)\n"
        "ap.add_argument('--label', default='x')\n"
        "args = ap.parse_args()\n"
        "json.dump({'experiment': 'E999', 'timestamp': '2026-10-12T00:00:00Z',\n"
        "           'value': args.value, 'label': args.label},\n"
        "          open(args.out, 'w'))\n"
    )

    def _fixture(self, td, fresh_value=1.0, fresh_label="x"):
        base = Path(td)
        golden = base / "golden"
        fresh = base / "fresh"
        scripts = base / "scripts"
        (golden / "experiments").mkdir(parents=True)
        (fresh / "experiments").mkdir(parents=True)
        scripts.mkdir(parents=True)
        (golden / "experiments" / "fake.json").write_text(json.dumps({
            "experiment": "E999", "timestamp": "2026-10-12T08:11:05.560134Z",
            "value": 1.0, "label": "x"}))
        (scripts / "fake_driver.py").write_text(self.FAKE_DRIVER)
        drivers = [("fake_driver.py", ["fake.json"], "fake_driver.py",
                    ["--out", str(fresh / "experiments" / "fake.json"),
                     "--value", str(fresh_value), "--label", fresh_label], 0)]
        return str(golden), str(fresh), str(scripts), drivers

    def test_matching_driver_is_recorded_as_clean(self):
        with tempfile.TemporaryDirectory() as td:
            golden, fresh, scripts, drivers = self._fixture(td)
            report = os.path.join(td, "report.json")
            out, _ = _quiet(RAV.run_extended_block, golden, fresh, drivers, scripts, report)
            results, records = out
            self.assertEqual(len(results), 1)
            self.assertTrue(results[0][1])
            self.assertEqual(records[0]["driver"], "fake_driver.py")
            self.assertTrue(records[0]["ok"])
            art = records[0]["artifacts"][0]
            self.assertEqual(art["artifact"], "experiments/fake.json")
            self.assertEqual(art["n_diffs"], 0)
            self.assertIsNone(art["max_rel_delta"])
            data = json.loads(Path(report).read_text())
            self.assertEqual(data["n_failed_drivers"], 0)
            self.assertEqual(data["drivers"][0]["artifacts"][0]["n_diffs"], 0)

    def test_drifting_driver_is_recorded_with_its_magnitude(self):
        with tempfile.TemporaryDirectory() as td:
            golden, fresh, scripts, drivers = self._fixture(td, fresh_value=1.5)
            report = os.path.join(td, "report.json")
            out, _ = _quiet(RAV.run_extended_block, golden, fresh, drivers, scripts, report)
            results, records = out
            self.assertFalse(results[0][1])
            self.assertFalse(records[0]["ok"])
            art = records[0]["artifacts"][0]
            self.assertEqual(art["n_numeric"], 1)
            self.assertEqual(art["n_structural"], 0)
            self.assertAlmostEqual(art["max_rel_delta"], 0.5 / 1.5)
            self.assertAlmostEqual(art["max_abs_delta"], 0.5)
            self.assertEqual(art["max_rel_delta_path"], "/value")
            self.assertEqual(art["worst_numeric"][0]["path"], "/value")
            data = json.loads(Path(report).read_text())
            self.assertEqual(data["n_failed_drivers"], 1)

    def test_structural_difference_is_recorded_as_structural(self):
        with tempfile.TemporaryDirectory() as td:
            golden, fresh, scripts, drivers = self._fixture(td, fresh_label="y")
            report = os.path.join(td, "report.json")
            out, _ = _quiet(RAV.run_extended_block, golden, fresh, drivers, scripts, report)
            results, records = out
            self.assertFalse(results[0][1])
            art = records[0]["artifacts"][0]
            self.assertEqual(art["n_structural"], 1)
            self.assertEqual(art["n_numeric"], 0)
            self.assertEqual(art["structural"][0]["path"], "/label")
            self.assertEqual(art["structural"][0]["golden"], "x")
            self.assertEqual(art["structural"][0]["fresh"], "y")

    def test_report_is_written_when_a_driver_exits_unexpectedly(self):
        with tempfile.TemporaryDirectory() as td:
            golden, fresh, scripts, _ = self._fixture(td)
            report = os.path.join(td, "report.json")
            (Path(scripts) / "crashing_driver.py").write_text("raise SystemExit(3)\n")
            drivers = [("crashing_driver.py", ["fake.json"], "crashing_driver.py", [], 0)]
            out, _ = _quiet(RAV.run_extended_block, golden, fresh, drivers, scripts, report)
            results, records = out
            self.assertFalse(results[0][1])
            self.assertEqual(records[0]["exit_code"], 3)
            self.assertEqual(records[0]["artifacts"], [])
            data = json.loads(Path(report).read_text())
            self.assertEqual(data["n_failed_drivers"], 1)


class TestDriftReport(unittest.TestCase):
    def _drivers(self):
        return [
            {
                "driver": "run_e011.py",
                "script": "experiments/run_e011.py",
                "exit_code": 0,
                "expected_exit_code": 0,
                "ok": True,
                "artifacts": [{
                    "artifact": "experiments/e011_regime_blend.json",
                    "n_diffs": 0, "n_numeric": 0, "n_structural": 0,
                    "max_abs_delta": None, "max_abs_delta_path": None,
                    "max_rel_delta": None, "max_rel_delta_path": None,
                    "worst_tol_ratio": None, "worst_tol_ratio_path": None,
                    "worst_numeric": [], "structural": [],
                }],
            },
            {
                "driver": "run_e029.py",
                "script": "experiments/run_e029.py",
                "exit_code": 0,
                "expected_exit_code": 0,
                "ok": False,
                "artifacts": [{
                    "artifact": "experiments/e029_fundamental_factors.json",
                    "n_diffs": 2, "n_numeric": 2, "n_structural": 0,
                    "max_abs_delta": 1e-07, "max_abs_delta_path": "/placebo/z_score",
                    "max_rel_delta": 0.0005, "max_rel_delta_path": "/placebo/z_score",
                    "worst_tol_ratio": 5.0, "worst_tol_ratio_path": "/placebo/z_score",
                    "worst_numeric": [], "structural": [],
                }],
            },
        ]

    def test_report_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            a = os.path.join(td, "a.json")
            b = os.path.join(td, "b.json")
            RAV.write_drift_report(self._drivers(), seed="42", path=a)
            RAV.write_drift_report(self._drivers(), seed="42", path=b)
            with open(a, "rb") as fa, open(b, "rb") as fb:
                self.assertEqual(fa.read(), fb.read())

    def test_report_is_strict_json_and_counts_failures(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "report.json")
            RAV.write_drift_report(self._drivers(), seed="42", path=path)
            text = Path(path).read_text()
            self.assertNotIn("Infinity", text)
            self.assertNotIn("NaN", text)
            data = json.loads(text)
            self.assertEqual(data["schema"], "extended_drift_report_v1")
            self.assertEqual(data["seed"], "42")
            self.assertEqual(data["n_drivers"], 2)
            self.assertEqual(data["n_failed_drivers"], 1)
            self.assertEqual(data["drivers"][1]["driver"], "run_e029.py")

    def test_non_finite_deltas_are_sanitised(self):
        drivers = self._drivers()
        drivers[1]["artifacts"][0]["max_rel_delta"] = float("inf")
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "report.json")
            RAV.write_drift_report(drivers, seed="42", path=path)
            data = json.loads(Path(path).read_text())
            self.assertIsNone(data["drivers"][1]["artifacts"][0]["max_rel_delta"])

    def test_default_report_path_is_outside_the_golden_directory(self):
        self.assertNotIn(os.sep + "experiments" + os.sep, RAV.EXTENDED_REPORT_PATH)
        self.assertTrue(RAV.EXTENDED_REPORT_PATH.startswith(os.path.join(RAV.ROOT, ".verify_reports")))

    def test_report_directory_is_gitignored(self):
        """The report must never be committable into the canonical baseline."""
        gitignore = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn(".verify_reports/", gitignore)
        probe = os.path.join(RAV.ROOT, ".verify_reports", "probe.json")
        res = subprocess.run(["git", "check-ignore", "-q", probe], cwd=str(ROOT))
        self.assertEqual(res.returncode, 0, "the drift report path is not gitignored")


if __name__ == "__main__":
    unittest.main()
