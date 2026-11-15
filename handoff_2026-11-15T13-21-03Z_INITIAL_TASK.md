# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T13-21-03Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `ec74a903` ("chore(kilo): checkpoint agent session")
**Sync:** `main...origin/main` → `0 0` (in sync at handoff time)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## TL;DR — Repository state

Independent, reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. **Research phase complete (E001–E051).** Dispositions, surviving validated strategies, and standing notes are in `ledger/RESEARCH_LEDGER.md`. There is **no open research task**. This session performed no research or verification; it only inspected state and created this handoff.

## Observed state at handoff creation

- **HEAD:** `ec74a903` on `main`, in sync with `origin/main` (0 ahead / 0 behind).
- **Interrupted verification markers:** `.verify_snapshot/` and `.verify_reports/` **absent** (no pending restore).
- **Working tree:** tracked modifications are limited to incidental `__pycache__/*.pyc` bytecode drift in `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/` (13 files total). No source, experiment, data, ledger, or canonical baseline files were modified in this session. Treat `*.pyc` changes as environment noise; do not commit casually.
- **Canonical artifacts/baselines:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned data/vintages are unchanged in this session.
- **Environment note:** prior handoffs in this environment observed missing `numpy`/`pandas`/`pytest`, so full `scripts/check.sh` / verification suite may require `pip install -r requirements.txt` (and `pytest` for tests) before end-to-end runs.

## Clear initial task for the next session

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, move goalposts, or modify canonical baselines/goldens without explicit direction.

### 1) Baseline integrity check (before substantive work)
```bash
git status --short --branch
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
# If deps are installed:
SEED=42 bash scripts/check.sh   # or: make check
```
If a stale snapshot is present, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`).

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
- If interrupted: restore with `--restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift; re-pin only with explicit direction, deliberate update commands, and ledger justification.

### 3) If new research work is explicitly requested
- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**.
- Use `SEED=42`; preserve data/cache/baseline invariants (`QUANT_RESEARCH_OFFLINE=1` expectations, pinned inputs).
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts as appropriate.
- Do not reopen closed E049/E050 or treat E041/E042 residual 1-ulp drift as a re-pin target.

## Guardrails

- **Seed:** always `SEED=42`.
- **Goldens:** `experiments/*.json` are canonical; verification must not leave modified goldens in the tree.
- **Baselines:** never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of verification.
- **Data:** add inputs only by committing + re-pinning (`python3 scripts/check_data_coverage.py --update`).
- **Optimizer determinism:** validate solver answers on problem constraints, not solver exit status (ledger E049 / `tests/test_portfolio_opt.py`).
- **CI:** `.github/workflows/` verification gate cannot be created by automated agents (template: `.github/workflow-templates/verification-gate.yml`).
- **Commits:** do not commit unless explicitly requested; never commit secrets.

## Key references

- `AGENTS.md` — commands, verification modes, baseline/integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions and standing notes (research complete E001–E051)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `data/vintages.json`, `data/fundamentals_vintages.json` — pinned data snapshots
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints

## Provenance

- Durable handoff created for continuity at `handoff_2026-11-15T13-21-03Z_INITIAL_TASK.md`.
- Prior `handoff_*` / `HANDOFF_*` files retained for history.
- No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff session.
