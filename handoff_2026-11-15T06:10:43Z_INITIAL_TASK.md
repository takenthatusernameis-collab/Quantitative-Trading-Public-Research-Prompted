# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T06:10:43Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `6f4151c23a8b5f5bce4edb360146cad3d7e37bf6` ("chore(kilo): checkpoint agent session", 2026-11-15 06:10:xx +0000); `origin/main...HEAD` = `0 0` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research item.
- **Delta since prior durable handoff (`handoff_2026-11-15T05:21:37Z_INITIAL_TASK.md`, HEAD `1bda7101` → `6f4151c2`):** 2 checkpoint commits; `git diff --name-only 1bda7101..6f4151c2` filtered for research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `ledger/`, `research_state/`, excl `__pycache__`/`*.pyc`) → **0 paths**. Only generic handoff-symlink repoints (2 lines each) and this new timestamped handoff artifact changed. No research substance changed.
- **Baseline integrity:** assumed still clean from prior session (`SEED=42 bash scripts/check.sh` → exit 0, "=== All checks passed ===" at `1bda7101`). Re-run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change. No verification run performed this session; no interrupted run pending. `.verify_snapshot/` absent at handoff time.
- **Working tree:** tracked `__pycache__/*.pyc` files show as modified (build noise; do not commit). Only intended changes are this handoff + symlink repoints.
- **Closed — do not reopen:** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## INITIAL TASK for the next session (clear)

**Default: await explicit user instructions.** Do not invent new experiments, run long verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment; treat `__pycache__/*.pyc` churn as non-canonical noise.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip3 install -r requirements.txt` (or `pip3 install --break-system-packages -r requirements.txt` in this environment).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` (fast guards); `SEED=42 python3 verify_convention_robustness.py` (read-only); `SEED=42 python3 run_all_verification.py` (quick, ~8 min); `--extended` (~21 min); `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Use **`SEED=42`** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin baselines without explicit, intentional instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `run_all_verification.py`, `scripts/check.sh`, `scripts/repoint_handoff.py`.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-15T06:10:43Z_INITIAL_TASK.md`
- **Supersedes operationally:** `handoff_2026-11-15T05:21:37Z_INITIAL_TASK.md` (retained for history)
- This session created this durable handoff only; no code, experiments, ledgers, baselines, or canonical artifacts were modified.
