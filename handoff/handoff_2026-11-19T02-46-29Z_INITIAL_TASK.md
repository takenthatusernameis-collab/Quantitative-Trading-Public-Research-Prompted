# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-19T02-46-29Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `192f691c` ("chore(kilo): checkpoint agent session") == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Start here (ordered first tasks)

1. **Orient (read-only):** `git status --short --branch` and `git rev-parse HEAD origin/main`.
   Confirm HEAD fast-forwards `origin/main`. Note any uncommitted files before touching anything.
2. **Recover, if needed:** confirm `.verify_snapshot/` and `.verify_reports/` are absent. If a
   snapshot is pending/stale (interrupted verification run), restore the pinned goldens **first**:
   `SEED=42 python3 run_all_verification.py --restore-only` (fallback:
   `git checkout <last-good-commit> -- experiments/<file>` per `AGENTS.md`).
3. **Install deps (this runner has none):** `python3 -m pip install -r requirements.txt`
   (bare `/usr/bin/python3` is 3.12.3; `import pandas` currently raises `ModuleNotFoundError`).
4. **Run the fast integrity gate:** `SEED=42 bash scripts/check.sh` (or `make check`, ~seconds).
   It covers golden-clean, golden-baseline pin, data coverage, optimizer and template tests.
   A golden mismatch must be fixed **before** any commit — never checkpoint verification output.
5. **Then: await explicit user instructions.** Do not invent experiments, run long verification
   unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts.
6. **Before finishing your own session:** leave a fresh durable handoff (procedure at the bottom).

## Current state (verified at handoff)

- **Research phase:** complete. Authoritative dispositions and surviving validated strategies live
  in `ledger/RESEARCH_LEDGER.md` (research E001–E051; handoff refreshes through E515). No actionable
  open/pending/blocked research item is indicated.
- **Verification snapshot:** `.verify_snapshot/` absent. `.verify_reports/` absent. No interrupted
  verification run to recover.
- **Working tree / HEAD:** HEAD `192f691c34783e332767bb0afa104ed3174dced8` == `origin/main`
  (0 ahead / 0 behind). `git status --short --branch` → `## main...origin/main`, tree clean.
- **Pins:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` present and parse.
  `git diff --name-only HEAD -- experiments/` → empty (canonical artifacts unchanged).
- **Environment note (this runner):** numpy/pandas/scipy **not** importable, so `scripts/check.sh`
  was **not** executed this session. Installing `requirements.txt` and running the fast gate are
  steps 3–4 above for the next session.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and the
  E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042
  artifacts to silence that drift.

## If verification / reproduction is explicitly requested

- Always **`SEED=42`**. The suite sets `QUANT_RESEARCH_OFFLINE=1`; a missing cache entry fails hard
  instead of silently downloading (yfinance is not bit-reproducible).
- Scopes: `make check` (~seconds) · `SEED=42 python3 verify_convention_robustness.py` (read-only) ·
  `SEED=42 python3 run_all_verification.py` (quick, ~8 min) · `--extended` (~21 min) ·
  `--full` (~15 min).
- Verification overwrites then restores `experiments/*.json`: **never leave a run half-finished**
  and **never commit verification output** over the goldens.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift.
  Re-pin only with explicit direction, a deliberate `--update` command, and a ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit,
  intentional re-baseline instruction plus a ledger entry.
- Never commit `__pycache__/`, `.verify_snapshot/`, or `.verify_reports/`.
- Do not reopen closed E049/E050 or the E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (controller cleans them; the
  repo token lacks `workflows` scope). Template + instructions:
  `.github/workflow-templates/verification-gate.yml`, `VERIFICATION_GATE_TEMPLATE.md`; a maintainer
  must add the workflow via the GitHub UI.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes
  without explicit justification and a ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants, drift history
- `ledger/RESEARCH_LEDGER.md` — dispositions, open items, handoff refresh log
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned SHA-256 fingerprints
- `experiments/*.json` — canonical research artifacts (138 tracked)
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py`, `run_all_verification.py`, `verify_convention_robustness.py`

## Leaving the next handoff (recurring procedure)

1. Write `handoff_<UTC ISO, colons→dashes>_INITIAL_TASK.md` at the repo root with: timestamp,
   HEAD SHA, current-state facts, an ordered/clear initial task list, guardrails, and provenance.
2. Mirror it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`
   and confirm all six copies share one SHA-256.
3. `python3 scripts/repoint_handoff.py handoff_<timestamp>_INITIAL_TASK.md` — repoints the generic
   aliases (`HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`, `handoff/CURRENT`,
   `.kilo/HANDOFF.md`, `handoff_latest`, `next.md`, …); a run reports `bad=0`.
4. Append a ledger entry recording actions, verification performed, and constraints honored.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-19T02-46-29Z_INITIAL_TASK.md` (repo root),
  to be mirrored byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Canonical pointers:** generic aliases repointed via
  `python3 scripts/repoint_handoff.py handoff_2026-11-19T02-46-29Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-19T02-46-03Z_INITIAL_TASK.md` (which pinned the
  older HEAD `4b22d98d`) and all prior `HANDOFF_*` / `handoff_*` artifacts, retained for history.
- **Current live state capture (this session):** HEAD `192f691c`; clean tree; no verification
  snapshot; pins parse; no artifact drift. No code, experiments, baselines, or canonical artifacts
  were modified; the new files are left uncommitted pending explicit commit direction.
