# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-11T05:26:24Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `13e9bad1` (`chore(kilo): checkpoint agent session`) — `HEAD == origin/main` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, or change gates/outcomes/baselines without explicit direction.

**Before starting any assigned work:**
1. `git status --short --branch` — confirm source state. At handoff time tracked source was clean except an unstaged bytecode artifact: ` M src/__pycache__/cache_keys.cpython-312.pyc` (**do not stage or commit `__pycache__`**).
2. Confirm `.verify_snapshot/` is absent. If present/stale, recover before other work: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`).
3. `board_read` for peer-coordinated work items when relevant.
4. Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and this handoff before substantive changes.

**If asked to run verification:**
- Use `SEED=42`. Never commit verification output over `experiments/*.json`.
- Restore goldens after any interrupted run (`--restore-only`). If guards report mismatch, fix the cause — **do not re-pin** `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence failures.
- Modes: `scripts/check.sh` / `make check` (~seconds), `run_all_verification.py` quick (~8m), `--extended` (~21m), `--full` (~15m).

**If asked to change code/artifacts:**
- Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes; `python3 -m py_compile` on changed Python files.
- Never commit secrets/keys. Never commit unless explicitly asked.

## Verified state (at handoff time)

- `git status --short --branch`: `## main...origin/main`; tracked worktree clean except ` M src/__pycache__/cache_keys.cpython-312.pyc`.
- `.verify_snapshot/`: absent (no interrupted/pending verification restore).
- Baseline guards (re-run at handoff): `scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**; `scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**.
- No substantive code, experiment, data, or baseline changes made in this handoff session.
- **Research phase complete (E001–E043).** Authoritative dispositions/outcomes: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration). E041/E042 residual 1-ulp/ill-conditioned QP drift (29–133 numeric diffs) is expected and **must not** be "fixed" by re-pinning artifacts.
- CI/workflow gate: template only (`.github/workflow-templates/verification-gate.yml`, `VERIFICATION_GATE_TEMPLATE.md`); do not create `.github/workflows/` as an automated agent.

## Key commands (only if explicitly requested)

```bash
git status --short --branch
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # extended
SEED=42 python3 run_all_verification.py --full        # full
SEED=42 python3 run_all_verification.py --restore-only
```

## Provenance

- **This durable artifact:** `handoff_2026-11-11T05-26-24Z_INITIAL_TASK.md`
- **Supersedes (operationally):** `handoff_2026-11-11T05-25-12Z_INITIAL_TASK.md` (HEAD `13e9bad1`) and earlier timestamped handoffs (retained as history).
