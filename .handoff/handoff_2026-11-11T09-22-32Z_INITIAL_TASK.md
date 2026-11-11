# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-11T09:22:32Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `75820dc144c4db3ad2a896298e4a547d13d6566c` (in sync with origin/main at handoff time; re-verify)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Verified State (at handoff)

- `git status --short --branch`: only ` M src/__pycache__/cache_keys.cpython-312.pyc` present. **Do not stage or commit** `__pycache__/*.pyc`.
- `.verify_snapshot/`: **absent** (no pending restore).
- Research phase **complete (E001–E043)**. Authoritative outcomes/dispositions: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. Verification runs must not replace them.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration). E041/E042 residual 1-ulp/ill-conditioned QP drift (29–133 numeric diffs) is expected; do **not** "fix" by re-pinning artifacts.
- Sandbox probe scripts present at root (`_probe_branch.py`, `_probe_e041_drift.py`, `_probe_exactqp.py`, `_probe2_e042lead.py`, `_probe3_e042lead.py`) — scratch only, not part of the repo baseline.
- Prior handoff artifacts retained as history under `.handoff/`; this one supersedes `handoff_2026-11-11T09-21-23Z_INITIAL_TASK.md` and all earlier handoffs.

## Initial Task for Next Session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or alter golden/data baselines without explicit direction.

**If asked to work:**
1. `git status --short --branch` — confirm state/HEAD; leave `src/__pycache__/*.pyc` unstaged.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and this handoff before substantive changes.
4. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`).

**If asked to run verification:**
- Use `SEED=42`.
- Never commit driver output over `experiments/*.json`; restore after interruption (`--restore-only`).
- If guards report mismatch, restore/fix the cause — **do not re-pin** baselines to silence.

## Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver output over canonical goldens; never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction and justification.
- Do not reopen E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer/template path per `AGENTS.md`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys.

## Handoff Provenance

- **This artifact:** `.handoff/handoff_2026-11-11T09-22-32Z_INITIAL_TASK.md`
- **Supersedes (operationally):** `.handoff/handoff_2026-11-11T09-21-23Z_INITIAL_TASK.md` and earlier handoffs (retained as history).
- **Discovery pointers:** `handoff`, `handoff_CURRENT`, `LATEST`, `NEXT_SESSION` symlinks repointed to this artifact.

(End of file - total 58 lines)