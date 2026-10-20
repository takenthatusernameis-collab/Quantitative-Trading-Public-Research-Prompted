import os
import unittest
from pathlib import Path

from scripts import audit_data_vintage

ROOT = Path(__file__).resolve().parent.parent


class TestCachePathMirror(unittest.TestCase):
    """The audit mirrors src/data.py::_cache_path; the mirror must not drift."""

    def test_matches_src_data_cache_path(self):
        from src import data
        cases = [
            (["SPY"], "2014-01-01", "2026-10-12"),
            (["TLT", "IEF", "SPY"], "2014-01-01", "2026-10-11"),
            (["BTC-USD", "ETH-USD"], "2014-01-01", "2026-10-11"),
        ]
        for tickers, start, end in cases:
            with self.subTest(tickers=tickers):
                expected = os.path.basename(
                    data._cache_path("|".join(tickers), start, end))
                actual = audit_data_vintage.cache_path("|".join(tickers), start, end)
                self.assertEqual(actual, expected)

    def test_non_default_variants_match_src(self):
        from src import data
        expected = os.path.basename(
            data._cache_path("SPY", "2014-01-01", "2026-10-12")) + ".adj0.act1"
        actual = audit_data_vintage.cache_path("SPY", "2014-01-01", "2026-10-12",
                                               auto_adjust=False, actions=True)
        self.assertEqual(actual, expected)


class TestDriverInputResolution(unittest.TestCase):
    """The audit must resolve the panels the drivers actually read."""

    def test_resolves_e034_etf_panel_with_explicit_end(self):
        inputs = audit_data_vintage.driver_inputs(
            ROOT / "experiments" / "run_e034.py", {}, "2026-10-12")
        etf = [i for i in inputs
               if i["cache"].startswith("TLT_IEF_LQD_HYG_GLD_DBC_VNQ_EEM_EFA_SPY_")]
        self.assertEqual(len(etf), 1)
        # the de-risked ETF panel is requested with an explicit (unpinned) end
        self.assertEqual(etf[0]["end"], "2026-10-11")
        # the SPY benchmark inherits the resolved (pinned) end date
        spy = [i for i in inputs if i["cache"].startswith("SPY_")]
        self.assertTrue(spy)
        self.assertEqual(spy[0]["end"], "2026-10-12")

    def test_resolves_constant_ticker_lists(self):
        # run_e026 reads a module-level constant list, not an inline literal.
        inputs = audit_data_vintage.driver_inputs(
            ROOT / "experiments" / "run_e026.py", {}, "2026-10-12")
        self.assertTrue(inputs)
        self.assertTrue(any(i["tickers"] and "AAPL" in i["tickers"] for i in inputs))

    def test_unresolvable_calls_are_skipped(self):
        inputs = audit_data_vintage.driver_inputs(
            ROOT / "experiments" / "run_e034.py", {}, None)
        # Without a pinned end date the calls that inherit the resolved date
        # cannot be resolved; the ones with an explicit end still can.
        self.assertTrue(all(i["end"] is not None for i in inputs))


if __name__ == "__main__":
    unittest.main()
