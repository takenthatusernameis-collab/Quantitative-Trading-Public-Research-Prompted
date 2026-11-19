# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-19T01-46-52Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a9aeacf8` (in sync with `origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)

- **Research phase:** complete (E001–E043). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items indicated.
- **Verification snapshot:** `.verify_snapshot/` absent. `.verify_reports/` absent. No interrupted verification run to recover.
- **Working tree:** clean (`git status --short` empty); `experiments/` matches HEAD; HEAD == `origin/main` (`a9aeacf8`).
- **Canonical baselines/artifacts unchanged** by this handoff session.
- **Environment note (this runner):** bare `/usr/bin/python3` (3.12.3); core deps are NOT importable (`import numpy` → ModuleNotFoundError). Before running any verification: `python3 -m pip install -r requirements.txt`.

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `python3 -m pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`** (the suite sets `QUANT_RESEARCH_OFFLINE=1`; missing cache entries fail hard instead of downloading).
- Scopes (see `AGENTS.md`): `make check` (fast guards, ~seconds), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick, ~8 min), `--extended` (~21 min), `--full` (~15 min).
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift (E041/E042 still drift by 1-ulp optimizer sensitivity; this is an accepted, documented open item).

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Never commit `__pycache__/`, `.verify_snapshot/`, or `.verify_reports/`.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned SHA-256 fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-19T01-46-52Z_INITIAL_TASK.md` (repo root), also reachable via the generic `handoff_CURRENT.md` / `handoff_LATEST.md` / `initial_task.md` symlinks.
- This session created this durable handoff only. No code, experiments, baselines, or canonical artifacts were modified.
