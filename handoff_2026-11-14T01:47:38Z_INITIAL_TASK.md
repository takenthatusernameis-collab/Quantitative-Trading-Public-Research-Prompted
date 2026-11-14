# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T01:47:38Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `3117669d` ("chore(kilo): checkpoint agent session") — verify against `origin/main` at session start
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (at handoff creation)

- **Project:** Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase:** Complete (E001–E051). Surviving validated strategies and dispositions: `ledger/RESEARCH_LEDGER.md`. Last research entry is **E051**; subsequent entries are durable-handoff refreshes only (E052–E263). No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` items.
- **Canonical artifacts:** `experiments/*.json` are the authoritative golden results (pinned in `ledger/golden_baseline.json`); pinned data inputs tracked in `ledger/data_baseline.json`.
- **Closed/resolved (do not reopen):** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Verification state:** No `.verify_snapshot/` or `.verify_reports/` present at clean handoff (confirmed absent). If present, treat as interrupted/stale until recovered.

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent experiments, run long verification unprompted, change gates/outcomes, or modify/re-pin golden or baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and working tree cleanliness (transient `__pycache__` diffs only are acceptable).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes. If dependencies are missing, install `pip install -r requirements.txt`.

### If verification / reproduction is requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` / `SEED=42 bash scripts/check.sh` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick ~8m), `--extended` (~21m), `--full` (~15m).
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before committing.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- **Reproducibility:** `SEED=42`; respect pinned data vintages/caches and `QUANT_RESEARCH_OFFLINE=1` under the suite.
- **Baselines/goldens:** the committed golden is authoritative; never replace/re-pin as a side effect of verification.
- **Discipline:** pre-registration and goalposts unchanged; sensitivity grids reported not gated; record negative results honestly.
- **Closed items:** do not reopen E049/E050 or E041/E042 drift.
- **CI:** do not create `.github/workflows/` as an automated agent (template: `.github/workflow-templates/verification-gate.yml`).
- **Security:** never commit/log secrets or keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-14T01:47:38Z_INITIAL_TASK.md` (this file).
- **Operational pointers:** generic handoff symlinks repointed to this artifact with `python3 scripts/repoint_handoff.py handoff_2026-11-14T01:47:38Z_INITIAL_TASK.md` (found 553, repointed 553, checked 553, bad 0).
- **Supersedes operationally:** `handoff_2026-11-14T01:41-36Z_INITIAL_TASK.md` and earlier handoff artifacts/symlinks (retained for history).