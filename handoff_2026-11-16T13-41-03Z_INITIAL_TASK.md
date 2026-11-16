# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T13:41:03Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `5441cd19` ("chore(kilo): checkpoint agent session") — confirm alignment with `origin/main` on start.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Outstanding task

**None assigned.** Await explicit user instructions.

## Current state (at handoff)

- **Research phase:** complete (E001–E043). Dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- **Verification state:** `.verify_snapshot/` and `.verify_reports/` absent — no interrupted/pending verification observed.
- **Working tree:** 15 pre-existing `__pycache__/*.pyc` modifications only (mtime drift). No source, experiment, ledger, golden-baseline, or data changes were made in this session.
- **Canonical artifacts unchanged:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` inputs.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for the next session (CLEAR)

**Default:** Do nothing until the user provides an explicit request. Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts.

### Before any substantive work (when requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (including pre-existing `__pycache__` drift and any uncommitted handoff files).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-16T13-41-03Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-16T13-40-16Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained for history).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.
