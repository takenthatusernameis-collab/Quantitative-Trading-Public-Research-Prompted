# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T13:27:41Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `e815af1b` ("chore(kilo): checkpoint agent session")
**Sync:** `main...origin/main` in sync at handoff time (0 ahead / 0 behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## TL;DR

Research phase is complete (E001–E051). Dispositions, validated survivors, and standing notes live in `ledger/RESEARCH_LEDGER.md`. **No open research task.** This session performed no research, verification, or canonical-baseline changes; it only inspected state, re-ran the offline guard scripts, and created this durable handoff.

## Observed state

- **Interrupted verification markers:** `.verify_snapshot/` and `.verify_reports/` absent (no pending restore).
- **Canonical artifacts/baselines unchanged:** `experiments/*.json` (107 tracked), `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/vintages.json` / `data/fundamentals_vintages.json`, and committed data snapshots.
- **Working tree (pre-existing/incidental, not modified intentionally):** tracked `__pycache__/*.pyc` bytecode drift only in `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/`. Treat as environment noise; do not commit casually.
- **Offline guard status (this session, per-step):** all **exit 0** —
  `scripts/check_json_artifacts.py` (114 JSON parse), `scripts/check_goldens_clean.py` (goldens match HEAD), `scripts/check_golden_baseline.py` (107 pinned goldens match), `scripts/check_data_coverage.py` (35 pinned inputs present/tracked/unchanged), `verify_convention_robustness.py`, `scripts/validate_template.py`, `scripts/check_experiment_imports.py`.
- **Dependency caveat:** `numpy`, `pandas`, and `pytest` are **not installed** in this sandbox. `scripts/check.sh` / unit tests that import them will fail here; run `pip install -r requirements.txt` (plus `pytest`) before full checks/verification.

## Clear initial task for next session

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, move goalposts, or modify canonical baselines/goldens without explicit direction.

### 1) Baseline/integrity check before substantive work
```bash
git status --short --branch
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
# After installing deps:
SEED=42 bash scripts/check.sh   # or: make check
```
If a stale `.verify_snapshot/` is present, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`). If `scripts/check.sh` reports golden mismatch, restore pinned artifacts before committing.

### 2) If verification/reproduction is explicitly requested
Always use **`SEED=42`**.
```bash
make check            # fast guards (~seconds, offline)
make verify           # convention robustness only (reads JSONs, no writes)
make verify-quick     # ~8 min
make verify-extended  # ~21 min
make verify-full      # ~15 min
```
- `run_all_verification.py` overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

### 3) If new research work is explicitly requested
- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**.
- Use `SEED=42`; preserve data/cache/baseline invariants (`QUANT_RESEARCH_OFFLINE=1` expectations, pinned inputs).
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts.
- Do not reopen closed E049/E050 or treat E041/E042 residual 1-ulp optimizer drift as a re-pin target.

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

Durable handoff created at `handoff_2026-11-15T13-27-41Z_INITIAL_TASK.md`. Prior `handoff_*` / `HANDOFF_*` files retained for history. No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff session.