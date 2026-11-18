# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-18T03:39:48Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `5af46cb5d26c3f431f3eab2bfca9acd2e16bd306` ("chore(kilo): checkpoint agent session"); in sync with `origin/main` (0 ahead / 0 behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. Ledger tail is at E479 (durable-handoff refresh at HEAD `263ab085`); no actionable open/pending/blocked research items.
- **Golden baseline:** 107 pinned `experiments/*.json` all match `ledger/golden_baseline.json` and HEAD (verified this session: `check_golden_baseline.py` → ALL 107 MATCH).
- **Verification snapshot:** `.verify_snapshot/` absent. `.verify_reports/` absent. No interrupted verification run pending.
- **Working tree at handoff:** only pre-existing tracked `__pycache__/*.pyc` modifications (`scripts/`, `src/`, `tests/`). No source, experiment, ledger, baseline, or data files changed by this handoff session. `git diff --name-only HEAD -- experiments/` is empty.
- **Canonical baselines/artifacts unchanged by this session:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Environment caveat (important)

- `python3` on this runner is **3.12.3** and **lacks the scientific stack** (`pandas`, `numpy`, `scipy`, `pyarrow`, `statsmodels`, `yfinance`). Running `scripts/check.sh` / `make check` will stop at the unittest steps with `ModuleNotFoundError: No module named 'pandas'` until dependencies are installed.
- **Fix for the next session:** `python3 -m pip install -r requirements.txt` before running the full gate. Non-pandas guards still run and pass individually (see below).

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files (including pre-existing `__pycache__` changes and this handoff artifact if uncommitted).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps: `python3 -m pip install -r requirements.txt` (required on this runner — scientific stack absent).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction + deliberate `--update` flow + ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action via GitHub UI).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.
- No separate linter configured; run `python3 -m py_compile` on changed Python files.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items (last research entry E051; handoff refreshes through E479)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-18T03-38-45Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and canonical pointers repointed via `python3 scripts/repoint_handoff.py`.
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts (retained for history). Note: the immediately-prior canonical pointers were **dangling** to `handoff_2026-11-18T03-37-20Z_INITIAL_TASK.md`, which was never written; this session repairs that by writing a fresh timestamped handoff and repointing.
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.

(End of file)