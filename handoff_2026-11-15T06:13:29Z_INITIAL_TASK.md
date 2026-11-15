# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T06:13:29Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `991e3534` (`chore(kilo): checkpoint agent session`); `origin/main...HEAD` in sync (0 0).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open, pending, or blocked research item.
- **Delta since prior durable handoff** (`handoff_2026-11-15T06:13:09Z_INITIAL_TASK.md`, HEAD `722c6694` → `991e3534`): `git diff --name-only 722c6694..991e3534` filtered for research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `ledger/`, `research_state/`, excl `__pycache__`/`*.pyc`/`handoff`/`*.md`) → **0 paths**. Only checkpoint commit + canonical symlink/handoff housekeeping. No research substance changed.
- **Baseline integrity:** prior session verified `SEED=42 bash scripts/check.sh` → `=== All checks passed ===` (107 pinned goldens match HEAD + `ledger/golden_baseline.json`; 35 pinned data inputs present, tracked, unchanged). Not re-verified this session; re-run before committing any substantive change.
- **Canonical artifacts:** `git status` shows no modifications to `experiments/`, `data/`, `ledger/`, source, scripts, or tests. No verification run is active; `.verify_snapshot/` is absent (confirmed via `ls -d .verify_snapshot`).
- **Working tree:** only tracked `__pycache__/*.pyc` files are modified (generated build noise). Do not commit.
- **Closed — do not reopen:** E049/E050 (optimizer determinism and exact KKT enumeration) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do not re-pin artifacts solely to silence that drift.

## INITIAL TASK for the next session

**Default: await explicit user instructions.** Do not invent experiments, run long verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before substantive work

1. Run `git status --short --branch` and confirm HEAD/remote alignment; ignore `__pycache__/*.pyc` churn.
2. Confirm `.verify_snapshot/` is absent. If an interrupted run is pending, run `SEED=42 python3 run_all_verification.py --restore-only` before any other work.
3. If dependencies are needed, use `pip3 install -r requirements.txt` (or `pip3 install --break-system-packages -r requirements.txt` in this environment).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing a substantive change.

### If verification or reproduction is explicitly requested

- Always use `SEED=42`.
- Scopes: `make check` (fast guards); `SEED=42 python3 verify_convention_robustness.py` (read-only); `SEED=42 python3 run_all_verification.py` (quick, ~8 min); `--extended` (~21 min); `--full`.
- Verification overwrites and restores `experiments/*.json`; never leave a run half-finished and never commit verification output over goldens. If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, the deliberate update command, and ledger justification.

## Guardrails

- Use `SEED=42` for reproducibility and verification runs.
- Never commit driver verification output over canonical goldens in `experiments/`.
- Never re-pin baselines without explicit instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent; the copyable template is `.github/workflow-templates/verification-gate.yml` and a maintainer must create the actual workflow.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `run_all_verification.py`, `scripts/check.sh`, `scripts/repoint_handoff.py`.

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T06:13:29Z_INITIAL_TASK.md`
- **Supersedes operationally:** `handoff_2026-11-15T06:13:09Z_INITIAL_TASK.md` (retained for history)
- This session created this durable handoff only; no code, experiments, ledgers, baselines, or canonical research artifacts were modified.