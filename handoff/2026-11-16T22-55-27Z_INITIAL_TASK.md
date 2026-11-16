# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T22:55:27Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `24d0b1955ff09550366c9f5d4c43d4920f79b7d0`
**Upstream:** `origin/main` (ahead/behind vs HEAD: `0	0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Outstanding task

**None assigned.** Await explicit user instructions.

## Current state (at handoff)

- **Research phase:** complete (E001–E043). Surviving validated strategies and dispositions: `ledger/RESEARCH_LEDGER.md`.
- **Verification state:** `.verify_snapshot/` absent, `.verify_reports/` absent.
- **Working tree:** only pre-existing `__pycache__` drift; HEAD aligned with origin/main.
- **Canonical artifacts:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` inputs are the authoritative baseline. Do not modify without explicit direction.

## Initial task for the next session (CLEAR)

**Default:** Do nothing until the user provides an explicit request. Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts.

### Before any substantive work (if explicitly requested)

1. `git status --short --branch` — confirm HEAD/alignment and note any uncommitted files (including pre-existing `__pycache__` drift).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Ensure dependencies if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes: `make check` (fast), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full` per `AGENTS.md`.
- Verification overwrites and restores `experiments/*.json`; never leave a run half-finished and never commit verification output over goldens.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift.

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never reopen closed ledger items or re-pin baselines to hide drift.
- Do not create `.github/workflows/` CI gates as an automated agent.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-16T22-55-27Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`.
- **Supersedes operationally:** prior timestamped handoffs (retained for history).
- This action created/refreshed the durable handoff message only; no code, experiments, ledgers, or canonical artifacts were modified.
