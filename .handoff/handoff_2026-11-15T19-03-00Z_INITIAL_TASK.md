# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T19:03:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `82efa4c8` ("chore(kilo): checkpoint agent session")
**Sync:** `origin/main...HEAD` = `0 0` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (observed at handoff)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. No open/pending/blocked research items recorded in ledger.
- **Working tree (non-handoff):** modified bytecode/cache files only: `scripts/__pycache__/*.pyc`, `src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc` (see `git status --short`). No source, `experiments/*.json`, pinned `data/` inputs, or `ledger/` baseline files modified.
- **Verification snapshot:** `.verify_snapshot/` absent (no active/stale interrupted verification snapshot detected in repo root at handoff time).
- **Goldens:** no tracked `experiments/*.json` diffs in working tree. Canonical fingerprints remain pinned in `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Environment note:** Python deps/tools (numpy/pandas/scipy/pyarrow/statsmodels/yfinance/pytest, and sometimes `rg`) may be unavailable in fresh sandboxes; install per `requirements.txt` before running verification/tests.

## Delta vs prior durable handoff

- **Prior handoff:** `handoff_2026-11-15T18-59-50Z_INITIAL_TASK.md` (HEAD `01561ca7` at that time).
- **Now:** HEAD advanced to `82efa4c8`; this session adds this durable handoff and repoints generic handoff pointers. No research content (experiments/data/src/scripts/tests/ledger baselines) changed for this handoff.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm clean research state; expect possible `__pycache__` noise and handoff artifacts.
2. If `.verify_snapshot/` exists or goldens look modified, recover before work: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`). Do **not** leave a verification run half-finished.
3. `pip install -r requirements.txt` if dependencies are missing.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Follow `AGENTS.md` scopes:
  - `make check` / `SEED=42 bash scripts/check.sh` (~seconds, offline)
  - `SEED=42 python3 verify_convention_robustness.py` (reads JSONs, no writes)
  - `SEED=42 python3 run_all_verification.py` (quick)
  - `SEED=42 python3 run_all_verification.py --extended`
  - `SEED=42 python3 run_all_verification.py --full`
- Verification overwrites and restores `experiments/*.json`; **never commit verification output** over goldens.
- Interrupted-run recovery: `SEED=42 python3 run_all_verification.py --restore-only`.

## Guardrails

- Never commit verification output over canonical `experiments/*.json` goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional instruction and ledger justification.
- Do not reopen closed items: E049/E050 (optimizer determinism / exact KKT enumeration) or E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer must create via GitHub UI).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (research complete E001–E051)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T19-03-00Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Supersedes operationally:** `handoff_2026-11-15T18-59-50Z_INITIAL_TASK.md` and earlier handoffs (retained for history).
- Generic handoff pointers repointed to this artifact via `scripts/repoint_handoff.py`.
- No experiments, data, source, tests, or ledger baselines modified for this handoff.
