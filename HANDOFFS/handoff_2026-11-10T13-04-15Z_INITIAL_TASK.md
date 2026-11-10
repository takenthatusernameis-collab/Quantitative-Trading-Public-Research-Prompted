# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T13:04:15Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `667c3009` (`chore: capture completed workflow run diagnostics`, 2026-11-10T13:03:59Z) — in sync with `origin/main` (0 ahead, 0 behind).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` — clean, no staged/unstaged tracked changes, no bytecode modifications.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- No source, experiment, ledger, script, test, or baseline artifact changes beyond this handoff artifact itself. `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` is empty.
- `git ls-files experiments/` → **138 tracked golden artifacts**, all matching HEAD.
- **Research phase complete (E001–E043).** Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md` (last entry E131, 2026-11-10T08:30Z). All items COMPLETE/CLOSED through E131; no OPEN/PENDING/BLOCKED/TODO markers anywhere in the ledger.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity, 29–133 numeric diffs). **Do not re-pin** E041/E042 artifacts to silence drift.
- Data note: `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be missing from a fresh working tree (gitignored); `QUANT_RESEARCH_OFFLINE=1` is enforced during verification, so missing pinned cache entries fail hard.

## Environment note

- If the environment resets, reinstall the pinned stack before checks: `pip install -r requirements.txt` (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0, statsmodels 0.15.0, yfinance 1.7.0).
- `check.sh`'s `FAIL experiments/d.json`, `experiments/b.json`, `experiments/x.json`, `e2.json`, `badlist.json`, `u.json`, `d2.json` lines are **intentional negative-control fixtures** consumed by `tests/test_json_guard` — not real artifacts, not a problem.
- `research_state/workflow_run_diagnostics.jsonl` (session-local runtime diagnostics) is not a tracked artifact.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm source state and `HEAD`/remote alignment.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report a golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never introduce logging of secrets.
- Do not stage/commit bytecode (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T13-04-15Z_INITIAL_TASK.md` (root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/` (identical content), with canonical symlinks (`handoff_LATEST`, `handoff_CURRENT`, `handoff_NEXT_SESSION`, `handoff_HANDOFF`, `handoff_INITIAL_TASK`, `initial_task`, `next_session`, and case variants) repointed to it.
- **Supersedes (operationally):** `handoff_2026-11-10T10-38-40Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
