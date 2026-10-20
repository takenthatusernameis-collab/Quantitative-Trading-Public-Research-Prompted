"""Cache-key computation for the on-disk parquet cache under ``data/``.

Single source of truth for the *names* of the cache files.  ``src/data.py``
uses this module to name the file it writes; ``scripts/check_data_coverage.py``
uses it to recompute the key of every data request a driver makes, so the
cache-coverage audit cannot drift away from the implementation.

Pure standard library on purpose: importing this module must stay cheap (no
numpy / pandas / yfinance), because the fast guard in ``scripts/check.sh``
imports it on every run.

The key encodes the requested ticker list *in order* plus the resolved start
and end dates, because the returned panel depends on all three.  The
``auto_adjust`` / ``actions`` pair is appended as a suffix only when it is not
the default combination, so the historical cache files keep their names.
"""
import hashlib

HASH_LEN = 16
NAME_LEN = 80


def join_tickers(tickers):
    """Canonical string form of a ticker list. Order is part of the key."""
    if isinstance(tickers, str):
        tickers = [tickers]
    return "|".join(str(t) for t in tickers)


def hash_key(key):
    """16-hex-character digest of the canonical ticker string."""
    return hashlib.sha256(str(key).encode()).hexdigest()[:HASH_LEN]


def safe_name(tickers):
    """Filesystem-safe prefix for a ticker list."""
    return join_tickers(tickers)[:NAME_LEN].replace("/", "_").replace("^", "").replace("|", "_")


def cache_filename(tickers, start, end):
    """File name (no directory) of the cache entry for a download request.

    Mirrors the naming rule that has always been used by ``src/data.py``:
    ``{safe}_{hash}_{start}_{end}.parquet``.
    """
    return f"{safe_name(tickers)}_{hash_key(join_tickers(tickers))}_{start}_{end}.parquet"


def cache_filename_with_flags(tickers, start, end, auto_adjust=True, actions=False):
    """Cache file name including the adjustment/actions suffix.

    The suffix is appended only when the request is not the default
    combination (adjusted close, no corporate actions), so the historical
    cache files keep their names.
    """
    name = cache_filename(tickers, start, end)
    if not (auto_adjust and not actions):
        name += f".adj{int(auto_adjust)}.act{int(actions)}"
    return name
