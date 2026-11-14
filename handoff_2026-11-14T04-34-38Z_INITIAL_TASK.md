# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T04:34:38Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `dff2ac35` ("chore(kilo): checkpoint agent session"), in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean (`git status --short --branch` → `## main...origin/main`, no unstaged/untracked changes) vs HEAD `dff2ac35`. Delta vs prior durable handoff HEAD `c6429e64` is the single checkpoint commit `dff2ac35` plus generic handoff symlink repoints under `.handoff/`, `.kilo/`, and the repo root. Treat symlink repoints as bookkeeping; do not commit substantive changes without explicit direction.
- **`.verify_snapshot/` / `.verify_reports/`:** absent — no interrupted verification run pending.
- **Canonical artifacts/baselines:** `experiments/`, `data/`, `src/`, `scripts/`, `tests/` show no modifications vs `c6429e64`. `ledger/golden_baseline.json` and `ledger/data_baseline.json` intact.
- **Research phase:** complete (E001–E051). Surviving validated strategies and dispositions: `ledger/RESEARCH_LEDGER.md`. Last research entry is **E051**; subsequent entries (E052+) are durable-handoff refreshes/bookkeeping only. No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` items.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment; handle any tracked `__pycache__` modifications explicitly.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change. Install deps if needed: `pip install -r requirements.txt`.

### If verification / reproduction is requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` / `SEED=42 bash scripts/check.sh` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick ~8m), `--extended` (~21m), `--full` (~15m).
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Reproduction / verification commands (run only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

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
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items (last research entry E051)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-14T04-34-38Z_INITIAL_TASK.md` (repo root).
- **Operational pointers:** repoint generic handoff symlinks with `python3 scripts/repoint_handoff.py handoff_2026-11-14T04-34-38Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-14T04-34-04Z_INITIAL_TASK.md` and all earlier handoff artifacts/symlinks (retained for history).
- This session verified state only (timestamp, HEAD/sync, delta vs prior handoff HEAD `c6429e64`→`dff2ac35`, `.verify_snapshot`/`.verify_reports` absence); no code, experiments, ledgers, baselines, or source files were modified.
