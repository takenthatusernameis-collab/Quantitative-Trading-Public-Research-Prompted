# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T06:11:41Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `7e137a2ad9551196f50b527568f97f7c5fc54d6f` ("chore(kilo): checkpoint agent session"); `origin/main...HEAD` in sync at handoff capture.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research item.
- **Delta since prior durable handoff (`handoff_2026-11-15T06:10:43Z_INITIAL_TASK.md`, HEAD `6f4151c2` → `7e137a2a`):** checkpoint commit(s) only; `git diff --name-only 6f4151c2..7e137a2a` filtered for research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `ledger/`, `research_state/`, excl `__pycache__`/`*.pyc`) → **0 paths**. Only prior handoff/symlink housekeeping expected; no research substance changed.
- **Baseline integrity:** not re-verified this session. Prior durable state reported `SEED=42 bash scripts/check.sh` clean at `1bda7101`; run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change. No verification run performed this session; no interrupted run pending. `.verify_snapshot/` absent at handoff time.
- **Working tree:** tracked `__pycache__/*.pyc` may appear modified (build noise; do not commit). Intended changes are this handoff + canonical symlink repoints.
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

- **Durable artifact (this session):** `handoff_2026-11-15T06:11:41Z_INITIAL_TASK.md`
- **Supersedes operationally:** `handoff_2026-11-15T06:10:43Z_INITIAL_TASK.md` (retained for history)
- This session created this durable handoff and repointed generic canonical symlinks; no code, experiments, ledgers, baselines, or canonical research artifacts were modified.
