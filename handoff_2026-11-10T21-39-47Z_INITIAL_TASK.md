# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T21:39:47Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `839632a6` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Verified State (this session)

- `git status --short --branch`: `## main...origin/main` — only ` M src/__pycache__/cache_keys.cpython-312.pyc` (unstaged bytecode artifact; **do not commit**).
- `.verify_snapshot/`: **absent** (no interrupted verification run; nothing to restore).
- Research phase **complete (E001–E043)**. Authoritative dispositions/outcomes: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative and must not be modified by routine verification:
  - `experiments/*.json` (golden artifacts)
  - `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration). E041/E042 residual 1-ulp/ill-conditioned QP drift (29–133 numeric diffs) is expected; **never re-pin** E041/E042 artifacts to silence it.
- Ledger research entries end at **E051 (Post-Closure Conformance Pass, 2026-11-02)**. Later entries are durable-handoff refreshes only (no new research, no gate/pre-registration/falsification/sensitivity-grid changes, no golden re-pinning). No OPEN/PENDING/BLOCKED/TODO markers.

## Delta vs Prior Handoff

- Previous durable handoff: `handoff_2026-11-10T21-38-44Z_INITIAL_TASK.md` (HEAD `437b2cca`).
- HEAD advanced by one checkpoint commit (`839632a6`) since prior handoff; no substantive source/data/experiment/ledger changes identified. This is a timestamped handoff refresh to provide a clear entry point for the next session.

## Initial Task for Next Session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or alter golden/data baselines without explicit direction.

**If asked to work:**
1. `git status --short --branch` — confirm clean source and HEAD vs `origin/main`; leave `__pycache__/*.pyc` unstaged.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and this handoff before making substantive changes.
4. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`).

**If asked to run verification:** use `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report mismatch, restore/fix — do not re-pin to silence.

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
- Never commit driver output over canonical goldens; never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction.
- Do not reopen E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer/template path only).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys.

## Provenance

- **This handoff:** `handoff_2026-11-10T21-39-47Z_INITIAL_TASK.md`
- **Previous:** `handoff_2026-11-10T21-38-44Z_INITIAL_TASK.md`
- **Latest pointer:** `handoff_next_session_latest.md` (this content)

(End of file - total 63 lines)