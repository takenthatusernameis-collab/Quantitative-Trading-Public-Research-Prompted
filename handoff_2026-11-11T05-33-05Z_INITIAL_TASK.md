# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-11T05:33:05Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `ba98ec9c` (`chore(kilo): checkpoint agent session`) — `HEAD == origin/main`, in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Verified State (at handoff time)

- `git status --short --branch`: `## main...origin/main` (clean vs remote). Only unstaged change: `M src/__pycache__/cache_keys.cpython-312.pyc` — a compiled bytecode cache artifact. **Do not stage or commit** `__pycache__` / `*.pyc` files (gitignored anyway).
- `.verify_snapshot/`: **absent** — no interrupted or pending verification run to recover.
- **No substantive source changes this session.** Diff vs `12031fbb` (last handoff HEAD) is limited to handoff artifacts + symlink repointing.
- Research phase **complete (E001–E043)**. Authoritative dispositions/outcomes/history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative and must not be replaced by verification output: `experiments/*.json` (107 artifacts), `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration). E041/E042 residual 1-ulp / ill-conditioned QP drift (29–133 numeric diffs) is expected and **must not** be "fixed" by re-pinning artifacts.

## Initial Task for Next Session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or alter golden/data baselines without explicit direction.

**If asked to work, verify state first:**
1. `git status --short --branch` — confirm source state and `HEAD` vs `origin/main`; leave `__pycache__/*.pyc` unstaged.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and this handoff before making substantive changes.
4. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`).

**If asked to run verification:**
- Use `SEED=42`.
- **Never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run (`--restore-only`).
- If guards report a golden/baseline mismatch, restore/fix the cause — **do not re-pin** baselines to silence.

## Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # ~21 min
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens; never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction and justification.
- Do not reopen E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer/template path only per `AGENTS.md`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys; never introduce logging of secrets.

## Handoff Provenance

- **This durable artifact:** `handoff_2026-11-11T05-33-05Z_INITIAL_TASK.md` (root)
- **Supersedes (operationally):** `handoff_2026-11-11T05-30-23Z_INITIAL_TASK.md` and earlier handoffs; retained as history.
- **Discovery:** generic handoff pointers/symlinks repointed to this artifact at creation time via `scripts/repoint_handoff.py`.

(End of file - total 62 lines)