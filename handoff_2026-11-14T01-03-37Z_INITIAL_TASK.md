# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T01:03:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `3b23cf05` ("chore(kilo): checkpoint agent session"), in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean apart from tracked `__pycache__/*.pyc` bytecode (13 files) — no source/experiment/data changes. `## main...origin/main`, `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync).
- **No interrupted verification state:** `.verify_snapshot/` and `.verify_reports/` absent.
- **Baseline/data guards (re-run at this handoff, all exit 0):**
  - `SEED=42 python3 scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT.
  - `SEED=42 python3 scripts/check_goldens_clean.py` → ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD.
  - `SEED=42 python3 scripts/check_data_coverage.py` → ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED.
  - `SEED=42 python3 scripts/check_json_artifacts.py` → 114 committed JSON artifacts checked, all parse OK.
- **Tracked artifacts:** `git ls-files experiments/` → 138 (107 JSON goldens + 31 drivers).
- **Research phase:** complete (E001–E051). Survivors/dispositions: `ledger/RESEARCH_LEDGER.md`. Last research entry is **E051**; **E052+** are durable-handoff refreshes only. No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` items.
- **Closed/resolved (do not reopen):** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Delta vs prior durable handoff (00:41:06Z, HEAD `1cecfaa68b` → `3b23cf05`):** `git diff --name-only 1cecfaa68b..3b23cf05 -- experiments/ data/ src/ tests/ scripts/ ledger/` → `ledger/RESEARCH_LEDGER.md` only (the E261 durable-handoff refresh entry). No research/source/data/experiment/baseline substance changed.

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent experiments, run long verification unprompted, change gates/outcomes, or modify/re-pin golden or baseline artifacts without explicit direction. The repository is in a closed, fully-verified research state; routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment (`main...origin/main`, clean apart from `__pycache__`).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes. If dependencies are missing, install `pip install -r requirements.txt`, or interpret known pandas/numpy-missing `tests/test_data_coverage.py` errors as environment-only.

### If verification / reproduction is requested

- Always use **`SEED=42`**.
- Scopes: `make check` / `SEED=42 bash scripts/check.sh` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick ~8m), `--extended` (~21m), `--full` (~15m) — see `AGENTS.md`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before committing.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- **Reproducibility:** `SEED=42`; respect pinned data vintages/caches and `QUANT_RESEARCH_OFFLINE=1` under the suite.
- **Baselines/goldens:** the committed golden is authoritative; never replace/re-pin as a side effect of verification.
- **Discipline:** pre-registration and goalposts unchanged; sensitivity grids reported not gated; record negative results honestly.
- **Closed items:** do not reopen E049/E050 or E041/E042 drift.
- **CI:** do not create `.github/workflows/` as an automated agent (template: `.github/workflow-templates/verification-gate.yml`).
- **Security:** never commit/log secrets or keys.
- **Code:** run `python3 -m py_compile` on changed files.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions/open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-14T01-03-37Z_INITIAL_TASK.md` (this file).
- **Operational pointers:** generic handoff symlinks repointed with `python3 scripts/repoint_handoff.py handoff_2026-11-14T01-03-37Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-14T00-41-06Z_INITIAL_TASK.md` and earlier handoff artifacts/symlinks (retained for history).