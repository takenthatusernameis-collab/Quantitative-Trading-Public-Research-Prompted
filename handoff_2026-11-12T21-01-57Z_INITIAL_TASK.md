# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T21:01:57Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a73a8068f193abaaec6a4eb0f2d6f2936ddb83ba` (`chore(kilo): checkpoint agent session`) — in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff creation)

- Working tree clean (`git status --short --branch` → `## main...origin/main`, 0 modifications / 0 untracked).
- No `.verify_snapshot/` pending (no interrupted verification run to recover).
- Baseline guards pass (run at handoff creation):
  - `python3 scripts/check_golden_baseline.py` → ALL 107 pinned golden artifacts match `ledger/golden_baseline.json`.
  - `python3 scripts/check_data_coverage.py` → ALL 35 pinned data inputs present, tracked and unchanged.
- Research phase complete (E001–E043). Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`; ranking: `ledger/PRIORITIZATION.md`. Canonical baselines: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- Closed / resolved — **do not reopen**: E049/E050 and residual E041/E042 ill-conditioned-QP drift (~1-ulp, ~1e-05). **Do not re-pin** E041/E042 artifacts to silence drift.
- Prior durable handoff: `handoff_2026-11-12T21-00-25Z_INITIAL_TASK.md`. This session's sole action is to create this handoff artifact and repoint generic canonical handoff pointers to it via `scripts/repoint_handoff.py`. No `experiments/`, `data/`, `src/`, `tests/`, ledgers, or baselines are modified by handoff creation.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes/sensitivity grids, or modify golden/baseline artifacts without explicit direction.

If work is requested, verify state first:
1. `git status --short --branch` — confirm HEAD/remote alignment and clean tree.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run guards before substantive changes/commits:
   - `SEED=42 bash scripts/check.sh` (or `make check`)
   - `python3 scripts/check_golden_baseline.py`
   - `python3 scripts/check_data_coverage.py`

## Reproduction / verification (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 scripts/check_golden_baseline.py      # 107 goldens vs ledger/golden_baseline.json
SEED=42 python3 scripts/check_data_coverage.py        # 35 pinned data inputs
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```
> Full checks/tests/verification require scientific deps (`pip install -r requirements.txt`: numpy, pandas, scipy, statsmodels, yfinance). Missing deps in a sandbox are environmental, not a repo defect.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit verification output over canonical goldens (`experiments/*.json`); restore after any interrupted run.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items; do not move pre-registered goalposts post-hoc.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit secrets/keys or log secrets.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-12T21-01-57Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-12T21-00-25Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained for history).
- Generic canonical handoff pointers repointed to this artifact via `scripts/repoint_handoff.py`. No `experiments/`, `data/`, `src/`, `tests/`, ledgers, or baselines modified by handoff creation.