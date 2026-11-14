# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T02:35:25Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `11e34fcac2b6cefe256c7da352b5a9e99bbf5a38` ("chore(kilo): checkpoint agent session"), in sync with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** `git status --short --branch` → `## main...origin/main` (clean). No unstaged/untracked changes observed. Delta vs prior durable-handoff HEAD `bc057bccb4654005473edafaa0719cdbac9d17c3` (`git diff --name-only bc057bcc..11e34fc`) is limited to generic handoff pointer repoints under `.handoff/`, `.kilo/`, `handoff/`, `HANDOFFS/` (bookkeeping only). No research/source/data/experiment/baseline substance changed.
- **`.verify_snapshot/` / `.verify_reports/`:** absent — no interrupted verification run pending.
- **Canonical artifacts/baselines:** `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `ledger/` unchanged by this handoff refresh. `ledger/golden_baseline.json` and `ledger/data_baseline.json` remain intact.
- **Research phase:** complete (E001–E051). Surviving validated strategies and dispositions: `ledger/RESEARCH_LEDGER.md`. Last research entry is **E051**; subsequent entries (E052–E267+) are durable-handoff refreshes/bookkeeping only. No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` items.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment; handle any tracked `__pycache__` modifications explicitly if present.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change. Install deps if needed: `pip install -r requirements.txt`.

### If verification / reproduction is requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` / `SEED=42 bash scripts/check.sh` (fast guards, ~seconds), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick ~8m), `--extended` (~21m), `--full` (~15m), `--skip-slow`, `--restore-only`.
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
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items (last research entry E051; subsequent entries are handoff refreshes)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-14T02-35-25Z_INITIAL_TASK.md` (repo root).
- **Mirrors:** `handoff/2026-11-14T02-35-25Z_INITIAL_TASK.md`, `.kilo/handoff/2026-11-14T02-35-25Z_INITIAL_TASK.md`.
- **Operational pointers:** repoint generic handoff symlinks with `python3 scripts/repoint_handoff.py handoff_2026-11-14T02-35-25Z_INITIAL_TASK.md`.
- **Supersedes operationally:** prior durable handoffs and generic pointers (retained for history), including `handoff_2026-11-14T02-34-17Z_INITIAL_TASK.md`.
- This session verified state only (timestamp, HEAD/sync, delta vs prior durable-handoff HEAD, `.verify_snapshot` absence); no code, experiments, ledgers, baselines, or source files were modified.
