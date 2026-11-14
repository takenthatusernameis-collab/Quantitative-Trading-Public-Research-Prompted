# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T16:37:52Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `f37b7969` ("chore(kilo): checkpoint agent session")
**Remote:** `origin/main` aligned with local `main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## State at handoff

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving strategies: `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items.
- **Verification snapshot:** `.verify_snapshot/` absent (no interrupted verification run pending); `.verify_reports/` absent.
- **Working tree:** clean of source/data changes. Only modified tracked `__pycache__/*.pyc` files from environment runs — **do not commit**. This session adds this durable handoff artifact/mirrors, ledger entry E319, and repoints generic handoff pointers/symlinks to it.
- **Baselines/guards:** canonical artifacts under `experiments/` and pinned fingerprints in `ledger/golden_baseline.json` and `ledger/data_baseline.json` are authoritative. Verified this session:
  - `SEED=42 python3 scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0).
  - `SEED=42 python3 scripts/check_data_coverage.py` → `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED` (exit 0).
- **Environment caveat:** `pandas`/`numpy` are not installed in this runtime, so `scripts/check.sh` and `tests.test_data_coverage` cannot run end-to-end here. This is environment-only, not a repo defect; install with `pip install -r requirements.txt`.
- **Delta since prior durable handoff:** `1977e4b5` → `f37b7969` (checkpoint commits only). Filtered for non-handoff content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`. Only `ledger/RESEARCH_LEDGER.md` (E318 provenance) plus generic handoff pointer/symlink files changed. No research substance changed. (Prior durable handoff `2026-11-14T16:35:09Z` reported the `3d50044a` → `1977e4b5` delta as likewise 0 substantive paths.)
- **Closed — do not reopen:** E049/E050 (optimizer determinism/KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task (clear)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (`__pycache__` noise and/or this handoff's deliverables only).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Ensure deps if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification/reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes: `make check` (guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full` (see `AGENTS.md`).
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin golden/data baselines without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit or log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions/open items (last recorded research entry E051; last recorded handoff entry E319)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-14T16-37-52Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/handoff_2026-11-14T16-37-52Z_INITIAL_TASK.md` and `.kilo/handoff/handoff_2026-11-14T16-37-52Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-14T16-35-09Z_INITIAL_TASK.md` and earlier handoff artifacts (retained for history). No new research entry; this is a state-refresh handoff resuming the ledger record at E319.
- This session created this durable handoff and repointed generic handoff pointers to it. No code, experiments, baselines, or canonical artifacts were modified.

(End of file - total 61 lines)