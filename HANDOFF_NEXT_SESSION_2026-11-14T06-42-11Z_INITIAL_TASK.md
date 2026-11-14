# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T06:42:11Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `aab6e829930b4f5d126c7427bc7a0ae8aafb6d3d` ("chore(kilo): checkpoint agent session")
**Remote sync:** `origin/main` in sync with local `main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean of research/code/baseline changes at handoff creation. Only this new handoff artifact (and any pointer repoints performed for it) may be uncommitted.
- **`.verify_snapshot/` / `.verify_reports/`:** absent — no interrupted verification run pending.
- **Canonical artifacts/baselines:** `experiments/`, `data/`, `src/`, `scripts/`, `tests/` unchanged. `ledger/golden_baseline.json` and `ledger/data_baseline.json` intact.
- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and identify any uncommitted handoff/pointer state.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`):
  - `make check` / `SEED=42 bash scripts/check.sh` — fast guards (~seconds, offline)
  - `SEED=42 python3 verify_convention_robustness.py` — reads JSONs, no writes
  - `SEED=42 python3 run_all_verification.py` — quick (~8 min)
  - `SEED=42 python3 run_all_verification.py --extended` — quick + 18 committed drivers (~21 min)
  - `SEED=42 python3 run_all_verification.py --full` — E042 n_sim=50 + 96-config grid (~15 min)
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

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

- **Durable artifact (this session):** `HANDOFF_NEXT_SESSION_2026-11-14T06-42-11Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `HANDOFF_NEXT_SESSION_2026-11-14T06-41-04Z_INITIAL_TASK.md`, `HANDOFF_NEXT_SESSION_2026-11-14T06-40-30Z_INITIAL_TASK.md`, and earlier handoff artifacts (retained for history).
- This session created this durable handoff and repointed generic handoff pointers to it; no code, experiments, ledgers, or baselines were modified.