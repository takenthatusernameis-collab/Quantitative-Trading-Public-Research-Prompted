# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T19:52:08Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `645fd6ce` ("chore(kilo): checkpoint agent session") (aligned with `origin/main` at the time of this handoff)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Outstanding task

**None assigned.** Await explicit user instructions. Do not start new research, experiments, refactors, or verification unless the user asks.

## Current state (at handoff)

- **Research phase:** complete (E001–E051 research; E052–E410 durable-handoff bookkeeping). Dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- **Ledger tail:** last committed entry is **E409** (HEAD `9c26f059`). This handoff is bookkeeping only (no ledger/code/experiment/baseline changes).
- **Verification snapshots/reports:** none present (`.verify_snapshot/`, `.verify_reports/` absent). No interrupted verification observed.
- **Working tree:** expected to be clean except possibly gitignored `__pycache__/*.pyc` mtime noise; verify with `git status --short --branch`.
- **Delta since prior durable handoff (`handoff_2026-11-16T19-50-46Z_INITIAL_TASK.md`):** this file adds a new timestamped handoff and repoints pointers only.
- **Canonical artifacts unchanged:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs unchanged.

## Initial task for the next session (CLEAR)

**Default action:** Take no action until the user gives an explicit request.

### If the user gives no request
- Reply concisely that no outstanding task is assigned and list the safe pre-work checks below if they want you to proceed.

### Before any substantive work (when requested)
1. `git status --short --branch` — confirm HEAD/remote alignment; note uncommitted files (including pre-existing `__pycache__` drift).
2. Confirm `.verify_snapshot/` absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. If deps missing, `pip install -r requirements.txt` (note: `scripts/check.sh` aborts if `numpy`/`pandas` unavailable).
4. Before committing substantive changes, run: `SEED=42 bash scripts/check.sh` (or `make check`).

### If verification/reproduction is explicitly requested
- Always use `SEED=42`.
- Scopes: `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites then restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift unless explicitly instructed with ledger justification.

## Guardrails (non-negotiable)

- Always use `SEED=42` for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit intentional instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 residual drift items (ill-conditioned QP ~1e-05).
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **This durable artifact:** `handoff_2026-11-16T19-52:08Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/` by the handoff process.
- **Supersedes operationally:** `handoff_2026-11-16T19-50-46Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained for history).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.

(End of file)
