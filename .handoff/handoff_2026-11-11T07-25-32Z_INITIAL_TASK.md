# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-11T07:25:32Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `0d4856e5` (`chore(kilo): checkpoint agent session`) — `HEAD == origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Verified State (at handoff time)

- `git status --short --branch`: `## main...origin/main` (no source diffs vs remote). Unstaged bytecode only: `M scripts/__pycache__/*.cpython-312.pyc`, `M src/__pycache__/*.cpython-312.pyc`, `M tests/__pycache__/*.cpython-312.pyc` (12 files). **Do not stage or commit `__pycache__` artifacts.**
- `.verify_snapshot/`: **absent**. `.verify_reports/`: **absent**.
- Research phase **complete (E001–E043)**. Authoritative dispositions/outcomes: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative and must not be replaced by verification output: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration). Residual E041/E042 1-ulp/ill-conditioned QP numeric drift (29–133 diffs, within known bounds) is expected; **do not "fix" by re-pinning artifacts**.

## Initial Task for Next Session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or alter golden/data baselines without explicit direction.

**If asked to work:**
1. `git status --short --branch` — confirm source state and HEAD vs `origin/main`; leave `__pycache__/*.pyc` unstaged.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and this handoff before making substantive changes.
4. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`) and address failures without re-pinning baselines unless explicitly instructed.

**If asked to run verification:**
- Always use `SEED=42`.
- **Never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run (`--restore-only`).
- If guards report mismatch, restore/fix the cause — **do not re-pin** `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence.

## Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # ~21 min
SEED=42 python3 run_all_verification.py --full        # ~15 min
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails

- Use **SEED=42** for all reproducibility/verification runs.
- Never commit driver output over canonical goldens; never re-pin baselines without explicit re-baseline instruction and justification in the diff/ledger.
- Do not reopen E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer/template path only; see `AGENTS.md` / `VERIFICATION_GATE_TEMPLATE.md`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or experiment outcomes without explicit justification and ledger update.
- Never commit secrets/keys.

## Handoff Provenance

- **This durable artifact:** `handoff_2026-11-11T07-25-32Z_INITIAL_TASK.md` (root) and `.handoff/handoff_2026-11-11T07-25-32Z_INITIAL_TASK.md` (archive copy)
- **Supersedes (operationally):** `handoff_2026-11-11T07-24-11Z_INITIAL_TASK.md` and earlier handoffs; retained as history.
- **Discovery:** generic `handoff_*` / `next_*` / `initial_task*` pointers updated to this artifact via `scripts/repoint_handoff.py`.

(End of file)