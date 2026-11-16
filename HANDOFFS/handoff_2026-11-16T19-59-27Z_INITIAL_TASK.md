# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T19:59:27Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `2389df85` ("chore(kilo): checkpoint agent session") — aligned with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Outstanding task

**None assigned.** Await explicit user instructions.

## Current state (at handoff)

- **Research phase:** complete (E001–E051 research; E052–E413 durable-handoff bookkeeping). Dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- **Ledger tail:** last entry is **E412** (HEAD `8f995795`, 2026-11-16T19:57:58Z). This session appends **E413**.
- **Verification state:** `.verify_snapshot/` and `.verify_reports/` absent — no interrupted/pending verification observed.
- **Working tree:** clean per `git status --short --branch` (only the pre-existing `src/__pycache__/cache_keys.cpython-312.pyc` modification, mtime drift, gitignored).
- **Delta since prior durable handoff (`8f995795` → `2389df85`):** only handoff bookkeeping — the now-superseded `handoff_2026-11-16T19-57-58Z_INITIAL_TASK.md` artifact plus generic canonical-pointer symlink repoint. No changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, or `ledger/` (other than this E413 append).
- **Canonical artifacts unchanged:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` inputs.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for the next session (CLEAR)

**Default:** Do nothing until the user provides an explicit request. Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts.

### Before any substantive work (when requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (including the pre-existing `__pycache__` drift).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip install -r requirements.txt` (`check.sh` aborts on missing `numpy`/`pandas`).
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
- Do not reopen closed E049/E050 or E041/E042 drift items.
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

- **Durable artifact (this session):** `handoff_2026-11-16T19-59-27Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Supersedes operationally:** `handoff_2026-11-16T19-57-58Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained for history).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.

(End of file)