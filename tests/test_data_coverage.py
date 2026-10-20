import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts import check_data_coverage as guard
from src import cache_keys


class TestCacheKeys(unittest.TestCase):
    """The cache-key rule must stay the single source of truth."""

    def test_matches_data_module(self):
        from src import data
        for tickers, start, end in [
            (["SPY"], "2014-01-01", "2026-10-12"),
            (["AAPL", "MSFT"], "2014-01-01", "2026-10-11"),
            (["BTC-USD", "ETH-USD"], "2014-01-01", "2026-10-11"),
        ]:
            joined = "|".join(tickers)
            self.assertEqual(
                cache_keys.cache_filename(joined, start, end),
                os.path.basename(data._cache_path(joined, start, end)),
            )

    def test_adjustment_suffix(self):
        plain = cache_keys.cache_filename_with_flags(["SPY"], "2014-01-01", "2026-10-12")
        self.assertTrue(plain.endswith(".parquet"))
        self.assertNotIn(".adj", plain)
        raw = cache_keys.cache_filename_with_flags(
            ["SPY"], "2014-01-01", "2026-10-12", auto_adjust=False, actions=True)
        self.assertTrue(raw.endswith(".adj0.act1"))

    def test_order_is_part_of_the_key(self):
        a = cache_keys.cache_filename(["A", "B"], "2014-01-01", "2026-10-12")
        b = cache_keys.cache_filename(["B", "A"], "2014-01-01", "2026-10-12")
        self.assertNotEqual(a, b)


class TestRequirementScanner(unittest.TestCase):
    """Every data request a driver makes must be resolvable statically."""

    def test_no_unresolved_requests_in_this_repository(self):
        requirements, unresolved = guard.scan_requirements(guard.ROOT)
        self.assertEqual(unresolved, [], f"unresolved data requests: {unresolved}")
        self.assertGreater(len(requirements), 20)

    def test_every_requirement_is_a_cache_file_under_data(self):
        requirements, _ = guard.scan_requirements(guard.ROOT)
        for driver, files in requirements.items():
            for rel in files:
                self.assertTrue(rel.startswith("data/"), f"{driver}: {rel}")
                self.assertIn(".parquet", rel, f"{driver}: {rel}")

    def test_e030_etf_panel_is_a_requirement(self):
        """The panel that made E030 drift must be a known dependency."""
        requirements, _ = guard.scan_requirements(guard.ROOT)
        files = requirements["experiments/run_e030.py"]
        self.assertTrue(any("SPY_QQQ_IWM_EFA_EEM_GLD_USO_DBC" in f for f in files), files)


class TestCoverageGuard(unittest.TestCase):
    """The guard must fail when the pinned cache coverage is broken."""

    def _repo(self, td):
        d = Path(td)
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
        (d / "data").mkdir(parents=True, exist_ok=True)
        payload = d / "data" / "panel.parquet"
        payload.write_bytes(b"panel")
        subprocess.run(["git", "add", "data/panel.parquet"], cwd=d, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "add"], cwd=d, check=True)
        manifest = d / "data_baseline.json"
        manifest.write_text(json.dumps({
            "schema": "data_baseline_fingerprint_v1",
            "files": {"data/panel.parquet": {
                "sha256": guard._sha256(payload), "bytes": payload.stat().st_size}},
        }))
        return d, manifest

    def _check(self, d, manifest):
        return guard.check(root=d, manifest=manifest)

    def test_complete_coverage_passes(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            self.assertEqual(self._check(d, manifest), 0)

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            (d / "data" / "panel.parquet").unlink()
            self.assertNotEqual(self._check(d, manifest), 0)

    def test_modified_file_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            (d / "data" / "panel.parquet").write_bytes(b"different")
            self.assertNotEqual(self._check(d, manifest), 0)

    def test_untracked_file_fails(self):
        """A fresh clone would not have the file, so the driver would download."""
        with tempfile.TemporaryDirectory() as td:
            d, manifest = self._repo(td)
            subprocess.run(["git", "rm", "-q", "--cached", "data/panel.parquet"],
                           cwd=d, check=True)
            self.assertNotEqual(self._check(d, manifest), 0)

    def test_missing_manifest_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d, _ = self._repo(td)
            self.assertNotEqual(self._check(d, Path(td) / "nope.json"), 0)


class TestOfflineGate(unittest.TestCase):
    """A cache miss in offline mode must be a hard, named failure."""

    def test_missing_cache_raises_offline(self):
        from src import data
        os.environ[data.OFFLINE_ENV] = "1"
        try:
            with self.assertRaises(data.OfflineDataUnavailable):
                data.download(["NOT_A_REAL_TICKER_XYZ"], start="2014-01-01",
                              end="2026-10-12")
        finally:
            os.environ.pop(data.OFFLINE_ENV, None)

    def test_offline_flag_is_off_by_default(self):
        from src import data
        os.environ.pop(data.OFFLINE_ENV, None)
        self.assertFalse(data._offline_required())


if __name__ == "__main__":
    unittest.main()
