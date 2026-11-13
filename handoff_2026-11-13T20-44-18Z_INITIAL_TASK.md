# INITIAL TASK — Handoff for the Next Agentic Work Session

**Handoff timestamp (UTC):** 2026-11-13T20:44:18Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `36578c4b chore(kilo): checkpoint agent session` on `main`
**Sync with origin:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (HEAD == `origin/main` = `36578c4b`)
**Working tree:** clean at handoff time — `git status --short --branch` → `## main...origin/main` with no modified/untracked files before the guard runs below. After running the guards, the only additional entries are the tracked `__pycache__/*.pyc` bytecode files (`.pyc` files are tracked in this repo and are rewritten whenever the Python guards execute — no source/artifact change). **No interrupted run** — `.verify_snapshot/` and `.verify_reports/` are both absent (checked in repo root and `$TMPDIR`).

---

## Verified state at handoff time

| Check | Command | Result |
|---|---|---|
| Goldens vs baseline fingerprint | `SEED=42 python3 scripts/check_golden_baseline.py` | **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT** (exit 0) |
| Goldens vs HEAD | `SEED=42 python3 scripts/check_goldens_clean.py` | **ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD** (exit 0) |
| Data coverage | `SEED=42 python3 scripts/check_data_coverage.py` | **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED** (exit 0) |
| Tracked experiment artifacts | `git ls-files experiments/ \| wc -l` | 138 (107 JSON + 31 driver `.py`) |
| JSON artifacts parse | `python3 scripts/check_json_artifacts.py` | exit 0 — all committed JSON parse |

### `SEED=42 bash scripts/check.sh` does NOT exit 0 in this sandbox — environment only, not a defect

Individual step results (run one-by-one):

| Step | Exit | Note |
|---|---|---|
| check_json_artifacts / check_goldens_clean / check_golden_baseline / check_data_coverage | 0 | all green |
| tests.test_json_guard / test_goldens_guard / test_golden_baseline / test_drift_report | 0 | all green |
| **tests.test_data_coverage** | 1 | 3 ERRORs: `ModuleNotFoundError: No module named 'pandas'` |
| **tests.test_portfolio_opt** | 1 | `ModuleNotFoundError: No module named 'numpy'` |
| verify_convention_robustness / validate_template / check_experiment_imports | 0 | all green |

- Root cause: this environment lacks `pandas` / `numpy`. `AGENTS.md` documents exactly this ("interpret known pandas-missing `tests/test_data_coverage.py` errors as environment-only").
- **All `FAIL` lines printed by the guard self-tests are deliberate negative fixtures** written to tempdirs by `tests/test_json_guard.py`, `test_goldens_guard.py`, `test_golden_baseline.py` and `tests/test_data_coverage.py` (e.g. `experiments/d.json`, `d2.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `data/panel.parquet`, `nope.json`, `pid 999999`, `experiments/e001.json`). They are **not** repository files and **not** baseline corruption. Confirmed: no such tracked files exist; no `.verify_snapshot` anywhere; `experiments/e001.json` is absent from HEAD and from the working tree.
- To get a fully green suite, install deps first: `pip install -r requirements.txt`, then `SEED=42 bash scripts/check.sh`.

Nothing was committed by this session.

---

## Project status

- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete.** Surviving validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`. Ledger's last *research* entry is **E051**; entries **E052–E239 are durable-handoff refreshes only**. No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` markers anywhere in the ledger.
- Canonical artifacts: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin them as a side effect of verification.**
- Closed / do not reopen: E049/E050 (optimizer determinism + exact KKT enumeration) and the residual E041/E042 ill-conditioned QP drift (~1-ulp, ~1e-05). **Do not re-pin E041/E042 to silence drift.**

---

## Supersedes

This handoff supersedes `handoff_2026-11-13T20-43-25Z_INITIAL_TASK.md` (HEAD `22756790`).

**Delta across `experiments/ data/ src/ tests/ scripts/ ledger/` between `22756790` and `36578c4b`** → only `ledger/RESEARCH_LEDGER.md` (+32 lines: the E239 durable-handoff entry written by the prior handoff). `experiments/`, `data/`, `src/`, `tests/`, `scripts/` unchanged. The intervening commit (`36578c4b`) touches only handoff bookkeeping (canonical pointers, `handoff_*` artifacts). **No research, source, data, experiment, or baseline substance changed.**

---

## CLEAR INITIAL TASK for the next session

1. **Do not begin substantive research work until the user gives explicit direction.** First read `AGENTS.md`, the tail of `ledger/RESEARCH_LEDGER.md`, and this handoff.
2. **Confirm the baseline is healthy** (cheap, offline, already green as of this handoff):
   ```bash
   git status --short --branch
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_goldens_clean.py
   SEED=42 python3 scripts/check_data_coverage.py
   ```
   If `bash scripts/check.sh` reports only `ModuleNotFoundError: pandas` / `numpy`, that is environment-only; `pip install -r requirements.txt` first.
3. **If reproduction/verification is explicitly requested**, always use `SEED=42` and the suites in `AGENTS.md` (`run_all_verification.py` default quick ~8 min, `--extended` ~21 min, `--full` ~15 min). The suite overwrites `experiments/*.json` while it runs and restores them afterwards — **never leave a run half-finished.** Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned goldens per `AGENTS.md`).
4. **Before committing anything**, run `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py`. If a golden mismatch appears, fix it before committing — never let a checkpoint commit capture verification output as the new baseline (this regressed the baseline four times historically; see `AGENTS.md`).
5. **Default disposition:** wait for explicit user instructions. Do not invent experiments, re-run verification unprompted, change pre-registered gates/outcomes, or re-pin goldens/data baselines.
6. **Leave the next durable handoff** when this session ends: a new `handoff_<UTC timestamp>_INITIAL_TASK.md` plus `python3 scripts/repoint_handoff.py <new file>` (repoints the generic canonical pointers in root, `.handoff/`, `.kilo/`, `.kilo/handoff/`, `handoff/`, `HANDOFFS/`), then append a matching `## E###: Durable Handoff Refresh` entry to `ledger/RESEARCH_LEDGER.md`.

## Guardrails

- **Reproducibility:** always `SEED=42`; use pinned data vintages/caches (`data/vintages.json`, `data/fundamentals_vintages.json`); never introduce live-network dependence into verification paths; the suite runs with `QUANT_RESEARCH_OFFLINE=1`.
- **Golden artifacts:** never replace/"refresh" `experiments/*.json` or re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` as a side effect of verification.
- **Pre-registration discipline:** new experiments must state gates, falsification expectations, and sensitivity handling *before* execution; sensitivity grids are reported, not gated; record negative results honestly (REJECTED / PARTIAL).
- **CI:** do not create `.github/workflows/` gates as an automated agent — the template is `.github/workflow-templates/verification-gate.yml`; creating the real workflow is a maintainer action.
- Never commit or log secrets/keys. Do not commit `__pycache__` or other verification output.
- On changed Python files, run `python3 -m py_compile <file>` (no separate linter is configured).

## Verification commands (run only when explicitly requested)

```bash
SEED=42 bash scripts/check.sh                          # fast guards (needs pandas/numpy)
SEED=42 python3 verify_convention_robustness.py        # reads JSONs, no writes
SEED=42 python3 run_all_verification.py                # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended     # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only # recover goldens
make check | make verify | make verify-quick | make verify-extended | make verify-full
```

## Pending work

- **None.** Baseline verified green (107 goldens match the pinned fingerprint and HEAD, 35/35 data inputs, JSON artifacts parse); working tree clean; repository closed (E001–E051 research, E052–E239 handoff refreshes). Await explicit user-directed work.