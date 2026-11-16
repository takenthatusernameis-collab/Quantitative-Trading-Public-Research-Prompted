# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T20:56:11Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `494edbdbe31420da9290f8042b5f9420ac9dc069` ("chore(kilo): checkpoint agent session") — aligned with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Outstanding task

**None assigned.** Await explicit user instructions.

## Current state (at handoff)

- **Research phase:** complete. Last *research* entry is **E051** (Post-Closure Conformance Pass, 2026-11-02); **E052–E414 are durable-handoff bookkeeping only**. Dispositions and the surviving validated strategies are recorded in `ledger/RESEARCH_LEDGER.md`.
- **Ledger tail:** last entry is **E414** (HEAD `c7b38d0a`, 2026-11-16T20:51:50Z). This session appends **E415**.
- **Verification state:** `.verify_snapshot/` and `.verify_reports/` are absent — no interrupted or pending verification run observed.
- **Working tree:** `git status --short --branch` shows only `main...origin/main` with the pre-existing `src/__pycache__/cache_keys.cpython-312.pyc` modification (tracked bytecode, mtime drift only; excluded from checkpoints by the controller).
- **Delta since prior durable handoff (`handoff_2026-11-16T20-54-43Z_INITIAL_TASK.md`, HEAD `494edbdb`):** handoff bookkeeping only — this new timestamped artifact, its canonical-pointer repoint, and the E415 ledger append. No changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`.
- **Canonical artifacts unchanged:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and the pinned `data/` / `data/fundamentals/` inputs.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and the E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for the next session (CLEAR)

**Default:** Do nothing until the user provides an explicit request. Do not invent new experiments, run verification unprompted, change pre-registered gates or outcomes, or modify golden/baseline artifacts. The research loop is closed; there are no actionable open items in the ledger.

### Before any substantive work (when explicitly requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (including the pre-existing `__pycache__` drift).
2. Confirm `.verify_snapshot/` is absent. If a stale/interrupted snapshot exists: `SEED=42 python3 run_all_verification.py --restore-only` (or restore the pinned goldens per `AGENTS.md`) **before** other work.
3. Install dependencies if needed: `pip install -r requirements.txt` (`scripts/check.sh` aborts on missing `numpy`/`pandas`).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes: `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction and ledger justification.

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit intentional instruction and ledger justification.
- Do not reopen closed E049/E050 or the E041/E042 drift item.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `PROMPT.MD` — autonomous research workflow and handoff requirements
- `ledger/RESEARCH_LEDGER.md` — dispositions, closure records, and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-16T20-56-11Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, and `.kilo/handoff/`; generic canonical pointers repointed with `python3 scripts/repoint_handoff.py handoff_2026-11-16T20-56-11Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-16T20-54-43Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained for history).
- This session created this durable handoff and the E415 ledger record only. No code, experiments, ledgers' research entries, baselines, or canonical artifacts were modified.

(End of file)