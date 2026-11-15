# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T08:08:54Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `5d439b9d4b1b17cf58046c0c4ebd2021ca77c818` (`chore(kilo): checkpoint agent session`)
**Sync:** local `main` == `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## INITIAL TASK for the next session

**Default: await explicit user instructions.**

Do **not** invent new experiments, run long verification unprompted, change
pre-registered gates/outcomes, or modify golden/baseline artifacts without
explicit direction. The research phase is closed and the baseline is clean.

### Before substantive work
1. `git status --short --branch` — confirm HEAD/remote alignment. The only
   tracked modifications expected are `__pycache__/*.pyc` (build noise; never
   commit them). Everything else should be handoff artifacts/symlinks.
2. Confirm `.verify_snapshot/` is absent (it is absent at this handoff). If an
   interrupted verification run is ever pending, recover first:
   `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout -- experiments/` **only** if HEAD is known-good per
   `ledger/golden_baseline.json`).
3. Runtime deps are **not installed in this sandbox** (`pandas` and `numpy`
   are missing; `numpy`/`scipy`/`statsmodels` are in `requirements.txt`).
   Install before any numerical work:
   `pip3 install -r requirements.txt` (add `--break-system-packages` if needed).
4. Before committing any substantive change: `SEED=42 bash scripts/check.sh`
   (or `make check`).

### If verification or reproduction is explicitly requested
- Always use `SEED=42`.
- Scopes: `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py`
  (read-only), `SEED=42 python3 run_all_verification.py` (quick, ~8 min),
  `--extended` (~21 min), `--full`.
- Verification overwrites and restores `experiments/*.json`; never leave a run
  half-finished and never commit verification output over goldens.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json`
  to silence drift. Re-pin only with explicit direction, the deliberate update
  command, and ledger justification.

---

## Current state (snapshot)

- **Research phase:** complete. Authoritative dispositions, surviving validated
  strategies, and open/closed items: `ledger/RESEARCH_LEDGER.md` (research
  record E001–E051; E052+ are durable-handoff refreshes). No actionable
  OPEN / PENDING / BLOCKED / TODO item.
- **Canonical baseline:** 107 tracked `experiments/*.json` artifacts pinned in
  `ledger/golden_baseline.json`; 35 data inputs pinned in
  `ledger/data_baseline.json`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism and exact KKT
  enumeration) and residual E041/E042 ill-conditioned-QP drift (~1-ulp,
  ~1e-05). Do not re-pin artifacts solely to silence that drift.
- **Working tree at handoff:** tracked `__pycache__/*.pyc` modifications only
  (build noise) plus this handoff deliverable and repointed generic pointers.
  No canonical research artifact modified.
- **CI note:** `.github/workflows/` verification gate cannot be created by
  automated agents; template at `.github/workflow-templates/verification-gate.yml`
  (see `VERIFICATION_GATE_TEMPLATE.md`).

## Guard status verified this session (2026-11-15T08:08:54Z)

Run with `SEED=42`:

| Step | Result |
|---|---|
| `scripts/check_json_artifacts.py` | exit 0 — 114 artifacts parse |
| `scripts/check_goldens_clean.py` | exit 0 — goldens match HEAD |
| `scripts/check_golden_baseline.py` | exit 0 — 107 pinned goldens match |
| `scripts/check_data_coverage.py` | exit 0 — 35 pinned data inputs present/tracked/unchanged |
| `verify_convention_robustness.py` | exit 0 |
| `scripts/validate_template.py` | exit 0 |
| `scripts/check_experiment_imports.py` | exit 0 |

`SEED=42 bash scripts/check.sh` exits **1 in this sandbox for environment
reasons only**: `tests.test_data_coverage` errors with
`ModuleNotFoundError: No module named 'pandas'` (3 errors) and `numpy` is also
absent. Every `FAIL …` line printed during the suite (`experiments/d.json`,
`d2.json`, `b.json`, `x.json`, `e2.json`, `badlist.json`, `data/panel.parquet`,
`nope.json`, `pid 999999`, `experiments/e001.json`) is a deliberate negative
fixture written to a temp dir by the guard self-tests — **none of those paths
exist in the repo or in HEAD**. `data/panel.parquet` is not in
`ledger/data_baseline.json` and not referenced by any driver. With
`requirements.txt` installed, `make check` is expected to pass end-to-end.

## Guardrails

- Use `SEED=42` for reproducibility and verification.
- Never commit driver verification output over canonical goldens in `experiments/`.
- Never re-pin baselines without explicit instruction and ledger justification.
- Do not change pre-registered gates, sensitivity grids, falsification
  expectations, or outcomes without explicit justification and a ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md`, `ledger/PRIORITIZATION.md` — dispositions and procedure.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `run_all_verification.py`, `scripts/check.sh`, `scripts/repoint_handoff.py`.
- Prior durable handoff (retained): `handoff_2026-11-15T08-06-33Z_INITIAL_TASK.md`.

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T08-08-54Z_INITIAL_TASK.md` (root),
  mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`,
  `.kilo/handoff/`.
- **Generic pointers repointed** via `scripts/repoint_handoff.py` to this artifact.
- This session created this durable handoff and repointed generic pointers only;
  no code, experiments, ledgers, baselines, or canonical research artifacts were
  modified.