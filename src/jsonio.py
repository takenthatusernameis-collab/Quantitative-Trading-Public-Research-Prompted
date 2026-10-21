"""Strict JSON serialization for committed artifacts.

The committed artifacts under ``experiments/`` are the canonical research
record of this repository. They are read by tools that parse JSON per
RFC 8259 (``jq``, Go's ``encoding/json``, Rust's ``serde_json``,
PostgreSQL's ``jsonb``, browser ``JSON.parse``). Python's ``json`` module
accepts the non-standard literals ``NaN`` / ``Infinity`` / ``-Infinity`` by
default, so a producer that dumps a non-finite float writes a file that no
strict parser can load -- the file parses fine with the standard library and
then fails for every other consumer.

Three committed artifacts were in that state (``e024_convention_audit.json``,
``e024_part_c.json``, ``e029_fundamental_factors.json``): undefined
statistics for tickers with no ex-dividend dates, and undefined
beta / alpha / correlation for a signal without cross-sectional variation,
were written as bare ``NaN``.

This module is the single write path for artifacts: non-finite floats become
``null`` (the RFC 8259 and ``pandas.DataFrame.to_json`` representation of a
missing value) and the file is written with ``allow_nan=False``, so a
non-finite value that slips through raises instead of silently producing an
artifact that no strict parser can read.

The transformation is value-preserving for every finite number: the
serialized bytes of an artifact that contains no non-finite float are
unchanged by switching to this writer.
"""
import json
import math
from pathlib import Path

import numpy as np


def _is_non_finite(value):
    """True for a float-like value that JSON cannot represent."""
    if isinstance(value, float):
        return not math.isfinite(value)
    if isinstance(value, np.floating):
        return not bool(np.isfinite(value))
    return False


def sanitize(obj):
    """Return a copy of ``obj`` with every non-finite float replaced by None.

    Containers are rebuilt (dicts, lists, tuples); every other value is
    returned unchanged, so finite numbers keep their exact repr and key
    order is preserved.
    """
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(v) for v in obj]
    if _is_non_finite(obj):
        return None
    return obj


def dumps(obj, indent=2, default=str, **kwargs):
    """Serialize ``obj`` to a strict RFC 8259 JSON string."""
    return json.dumps(sanitize(obj), indent=indent, default=default,
                      allow_nan=False, **kwargs)


def dump(obj, fp, indent=2, default=str, **kwargs):
    """Write ``obj`` to the file-like object ``fp`` as strict RFC 8259 JSON.

    Mirrors ``json.dump`` so call sites change by a single import swap.
    """
    fp.write(dumps(obj, indent=indent, default=default, **kwargs))


def write_json(obj, path, indent=2, default=str, **kwargs):
    """Write ``obj`` to ``path`` as strict RFC 8259 JSON and return the text."""
    text = dumps(obj, indent=indent, default=default, **kwargs)
    Path(path).write_text(text, encoding="utf-8")
    return text
