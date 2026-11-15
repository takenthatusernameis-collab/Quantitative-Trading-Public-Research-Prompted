# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T13:56:27Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `bfaf5506db1eb44f429559c161461373e79a2bc6` ("chore(kilo): checkpoint agent session")
**Sync:** `main...origin/main` in sync at handoff time (`0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## TL;DR

Research phase is **complete (E001–E051)**; dispositions, validated survivors, and standing notes are in `ledger/RESEARCH_LEDGER.md`. **No open research task.** This session performed no research, verification, or canonical-baseline changes. It re-verified baseline integrity (per-step, no verification run), wrote this durable handoff, and repointed generic handoff aliases. `.verify_snapshot/` and `.verify_reports/` are absent (no interrupted verification run).

## Observed state

- **Latest prior durable handoff:** `handoff_2026-11-15T13-54-44Z_INITIAL_TASK.md` (superseded by this handoff, retained for history).
- **Interrupted verification markers:** `.verify_snapshot/` and `.verify_reports/` **absent**.
- **Working tree (pre-handoff):** only tracked `src/__pycache__/cache_keys.cpython-312.pyc` modified; no canonical research/data/experiment/ledger source files modified by this handoff session.
- **Canonical artifacts/baselines unchanged:** `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`, and pinned data snapshots.
- **Dependencies note:** `pytest`/`numpy`/`pandas` may not be installed in this sandbox, so unit tests/full `scripts/check.sh` can fail solely due to missing dependencies. Install `pip install -r requirements.txt` (plus `pytest` if needed) before running full checks/tests/verification.

## Baseline integrity re-verified this session (per-step, no verification run)

All exited 0:

- `scripts/check_json_artifacts.py` — 114 JSON artifacts parse
- `scripts/check_goldens_clean.py` — goldens match HEAD
- `scripts/check_golden_baseline.py` — all 107 pinned goldens match
- `scripts/check_data_coverage.py` — all 35 pinned data inputs present/tracked/unchanged
- `verify_convention_robustness.py` — convention robustness OK
- `scripts/validate_template.py` — template valid
- `scripts/check_experiment_imports.py` — experiment imports OK

A full `SEED=42 bash scripts/check.sh` / unit-test run was not treated as a research gate here because this is a handoff-only session; if run in an environment missing pandas/numpy/pytest it may exit non-zero only for that dependency reason.

## Clear initial task for next session

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, move goalposts, or modify canonical baselines/goldens without explicit direction.

### 1) Baseline/integrity check before any substantive work
```bash
git status --short --branch
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
# after deps installed:
SEED=42 bash scripts/check.sh   # or: make check
```
- If a stale `.verify_snapshot/` exists, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
- If `scripts/check.sh` reports golden mismatch, restore pinned artifacts before committing (`git checkout <pinned-commit> -- experiments/<file>` when HEAD itself is contaminated; see `AGENTS.md`).

### 2) If verification/reproduction is explicitly requested
Always use **`SEED=42`** and never leave a verification run half-finished.
```bash
make check            # fast guards (~seconds, offline)
make verify           # convention robustness only (reads JSONs, no writes)
make verify-quick     # ~8 min
make verify-extended  # ~21 min
make verify-full      # ~15 min
```
- `run_all_verification.py` overwrites and restores `experiments/*.json`; **never commit verification output** over goldens.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift (E041/E042 residual 1-ulp optimizer drift is known and must not be re-pinned).

### 3) If new research work is explicitly requested
- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**.
- Use `SEED=42`; preserve data/cache/baseline invariants (`QUANT_RESEARCH_OFFLINE=1` expectations, pinned inputs).
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts.
- Do not reopen closed findings (E049/E050) or treat E041/E042 residual optimizer drift as a re-pin target.

## Guardrails

- **Seed:** always `SEED=42`.
- **Goldens:** `experiments/*.json` are canonical; verification must not leave modified goldens.
- **Baselines:** never re-pin golden/data baselines as a side effect of verification.
- **Data:** add inputs only by committing files and re-pinning (`python3 scripts/check_data_coverage.py --update`).
- **Optimizer determinism:** validate solver answers on problem constraints, not solver exit status (ledger E049 / `tests/test_portfolio_opt.py`).
- **CI:** `.github/workflows/` verification gate cannot be created by automated agents (template: `.github/workflow-templates/verification-gate.yml`).
- **Commits:** do not commit unless explicitly requested; never commit secrets.

## Key references

- `AGENTS.md` — commands, verification modes, baseline/integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions and standing notes (E001–E051 complete)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `data/vintages.json`, `data/fundamentals_vintages.json` — pinned snapshots
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints

## Provenance

Durable handoff created at `handoff_2026-11-15T13-56-27Z_INITIAL_TASK.md`, mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`. Generic symlinks repointed via `scripts/repoint_handoff.py`. Prior `handoff_*` / `HANDOFF_*` files and timestamped aliases retained for continuity. No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff session.