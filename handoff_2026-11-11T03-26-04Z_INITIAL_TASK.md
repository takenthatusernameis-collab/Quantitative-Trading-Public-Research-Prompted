# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-11T03:26:04Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `96116509c82ddeb3d7e929a7d5504ceeb68722c7` (`chore(kilo): checkpoint agent session`, 2026-11-11 03:25:56 +0000) — `origin/main` is at the identical SHA (in sync).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Verified State (at handoff time)

- `git status --short --branch`: `## main...origin/main` — clean source; no staged or unstaged source changes. `src/__pycache__/cache_keys.cpython-312.pyc` may appear modified locally (unstaged bytecode); **do not stage/commit** `__pycache__` artifacts.
- `.verify_snapshot/`: **absent** — no interrupted verification run pending restore.
- Research phase **complete (E001–E043)**. Authoritative dispositions/outcomes: `ledger/RESEARCH_LEDGER.md` (research entries through **E051**, Post-Closure Conformance Pass 2026-11-02; E052+ are durable-handoff refreshes only). No OPEN/PENDING/BLOCKED/TODO markers.
- Baseline guards re-run this session: `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**.
- Canonical baselines are authoritative and must not be modified by routine verification: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration). E041/E042 residual 1-ulp/ill-conditioned QP drift (29–133 numeric diffs) is expected and **must not** be "fixed" by re-pinning artifacts.
- Data/vintage notes (per `AGENTS.md`): pinned 2026-10-12 and 2026-10-11 vintages committed; E029 fundamentals pinned in `data/fundamentals/`; cache coverage enforced via `ledger/data_baseline.json` (`QUANT_RESEARCH_OFFLINE=1` during suite).

## Delta vs Prior Handoff

- Previous durable handoff: `handoff_2026-11-11T01-39-40Z_INITIAL_TASK.md` (HEAD `1bcbbca6`, in sync with origin).
- HEAD advanced `1bcbbca6` → `96116509` via checkpoint commits touching only handoff/session artifacts; no research artifacts, baselines, source, tests, scripts, or ledger substance changed. Prior closed/conformance state adopted.
- This handoff supersedes prior timestamped handoffs for next-session bootstrapping.

## Initial Task for Next Session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or alter golden/data baselines without explicit direction.

**If asked to work:**
1. `git status --short --branch` — confirm clean source and HEAD vs `origin/main`; leave `__pycache__/*.pyc` unstaged.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and this handoff before making substantive changes.
4. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`).

**If asked to run verification:**
- Use `SEED=42`.
- **Never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run.
- If guards report mismatch, restore/fix the cause — **do not re-pin** baselines to silence.

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

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver output over canonical goldens; never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction and justification.
- Do not reopen E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer/template path only per `AGENTS.md`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys.

## Provenance

- **This handoff:** `handoff_2026-11-11T03-26-04Z_INITIAL_TASK.md`
- **Previous:** `handoff_2026-11-11T01-39-40Z_INITIAL_TASK.md`