import math
import unittest

from run_all_verification import MATERIAL_REL_DEV, deep_compare, diff_records


class TestDiffRecords(unittest.TestCase):
    """diff_records must not change the verdict of deep_compare.

    The suite reports structural and numeric divergences separately, but the
    accept/reject decision has to stay exactly where it was: the reported
    difference set and the pass/fail outcome of deep_compare are unchanged.
    """

    CASES = [
        ({}, {}),
        ({"a": 1}, {"a": 1}),
        ({"a": 1}, {"a": 1.0}),
        ({"a": 1}, {"a": 2}),
        ({"a": 1.0}, {"a": 1.0000000001}),
        ({"a": 1.0}, {"a": 1.001}),
        ({"a": 0.0}, {"a": 1e-13}),
        ({"a": 0.0}, {"a": 1e-9}),
        ({"a": 1.0}, {"a": 1.0e-5}),
        ({"a": "x"}, {"a": "x"}),
        ({"a": "x"}, {"a": "y"}),
        ({"a": True}, {"a": False}),
        ({"a": True}, {"a": 1.0}),
        ({"a": None}, {"a": 1}),
        ({"a": 1}, {"b": 1}),
        ({"a": 1, "b": 2}, {"a": 1}),
        ({"a": [1, 2]}, {"a": [1, 2]}),
        ({"a": [1, 2]}, {"a": [1]}),
        ({"a": [1, 2]}, {"a": [1, 2.5]}),
        ({"a": [{"b": 1}]}, {"a": [{"b": 2}]}),
        ({"a": {"b": {"c": 1.0}}}, {"a": {"b": {"c": 1.2}}}),
        ({"x": float("nan")}, {"x": float("nan")}),
        ({"x": float("nan")}, {"x": 1.0}),
    ]

    def _assert_same_verdict(self, golden, fresh, tol):
        expected = sorted(deep_compare(golden, fresh, numeric_tol=tol))
        records = diff_records(golden, fresh, numeric_tol=tol)
        self.assertEqual(expected, sorted(r["text"] for r in records))
        # The verdict itself: a non-empty difference set fails the comparison.
        self.assertEqual(bool(expected), bool(records))

    def test_matches_deep_compare_at_default_tolerance(self):
        for golden, fresh in self.CASES:
            with self.subTest(golden=golden, fresh=fresh):
                self._assert_same_verdict(golden, fresh, 1e-9)

    def test_matches_deep_compare_at_drift_tolerance(self):
        for golden, fresh in self.CASES:
            with self.subTest(golden=golden, fresh=fresh):
                self._assert_same_verdict(golden, fresh, 1e-4)

    def test_classifies_numeric_and_structural(self):
        golden = {"numeric": 1.0, "string": "a", "missing": 1}
        fresh = {"numeric": 2.0, "string": "b", "added": 2}
        records = diff_records(golden, fresh, numeric_tol=1e-4)
        kinds = {r["path"]: r["kind"] for r in records}
        self.assertEqual(kinds["/numeric"], "numeric")
        self.assertEqual(kinds["/string"], "structural")
        self.assertEqual(kinds["/missing"], "structural")
        self.assertEqual(kinds["/added"], "structural")

    def test_numeric_record_carries_magnitude(self):
        records = diff_records({"a": 0.0}, {"a": 0.05}, numeric_tol=1e-4)
        self.assertEqual(len(records), 1)
        rec = records[0]
        self.assertAlmostEqual(rec["abs_dev"], 0.05)
        self.assertAlmostEqual(rec["rel_dev"], 1.0)
        self.assertGreaterEqual(rec["rel_dev"], MATERIAL_REL_DEV)

    def test_relative_deviation_is_scaled_by_the_larger_magnitude(self):
        records = diff_records({"a": 2.0}, {"a": 2.1}, numeric_tol=1e-4)
        rec = records[0]
        self.assertAlmostEqual(rec["abs_dev"], 0.1, places=12)
        self.assertAlmostEqual(rec["rel_dev"], 0.1 / 2.1, places=12)

    def test_nan_equality_is_not_reported(self):
        self.assertEqual(diff_records({"a": float("nan")}, {"a": float("nan")}), [])

    def test_bools_compare_as_numbers_like_deep_compare(self):
        # deep_compare treats bool as int (isinstance(True, int) is True); the
        # classification must not silently change that verdict.
        self.assertEqual(deep_compare({"a": True}, {"a": 1.0}), [])
        self.assertEqual(diff_records({"a": True}, {"a": 1.0}), [])

    def test_bool_flag_flip_is_reported_as_structural(self):
        # A gate flag flipping True -> False is a decision change, not a
        # numeric drift, and must never be relaxed.
        records = diff_records({"gates": {"G2": True}}, {"gates": {"G2": False}},
                                numeric_tol=1e-4)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["kind"], "structural")
        self.assertEqual(records[0]["path"], "/gates/G2")
        self.assertEqual(len(deep_compare({"gates": {"G2": True}},
                                           {"gates": {"G2": False}},
                                           numeric_tol=1e-4)), 1)


if __name__ == "__main__":
    unittest.main()
