# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-18T22-28-16Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `d8e61ea7fb06b03325c6c54689ab097f1460ef13` ("chore(kilo): checkpoint agent session", 2026-11-18T20:24:38Z)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)

- **Research phase:** complete. Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md` (research E001–E051; ledger entries continue through handoff-refresh E507, this handoff adds E508). No actionable open/pending/blocked research items indicated.
- **Verification snapshot:** `.verify_snapshot/` absent. `.verify_reports/` absent. No interrupted verification run to recover.
- **Working tree:** clean at start of session (`git status --short --branch` → `## main...origin/main`, no changes; `experiments/` matches HEAD).
- **Canonical baselines/artifacts unchanged** by this handoff session: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs.
- **Environment note (this runner):** bare `/usr/bin/python3` (3.12.3); core deps are **not** importable (`import pandas` → `ModuleNotFoundError`). Before running any verification, install deps: `python3 -m pip install -r requirements.txt`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and the E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `python3 -m pip install -r requirements.txt` (this runner has none installed).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`** (and `QUANT_RESEARCH_OFFLINE=1` is set by the suite; missing cache entries fail hard).
- Scopes (see `AGENTS.md`): `make check` (fast guards, ~seconds), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick, ~8 min), `--extended` (~21 min), `--full` (~15 min).
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate `--update` commands, and a ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Never commit `__pycache__/`, `.verify_snapshot/`, or `.verify_reports/`.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items (research E001–E051; refresh log through E508)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned SHA-256 fingerprints
- `experiments/*.json` — canonical research artifacts (138 tracked)
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-18T22-28-16Z_INITIAL_TASK.md` (repo root), mirrored byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Canonical pointers:** generic aliases (`HANDOFF.md`, `LATEST.md`, `HANDOFF_CURRENT.md`, `HANDOFF_LATEST.md`, `HANDOFF_NEXT_SESSION.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`, `handoff/CURRENT`, `.kilo/HANDOFF.md`, …) repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-18T22-28-16Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-18T21-23-32Z_INITIAL_TASK.md` (E507 refresh) and all prior `HANDOFF_*` / `handoff_*` artifacts, which are retained for history.
- This session created this durable handoff and appended ledger entry E508 only. No code, experiments, baselines, or canonical artifacts were modified.