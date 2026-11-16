# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T22:03:25Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `b30c5ab5251b41b5bce23b682996a6d030f43785` ("chore(kilo): checkpoint agent session") — aligned with `origin/main`.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Outstanding task

**None assigned.** Await explicit user instructions.

## Current state (at handoff)

- **Research phase:** complete (E001–E051 research; E052–E419 durable-handoff bookkeeping). Dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- **Ledger tail:** last recorded entry is **E418** (HEAD `04b79efb`, 2026-11-16T21:02:00Z).
- **Verification state:** `.verify_snapshot/` and `.verify_reports/` absent — no interrupted or pending verification run observed.
- **Working tree at handoff creation:** no intentional changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`. Pre-existing tracked `__pycache__` mtime drift may be present; exclude from checkpoints.
- **Canonical artifacts unchanged:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` inputs.

## Initial task for the next session (CLEAR)

**Default:** Do nothing until the user provides an explicit request. Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts. The research loop is closed; there are no actionable open items in the ledger.

### Before any substantive work (when explicitly requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (including pre-existing `__pycache__` drift).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install dependencies if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes: `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction and ledger justification.

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification runs.
- Never commit verification output over canonical goldens.
- Never move goalposts or re-pin baselines without explicit direction.
" filePath="/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/.handoff/handoff_2026-11-16T22-03-25Z_INITIAL_TASK.md