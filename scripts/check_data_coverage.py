#!/usr/bin/env python3
"""Fast offline guard: the cached data inputs the committed artifacts depend on
are present in the repository, git-tracked, and match their pinned fingerprint.

Why this exists
---------------
``data/`` is gitignored except for the pinned 2026-10-12 vintage, so a fresh
clone contains only the cache files the repository explicitly carries.  A
driver whose data request does not resolve to one of those files silently
falls through to a live yfinance download.  That download is *not*
reproducible: two downloads of the same request minutes apart differ by
~1e-6 in the resulting correlations (measured 2026-10-20, see the ledger's
E048 entry), which is enough to flip a value that sits on a 4-decimal
rounding boundary and to blow past a 1e-4 relative tolerance on
near-zero quantities.

That is exactly how E030 drifted (28 numeric differences against its
committed golden) while every other extended driver reproduced with zero
differences: E030's 16-ETF panel was never pinned, so its input was
re-downloaded from the network on every run.

The invariant this guard enforces
---------------------------------
Every cached data file a committed driver reads must

  1. exist in the working tree,
  2. be **git-tracked** (otherwise a fresh clone would re-download it), and
  3. match the SHA-256 pinned in ``ledger/data_baseline.json``.

and every ``data.download()`` call site a driver contains must resolve to a
file that is pinned.

Deliberate updates
------------------
Re-pinning is an explicit act::

    python3 scripts/check_data_coverage.py --update

which rewrites the fingerprints and prints what changed (added / changed /
removed) so the change is reviewable.  Without ``--update`` the guard only
reads.

Note on the pinned cache
------------------------
Pinning an input file pins the *snapshot* the committed artifact was derived
from.  It does not retroactively make an artifact that was derived from an
unpinned input reproducible; that needs a deliberate re-pin of the artifact
itself (see ``scripts/check_golden_baseline.py --update``).

Exit codes: 0 = cache coverage is complete, 1 = coverage gap.
"""
import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.cache_keys import cache_filename_with_flags  # noqa: E402

DEFAULT_MANIFEST = ROOT / "ledger" / "data_baseline.json"
DATA_DIR = "data"
VINTAGES_PATH = "data/vintages.json"

#: Driver sources that the verification suite re-executes. Every one of them
#: is scanned for data requests.
DRIVER_SOURCES = [
    "experiments/run_e011.py",
    "experiments/run_e012.py",
    "experiments/run_e013.py",
    "experiments/run_e015.py",
    "experiments/run_e016.py",
    "experiments/run_e017.py",
    "experiments/run_e018.py",
    "experiments/run_e019.py",
    "experiments/run_e020.py",
    "experiments/run_e021.py",
    "experiments/run_e022.py",
    "experiments/run_e023.py",
    "experiments/run_e024.py",
    "experiments/run_e025.py",
    "experiments/run_e026.py",
    "experiments/run_e027.py",
    "experiments/run_e028.py",
    "experiments/run_e029.py",
    "experiments/run_e030.py",
    "experiments/run_e034.py",
    "experiments/run_e035.py",
    "experiments/run_e036.py",
    "experiments/run_e037.py",
    "experiments/run_e039.py",
    "experiments/run_e041.py",
    "experiments/run_e042.py",
    "experiments/run_e042_lead.py",
    "src/batch_run.py",
    "src/validate.py",
    "src/run_experiment.py",
]


class Unresolved(Exception):
    """Raised when a request cannot be resolved statically."""


# --------------------------------------------------------------------------
# git / hashing helpers
# --------------------------------------------------------------------------

def _git(root, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_files(root):
    """Relative paths of all git-tracked files (None if git is unavailable)."""
    res = _git(root, "ls-files")
    if res.returncode != 0:
        return None
    return set(res.stdout.split())


def vintage_end_date(root):
    """The pinned end date used when SEED is set (reproducible mode)."""
    try:
        with open(Path(root) / VINTAGES_PATH) as f:
            return json.load(f).get("default_end_date", "2026-10-12")
    except (OSError, ValueError):
        return "2026-10-12"


# --------------------------------------------------------------------------
# static scanning of driver sources
# --------------------------------------------------------------------------

def _import_names(node, root, depth=0):
    """Names bound by an import statement, resolved without executing code."""
    out = {}
    if depth > 3:
        return out
    if isinstance(node, ast.ImportFrom):
        if not node.module:
            return out
        if node.module == "src":
            for alias in node.names:
                sub = Path(root) / "src" / (alias.name + ".py")
                if sub.is_file():
                    out[alias.asname or alias.name] = _literal_namespace(sub, root, depth + 1)
            return out
        candidates = []
        if node.module.startswith("src."):
            candidates.append(Path(root) / (node.module.replace(".", "/") + ".py"))
        elif node.module.startswith("experiments."):
            candidates.append(Path(root) / (node.module.replace(".", "/") + ".py"))
        else:
            candidates.append(Path(root) / "experiments" / (node.module + ".py"))
            candidates.append(Path(root) / "src" / (node.module + ".py"))
        for sub in candidates:
            if not sub.is_file():
                continue
            sub_ns = _literal_namespace(sub, root, depth + 1)
            for alias in node.names:
                if alias.name in sub_ns:
                    out[alias.asname or alias.name] = sub_ns[alias.name]
                else:
                    out[alias.asname or alias.name] = sub_ns
            break
    elif isinstance(node, ast.Import):
        for alias in node.names:
            if alias.name.startswith("src"):
                sub = Path(root) / (alias.name.replace(".", "/") + ".py")
                if sub.is_file():
                    out[alias.asname or alias.name.split(".")[0]] = _literal_namespace(
                        sub, root, depth + 1)
    return out


def _literal_namespace(path, root, depth=0):
    """Module-level constants of a Python file, resolved without executing it.

    Only literal values are used, so importing a driver never runs its code.
    Names imported from ``src.*`` are resolved by scanning those modules too.
    """
    ns = {}
    try:
        tree = ast.parse(Path(path).read_text())
    except (OSError, SyntaxError):
        return ns
    for node in tree.body:
        if isinstance(node, ast.Assign):
            value = _literal(node.value)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    ns[target.id] = value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            ns[node.target.id] = _literal(node.value)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            ns.update(_import_names(node, root, depth))
    # second pass: constants that are only derivable from earlier constants
    # (e.g. ``LARGE_LIQUID = UNIVERSES["large_liquid"]``)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and ns.get(target.id) is None:
                    try:
                        ns[target.id] = _eval(node.value, ns)
                    except Unresolved:
                        pass
    return ns


def _literal(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError, TypeError):
        return None


def _eval(node, env):
    """Evaluate a small, safe subset of Python expressions.

    Supports literals, names, attribute access on dicts, subscripts (with
    slices), lists, tuples, sets, dicts, ``+`` concatenation, comprehensions
    over resolvable iterables, and the handful of builtins the drivers use
    (``list``/``set``/``sorted``/``tuple``/``len``) plus ``dict.keys()``,
    ``dict.values()`` and ``dict.items()``.

    Anything outside that subset raises :class:`Unresolved`; the scanner then
    reports the call site as "not statically audited" instead of guessing.
    """
    try:
        return _eval_inner(node, env)
    except Unresolved:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        raise Unresolved(type(exc).__name__)


def _eval_inner(node, env):
    if node is None:
        return None
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise Unresolved(node.id)
    if isinstance(node, ast.Attribute):
        base = _eval(node.value, env)
        if isinstance(base, dict) and node.attr in base:
            return base[node.attr]
        raise Unresolved(ast.dump(node))
    if isinstance(node, ast.Subscript):
        base = _eval(node.value, env)
        if isinstance(node.slice, ast.Slice):
            key = _eval(node.slice, env)
            if isinstance(base, (list, tuple, str)) and isinstance(key, slice):
                return base[key]
            raise Unresolved("slice")
        key = _eval(node.slice, env)
        try:
            return base[key]
        except Exception:
            raise Unresolved(ast.dump(node))
    if isinstance(node, ast.Slice):
        lower = _eval(node.lower, env) if node.lower is not None else None
        upper = _eval(node.upper, env) if node.upper is not None else None
        return slice(lower, upper)
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        items = [_eval(e, env) for e in node.elts]
        return items if not isinstance(node, ast.Tuple) else tuple(items)
    if isinstance(node, ast.Dict):
        out = {}
        for k, v in zip(node.keys, node.values):
            if k is None:
                raise Unresolved("dict unpack")
            out[_eval(k, env)] = _eval(v, env)
        return out
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return _eval(node.left, env) + _eval(node.right, env)
    if isinstance(node, ast.ListComp):
        return _comprehension(node, env, "list")
    if isinstance(node, ast.GeneratorExp):
        return _comprehension(node, env, "gen")
    if isinstance(node, ast.Call):
        return _call(node, env)
    raise Unresolved(ast.dump(node)[:60])


def _comprehension(node, env, kind):
    results = []
    for value in _iterable(node.generators[0], env):
        local = dict(env)
        _bind(node.generators[0].target, value, local)
        results.append(_eval(node.elt, local))
    if kind == "gen":
        return results
    return results


def _iterable(gen, env):
    source = _eval(gen.iter, env)
    if not isinstance(source, (list, tuple, set)):
        raise Unresolved(ast.dump(gen.iter)[:60])
    return list(source)


def _bind(target, value, env):
    if isinstance(target, ast.Name):
        env[target.id] = value
    elif isinstance(target, (ast.Tuple, ast.List)):
        if not isinstance(value, (list, tuple)):
            raise Unresolved("tuple binding")
        if len(value) != len(target.elts):
            raise Unresolved("tuple arity")
        for i, elt in enumerate(target.elts):
            _bind(elt, value[i], env)
    else:
        raise Unresolved(ast.dump(target)[:60])


def _call(node, env):
    if isinstance(node.func, ast.Name) and node.func.id in ("list", "set", "sorted", "tuple", "len"):
        args = [_eval(a, env) for a in node.args]
        if node.func.id == "len":
            return len(args[0])
        if node.func.id == "sorted":
            return sorted(args[0])
        if node.func.id == "tuple":
            return tuple(args[0])
        if node.func.id == "list":
            return list(args[0])
        return set(args[0])
    if isinstance(node.func, ast.Attribute) and node.func.attr in ("keys", "values", "items"):
        base = _eval(node.func.value, env)
        if not isinstance(base, dict):
            raise Unresolved(ast.dump(node)[:60])
        if node.func.attr == "keys":
            return list(base.keys())
        if node.func.attr == "values":
            return list(base.values())
        return list(base.items())
    raise Unresolved(ast.dump(node)[:60])


def _is_data_call(node):
    return (isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "data"
            and node.func.attr in ("download", "get_benchmark"))


def _expand_dict_subscript(node, env):
    """Values of a dict-valued subscript, when the key is not statically known.

    ``UNIVERSES[args.universe]`` selects one of the universe lists at run
    time; every one of them is a data dependency of the driver, so all of
    them are reported.
    """
    if not isinstance(node, ast.Subscript):
        return None
    base = env.get(node.value.id) if isinstance(node.value, ast.Name) else None
    if not isinstance(base, dict):
        return None
    values = []
    for value in base.values():
        if isinstance(value, (list, tuple)) and value and all(isinstance(v, str) for v in value):
            values.append(list(value))
    return values or None


def _requests_from_call(node, env, end_default):
    """All ``(tickers, start, end, auto_adjust, actions)`` for a data call."""
    kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}
    if node.func.attr == "get_benchmark":
        ticker_arg = node.args[0] if node.args else kwargs.get("ticker")
        rest = {k: v for k, v in kwargs.items() if k != "ticker"}
        ticker_nodes = [ticker_arg]
    else:
        ticker_nodes = [node.args[0] if node.args else kwargs.get("tickers")]
        rest = kwargs

    ticker_sets = []
    for ticker_node in ticker_nodes:
        try:
            value = _eval(ticker_node, env)
        except Unresolved:
            expanded = _expand_dict_subscript(ticker_node, env)
            if not expanded:
                raise
            ticker_sets.extend(expanded)
            continue
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, (list, tuple)) or not value:
            raise Unresolved("ticker list")
        if all(isinstance(v, (list, tuple)) for v in value):
            # a universe selection: every member is a separate data request
            for entry in value:
                ticker_sets.append([str(t) for t in entry])
        else:
            ticker_sets.append([str(t) for t in value])

    start = _eval(rest["start"], env) if "start" in rest else "2015-01-01"
    if "end" in rest:
        end = _eval(rest["end"], env)
    else:
        end = end_default
    if end is None:
        end = end_default
    auto_adjust = _eval(rest["auto_adjust"], env) if "auto_adjust" in rest else True
    actions = _eval(rest["actions"], env) if "actions" in rest else False

    return [(tickers, str(start), str(end), bool(auto_adjust), bool(actions))
            for tickers in ticker_sets]


def _walk_function(func, env, end_default, out, unresolved):
    """Collect the data requests of one function body under ``env``."""
    local = dict(env)
    for node in func.body:
        _exec_statements(node, local, end_default, out, unresolved)


def _record_request(node, local, end_default, out, unresolved):
    """Record a data request if ``node`` is one. Returns True when it was."""
    if not _is_data_call(node):
        return False
    try:
        requests = _requests_from_call(node, local, end_default)
    except Unresolved as exc:
        unresolved.append((node.lineno, str(exc)))
        return True
    out.extend(requests)
    return True


def _exec_statements(node, local, end_default, out, unresolved):
    if isinstance(node, ast.Assign):
        if _record_request(node.value, local, end_default, out, unresolved):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    local[target.id] = None
            return
        try:
            value = _eval(node.value, local)
        except Unresolved:
            value = _expand_dict_subscript(node.value, local)
        for target in node.targets:
            if isinstance(target, ast.Name):
                local[target.id] = value
            else:
                try:
                    _bind(target, value, local)
                except Unresolved:
                    pass
    elif isinstance(node, ast.AnnAssign):
        if _record_request(node.value, local, end_default, out, unresolved):
            return
        try:
            value = _eval(node.value, local)
        except Unresolved:
            value = None
        if isinstance(node.target, ast.Name):
            local[node.target.id] = value
    elif isinstance(node, ast.For):
        try:
            source = _eval(node.iter, local)
        except Unresolved:
            source = None
        if not isinstance(source, (list, tuple, set)):
            for stmt in node.body:
                _exec_statements(stmt, local, end_default, out, unresolved)
            return
        for item in source:
            inner = dict(local)
            try:
                _bind(node.target, item, inner)
            except Unresolved:
                pass
            for stmt in node.body:
                _exec_statements(stmt, inner, end_default, out, unresolved)
    elif isinstance(node, ast.If):
        for stmt in node.body:
            _exec_statements(stmt, local, end_default, out, unresolved)
    elif isinstance(node, (ast.With, ast.Try)):
        for stmt in node.body:
            _exec_statements(stmt, local, end_default, out, unresolved)
    elif isinstance(node, ast.Expr):
        _record_request(node.value, local, end_default, out, unresolved)
    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        local.update(_import_names(node, ROOT))
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        # nested helper: scan it separately with the enclosing environment
        _walk_function(node, local, end_default, out, unresolved)


def _assignment_values(tree, name):
    """Value nodes assigned to ``name`` anywhere in a module."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    yield node.value


def _bind_argument(arg, ns, tree):
    """Resolve a call argument, falling back to a module-wide assignment."""
    try:
        return _eval(arg, ns)
    except Unresolved:
        pass
    if isinstance(arg, ast.Name):
        for value_node in _assignment_values(tree, arg.id):
            try:
                return _eval(value_node, ns)
            except Unresolved:
                continue
    return None


def _function_calls(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == name:
            yield node


def scan_requests(root, driver_sources=None):
    """Resolved data requests per driver.

    Returns ``(requests, unresolved)`` where ``requests`` maps a driver path
    to the list of ``(tickers, start, end, auto_adjust, actions)`` tuples it
    asks for.
    """
    root = Path(root)
    end_default = vintage_end_date(root)
    sources = driver_sources if driver_sources is not None else DRIVER_SOURCES
    requests = {}
    unresolved = []

    for rel in sources:
        path = root / rel
        if not path.is_file():
            continue
        try:
            tree = ast.parse(path.read_text())
        except SyntaxError as exc:
            unresolved.append((rel, 0, f"syntax error: {exc}"))
            continue
        ns = _literal_namespace(path, root)
        found = []
        local_unresolved = []

        # module level statements
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            _exec_statements(node, ns, end_default, found, local_unresolved)

        # functions: bind parameters from their call sites
        for func in [n for n in ast.walk(tree)
                     if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            params = [a.arg for a in func.args.args]
            calls = list(_function_calls(tree, func.name))
            if not calls:
                bound = dict(ns)
                # a ``universe`` parameter that is selected at run time from
                # the UNIVERSES table: every member is a data dependency
                for param in params:
                    if param == "universe" and isinstance(ns.get("UNIVERSES"), dict):
                        bound[param] = [list(v) for v in ns["UNIVERSES"].values()
                                        if isinstance(v, (list, tuple))]
                _walk_function(func, bound, end_default, found, local_unresolved)
                continue
            for call in calls:
                bound = dict(ns)
                # parameters that are not supplied at the call site keep their
                # declared default
                defaults = list(func.args.defaults)
                offset = len(params) - len(defaults)
                for i, default in enumerate(defaults):
                    try:
                        bound[params[offset + i]] = _eval(default, ns)
                    except Unresolved:
                        bound[params[offset + i]] = None
                for i, arg in enumerate(call.args):
                    if i < len(params):
                        bound[params[i]] = _bind_argument(arg, ns, tree)
                for kw in call.keywords:
                    if kw.arg in params:
                        bound[kw.arg] = _bind_argument(kw.value, ns, tree)
                # a ``universe`` parameter selected at run time from the
                # UNIVERSES table: every member is a data dependency
                for param in params:
                    if param == "universe" and not bound.get(param):
                        if isinstance(ns.get("UNIVERSES"), dict):
                            bound[param] = [list(v) for v in ns["UNIVERSES"].values()
                                            if isinstance(v, (list, tuple))]
                _walk_function(func, bound, end_default, found, local_unresolved)

        if found:
            requests[rel] = found
        for lineno, reason in local_unresolved:
            unresolved.append((rel, lineno, reason))

    return requests, unresolved


def scan_macro_requirements(root):
    """Cached FRED series and the pinned fundamentals snapshot.

    ``src.macro.fetch_fred`` caches each series as
    ``data/fred_{series}_{hash}.parquet``; ``src.fundamentals`` caches the
    quarterly panels under ``data/fundamentals/``. Both are fetched from the
    network when the cache misses, so both must be committed.
    """
    root = Path(root)
    files = set()

    macro_path = root / "src" / "macro.py"
    if macro_path.is_file():
        ns = _literal_namespace(macro_path, root)
        themes = ns.get("THEMES")
        if isinstance(themes, dict):
            for spec in themes.values():
                series = spec.get("series") if isinstance(spec, dict) else None
                if not series:
                    continue
                h = hashlib.sha256(str(series).encode()).hexdigest()[:16]
                files.add(f"{DATA_DIR}/fred_{series}_{h}.parquet")

    fund_path = root / "data" / "fundamentals_vintages.json"
    if fund_path.is_file():
        try:
            vintage = json.loads(fund_path.read_text()).get("default_vintage")
        except ValueError:
            vintage = None
        if vintage:
            for panel in ("rev", "cogs", "ta"):
                files.add(f"{DATA_DIR}/fundamentals/fundamentals_*_{vintage}.parquet.{panel}.parquet")
    return files


def fundamentals_panels(root):
    """(vintage, [panel paths]) of the pinned fundamentals snapshot."""
    root = Path(root)
    fund_dir = root / "data" / "fundamentals"
    vintages = root / "data" / "fundamentals_vintages.json"
    vintage = None
    if vintages.is_file():
        try:
            vintage = json.loads(vintages.read_text()).get("default_vintage")
        except ValueError:
            vintage = None
    panels = []
    if fund_dir.is_dir():
        for path in sorted(fund_dir.glob("*.parquet")):
            panels.append(str(path.relative_to(root)))
    return vintage, panels


def _strip_globs(files):
    """Drop wildcard entries: they are checked by a dedicated pass."""
    return {f for f in files if "*" not in f}


def scan_raw_requirements(root):
    """The E024 raw (unadjusted) OHLCV cache.

    ``experiments/run_e024.py`` keeps a second, raw price panel under a
    ``raw_`` cache prefix. It is fetched with ``yf.download`` directly, so the
    guard has to model its key separately.
    """
    root = Path(root)
    files = set()
    path = root / "experiments" / "run_e024.py"
    if not path.is_file():
        return files
    ns = _literal_namespace(path, root)
    large_liquid = ns.get("LARGE_LIQUID")
    if not isinstance(large_liquid, list):
        return files
    tickers = sorted(["SPY"] + list(large_liquid)[:10])
    h = hashlib.sha256(("raw|" + "|".join(tickers)).encode()).hexdigest()[:16]
    safe = "_".join(tickers)[:80]
    end = vintage_end_date(root)
    files.add(f"{DATA_DIR}/raw_{safe}_{h}_2014-01-01_{end}.parquet")
    return files


def scan_requirements(root, driver_sources=None):
    """Discover the cached data files every driver reads.

    Returns ``(requirements, unresolved)`` where ``requirements`` maps a
    driver path to the set of ``data/...`` cache files it needs, and
    ``unresolved`` lists the call sites that could not be resolved
    statically (they are covered by the empirical audit instead).
    """
    requests, unresolved = scan_requests(root, driver_sources)
    requirements = {}
    for rel, found in requests.items():
        files = set()
        for tickers, start, end, auto_adjust, actions in found:
            name = cache_filename_with_flags("|".join(tickers), start, end,
                                             auto_adjust, actions)
            files.add(f"{DATA_DIR}/{name}")
        if files:
            requirements[rel] = files
    return requirements, unresolved


# --------------------------------------------------------------------------
# manifest handling
# --------------------------------------------------------------------------

def _load_manifest(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except OSError as exc:
        return None, f"cannot read manifest: {exc.strerror or exc}"
    except ValueError as exc:
        return None, f"manifest is not valid JSON: {exc}"
    if not isinstance(data, dict) or not isinstance(data.get("files"), dict):
        return None, "manifest has no 'files' object"
    return data, None


def build_fingerprint(root, files):
    root = Path(root)
    out = {}
    for rel in sorted(files):
        path = root / rel
        if path.is_file():
            out[rel] = {
                "sha256": _sha256(path),
                "bytes": path.stat().st_size,
            }
        else:
            out[rel] = {"sha256": None, "bytes": None}
    return out


def _all_requirements(root, driver_sources=None):
    """Every cached data file a driver reads, across all cache families."""
    requirements, unresolved = scan_requirements(root, driver_sources)
    extra = scan_macro_requirements(root) | scan_raw_requirements(root)
    if extra:
        requirements.setdefault("(macro / fundamentals / raw families)", set()).update(
            _strip_globs(extra))
    return requirements, unresolved, extra


def _update(root, manifest_path, requirements=None):
    root = Path(root)
    manifest_path = Path(manifest_path)
    old, err = _load_manifest(manifest_path)
    old_files = dict(old["files"]) if old else {}
    if requirements is None:
        requirements, _, _ = _all_requirements(root)
    wanted = set()
    for files in requirements.values():
        wanted |= files
    # keep previously pinned files that the scan does not rediscover: they may
    # belong to a request that is only reachable dynamically. They are still
    # required, and dropping them silently would weaken the guard.
    wanted |= set(old_files)

    new_files = build_fingerprint(root, wanted)
    changed = []
    added = []
    for rel, meta in new_files.items():
        prev = old_files.get(rel)
        if prev is None:
            added.append(rel)
        elif prev.get("sha256") != meta["sha256"]:
            changed.append((rel, prev.get("sha256"), meta["sha256"]))

    payload = {
        "schema": "data_baseline_fingerprint_v1",
        "algorithm": "sha256",
        "scope": "cached parquet inputs under data/ that the committed experiment drivers read",
        "note": ("Pinned fingerprint of the cached data inputs behind the committed "
                 "experiment artifacts. Regenerate deliberately with: "
                 "python3 scripts/check_data_coverage.py --update"),
        "n_files": len(new_files),
        "files": new_files,
        "drivers": {rel: sorted(files) for rel, files in sorted(requirements.items())},
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"updated {manifest_path} ({len(new_files)} data file(s))")
    for rel in added:
        print(f"  + added    {rel}")
    for rel, was, now in changed:
        print(f"  ~ changed  {rel}")
        print(f"      was: {was}")
        print(f"      now: {now}")
    if not (added or changed):
        print("  (no change)")
    return 0


def check(root=None, manifest=None):
    root = Path(root) if root is not None else ROOT
    manifest_path = Path(manifest) if manifest is not None else DEFAULT_MANIFEST

    data, err = _load_manifest(manifest_path)
    if data is None:
        print(f"FAIL {err}: {manifest_path}")
        print("  the pinned data fingerprint is missing or unreadable")
        print("  regenerate with: python3 scripts/check_data_coverage.py --update")
        return 1

    files = data["files"]
    tracked = tracked_files(root)
    if tracked is None:
        print("NOTE git ls-files failed - skipped the git-tracked scan")
        tracked = set()

    missing, changed, untracked = [], [], []
    for rel, meta in sorted(files.items()):
        path = root / rel
        if not path.is_file():
            missing.append(rel)
            continue
        actual = _sha256(path)
        if actual != meta.get("sha256"):
            changed.append((rel, meta.get("sha256"), actual))
        if rel not in tracked:
            untracked.append(rel)

    requirements, unresolved, extra = _all_requirements(root)
    scanned = set()
    for files_ in requirements.values():
        scanned |= files_
    unpinned = sorted(f for f in scanned if f not in files)

    # The pinned fundamentals snapshot: every panel must be present and tracked.
    vintage, panels = fundamentals_panels(root)
    fund_missing = []
    fund_untracked = []
    for rel in panels:
        if not (root / rel).is_file():
            fund_missing.append(rel)
        elif rel not in tracked:
            fund_untracked.append(rel)
    if vintage and not panels:
        fund_missing.append(f"data/fundamentals/ (no panels for vintage {vintage})")

    ok = True
    if missing:
        ok = False
        print(f"FAIL {len(missing)} pinned data file(s) missing from the working tree:")
        for rel in missing:
            print(f"  {rel}")
        print("  a driver that needs this input will re-download it from the network")
    if changed:
        ok = False
        print(f"FAIL {len(changed)} pinned data file(s) differ from the pinned fingerprint:")
        for rel, was, now in changed:
            print(f"  {rel}")
            print(f"    pinned: {was}")
            print(f"    actual: {now}")
        print("  the committed artifacts were derived from the pinned snapshot")
    if untracked:
        ok = False
        print(f"FAIL {len(untracked)} pinned data file(s) are not git-tracked:")
        for rel in untracked:
            print(f"  {rel}")
        print("  a fresh clone would not contain them and would re-download from the network")
        print("  add them with: git add -f <path>   (.gitignore ignores data/*.parquet)")
    if unpinned:
        ok = False
        print(f"FAIL {len(unpinned)} data file(s) a driver reads are not pinned:")
        for rel in unpinned:
            print(f"  {rel}")
        print("  pin them with: python3 scripts/check_data_coverage.py --update")
    if fund_missing:
        ok = False
        print(f"FAIL {len(fund_missing)} pinned fundamentals panel(s) missing:")
        for rel in fund_missing:
            print(f"  {rel}")
    if fund_untracked:
        ok = False
        print(f"FAIL {len(fund_untracked)} pinned fundamentals panel(s) are not git-tracked:")
        for rel in fund_untracked:
            print(f"  {rel}")

    if unresolved:
        print(f"NOTE {len(unresolved)} data request(s) could not be resolved "
              "statically (covered by the empirical audit, not by this scan):")
        for rel, lineno, reason in unresolved:
            print(f"  {rel}:{lineno}  {reason}")

    if not ok:
        return 1
    print(f"ALL {len(files)} PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--update", action="store_true",
                    help="regenerate the pinned fingerprint from the working tree "
                         "(a deliberate act: re-pinning replaces the data baseline)")
    ap.add_argument("--audit", action="store_true",
                    help="print the static requirement inventory and exit")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                    help=f"fingerprint manifest path (default: {DEFAULT_MANIFEST})")
    args = ap.parse_args(argv)
    if args.update:
        return _update(ROOT, args.manifest)
    if args.audit:
        requirements, unresolved = scan_requirements(ROOT)
        for rel in sorted(requirements):
            print(rel)
            for f in sorted(requirements[rel]):
                print(f"  {f}")
        for rel, lineno, reason in unresolved:
            print(f"UNRESOLVED {rel}:{lineno}  {reason}")
        return 0
    return check(ROOT, args.manifest)


if __name__ == "__main__":
    sys.exit(main())
