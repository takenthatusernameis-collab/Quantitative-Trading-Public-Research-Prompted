# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-28T00:49:45Z
**Session**: Initial task message for the next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Authoritative copy**: `.handoff.md` (mirrors this file); `CURRENT` / `CURRENT.md` / `current` / `current.md` / `handoff_LATEST` point to the latest `handoff_<ts>_INITIAL_TASK.md`

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. All experiments are pre-registered with falsification
expectations and promotion gates. **Research phase complete (E001–E043).**
Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Verified state (2026-11-28T00:49:45Z)
- HEAD `f5f7a321633053cc408599e1592a1042ff825efc` == origin/main; branch `main`.
- Working tree clean for canonical artifacts (`experiments/`, `data/`, `ledger/`). The only
  working-tree change is a non-canonical tracked bytecode file
  (`src/__pycache__/cache_keys.cpython-312.pyc`) — ignore it; do not commit it.
- No `.verify_snapshot/` — no interrupted verification run pending recovery, and no live run owns the snapshot.
- **Dependencies are NOT installed in this environment**: `python3 -c "import numpy"` fails
  (`ModuleNotFoundError: No module named 'numpy'`); `pip show numpy` reports not found.
  Python is `/usr/bin/python3` (3.12.3). Run `python3 -m pip install -r requirements.txt`
  before executing any driver, `scripts/check.sh`, or the verification suite.
- Guard scripts present: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py`, `run_all_verification.py`, `requirements.txt`.

## Next Steps for New Session (in order, then stop)
1. Read `AGENTS.md` (baseline integrity, reproducibility, cache-coverage invariant).
2. Install deps if missing: `python3 -m pip install -r requirements.txt`; confirm
   `python3 -c "import numpy, pandas"`.
3. Confirm canonical state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`;
   confirm HEAD == origin/main and no `.verify_snapshot/`.
4. Confirm goldens match the pinned baseline: `python3 scripts/check_goldens_clean.py` and
   `python3 scripts/check_golden_baseline.py`.
5. If a verification run was interrupted, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout <pinned-commit> -- experiments/<file>`).
6. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items.
7. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens +
   data coverage + JSON guards are green — only if the user directs it.
8. Then pick up the next user-directed research/engineering task. If this session itself hands
   off, create its own timestamped durable handoff following the established pattern
   (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root), then update the
   `handoff_LATEST` / `CURRENT` / `current` / `current.md` symlinks and `.handoff.md`.

## Key Constraints
- Never leave a verification run half-finished; never commit verification output.
- Always `SEED=42`; close-to-close is the v1.2.3 primary convention.
- Never re-pin artifacts to silence drift; the committed golden is authoritative.
- CI workflow cannot be created by automated agents; use local `make check` / `make verify*`.
- Closed items — do not re-open: E049/E050 optimizer determinism + exact KKT enumeration;
  E041/E042 ill-conditioned QP drift. All closed; artifacts reproduce 0 diffs.

## Initial Task for This Session
None pending — this handoff leaves the repo in a clean, canonical state awaiting the next
user-directed task. The one environment gap to close first is installing `requirements.txt`
(numpy/pandas are absent here).

*This handoff was created for the next agentic work session.*
