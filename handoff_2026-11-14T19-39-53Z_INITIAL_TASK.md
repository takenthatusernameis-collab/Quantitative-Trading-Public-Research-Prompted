# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T19:39:53Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `dc721c31` ("chore(kilo): checkpoint agent session")
**Remote:** `origin/main` aligned with local `main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## State at handoff

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving strategies: `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items. Ledger's last *research* entry is E051 (2026-11-02); E052–E331 are durable-handoff refreshes only. This session adds entry E332.
- **Verification snapshot:** `.verify_snapshot/` absent (no interrupted verification run pending); `.verify_reports/` absent.
- **Working tree:** modified tracked `__pycache__/*.pyc` files only (environment artifact) — **do not commit**. This session adds this durable handoff artifact as requested.
- **Delta since prior durable handoff (`handoff_2026-11-14T19-38-17Z_INITIAL_TASK.md`, HEAD `d9ec0eef` → `dc721c31`):** one checkpoint commit only (the prior handoff deliverable itself). Filtered for non-handoff/research content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`. Only the handoff/symlink tree (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`) and `ledger/RESEARCH_LEDGER.md` (prior refresh record) changed. No research substance changed.
- **Baselines/guards (verified this session, SEED=42):**
  - `scripts/check_json_artifacts.py` → "checked 114 committed JSON artifacts / ALL COMMITTED JSON ARTIFACTS PARSE OK" (exit 0)
  - `scripts/check_goldens_clean.py` → "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD" (exit 0)
  - `scripts/check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT" (exit 0)
  - `scripts/check_data_coverage.py` → "ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED" (exit 0)
  - `check.sh` end-to-end not fully runnable in this environment: `tests.test_data_coverage` errors with `ModuleNotFoundError: No module named 'pandas'` (3 errors); the `panel.parquet` "FAIL" lines in its output come from `tests/test_data_coverage.py`'s temp-dir fixtures, not the real repo. Install deps with `pip install -r requirements.txt` for a full end-to-end `make check`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism/KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task (clear)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (`__pycache__` noise and/or handoff deliverables only).
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
- `ledger/RESEARCH_LEDGER.md` — dispositions/open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-14T19-39-53Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/` and `.kilo/handoff/` as applicable.
- **Supersedes operationally:** `handoff_2026-11-14T19-38-17Z_INITIAL_TASK.md` and earlier handoff artifacts (retained for history).
- This session created this durable handoff and repointed generic handoff aliases to it. No code, experiments, baselines, or canonical artifacts were modified.

(End of file - total 64 lines)