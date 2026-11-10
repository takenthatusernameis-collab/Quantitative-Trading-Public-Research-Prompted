# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T23:32:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `9e2e5ce99600281520bd9585127818279b6eab3a` (2026-11-10 23:31:43 +0000) "chore(kilo): checkpoint agent session" — `origin/main` in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` — clean tracked working tree; only unstaged bytecode ` M src/__pycache__/cache_keys.cpython-312.pyc` (pre-existing, not committed).
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Research phase **complete (E001–E043)**. Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`. Last *research* entry is E051 (2026-11-02 conformance pass); E052–E140 are durable-handoff refreshes only. No `OPEN`/`PENDING`/`BLOCKED`/`TODO` markers.
- Canonical baselines are authoritative: `experiments/*.json` (138 tracked artifacts matching HEAD), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity, 29–133 numeric diffs). **Do not re-pin** E041/E042 artifacts to silence drift.
- Baseline guards re-run this session: `scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**; `scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**.
- Known note: some pinned data (e.g. `data/panel.parquet`) is gitignored and may be absent in a fresh tree; verification enforces `QUANT_RESEARCH_OFFLINE=1` so a missing pinned cache fails hard rather than re-downloading.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean source state and HEAD/remote alignment.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction; re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear explicitly in the diff.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer action; template: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys or log secrets. Do not stage/commit `src/__pycache__/*.pyc`.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T23-32-37Z_INITIAL_TASK.md` (mode 0600).
- **Canonical pointers repointed** to this artifact via `scripts/repoint_handoff.py` (NEW constant updated to `handoff_2026-11-10T23-32-37Z_INITIAL_TASK.md`); all generic stable-alias pointers across root, `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` now resolve here. Historical timestamped-named pointers left untouched.
- **Supersedes (operationally):** `handoff_2026-11-10T22-30-09Z_INITIAL_TASK.md` (E140) and earlier timestamped handoffs (retained as history).