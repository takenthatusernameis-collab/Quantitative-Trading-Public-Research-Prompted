# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T06:34:38Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `092de2cb` ("chore(kilo): checkpoint agent session"), in sync with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean (`git status --short --branch` → `## main...origin/main`, no unstaged/untracked changes). HEAD advanced from `913fccb3` to `092de2cb` via a checkpoint commit; no research delta.
- **Prior operational handoff:** `handoff_2026-11-14T06-33-43Z_INITIAL_TASK.md` (generic symlinks previously pointed to it). No research delta introduced by this handoff session.
- **`.verify_snapshot/` / `.verify_reports/`:** absent — no interrupted verification run pending.
- **Canonical artifacts/baselines:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` intact; `experiments/*.json` treated as canonical committed goldens (verify before commit if any doubt).
- **Research phase:** complete (E001–E051). Surviving validated strategies/dispositions are documented in `ledger/RESEARCH_LEDGER.md`. Entries after E051 are handoff/bookkeeping refreshes only. No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` research items.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and understand any local/uncommitted handoff artifacts.
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

- **Durable artifact (this session):** `handoff_2026-11-14T06-34-38Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/2026-11-14T06-34-38Z_INITIAL_TASK.md` and `.kilo/handoff/2026-11-14T06-34-38Z_INITIAL_TASK.md`.
- **Operational pointers:** generic handoff symlinks repointed with `python3 scripts/repoint_handoff.py handoff_2026-11-14T06-34-38Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-14T06-33-43Z_INITIAL_TASK.md` and all earlier handoff artifacts/symlinks (retained for history).
- This session created the durable handoff and repointed generic aliases only; no research code, experiments, ledgers, or baseline artifacts were modified.

(End of file - total 70 lines)