# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T18:49:14Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `0e3881c2` (`chore: capture completed workflow run diagnostics`, 2026-11-12 18:48:18 +0000) — in sync with `origin/main` (`+0 -0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (at handoff)
- **Working tree:** clean — `git status --short --branch` → `## main...origin/main` with **0 modifications / 0 untracked**. No source, experiment, script, test, or baseline artifact changes pending.
- **`.verify_snapshot/`:** absent (no interrupted verification run pending).
- **Delta vs prior durable handoff (E175, HEAD `5740065b` → handoff at 2026-11-12T16:17:37Z):** HEAD advanced `5740065b` → `0e3881c2` via two commits (`99ecd512` checkpoint + `0e3881c2` diagnostics capture). `git diff --name-only 5740065b..0e3881c2` → 549 paths. All are handoff-related (timestamped artifacts, generic canonical-pointer symlinks in root/`handoff/`/`HANDOFFS/`/`.handoff/`/`.kilo/`, and `ledger/RESEARCH_LEDGER.md` carrying the E175 entry) **except** one genuine addition: `research_state/workflow_run_diagnostics.jsonl` (+1 line, CI workflow-run diagnostic capture; not research substance). No `experiments/`, `data/`, `src/`, or `tests/` change.
- **Baseline guards re-run:** `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**; `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**. `git diff HEAD -- experiments/ data/` → empty. `git ls-files experiments/` → 138 tracked entries (107 golden JSONs + 31 drivers).
- **Research phase:** complete (E001–E043). Authoritative dispositions and open items: `ledger/RESEARCH_LEDGER.md`. Last research entry E051; E052–E175 are durable-handoff refreshes only. grep for `OPEN|PENDING|BLOCKED|TODO` → 0 actionable markers.
- **Canonical baselines (authoritative):** `experiments/*.json` (138 tracked entries: 107 golden JSONs + 31 drivers), `ledger/golden_baseline.json`, `ledger/data_baseline.json` — do not modify or re-pin during routine verification.
- **Closed/resolved (do not reopen):** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)
**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)
1. `git status --short --branch` — confirm HEAD/remote alignment. Treat any tracked `__pycache__` modifications explicitly (restore/discard/commit only with explicit direction); do not let bytecode changes contaminate substantive commits.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change. Note: in this environment `/usr/bin/python3` may lack `requirements.txt` packages (numpy, pandas, scipy, statsmodels, yfinance); `tests.test_data_coverage` / `tests.test_portfolio_opt` can fail with `ModuleNotFoundError` — environmental, not a code defect. Use an interpreter with dependencies installed.

### If asked to run verification
- Always use **`SEED=42`**.
- Use `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full` as appropriate.
- **Never commit verification output** over `experiments/*.json`.
- If a run is interrupted, restore goldens before committing (`--restore-only`; `git checkout -- experiments/` only when HEAD holds the pinned baseline).
- If guards report golden/baseline mismatch, fix/restore before committing — **do not re-pin to silence drift**.

## Reproduction / verification commands (run only if explicitly requested)
```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails
- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys; never log secrets.

## Handoff provenance
- **Durable artifact (this session):** `handoff_2026-11-12T18-49-14Z_INITIAL_TASK.md` (root).
- **Supersedes operationally:** `handoff_2026-11-12T16-17-37Z_INITIAL_TASK.md` and all prior timestamped handoff artifacts/symlinks (retained for history).

(End of handoff)