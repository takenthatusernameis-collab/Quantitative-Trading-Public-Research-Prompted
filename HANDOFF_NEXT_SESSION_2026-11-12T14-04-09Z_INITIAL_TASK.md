# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T14:04:09Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `cd90bd95` (`chore(kilo): checkpoint agent session`) — tracking `origin/main` (in sync, no divergence observed)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff time)

- **Working tree:** no source changes. The only modifications are tracked `__pycache__/*.pyc` bytecode/timestamp drift under `src/`, `scripts/`, and `tests/`. This is build noise: do not commit it, and do not let it contaminate a substantive commit. Handle it explicitly (restore/discard/commit) only with explicit direction.
- **`.verify_snapshot/`:** absent — no interrupted verification run pending, no recovery needed.
- **Ledgers/artifacts:** `ledger/`, `experiments/`, and `data/` show no modifications. Canonical baselines are intact: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Research phase:** complete (E001–E043). Authoritative dispositions and open items in `ledger/RESEARCH_LEDGER.md`; ranking in `ledger/PRIORITIZATION.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm HEAD/remote alignment; handle tracked `__pycache__` modifications explicitly.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** always use `SEED=42`; **never commit verification output** over `experiments/*.json`; restore goldens after any interrupted run. If guards report golden/baseline mismatch, fix or restore before committing — do not re-pin to silence it.

## Reproduction / verification commands (run only if explicitly requested)

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

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_NEXT_SESSION_2026-11-12T14-04-09Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-12T14-03-02Z_INITIAL_TASK.md`, `handoff_2026-11-12T14-02-07Z_INITIAL_TASK.md`, `HANDOFF-2026-11-12T13:11:49Z.md`, and all earlier timestamped handoffs (retained for history).
- This session created the handoff artifact and repointed the root convenience symlinks (`CURRENT`, `CURRENT.md`, `HANDOFF`) to it. No code, experiments, ledgers, baselines, or source files were modified.