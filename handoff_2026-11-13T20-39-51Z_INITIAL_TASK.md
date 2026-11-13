# INITIAL TASK — Handoff for the Next Agentic Work Session

**Handoff timestamp (UTC):** 2026-11-13T20:39:51Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `df924055 chore(kilo): checkpoint agent session` on `main`
**Sync with origin:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (HEAD == `origin/main` = `df924055`)
**Working tree:** clean for `experiments/`, `data/`, `src/`, `tests/`, `scripts/`, `ledger/` (only tracked `__pycache__/*.pyc` bytecode files show as modified — binary, no functional impact). No untracked files outside `__pycache__`.
**Interrupted run:** none — `.verify_snapshot/` absent; `.verify_reports/` absent.

---

## Verified state at handoff time

| Check | Command | Result |
|---|---|---|
| Goldens vs HEAD | `SEED=42 python3 scripts/check_goldens_clean.py` | **ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD** (exit 0) |
| Data coverage | `SEED=42 python3 scripts/check_data_coverage.py` | **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED** (exit 0) |
| Tracked experiment artifacts | `git ls-files experiments/ \| wc -l` | 138 |

No research, source, data, experiment, or baseline substance changed during this handoff. Nothing was committed by this session.

> `SEED=42 bash scripts/check.sh` may report `ModuleNotFoundError: pandas` / `numpy` in this sandbox — environment only, not a defect (`AGENTS.md` documents this). Install `pip install -r requirements.txt` first for a fully green suite.

---

## Project status

- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete.** Surviving validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`. Ledger's last *research* entry is E051; entries E052+ are durable-handoff refreshes only. No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` markers anywhere in the ledger.
- Canonical artifacts: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin them as a side effect of verification.**
- Closed / do not reopen: E049/E050 (optimizer determinism + exact KKT enumeration) and the residual E041/E042 ill-conditioned QP drift (~1-ulp, ~1e-05). **Do not re-pin E041/E042 to silence drift.**

---

## Supersedes

This handoff supersedes `handoff_2026-11-13T20-37-30Z_INITIAL_TASK.md` (HEAD `9876e4d2`). Delta across `experiments/ data/ src/ tests/ scripts/ ledger/` is **empty** — this handoff is a pure bookkeeping refresh with no substantive change.

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

- **None.** Baseline verified green (goldens match HEAD, 35/35 data inputs, JSON artifacts parse); working tree clean; repository closed (E001–E051 research, E052+ handoff refreshes). Await explicit user-directed work.
