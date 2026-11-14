# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T10:31:11Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `984e90f7` (tracking `origin/main`, in sync — `git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (snapshot at handoff)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md` (last research entry E051; handoff entries through E294). No actionable open/pending/blocked research items recorded.
- **HEAD delta vs prior durable handoff** (2026-11-14T10:26:30Z, `1e8e27ee` → `984e90f7`): four intermediate `chore(kilo): checkpoint agent session` commits. Filtered for non-handoff/non-ledger content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`. All deltas are generic canonical-pointer symlinks, timestamped handoff artifacts, and ledger handoff entries. No research substance, experiments, ledgers, baselines, or canonical artifacts changed.
- **Working tree:** only the pre-existing/regenerated `src/__pycache__/cache_keys.cpython-312.pyc` modified (do **not** commit). No `experiments/`, `ledger/`, `data/`, `src/`, `scripts/`, or `tests/` changes.
- **Verification snapshot:** `.verify_snapshot/` and `.verify_reports/` absent at handoff time (no interrupted verification run pending).
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Guards verified this session (exit 0)

- `SEED=42 python3 scripts/check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
- `SEED=42 python3 scripts/check_data_coverage.py` → "ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED"

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (pre-existing `__pycache__` change and any handoff/ledger deliverables).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items (last research entry E051; handoff entries through E294)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-14T10-31-11Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/2026-11-14T10-31-11Z_INITIAL_TASK.md` and `.kilo/handoff/2026-11-14T10-31-11Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-14T10-26-30Z_INITIAL_TASK.md` (predecessor) and earlier handoff artifacts (retained for history).
- This session created this durable handoff and repointed the generic handoff pointers. No code, experiments, ledgers, baselines, or canonical artifacts were modified otherwise. No commit was made (left uncommitted pending explicit direction).