"""Offline-mode gate for data acquisition.

Set ``QUANT_RESEARCH_OFFLINE=1`` to forbid network access for cached data.
Every acquisition path in the repository (prices, FRED macro series,
yfinance fundamentals, and the E024 raw OHLCV panel) checks the gate before
it would reach the network, so a missing cache entry becomes a hard, named
failure instead of a quiet download whose result is not reproducible.

The verification suite sets the variable for every driver it re-executes, so
a passing run is also evidence that the committed artifacts can be rebuilt
from the pinned cache in ``data/`` alone.
"""
import os

OFFLINE_ENV = "QUANT_RESEARCH_OFFLINE"

_TRUTHY = ("1", "true", "yes", "on")


class OfflineDataUnavailable(RuntimeError):
    """Raised when a data request would need the network in offline mode."""


def offline_required() -> bool:
    """True when the environment forbids fetching data from the network."""
    return os.environ.get(OFFLINE_ENV, "").strip().lower() in _TRUTHY
