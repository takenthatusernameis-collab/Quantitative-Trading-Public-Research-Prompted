# Agentic Handoff — Initial Task

**Created:** 2026-11-12T15:05:56Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** `92c230a2` (main = origin/main, in sync)

## Verified state (checked 2026-11-12T15:05:56Z)

- Research phase complete (E001–E043). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- `.verify_snapshot/` absent — no interrupted verification run to recover.
- `git status --short` shows only `__pycache__/*.pyc` bytecode drift (src/, scripts/, tests/). This is build noise, not canonical source change. Do not commit it.
- No source, experiment, ledger, script, test, or baseline changes made in this session beyond this handoff file.

## Initial task for next session

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**

1. `git status --short --branch` — confirm clean source state and `HEAD`/remote alignment.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 (optimizer determinism + exact KKT enumeration) or E041/E042 residual ill-conditioned QP drift items. Do not re-pin E041/E042 artifacts to silence drift.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never introduce logging of secrets.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-12T15-05-56Z_INITIAL_TASK.md` (+ `.kilo/handoff_2026-11-12T15-05-56Z_INITIAL_TASK.md` mirror).
- Supersedes earlier timestamped handoffs (retained as history).
- Convenience symlinks `CURRENT`, `HANDOFF`, `LATEST`, `INITIAL_TASK`, `NEXT_SESSION` point to this file.

## References

- `AGENTS.md` — commands, reproducibility, baseline integrity rules.
- `ledger/RESEARCH_LEDGER.md` — E001–E169 records/dispositions.
- `ledger/PRIORITIZATION.md` — ranking criteria and procedure.
